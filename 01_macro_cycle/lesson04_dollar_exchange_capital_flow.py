r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 4/5 课
第 4 课：美元指数、汇率弹性与资本流动冲击指数 (Dollar Index, FX Elasticity & Capital Flows)
================================================================================

【课程定位与第一性原理】
在布雷顿森林体系解体后的全球现代法币体系中，美元（USD）是全球储备、国际贸易结算与跨境融资
的底层锚定资产。美联储的货币收紧与宽松，直接驱动全球“美元潮汐（Global Dollar Cycle）”：
1. 抛补利率平价 (CIP) 与套息交易 (Carry Trade)：
   当美债收益率显著高于他国国债收益率（如中美利差倒挂加深: US 10Y - CN 10Y > 0），
   全球投机与避险资本借入低息人民币或日元，通过即期买入并持有美元资产套取无风险息差。
2. 汇率传导与权益折价：
   离岸人民币（USD/CNH）汇率反映国际投行对中国宏观资产的边际风险溢价定价。
   当美元指数（DXY）走强且人民币快速走弱时，以外币计价的跨国基金（如挂钩 MSCI 中国或富时A50的全球ETF）
   面临双重汇率折损，被迫系统性减配以贵州茅台、宁德时代为代表的 A 股核心资产白马股。

【核心传导机制】
```mermaid
flowchart TD
    FedRates["美联储保持高利率 / 美债 10Y 居高不下"] --> Spread["中美利差深度倒挂 (美债收益率 > 中债收益率)"]
    DXY["全球避险或经济分化 ➔ 美元指数 DXY 强势走高"] --> FXPressure
    Spread --> FXPressure["人民币贬值压力增大 (USD/CNH 汇率上行)"]
    FXPressure --> UnhedgedLoss["海外全球宏观配置基金遭遇外汇折算亏损与 VaR 预警"]
    UnhedgedLoss --> Outflow["北向资金 (陆股通) 呈现持续净流出"]
    Outflow --> CoreEquity["A 股核心资产权重股杀估值，指数面临系统性流动性抽水"]
```

【量化模型：资本流动冲击指数 (Capital Flow Shock Index, CFSI)】
综合利差、美元动量与汇率变化率，构建量化预警指标：
    Spread_diff = us_yield - cn_yield
    CFSI = w_spread * Spread_diff + w_dxy * dxy_pct + w_cnh * cnh_pct
根据 CFSI 阈值将市场状态划分为：
- CFSI > 2.0: 'Extreme_Shock' (极度冲击，北向资金大单流出高危期)
- 1.0 < CFSI <= 2.0: 'Warning' (预警状态，外资风险偏好收缩)
- CFSI <= 1.0: 'Normal' (常态或资金顺差流入期)

【思考题】
Q1: 为什么人民币汇率快速贬值（如 USD/CNH 向上突破关键心理关口 7.20 / 7.30）时，往往伴随着
    北向资金（陆股通）的巨额净流出和 A 股核心资产的剧烈估值踩踏？
    请从外币净值结算、外汇风险敞口对冲成本（FX Hedging Cost）以及海外多资产基金的主动降仓规则推导。
Q2: 什么是跨国套利交易（Carry Trade）？2024年8月初“日元套息交易大崩溃”（Yen Carry Trade Unwind）
    为什么会在短短几天内引发日经225单日暴跌12%、美股七巨头重挫和全球恐慌指数 VIX 飙升至 65？
Q3: 央行外汇管理工具箱中，“中间价逆周期调节因子（Counter-Cyclical Factor）”、“外汇存款准备金率”
    与“离岸央票发行”如何通过影响离岸人民币流动性成本来击退空头？在量化微观层面会留下怎样的特征信号？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现资本外流基础压力模型 (1分)；
  2. 准确计算汇率对股票收益率的回归弹性敏感度 (1.5分)；
  3. 准确计算综合资本流动冲击指数 CFSI 并完成状态评级 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须阐释跨国资金流、对冲成本与借贷平仓机制；
- 通过线：8/10 分。一票否决：利差方向算反、将汇率贬值误判为跨国资本流入、删除断言。
"""

from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd


def calculate_capital_flow_pressure(us_yield: pd.Series, cn_yield: pd.Series, dxy_change: pd.Series) -> pd.Series:
    """
    资本外流压力评分指数:
    Spread_diff = us_yield - cn_yield (美中国债利差倒挂程度, %)
    Pressure = Spread_diff * 0.6 + dxy_change * 0.4

    参数:
        us_yield: 美国10年期国债收益率 (%)
        cn_yield: 中国10年期国债收益率 (%)
        dxy_change: 美元指数百分比变化率 (%)

    返回:
        pd.Series: 压力评分
    """
    # TODO: 实现资本流动压力计算公式
    pass


def calculate_exchange_rate_elasticity(cnh_returns: pd.Series, equity_returns: pd.Series) -> float:
    """
    计算股票资产对人民币汇率变动的弹性系数 (Beta):
        Elasticity = Cov(equity_returns, cnh_returns) / Var(cnh_returns)
    注: USD/CNH 上升代表人民币贬值，若 A 股随之受挫下跌，则 Elasticity 为显著负值。

    参数:
        cnh_returns: USD/CNH 汇率变化率 (百分比或对数收益)
        equity_returns: 股票基准指数收益率 (同周期)

    返回:
        float: 弹性系数 Beta
    """
    # TODO: 计算协方差与方差并返回一阶回归弹性
    pass


def compute_composite_cfsi(
    us_yield: pd.Series,
    cn_yield: pd.Series,
    dxy_pct: pd.Series,
    cnh_pct: pd.Series,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[pd.Series, pd.Series]:
    """
    计算多因子综合资本流动冲击指数 (CFSI) 与体制标签:
        Spread = us_yield - cn_yield
        CFSI = w_spread * Spread + w_dxy * dxy_pct + w_cnh * cnh_pct
    状态判定规则:
        - CFSI > 2.0 -> 'Extreme_Shock'
        - 1.0 < CFSI <= 2.0 -> 'Warning'
        - CFSI <= 1.0 -> 'Normal'

    参数:
        us_yield: 美债10Y收益率
        cn_yield: 中债10Y收益率
        dxy_pct: 美元指数变动 (%)
        cnh_pct: USD/CNH 变动 (%)
        weights: 权重配置字典，默认 {'spread': 0.4, 'dxy': 0.3, 'cnh': 0.3}

    返回:
        Tuple[pd.Series, pd.Series]: (cfsi_score, regime_labels)
    """
    # TODO: 合成 CFSI 并标记对应的三个预警等级
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 利差与流动压力 ----------------
    us_y = pd.Series([4.5, 4.8, 5.0])
    cn_y = pd.Series([2.5, 2.4, 2.2])
    dxy_pct = pd.Series([0.5, 1.2, -0.8])
    pressure = calculate_capital_flow_pressure(us_y, cn_y, dxy_pct)
    assert abs(pressure.iloc[0] - (2.0 * 0.6 + 0.5 * 0.4)) < 1e-4, f"压力计算偏差: {pressure.iloc[0]}"
    assert abs(pressure.iloc[1] - (2.4 * 0.6 + 1.2 * 0.4)) < 1e-4, f"压力计算偏差: {pressure.iloc[1]}"

    # ---------------- 基础测试 2: 汇率敏感弹性 ----------------
    # 模拟汇率贬值 (cnh_ret > 0) 时股票承压下行 (eq_ret < 0) 的典型市场关系
    np.random.seed(42)
    synth_cnh_ret = pd.Series(np.random.normal(0.2, 0.5, 40))
    synth_eq_ret = -1.5 * synth_cnh_ret + pd.Series(np.random.normal(0.0, 0.1, 40))
    elasticity = calculate_exchange_rate_elasticity(synth_cnh_ret, synth_eq_ret)
    assert -1.7 <= elasticity <= -1.3, f"弹性回归系数应在 -1.7 ~ -1.3 之间, 实际为: {elasticity}"

    # ---------------- 基础测试 3: 综合 CFSI 冲击指数 ----------------
    us_t = pd.Series([3.0, 4.5, 5.2])
    cn_t = pd.Series([2.8, 2.3, 2.0]) # 利差依次为: 0.2, 2.2, 3.2
    dxy_t = pd.Series([0.2, 1.0, 2.5])
    cnh_t = pd.Series([0.1, 0.8, 2.0])

    cfsi, regimes = compute_composite_cfsi(us_t, cn_t, dxy_t, cnh_t)
    assert cfsi.iloc[0] < 1.0, f"第0期应为平稳常态, 实际为: {cfsi.iloc[0]}"
    assert regimes.iloc[0] == 'Normal', f"预期 Normal, 实际为: {regimes.iloc[0]}"

    assert 1.0 < cfsi.iloc[1] <= 2.0, f"第1期应为预警状态, 实际为: {cfsi.iloc[1]}"
    assert regimes.iloc[1] == 'Warning', f"预期 Warning, 实际为: {regimes.iloc[1]}"

    assert cfsi.iloc[2] > 2.0, f"第2期应为极端冲击, 实际为: {cfsi.iloc[2]}"
    assert regimes.iloc[2] == 'Extreme_Shock', f"预期 Extreme_Shock, 实际为: {regimes.iloc[2]}"

    print("Lesson 04 Exercise Passed!")
