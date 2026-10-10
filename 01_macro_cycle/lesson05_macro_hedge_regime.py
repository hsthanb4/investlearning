r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 5/5 课
第 5 课：宏观体制切换与全天候对冲配置 (Macro Regime Switching & All-Weather Hedging)
================================================================================

【课程定位与第一性原理】
达利欧（Ray Dalio）领导的桥水基金（Bridgewater）在 1996 年创立全天候策略（All Weather Strategy），
其核心哲学奠基于一个深刻的宏观公理：
“没有单一资产能够在所有宏观环境下持续战胜通胀与回撤，但特定资产在特定宏观体制下具有高确定性表现。”

传统金融资产定价模型假定收益率服从独立同分布（IID Gaussian），但在现实金融市场中，
宏观环境呈现出显著的“体制切换（Regime Shifts）”特征（Hamilton, 1989）：
1. 市场由“流动性环境（宽松 vs 紧缩）”与“波动率/风险溢价（平静 vs 恐慌）”构成的多稳态驱动；
2. 在平稳宽松体制下，加杠杆做多高 Beta 资产（股票、高收益债）能够享受充沛的流动性溢价；
3. 但在流动性急剧冻结或波动率飙升的“危机体制（Crisis Regime）”下，各类资产相关性瞬间收敛至 1.0，
   杠杆资金将引发连环踩踏清算。

【宏观体制状态机与全天候对冲架构】
```mermaid
flowchart TD
    RawData["宏观输入: 央行流动性脉冲 (Liquidity) + 市场波动率 (VIX)"] --> StateMachine["宏观体制自适应状态机 (Macro Regime Machine)"]
    StateMachine --> Regime1["1. 扩张期 (Expansion: 流动性宽松 + 低波动) ➔ 股票权益 90%, 适度杠杆"]
    StateMachine --> Regime2["2. 中性防御期 (Neutral: 流动性收紧 + 低波动) ➔ 股票 50%, 增配平价国债"]
    StateMachine --> Regime3["3. 危机风暴期 (Crisis: VIX > 30 恐慌) ➔ 触发风险断路器, 股票强制压缩至 20%, 现金与黄金防御"]
    Regime1 --> Portfolio["全天候自适应对冲组合: 动态回撤控制与夏普比率倍增"]
    Regime2 --> Portfolio
    Regime3 --> Portfolio
```

【自适应动态对冲数学模型】
1. 股票目标敞口判定函数：
       Exposure = f(Liquidity_Trend, Volatility_VIX)
   - 当 VIX > 30.0 时，无论宏观流动性多充裕，市场处于非理性清算阶段，敞口强制压缩至 0.2；
   - 当 VIX <= 30.0 且流动性趋势 > 0 时，处于积极做多窗口，敞口设定为 0.9；
   - 当 VIX <= 30.0 且流动性趋势 <= 0 时，处于流动性紧缩但未恐慌，敞口收缩至 0.5。
2. 动态对冲组合净值追踪：
       R_{portfolio, t} = Exposure_{t-1} \times R_{equity, t} + (1 - Exposure_{t-1}) \times R_{cash, t}
   通过在危机阶段大幅规避股票单边深跌，使全周期最大回撤显著收窄，同时捕获主升浪 Beta。

【思考题】
Q1: 为什么基于宏观指标的择时与体制切换策略在超高频（如日度、分钟级）往往胜率较低甚至充斥伪信号，
    而在中长周期（季度至年度、6~18个月）却具有极高的稳健性与穿透力？
    请从宏观经济变量的发布滞后性、信号噪声比（SNR）与信贷周期传导惯性推导。
Q2: 经典风险平价（Risk Parity）全天候模型在面临 2022 年“高通胀 + 美联储暴力加息”引发的股债双杀时，
    为什么遭遇了重大净值回撤？怎样通过引入“宏观通胀/流动性体制先验过滤器”来修补这一缺陷？
Q3: 为什么现代量化宏观对冲基金在设计“危机防御哨兵”（Kill Switch / Crisis Protocol）时，
    绝不能仅依赖价格技术止损，而必须设置外生流动性硬门槛（如 interbank spread 跨越阈值、隔夜拆借冻结）？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现多体制股票敞口动态映射规则 (1.5分)；
  2. 实现全天候自适应宏观状态机类与多资产权重分配 (1.5分)；
  3. 实现动态对冲回测与回撤风险平抑评估 (1分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须深入剖析宏观因果链与微观清算机制；
- 通过线：8/10 分。一票否决：危机阶段未降仓、回测存在未来函数、删除断言。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def determine_equity_exposure(liquidity_trend: float, volatility_vix: float) -> float:
    """
    根据流动性与波动率决定股票权益目标敞口 (0.0 ~ 1.0):
    - VIX > 30 (高风险恐慌): 无论流动性如何，敞口降至 0.2
    - VIX <= 30 且 liquidity_trend > 0: 积极看多，敞口 0.9
    - VIX <= 30 且 liquidity_trend <= 0: 中性防御，敞口 0.5

    参数:
        liquidity_trend: 净流动性环比或一阶趋势加速度 (正数代表宽松，负数代表紧缩)
        volatility_vix: 市场恐慌波动率指数 VIX

    返回:
        float: 目标股票配置权重 [0.0, 1.0]
    """
    # TODO: 实现规则判定
    pass


class MacroRegimeStateMachine:
    """
    全天候宏观体制自适应状态机 (Macro Regime State Machine)
    将市场划分为四大离散状态:
    - 'Expansion' (扩张期: 宽松 + 低波): 股票高配 (60%), 国债 (20%), 商品 (10%), 现金 (10%)
    - 'Neutral' (中性防御: 紧缩 + 低波): 股票标配 (30%), 国债 (40%), 商品 (10%), 现金 (20%)
    - 'Inflationary' (通胀高波: 紧缩 + 中高波 VIX 在 22~30): 股票 (15%), 国债 (15%), 商品 (40%), 现金 (30%)
    - 'Crisis' (危机流动性休克: VIX > 30): 股票 (10%), 国债 (30%), 黄金商品 (10%), 现金 (50%)
    """

    def __init__(self):
        self.current_state = "Neutral"

    def update_state(self, liquidity_trend: float, vix: float) -> str:
        """
        根据当期输入转移状态机内部状态并返回状态名称
        """
        # TODO: 根据流动性趋势与 VIX 判定并更新状态
        pass

    def get_target_allocation(self) -> Dict[str, float]:
        """
        返回当前状态下的四资产目标配置权重
        """
        # TODO: 返回目标资产权重字典
        pass


def simulate_dynamic_hedge(
    equity_returns: pd.Series,
    liquidity_trends: pd.Series,
    vix_series: pd.Series,
    cash_return_per_period: float = 0.0002,
) -> Dict[str, float]:
    """
    回测宏观体制动态敞口调节对冲策略与买入持有基准表现对比:
    在每期 t，使用 t-1 期的宏观信号决定 t 期的权益敞口 (防止前视偏差):
        r_port_t = exposure_{t-1} * equity_returns_t + (1 - exposure_{t-1}) * cash_return

    返回绩效字典:
        {
            "benchmark_max_drawdown": 纯股票买入持有最大回撤 (%),
            "hedged_max_drawdown": 动态宏观对冲最大回撤 (%),
            "max_drawdown_reduction": 回撤降低幅度 (基准回撤 - 对冲回撤, %),
            "hedged_total_return": 对冲策略累计总回报 (%)
        }
    """
    # TODO: 逐期滚动回测，严格按上一期信号计算当期收益，输出风险平抑效果
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础敞口规则 ----------------
    assert determine_equity_exposure(0.5, 18.0) == 0.9
    assert determine_equity_exposure(-0.2, 22.0) == 0.5
    assert determine_equity_exposure(0.8, 35.0) == 0.2

    # ---------------- 基础测试 2: 全天候状态机多资产权重 ----------------
    sm = MacroRegimeStateMachine()
    s1 = sm.update_state(0.4, 16.0)
    assert s1 == "Expansion", f"预期 Expansion, 实际 {s1}"
    w1 = sm.get_target_allocation()
    assert abs(w1["Stocks"] - 0.60) < 1e-4
    assert abs(sum(w1.values()) - 1.0) < 1e-4

    s2 = sm.update_state(-0.3, 19.0)
    assert s2 == "Neutral", f"预期 Neutral, 实际 {s2}"
    w2 = sm.get_target_allocation()
    assert abs(w2["Stocks"] - 0.30) < 1e-4

    s3 = sm.update_state(-0.5, 38.0)
    assert s3 == "Crisis", f"预期 Crisis, 实际 {s3}"
    w3 = sm.get_target_allocation()
    assert abs(w3["Stocks"] - 0.10) < 1e-4
    assert abs(w3["Cash"] - 0.50) < 1e-4

    # ---------------- 基础测试 3: 动态对冲模拟与回撤控制 ----------------
    np.random.seed(42)
    periods = 60
    # 构造一段包含牛市平稳与突发暴跌危机的行情序列
    eq_rets = [0.02] * 20 + [-0.08] * 10 + [0.015] * 30
    liq_s = [0.5] * 20 + [-0.8] * 10 + [0.3] * 30
    vix_s = [16.0] * 20 + [38.0] * 10 + [18.0] * 30

    res = simulate_dynamic_hedge(pd.Series(eq_rets), pd.Series(liq_s), pd.Series(vix_s))
    assert res["benchmark_max_drawdown"] > 50.0, f"基准遭遇暴跌回撤应超过50%, 实际: {res['benchmark_max_drawdown']}"
    assert res["hedged_max_drawdown"] < 25.0, f"动态对冲后最大回撤应显著压缩至25%以下, 实际: {res['hedged_max_drawdown']}"
    assert res["max_drawdown_reduction"] > 30.0, f"回撤降低幅度应大于30%, 实际: {res['max_drawdown_reduction']}"

    print("Lesson 05 Exercise Passed!")
