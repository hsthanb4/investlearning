r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 4/5 课
第 4 课：美元指数、汇率弹性与资本流动冲击指数 (Dollar Index, FX Elasticity & Capital Flows)
================================================================================

::: {.callout-note}
### 投决会外汇风险公理：汇率不是技术点位，而是跨国资本无风险套利平价的清算中枢
- **[全球储备锚定本质]**：美元是全球国际贸易结算、大宗商品计价与离岸跨国银行业务的绝对底层储备资产。美联储的货币收紧与宽松直接主导全球资本潮汐。
- **[抛补利率平价守恒]**：根据 Covered Interest Parity (CIP)，两国外币远期汇率与即期汇率升贴水严格锚定两国无风险国债利差。利差深度倒挂必然驱动套息交易（Carry Trade）资金回流高息货币。
- **[跨国资产折现压制]**：海外全球配置基金（以美元为核算基准）持有 A 股资产时，人民币快速贬值会带来严重的“外币计价折算亏损”，触发主动降低权益敞口的强平风控。
:::

- **[理论传导机制：抛补利率平价与套息资本流]**：

$$
\frac{F_{t, T}}{S_t} = \frac{1 + y^{\text{US}}_{T}}{1 + y^{\text{CN}}_{T}} \implies \text{Spread Difference} \approx y^{\text{US}}_{T} - y^{\text{CN}}_{T}
$$

- **[变量定义域与物理意义]**：
  - $S_t \in \mathbb{R}^+$：即期汇率（USD/CNH）。
  - $F_{t, T} \in \mathbb{R}^+$：期限 $T$ 的远期汇率外汇合约价格。
  - $y^{\text{US}}_{10Y} - y^{\text{CN}}_{10Y}$：中美 10 年期国债收益率剪刀差。利差倒挂越深，套息交易无风险息差诱惑越大，非美货币资本外流压力越大。

- **[引导句锚点 1]**：美元流动性潮汐与全球跨境资本虹吸/泄洪双向通道拓扑如下所示：

```mermaid
flowchart TD
    FedRates["美联储维持高基准利率 / 美债 10Y 居高不下"] --> SpreadInvert["中美利差深度倒挂 (美债收益率 > 中债收益率)"]
    DXYStrong["避险情绪激化 ➔ 美元指数 DXY 强势走高"] --> FXDeprec
    SpreadInvert --> FXDeprec["离岸人民币承压 (USD/CNH 汇率向上贬值破位)"]
    FXDeprec --> UnhedgedLoss["海外全球配置基金遭遇外币结算折算亏损与 VaR 超限"]
    UnhedgedLoss --> NorthOutflow["北向资金 (陆股通) 呈现系统性无差别大单流出"]
    NorthOutflow --> ValuationDrop["A 股茅台/宁德等核心资产杀估值，引发流动性折价"]
```

- **[架构要点拆解 1]**：
  - **[1. 美债高息虹吸]**：美联储维持高基准利率，美债无风险资产收益吸引全球跨国流动性回流美国。
  - **[2. 汇率承压贬值]**：离岸人民币（USD/CNH）面临外生抛压，外币折算损耗增加。
  - **[3. 白马权重抛压]**：北向陆股通资金被迫被动减仓，茅台、宁德等核心白马面临跨期折现估值收缩。

- **[资本流动冲击指数 (Capital Flow Shock Index, CFSI)]**：
  - 综合利差倒挂、美元指数动量与汇率变动率构建量化预警指标：

$$
\text{CFSI}_t = w_s \cdot (y^{\text{US}}_{10Y, t} - y^{\text{CN}}_{10Y, t}) + w_d \cdot \% \Delta \text{DXY}_t + w_e \cdot \% \Delta \text{USDCNH}_t
$$

- **[变量定义域与权重分配]**：
  - $w_s = 0.6, w_d = 0.2, w_e = 0.2$。状态划分阈值：
    - $\text{CFSI} > 2.0$：极度冲击状态（Extreme Shock），北向资金大单流出高危期。
    - $1.0 < \text{CFSI} \le 2.0$：预警状态（Warning），跨国资金风险偏好边际收缩。
    - $\text{CFSI} \le 1.0$：常态或资金顺差流入期（Normal）。

- **[引导句锚点 2]**：资本流动冲击指数（CFSI）三档决策状态分布如下所示：

```mermaid
flowchart LR
    CFSIVal{"CFSI 评分 ?"}
    CFSIVal -->|CFSI <= 1.0| S1["常态顺差期 ➔ 核心白马超配，享受外资溢价"]
    CFSIVal -->|1.0 < CFSI <= 2.0| S2["预警防御期 ➔ 暂停加仓，降低外资高重仓股"]
    CFSIVal -->|CFSI > 2.0| S3["极度冲击期 ➔ 启动汇率风险对冲，防御流动性抽水"]
```

- **[架构要点拆解 2]**：
  - **[1. 常态顺差 (CFSI ≤ 1.0)]**：外资保持稳定净流入，权益白马资产享受估值溢价。
  - **[2. 预警状态 (1.0 < CFSI ≤ 2.0)]**：汇率波动加大，暂停盲目加仓，收窄外资持股比例过高标的。
  - **[3. 极度冲击 (CFSI > 2.0)]**：外资系统性流出，坚决启动外汇风险对冲，配置防御资产。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[外币 NAV 估值盲区]**：境内投资者以人民币看待标的估值，而跨国宏观基金按美元核算净值。汇率贬值直接触发外资 VaR 风险预算硬约束。
- **[优先抛售流动性资产]**：外资被动降仓时，首先遭到清算的是成交额最大、流动性最好的大市值白马龙头，形成反直觉的“优质资产跌得更狠”。
:::

【思考题】
Q1: 为什么人民币汇率快速贬值（如 USD/CNH 向上突破关键心理关口 7.20 / 7.30）时，往往伴随着北向资金（陆股通）的巨额净流出和 A 股核心资产的剧烈估值踩踏？请从外币净值结算、外汇风险敞口对冲成本（FX Hedging Cost）以及海外多资产基金的主动降仓规则推导。
Q2: 什么是跨国套利交易（Carry Trade）？2024年8月初“日元套息交易大崩溃”（Yen Carry Trade Unwind）为什么会在短短几天内引发日经225单日暴跌12%、美股七巨头重挫和全球恐慌指数 VIX 飙升至 65？
Q3: 央行外汇管理工具箱中，“中间价逆周期调节因子（Counter-Cyclical Factor）”、“外汇存款准备金率”与“离岸央票发行”如何通过影响离岸人民币流动性成本来击退空头？在量化微观层面会留下怎样的特征信号？

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
