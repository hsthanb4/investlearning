r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 5/5 课
第 5 课：宏观体制切换与全天候对冲配置 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么基于宏观指标的择时与体制切换策略在超高频（如日度、分钟级）往往胜率较低甚至充斥伪信号，而在中长周期（季度至年度、6~18个月）却具有极高的稳健性与穿透力？
- **[信息信噪比与宏观传导物理惯性]**：
  - **[1. 高频价格由微观订单流驱动]**：日度或分钟级的资产价格波动本质上是交易所订单簿（LOB）挂单撤单、做市商库存再平衡与期权 Gamma 对冲等微观微秒级博弈的随机碰撞，受情绪噪音主导，宏观经济基本面无法在纳秒间产生物理改变。
  - **[2. 宏观数据披露的低频与滞后性]**：GDP、非农就业、CPI、央行资产负债表等宏观变量发布频率为周频或月频，且初值在后续数月内频繁面临大幅修正。在高频时间尺度下，宏观变量呈现离散跳跃或阶梯状，信噪比（Signal-to-Noise Ratio）极低。
  - **[3. 信贷与商业周期的物理惯性]**：实体经济投资决策（如建厂扩产、商业地产开发、按揭贷款）具有极强的跨期资本黏性与多季度传导惯性。加息对企业现金流的侵蚀通常需要 3~4 个季度才能完全体现，宏观趋势一旦形成即具备强大的自维持动量，因此在中长周期（6~18个月）具有极强的确定性与穿透力。

【Q2 投决会深度解析】
经典风险平价（Risk Parity）全天候模型在面临 2022 年“高通胀 + 美联储暴力加息”引发的股债双杀时，为什么遭遇了重大净值回撤？怎样通过引入“宏观通胀/流动性体制先验过滤器”来修补这一缺陷？
- **[风险平价缺陷与先验体制修复]**：
  - **[1. 杠杆化低波债券的脆弱性暴露]**：经典风险平价通过波动率倒数加权分配资产权重。由于长期国债年化波动率（通常 4%~8%）远低于股票（15%~20%），为了实现各资产等风险贡献，模型通常对低波动的长期国债加杠杆配置（名义杠杆常达到 2~3 倍）。
  - **[2. 股债负相关性假说的破灭]**：过去 30 年“大缓和（Great Moderation）”时期形成的股债负相关性在 2022 年供给冲击引发的高通胀下彻底崩溃。美联储单年加息超过 400 bps，引发了美债 40 年未见的大崩盘（10Y/30Y 美债回撤超 30%）。高杠杆的债券端亏损非但没有对冲股票亏损，反而放大了组合整体回撤。
  - **[3. 引入宏观先验过滤器]**：量化投资团队必须在底层协方差优化之外构建**“宏观通胀/流动性体制过滤器”**：当监测到通胀加速度 $\Delta \text{CPI} > 0$ 且美联储处于加息周期时，强制解除债券杠杆，动态限制久期敞口，并将风险预算重分配至大宗商品、通胀保值国债（TIPS）及现金等价物。

【Q3 投决会深度解析】
为什么现代量化宏观对冲基金在设计“危机防御哨兵”（Kill Switch / Crisis Protocol）时，绝不能仅依赖价格技术止损，而必须设置外生流动性硬门槛（如 interbank spread 跨越阈值、隔夜拆借冻结）？
- **[内生价格滞后性与流动性黑洞防御]**：
  - **[1. 价格止损在跳空流动性真空中的失效]**：纯价格技术指标（如突破均线、跌破关键支撑位、ATR 移动止损）是交易结果的事后投影。在雷曼破产、硅谷银行闪崩等重大系统性黑天鹅爆发瞬间，二级市场开盘直接跳空 20%~30%，订单簿深度瞬间蒸发，技术止损单面临极端穿仓滑点，根本无法以预设价格成交。
  - **[2. 货币市场是整个金融资产的终极底座]**：金融机构的杠杆生命线维系于银行间与回购市场（Repo Market）。当 FRA-OIS 利差、商业票据利率（CP）或 SOFR 出现异常飙升、无担保拆借市场冻结时，意味着一级交易商和影子银行的流动性清算通道已被切断，杠杆强制清算踩踏已不可避免。
  - **[3. 外生硬门槛的先验断路保护]**：现代量化风控系统将外生流动性指标（如 interbank spread 超过特定分位数、VIX 突破 30、回购利差异动）设定为一票否决式的“防空警报”，在现货价格尚未完全崩塌之前，先行执行强制降低风险资产仓位，从而在流动性黑洞彻底关闭前锁定保命现金。
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
    """
    if volatility_vix > 30.0:
        return 0.2
    elif liquidity_trend > 0:
        return 0.9
    else:
        return 0.5


class MacroRegimeStateMachine:
    """
    全天候宏观体制自适应状态机 (Macro Regime State Machine)
    """

    def __init__(self):
        self.current_state = "Neutral"

    def update_state(self, liquidity_trend: float, vix: float) -> str:
        """
        根据当期输入转移状态机内部状态并返回状态名称
        """
        if vix > 30.0:
            self.current_state = "Crisis"
        elif vix > 22.0 and liquidity_trend <= 0:
            self.current_state = "Inflationary"
        elif liquidity_trend > 0:
            self.current_state = "Expansion"
        else:
            self.current_state = "Neutral"
        return self.current_state

    def get_target_allocation(self) -> Dict[str, float]:
        """
        返回当前状态下的四资产目标配置权重
        """
        allocations = {
            "Expansion": {"Stocks": 0.60, "Bonds": 0.20, "Commodities": 0.10, "Cash": 0.10},
            "Neutral": {"Stocks": 0.30, "Bonds": 0.40, "Commodities": 0.10, "Cash": 0.20},
            "Inflationary": {"Stocks": 0.15, "Bonds": 0.15, "Commodities": 0.40, "Cash": 0.30},
            "Crisis": {"Stocks": 0.10, "Bonds": 0.30, "Commodities": 0.10, "Cash": 0.50},
        }
        return allocations.get(self.current_state, allocations["Neutral"])


def simulate_dynamic_hedge(
    equity_returns: pd.Series,
    liquidity_trends: pd.Series,
    vix_series: pd.Series,
    cash_return_per_period: float = 0.0002,
) -> Dict[str, float]:
    """
    回测宏观体制动态敞口调节对冲策略与买入持有基准表现对比
    """
    n = len(equity_returns)
    hedged_rets = []

    # t=0 时刻信号来自 t=0
    exp_prev = determine_equity_exposure(liquidity_trends.iloc[0], vix_series.iloc[0])

    for t in range(n):
        if t > 0:
            exp_t = determine_equity_exposure(liquidity_trends.iloc[t - 1], vix_series.iloc[t - 1])
        else:
            exp_t = exp_prev

        eq_r = equity_returns.iloc[t]
        h_r = exp_t * eq_r + (1.0 - exp_t) * cash_return_per_period
        hedged_rets.append(h_r)

    hedged_rets = np.array(hedged_rets)
    benchmark_rets = equity_returns.values

    # 计算净值
    bm_nav = np.cumprod(1.0 + benchmark_rets)
    hd_nav = np.cumprod(1.0 + hedged_rets)

    # 计算最大回撤
    bm_peaks = np.maximum.accumulate(bm_nav)
    bm_dd = np.max((bm_peaks - bm_nav) / bm_peaks) * 100.0

    hd_peaks = np.maximum.accumulate(hd_nav)
    hd_dd = np.max((hd_peaks - hd_nav) / hd_peaks) * 100.0

    total_hd_ret = (hd_nav[-1] - 1.0) * 100.0

    return {
        "benchmark_max_drawdown": float(bm_dd),
        "hedged_max_drawdown": float(hd_dd),
        "max_drawdown_reduction": float(bm_dd - hd_dd),
        "hedged_total_return": float(total_hd_ret),
    }


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
    eq_rets = [0.02] * 20 + [-0.08] * 10 + [0.015] * 30
    liq_s = [0.5] * 20 + [-0.8] * 10 + [0.3] * 30
    vix_s = [16.0] * 20 + [38.0] * 10 + [18.0] * 30

    res = simulate_dynamic_hedge(pd.Series(eq_rets), pd.Series(liq_s), pd.Series(vix_s))
    assert res["benchmark_max_drawdown"] > 50.0, f"基准遭遇暴跌回撤应超过50%, 实际: {res['benchmark_max_drawdown']}"
    assert res["hedged_max_drawdown"] < 25.0, f"动态对冲后最大回撤应显著压缩至25%以下, 实际: {res['hedged_max_drawdown']}"
    assert res["max_drawdown_reduction"] > 30.0, f"回撤降低幅度应大于30%, 实际: {res['max_drawdown_reduction']}"

    print("Lesson 05 Answer Verified!")
