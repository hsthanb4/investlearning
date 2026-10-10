"""
================================================================================
模块 10：量化回测引擎避坑指南与实盘系统工程 · 第 1/4 课
第 1 课：回测致命陷阱：前视偏差、幸存者偏差与未来函数静态审计【参考实现】
================================================================================
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
    1. 负向 shift: df.shift(-k) 或 shift(periods=-k) (k > 0)
    2. 反向填充: .bfill(), .backfill(), 或 fillna(method='bfill' / method='backfill')
    3. 中心化移动窗口: .rolling(..., center=True)
    """
    tree = ast.parse(code_str)
    violations: List[Dict[str, Any]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id

        # 1. 检查 shift(-k) 或 shift(periods=-k)
        if func_name == "shift":
            is_neg = False
            # 检查位置参数 args[0]
            if node.args:
                arg0 = node.args[0]
                if isinstance(arg0, ast.UnaryOp) and isinstance(arg0.op, ast.USub):
                    is_neg = True
                elif isinstance(arg0, ast.Constant) and isinstance(arg0.value, (int, float)) and arg0.value < 0:
                    is_neg = True
            # 检查关键字参数 periods
            for kw in node.keywords:
                if kw.arg == "periods":
                    if isinstance(kw.value, ast.UnaryOp) and isinstance(kw.value.op, ast.USub):
                        is_neg = True
                    elif isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, (int, float)) and kw.value.value < 0:
                        is_neg = True
            if is_neg:
                violations.append({
                    "line": node.lineno,
                    "rule": "NEGATIVE_SHIFT",
                    "message": "调用 shift() 传入负数位移，提前偷看未来序列数据 (Lookahead Leakage)"
                })

        # 2. 检查反向填充: bfill / backfill / fillna(method='bfill')
        elif func_name in ("bfill", "backfill"):
            violations.append({
                "line": node.lineno,
                "rule": "BACKFILL",
                "message": f"调用 {func_name}() 反向填充未来数据覆盖历史缺失值"
            })
        elif func_name == "fillna":
            for kw in node.keywords:
                if kw.arg == "method" and isinstance(kw.value, ast.Constant) and kw.value.value in ("bfill", "backfill"):
                    violations.append({
                        "line": node.lineno,
                        "rule": "BACKFILL",
                        "message": "调用 fillna(method='bfill') 将未来数据泄露至过去"
                    })

        # 3. 检查中心化移动窗口 rolling(..., center=True)
        elif func_name == "rolling":
            for kw in node.keywords:
                if kw.arg == "center" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    violations.append({
                        "line": node.lineno,
                        "rule": "CENTERED_WINDOW",
                        "message": "调用 rolling() 启用了 center=True 中心化滤波，偷看了未来半窗口数据"
                    })

    return violations


# ==============================================================================
# 算法 2：交易记录与盘口可行性静态校验引擎
# ==============================================================================

def detect_trade_feasibility_violations(
    trades_df: pd.DataFrame,
    market_df: pd.DataFrame
) -> pd.DataFrame:
    """
    静态审计策略回测中生成的成交记录列表，识别违背交易所物理现实的虚假撮合
    """
    merged = pd.merge(trades_df, market_df, on=["date", "symbol"], how="left")
    violations = []

    for _, row in merged.iterrows():
        v_type = None
        v_desc = None

        # 1. 停牌违规
        is_suspended = row.get("is_suspended", False)
        market_vol = row.get("volume_y", row.get("volume", 0))
        if is_suspended or market_vol == 0:
            v_type = "SUSPENSION_VIOLATION"
            v_desc = "标的处于停牌或零成交状态，物理上无法执行任何撮合"
        # 2. 极端涨跌停封板流动性违规
        elif row["action"] == "BUY" and row["low"] >= row["limit_up"] and row["high"] >= row["limit_up"]:
            v_type = "LIMIT_LOCK_VIOLATION"
            v_desc = "一字涨停板买单封死，普通买单排在队尾无法成交"
        elif row["action"] == "SELL" and row["low"] <= row["limit_down"] and row["high"] <= row["limit_down"]:
            v_type = "LIMIT_LOCK_VIOLATION"
            v_desc = "一字跌停板卖单封死，卖单无法撮合成交出逃"
        # 3. 价格越界
        elif row["price"] < row["low"] - 1e-6 or row["price"] > row["high"] + 1e-6:
            v_type = "PRICE_OUT_OF_BOUNDS"
            v_desc = f"成交价 {row['price']} 超出日内价格区间 [{row['low']}, {row['high']}]"
        # 4. 决策时序倒挂
        elif str(row["signal_time"]) >= str(row["trade_time"]):
            v_type = "LOOKAHEAD_TIMING_VIOLATION"
            v_desc = f"决策时间 {row['signal_time']} 不早于撮合执行时间 {row['trade_time']}"

        if v_type:
            rec = trades_df.loc[trades_df["trade_id"] == row["trade_id"]].copy().iloc[0].to_dict()
            rec["violation_type"] = v_type
            rec["violation_desc"] = v_desc
            violations.append(rec)

    return pd.DataFrame(violations)


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
    计算紧缩夏普比率 (Deflated Sharpe Ratio, DSR) 的统计显著性置信度 (Phi(Z))
    """
    if num_trials <= 1 or variance_of_trials <= 0.0:
        exp_max_sr = 0.0
    else:
        gamma = 0.57721566490153286
        p1 = 1.0 - 1.0 / num_trials
        p2 = 1.0 - 1.0 / (num_trials * math.e)
        exp_max_sr = math.sqrt(variance_of_trials) * ((1.0 - gamma) * norm_ppf(p1) + gamma * norm_ppf(p2))

    var_sr = (1.0 - returns_skew * observed_sr + ((returns_kurt - 1.0) / 4.0) * (observed_sr ** 2)) / (sample_length - 1.0)
    se_sr = math.sqrt(max(var_sr, 1e-12))
    z = (observed_sr - exp_max_sr) / se_sr
    return norm_cdf(z)


# ==============================================================================
# 自动化测试与参考答案解析
# ==============================================================================

if __name__ == "__main__":
    print("正在运行 10_system_infra / Lesson 01 参考实现断言验证...")

    # 1. 验证 AST 审计器
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
    assert violations is not None and len(violations) == 3
    rules_detected = [v["rule"] for v in violations]
    assert "NEGATIVE_SHIFT" in rules_detected
    assert "BACKFILL" in rules_detected
    assert "CENTERED_WINDOW" in rules_detected

    # 2. 验证交易可行性审计
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
    assert violations_df is not None and len(violations_df) == 5
    violation_ids = set(violations_df["trade_id"].values)
    assert violation_ids == {"T02", "T03", "T04", "T05", "T06"}

    # 3. 验证 DSR 检验
    dsr_single = compute_deflated_sharpe_ratio(2.0, 1, 0.0, -0.5, 4.0, 252 * 3)
    assert dsr_single > 0.99
    dsr_overfit = compute_deflated_sharpe_ratio(1.2, 10000, 0.5, -0.8, 4.5, 252 * 2)
    assert dsr_overfit < 0.10

    print("Lesson 01 参考实现全部断言通过 (Exit Code 0)！\n")

    print("=" * 80)
    print("【思考题标准答案深度解析 (Q1 ~ Q3)】")
    print("=" * 80)
    print("Q1 解析:")
    print("  在真实的撮合交易中，'当日收盘价' (Close) 必须等到 15:00 收盘集合竞价结束才确立。如果在 15:00 之后计算均线")
    print("  金叉信号，此时当天的交易通道早已关闭，策略绝不可能在物理上以'当日收盘价'买入，这属于典型的时序前视。")
    print("  工业级解决方案：")
    print("  (1) 次日开盘撮合架构 (T+1 Open): 每日 15:00 盘后生成信号，在 T+1 日 09:25 集合竞价或 09:30 开盘以开盘价委托撮合；")
    print("  (2) 盘尾近收盘截面撮合 (MOC - Market On Close): 提前至 14:55:00 截断前 3 小时 55 分钟的行情快照计算信号，并在最后")
    print("      5 分钟通过 VWAP/TWAP 算法以盘中成交量加权均价执行撮合。")
    print("-" * 80)
    print("Q2 解析:")
    print("  使用'当前最新沪深300成分股'回测历史10年，会引入极其严重的幸存者偏差（Survivorship Bias）：")
    print("  (1) 机制机理：历史上曾经入选沪深300但在过去几年中因业绩恶化、造假暴雷、退市（如康得新、康美药业、乐视网等）的公司，")
    print("      在今天已经被剔除出指数。如果仅使用今天存活的成分股，相当于回溯性地为历史投资组合赋予了'先验不会退市、质地优良'的未来光环。")
    print("  (2) 扭曲方向：策略的多头年化收益率（Alpha）通常会被人为系统性虚增 3%~8%，组合的最大回撤（Max Drawdown）被显著低估，")
    print("      因为真实历史上那些动辄 80%~90% 断崖下跌并退市的惨烈亏损标的被直接凭空蒸发了。")
    print("  (3) 生产级点截面构建 (Point-in-Time Universe)：建立历史成分股变动快照表（包含 symbol, in_date, out_date），")
    print("      在回测历史上的任意日期 T，仅选择满足 `in_date <= T < out_date` 的股票构成合规候选池。")
    print("-" * 80)
    print("Q3 解析:")
    print("  (1) 金融数据具有不可逆的时序因果性与强自相关性。随机 K 折交叉验证会随机打乱时间，使得测试集中的样本前后都包含来自")
    print("      训练集的相邻时刻样本（Data Leakage / 信息渗漏），导致模型轻易记住跨时间的相关性，测得极高但无法在实盘落地的夏普比率。")
    print("      必须使用 Purged Walk-Forward TimeSeriesSplit（时序滚动向前推进，并在训练集与测试集交界处设置净化隔离缓冲区 Purge Window）。")
    print("  (2) 如果在 split 之前调用全局 `StandardScaler().fit_transform(X)`，会将测试期（未来）的全局均值 $\\mu$ 和方差 $\\sigma$")
    print("      提前泄露给训练期。在极端市场（如 2008 年金融危机或 2015 年股灾）中，全局方差会被未来剧烈波动拉高，导致训练期特征被缩小，")
    print("      使模型获得了感知未来全局波动率分布的作弊能力。")
    print("=" * 80)
