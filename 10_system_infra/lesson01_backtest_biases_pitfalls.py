"""
================================================================================
模块 10：量化回测引擎避坑指南与实盘系统工程 · 第 1/4 课
第 1 课：回测致命陷阱：前视偏差、幸存者偏差与未来函数静态审计
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 思考题深入分析并达到工业级认知线：各 2 分（共 6 分）
- 综合及格线：8/10 分

【理论精讲】
量化交易研究中最具迷惑性的现象是：“回测曲线如天梯，实盘上线就归零”。
在大多数情况下，这绝不是策略的 Beta 风格漂移，而是回测逻辑中潜藏着致命的统计偏差与工程漏洞：

1. 前视偏差 (Lookahead Bias / Future Leakage)：
   - 概念：在历史回测时，某个时刻 t 的决策逻辑（特征、过滤条件、权重）使用了只有在 t 之后才可能知晓的未来信息。
   - 经典灾难案例：
     * 收盘价决策与开盘价成交：在 15:00 收盘后根据当日 Close 计算指标（如破位、均线交叉），却在回测中假定“以当日 Open 价格成交”。
     * 盘中偷看日内极值：在日频策略中，使用当天的 High 和 Low 作为日内开仓的触发信号，实际上当天的极值必须在收盘后才能确定。
     * 财报报告期 vs. 实际披露日（Point-in-Time 缺失）：上市公司 Q3 财报所属期是 9 月 30 日，但实际公开披露日通常是 10 月 28 日。如果策略在 10 月 1 日就使用 Q3 净利润选股，便产生了将近 1 个月的前视穿透。
     * 数据平滑中心化：在降噪处理时使用 `rolling(window, center=True)` 或高斯双向滤波，无意中引入了未来 N/2 期的价格。

2. 幸存者偏差 (Survivorship Bias)：
   - 概念：回测的标的池（Universe）只包含“当前仍然存活/上市的公司”，或者直接使用“当前最新的沪深300指数成分股”去回测历史10年。
   - 影响：历史上被 ST、暴雷、退市或长期停牌的公司被完全剔除出回测池。真实历史中，投资组合不可避免会踩雷跌入仙股，剔除退市股会人为系统性虚增年化收益率 3%~8%，并大幅低估最大回撤。

3. 过拟合与数据窥探 (Overfitting & Data Snooping)：
   - 当研究人员尝试了 10,000 组参数网格（Grid Search）或测试了 5,000 个 Alpha 因子时，即使输入完全是高斯白噪声，纯凭统计巧合也能找到数个历史年化 30% 以上的“神级策略”。
   - 德普拉多（Marcos López de Prado）提出的紧缩夏普比率（Deflated Sharpe Ratio, DSR）指出：
     多重检验下的期望最大夏普比率 $E[\max(SR)]$ 随着试验次数 $N$ 的对数增长。如果不根据试验次数和收益非正态性（偏度、峰度）对夏普比率进行通胀挤出，回测报告就只是一纸谎言。

4. 流动性与停牌陷阱 (Liquidity & Suspension Illusion)：
   - 股票处于停牌（Volume = 0 或 Suspended）时，撮合引擎必须判定无法买入且无法卖出。
   - 一字涨停板（Limit Up）封死时，买方挂单堆积极大，普通散户与策略买单排在队列末尾极大概率无法成交；一字跌停板（Limit Down）封死时，卖盘无法出逃。无视微观盘口限制的回测，会把“跌停无法止损”的巨大灾难粉饰为“已在跌停价平仓逃跑”。

【三个思考题 (Q1~Q3)】
Q1: 某研究员构建了一个双均线策略（MA5 与 MA20），每日收盘后计算金叉并在“当日收盘价”挂单成交。为什么这在真实的交易所交易机制下属于事实上的“前视偏差”？在工程上应如何设计规范的数据时序流？
Q2: 为什么直接读取当前最新的“沪深300成分股”对过去10年进行因子回测会产生严重的幸存者偏差？请推导这种偏差对多头超额收益（Alpha）和组合最大回撤（Max Drawdown）的扭曲方向，并说明生产环境中如何构建真正的点截面（Point-in-Time Universe）数据池？
Q3: 为什么在金融时间序列上绝对不能使用标准的“随机 K 折交叉验证（Random K-Fold Cross Validation）”？如果在特征工程阶段，在训练集与测试集拆分之前直接对全量数据调用了 `StandardScaler().fit_transform(X)`，会引发什么形式的未来信息泄露？
"""

import ast
import math
from typing import List, Dict, Any
import numpy as np
import pandas as pd


# ==============================================================================
# 算法 1：Python 代码抽象语法树 (AST) 静态未来函数审计器
# ==============================================================================

def audit_ast_lookahead_risk(code_str: str) -> List[Dict[str, Any]]:
    """
    通过 Python AST 语法树静态分析策略源码，精准扫描可能引入未来函数的危险模式：
    1. 负向 shift: df.shift(-k) 或 shift(periods=-k) (k > 0) -> rule: 'NEGATIVE_SHIFT'
    2. 反向填充: .bfill(), .backfill(), 或 fillna(method='bfill' / method='backfill') -> rule: 'BACKFILL'
    3. 中心化移动窗口: .rolling(..., center=True) -> rule: 'CENTERED_WINDOW'
    
    参数:
        code_str: 待审计的 Python 代码字符串
        
    返回:
        List[Dict[str, Any]]: 发现的安全违规项列表，每个元素包含:
            {
                "line": int,            # 违规发生的行号
                "rule": str,            # 违规规则名称
                "message": str          # 违规详细解释
            }
    """
    # TODO: 使用 ast.parse 解析 code_str，遍历节点并检测上述三种未来函数特征模式。
    pass


# ==============================================================================
# 算法 2：交易记录与盘口可行性静态校验引擎
# ==============================================================================

def detect_trade_feasibility_violations(
    trades_df: pd.DataFrame,
    market_df: pd.DataFrame
) -> pd.DataFrame:
    """
    静态审计策略回测中生成的成交记录列表，识别违背交易所物理现实的虚假撮合：
    1. 停牌日成交违规 (SUSPENSION_VIOLATION):
       - 当日 volume == 0 或 is_suspended == True 时，任何 BUY 或 SELL 均为非法成交。
    2. 极端涨跌停封板流动性违规 (LIMIT_LOCK_VIOLATION):
       - 一字涨停封死 (low == high == limit_up): 禁止 BUY 成交 (买单排队无法买入)。
       - 一字跌停封死 (low == high == limit_down): 禁止 SELL 成交 (卖单排队无法卖出出逃)。
    3. 成交价格超出日内真实价格极值 (PRICE_OUT_OF_BOUNDS):
       - 成交价 price < low 或 price > high。
    4. 决策时序倒挂 (LOOKAHEAD_TIMING_VIOLATION):
       - 同日内决策信号时间大于或等于撮合执行时间 (signal_time >= trade_time)。
       
    参数:
        trades_df: pd.DataFrame，列包含:
            ['trade_id', 'date', 'symbol', 'action', 'price', 'volume', 'signal_time', 'trade_time']
        market_df: pd.DataFrame，列包含:
            ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'limit_up', 'limit_down', 'is_suspended']
            
    返回:
        pd.DataFrame: 违规交易清单，包含 trades_df 原字段并附加 'violation_type' 和 'violation_desc' 列。
    """
    # TODO: 校验 trades_df 与 market_df，筛选出所有违规成交记录并返回。
    pass


# ==============================================================================
# 算法 3：多重测试过拟合惩罚：紧缩夏普比率 (Deflated Sharpe Ratio, DSR)
# ==============================================================================

def norm_cdf(x: float) -> float:
    """标准正态分布累积分布函数 CDF (使用误差函数 erf 实现)"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_ppf(p: float) -> float:
    """
    标准正态分布分位数函数 (Acklam 逆累积分布高精度逼近算法)
    """
    if p <= 0.0 or p >= 1.0:
        raise ValueError("概率 p 必须在区间 (0, 1) 内")
    
    a = [-3.969683028665376e+01,  2.209460984245205e+02,
         -2.759285104469687e+02,  1.383577518672690e+02,
         -3.066479806614716e+01,  2.506628277459239e+00]
    b = [-5.447609879822406e+01,  1.615858368580409e+02,
         -1.556989798598866e+02,  6.680131188771972e+01,
         -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549732539343734e+00,
          4.374664141464968e+00,  2.938163982698783e+00]
    d = [ 7.784695709041462e-03,  3.224671290700398e-01,
          2.445134137142996e+00,  3.754408661907416e+00]
    
    p_low = 0.02425
    p_high = 1.0 - p_low
    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
               ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5])*q / \
               (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1.0)
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
                ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)

def compute_deflated_sharpe_ratio(
    observed_sr: float,
    num_trials: int,
    variance_of_trials: float,
    returns_skew: float,
    returns_kurt: float,
    sample_length: int
) -> float:
    """
    计算紧缩夏普比率 (Deflated Sharpe Ratio, DSR) 的统计显著性置信度 (Phi(Z)):
    
    数学推导:
    1. 期望最大夏普比率 (极值理论):
       当 num_trials > 1 时:
       gamma ≈ 0.5772156649 (Euler-Mascheroni 常数)
       E[max(SR)] = sqrt(variance_of_trials) * [ (1 - gamma) * Phi^{-1}(1 - 1/N) + gamma * Phi^{-1}(1 - 1/(N * e)) ]
       当 num_trials <= 1 时:
       E[max(SR)] = 0.0
       
    2. 非正态分布下夏普比率的标准误:
       SE(SR) = sqrt( (1 - skew * SR + ((kurt - 1) / 4) * SR^2) / (sample_length - 1) )
       
    3. 检验统计量:
       Z = (observed_sr - E[max(SR)]) / SE(SR)
       DSR = norm_cdf(Z)
    """
    # TODO: 实现 DSR 统计检验
    pass


# ==============================================================================
# 自动化测试断言
# ==============================================================================

if __name__ == "__main__":
    print("正在运行 10_system_infra / Lesson 01 单元测试...")

    # 测试 1: AST 静态未来函数审计器
    malicious_code = """
import pandas as pd

def compute_factors(df):
    df['next_return'] = df['close'].shift(-1) / df['close'] - 1.0
    df['clean_open'] = df['open'].bfill()
    df['smooth_ma'] = df['close'].rolling(window=10, center=True).mean()
    df['hist_ma'] = df['close'].shift(1).rolling(window=5).mean()
    return df
"""
    violations = audit_ast_lookahead_risk(malicious_code)
    assert violations is not None, "AST 审计器返回结果不能为 None"
    assert len(violations) == 3, f"预期捕获 3 处违规，实际捕获 {len(violations)} 处"
    
    rules_detected = [v["rule"] for v in violations]
    assert "NEGATIVE_SHIFT" in rules_detected, "未捕获负向 shift 未来函数"
    assert "BACKFILL" in rules_detected, "未捕获 bfill 反向填充未来函数"
    assert "CENTERED_WINDOW" in rules_detected, "未捕获 center=True 中心化移动窗口"
    print("✅ 测试 1 (AST 静态代码未来函数审计) 通过！")

    # 测试 2: 交易记录与盘口可行性静态校验引擎
    market_data = pd.DataFrame([
        {"date": "2024-01-02", "symbol": "000001.SZ", "open": 10.0, "high": 10.5, "low": 9.8, "close": 10.2, "volume": 100000, "limit_up": 11.0, "limit_down": 9.0, "is_suspended": False},
        {"date": "2024-01-03", "symbol": "000001.SZ", "open": 10.2, "high": 10.2, "low": 10.2, "close": 10.2, "volume": 0, "limit_up": 11.22, "limit_down": 9.18, "is_suspended": True},
        {"date": "2024-01-04", "symbol": "000001.SZ", "open": 11.22, "high": 11.22, "low": 11.22, "close": 11.22, "volume": 2000, "limit_up": 11.22, "limit_down": 9.18, "is_suspended": False},
        {"date": "2024-01-05", "symbol": "000001.SZ", "open": 10.10, "high": 10.10, "low": 10.10, "close": 10.10, "volume": 1500, "limit_up": 12.34, "limit_down": 10.10, "is_suspended": False},
    ])

    test_trades = pd.DataFrame([
        {"trade_id": "T01", "date": "2024-01-02", "symbol": "000001.SZ", "action": "BUY", "price": 10.1, "volume": 1000, "signal_time": "09:30:00", "trade_time": "09:31:00"},
        {"trade_id": "T02", "date": "2024-01-03", "symbol": "000001.SZ", "action": "BUY", "price": 10.2, "volume": 1000, "signal_time": "09:30:00", "trade_time": "09:35:00"},
        {"trade_id": "T03", "date": "2024-01-04", "symbol": "000001.SZ", "action": "BUY", "price": 11.22, "volume": 2000, "signal_time": "09:30:00", "trade_time": "09:30:01"},
        {"trade_id": "T04", "date": "2024-01-05", "symbol": "000001.SZ", "action": "SELL", "price": 10.10, "volume": 1000, "signal_time": "09:30:00", "trade_time": "09:32:00"},
        {"trade_id": "T05", "date": "2024-01-02", "symbol": "000001.SZ", "action": "BUY", "price": 9.5, "volume": 1000, "signal_time": "09:30:00", "trade_time": "09:31:00"},
        {"trade_id": "T06", "date": "2024-01-02", "symbol": "000001.SZ", "action": "BUY", "price": 10.0, "volume": 1000, "signal_time": "15:00:00", "trade_time": "09:30:00"},
    ])

    violations_df = detect_trade_feasibility_violations(test_trades, market_data)
    assert violations_df is not None, "交易违规检测返回不能为 None"
    assert len(violations_df) == 5, f"预期检出 5 笔违规交易，实际检出 {len(violations_df)} 笔"
    assert "T01" not in violations_df["trade_id"].values, "合规交易 T01 不应被误判为违规"
    
    violation_ids = set(violations_df["trade_id"].values)
    assert violation_ids == {"T02", "T03", "T04", "T05", "T06"}, f"违规 ID 不匹配: {violation_ids}"
    print("✅ 测试 2 (交易记录盘口可行性与停牌校验) 通过！")

    # 测试 3: 紧缩夏普比率 (Deflated Sharpe Ratio)
    dsr_single = compute_deflated_sharpe_ratio(
        observed_sr=2.0,
        num_trials=1,
        variance_of_trials=0.0,
        returns_skew=-0.5,
        returns_kurt=4.0,
        sample_length=252 * 3
    )
    assert dsr_single > 0.99, f"单次试验夏普 2.0 显著性应极高，实际 DSR={dsr_single:.4f}"

    dsr_overfit = compute_deflated_sharpe_ratio(
        observed_sr=1.2,
        num_trials=10000,
        variance_of_trials=0.5,
        returns_skew=-0.8,
        returns_kurt=4.5,
        sample_length=252 * 2
    )
    assert dsr_overfit < 0.10, f"海量挖掘产生的虚假夏普 DSR 应该极低，实际 DSR={dsr_overfit:.4f}"
    
    print(f"  场景 A (严谨单次试验 SR=2.0): DSR = {dsr_single:.6f} (极其显著)")
    print(f"  场景 B (万次窥探挖掘 SR=1.2): DSR = {dsr_overfit:.6f} (过拟合伪夏普)")
    print("✅ 测试 3 (Deflated Sharpe Ratio 极值惩罚) 通过！")

    print("\n🎉 Lesson 01 全部单元测试顺利通过！")
