r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 5/5 课
第 5 课：宏观体制切换与全天候对冲配置 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么基于宏观指标的择时与体制切换策略在超高频（如日度、分钟级）往往胜率较低甚至充斥伪信号，
而在中长周期（季度至年度、6~18个月）却具有极高的稳健性与穿透力？
- **信号噪声比与宏观传导物理惯性**：
  1. **高频维度的信息噪声与博弈扰动**：日度乃至分钟级的资产价格波动，主要受微观订单簿挂撤单、
     短期情绪热点、衍生品期权 Gamma 挤压与跨市场高频套利主导。宏观经济基本面在一天甚至一周内
     几乎没有物理变化（GDP、就业、工业产出属于低频累积变量），在高频切片下，宏观因子的信噪比（SNR）趋近于零。
  2. **宏观经济变量的发布滞后与事后修正**：宏观统计数据（如非农、CPI、GDP）通常按月度/季度发布，
     且往往在次月伴随大幅度初值修正。若在高频交易中直接对未经滤波的宏观离散跳跃做粗暴反应，
     极易被短期数据统计误差与“买预期、卖事实”的逆向行情来回打脸。
  3. **信贷周期与实体投资的刚性物理时滞**：央行从下调基准利率、降低法定准备金率，到商业银行资本金扩容、
     向实体投放信贷、企业启动资本开支（CapEx）、最终体现为上市公司订单收入与现金流，具有 2~4 个季度的
     客观物理时滞。这种长周期趋势一旦形成，便具备巨大的不可逆宏观动量（Momentum），因此在 6~18 个月
     的跨期维度上，宏观流动性与体制切换具备极强的战略穿透力和极高的风险收益比。

【Q2 深度参考答案】
经典风险平价（Risk Parity）全天候模型在面临 2022 年“高通胀 + 美联储暴力加息”引发的股债双杀时，
为什么遭遇了重大净值回撤？怎样通过引入“宏观通胀/流动性体制先验过滤器”来修补这一缺陷？
- **传统风险平价的隐形杠杆缺陷与体制滤波修补**：
  1. **低波动陷阱与债券端杠杆放大**：传统风险平价的核心是让各类资产贡献等额的风险预算（Risk Contribution）。
     由于国债的历史波动率显著低于股票（例如美债年化波动率 4% vs 标普 16%），为了匹配股票的风险，
     模型必须给债券端施加高达 3~4 倍的财务杠杆。
  2. **股债负相关假设彻底失效**：2022 年美联储为遏制 9.1% 的恶性通胀而开启连续 75 bps 的暴力加息。
     名义长债收益率飙升导致杠杆债券端遭遇世纪暴跌；与此同时，加息与原材料通胀重创美股。
     股债相关系数从 $-0.4$ 骤变至 $+0.7$，高杠杆的债券不仅没有提供对冲避险，反而成为组合最大回撤的“爆雷点”。
  3. **引入体制先验过滤器的修补方案**：
     - 构建“通胀加速度先验状态机”：当通胀动量高于阈值（如 CPI 趋势向上且超标 3%），
       强行调低债券杠杆倍数，将固定收益久期大幅收缩至超短端（Cash / T-Bills）；
     - 引入“商品/通胀对冲资产硬配额”：在通胀体制下，将大宗商品、TIPS（通胀保值国债）以及黄金的风险预算
       提升至 40% 以上，利用大宗商品对意外通胀的正向暴露，中和股债双杀的系统性下行压力。

【Q3 深度参考答案】
为什么现代量化宏观对冲基金在设计“危机防御哨兵”（Kill Switch / Crisis Protocol）时，
绝不能仅依赖价格技术止损，而必须设置外生流动性硬门槛（如 interbank spread 跨越阈值、隔夜拆借冻结）？
- **价格滞后性与流动性黑洞的微观因果**：
  1. **资产价格是流动性抽离的“后视镜”**：在流动性危机初期（如 2008 年雷曼倒闭前夕、2020 年 3 月国债基差策略崩盘），
     许多底层资产由于场外交易（OTC）流动性枯竭而根本无法连续撮合成交，屏幕上的价格变动往往是滞后的。
     若仅依赖移动平均线或价格跌幅止损，当价格真正击穿技术均线时，市场已经陷入无承接盘的“流动性黑洞”。
  2. **银行间利差与拆借冻结是系统性去杠杆的源头**：银行间利差（如 FRA-OIS Spread、Libor/SOFR 溢价、中国 R007-DR007 利差）
     直接度量金融机构之间的交易对手信用风险。当该利差突破极值警戒线时，意味着一级交易商已经拒绝给对冲基金拆借隔夜资金，
     杠杆基金的强制平仓（Liquidation Wave）已经不可避免。
  3. **抢先一步撤离的“防火门效应”**：外生流动性哨兵能够比价格下跌提前 24~72 小时发出红色警报。
     量化系统在全市场普遍踩踏割肉之前，趁订单簿尚有深度时主动砍掉 80% 风险敞口，转入超额现金与国库券，
     从而保全基金的生命线。
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
