r"""
================================================================================
模块 09：特殊事件驱动与低风险套利 · 第 1/4 课
第 1 课：现金并购套利、年化利差与交易破裂概率模型 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：在压路机前捡硬币的非对称负偏斜博弈
并购套利（Merger Arbitrage）属于事件驱动策略的王冠。当收购要约公布后，标的资产市价通常上涨至接近但略低于要约现金价，其间折价即为并购利差（Spread）。这一利差并非免费午餐，而是市场对交易因反垄断审查、国家安全调查（CFIUS）或融资破裂导致流产的风险定价补偿。投决会第一要义是穿透赔率结构：成功时仅获取 3%~5% 的有界微利，破裂时却面临标的暴跌 20%~50% 跌回原价的单边无界深渊。
:::

- **[非对称赔率的第一性原理]**：并购套利的单笔胜率极高（历史常态下 90%~95%），但盈亏比极差（$b \approx 0.15 \sim 0.25$）。一次破裂即可抹平数宗成功案例的全年利润。
- **[市场隐含破裂概率反推]**：通过当前市价、要约价与未受干扰价格（Unaffected Price），能够精确反推出市场边际定价所隐含的交易破裂概率（Implied Break Probability）。
- **[监管体制转移（Regime Shift）防范]**：反垄断政策收紧会导致历史统计样本严重失效，特质风险瞬间共振为行业系统性清盘危机。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了现金要约收购中价格收敛与交易破裂下行路径的物理分流拓扑。

```mermaid
flowchart TD
    Unaffected["未受干扰参考价 P_unaffected ($80)"] -->|并购消息公布| Announce["公告日跳涨至市价 P_current ($100)"]
    Announce --> Spread["利差 Spread = P_offer - P_current ($5.0)"]
    Spread --> Branch{"监管审查与股东大会决议"}
    Branch -->|反垄断/审批通过 (成功)| Close["交割完成: 价格收敛至 P_offer ($105) ➔ 获利 +5%"]
    Branch -->|监管否决/交易流产 (破裂)| Break["交易破裂: 暴跌跌回 P_unaffected ($80) ➔ 亏损 -20%"]
```

- **[要点 1：利差包含时间价值与信用溢价]**：利差不仅反映监管审批风险，还包含资金占用期间的货币时间价值与收购方的信用履约风险。
- **[要点 2：破裂下行的刚性重力吸引]**：交易一旦破裂，投机套利资金在数分钟内踩踏出逃，股价几乎必然跌回公告前的真实基本面支撑底价。
- **[要点 3：年化利差的期限弹性]**：交割天数越短，即使名义利差仅 3%，折合简单年化收益率也能突破 20%，对冲基金聚焦于高确定性短周期案源。

锚点指引：下图揭示了并购期望收益模型中盈亏平衡胜率与隐含破裂概率的代数权衡。

```mermaid
flowchart LR
    A["单股期望收益 E[Payoff] = p·Spread - (1-p)·Downside"] --> B{"令期望 E = 0 (临界点)"}
    B --> C["盈亏平衡胜率 p* = Downside / (Spread + Downside) = 80%"]
    B --> D["市场隐含破裂概率 q* = Spread / (Spread + Downside) = 20%"]
    C & D --> E["投决会准入: 主观成功率评估必须显著高于 80% (如 95%) 且严禁单票重仓"]
```

- **[要点 1：盈亏平衡胜率的硬门槛]**：若下行损失高达 20 美元而利差仅 5 美元，策略必须具备至少 80% 的成功率才能达到数学期望保本。
- **[要点 2：市场折价反映的真实分歧]**：利差拉大意味着市场对反垄断审查的悲观预期升温，隐含破裂概率大幅上升。
- **[要点 3：严禁依靠杠杆美化低赔率]**：3~5 倍杠杆会把 20% 的单笔破裂下行直接放大为基金净值穿仓清盘。

【数学与估值模型】
现金并购套利全套核心度量方程：
$$
\text{Gross Spread} = P_{\text{offer}} - P_{\text{current}}, \quad R_{\text{gross}} = \frac{P_{\text{offer}} - P_{\text{current}}}{P_{\text{current}}}
$$
$$
R_{\text{ann}} = R_{\text{gross}} \times \frac{365}{\text{Days to Close}}
$$
$$
\text{Downside Loss} = P_{\text{current}} - P_{\text{unaffected}}, \quad \text{Loss}_{\text{pct}} = \frac{P_{\text{current}} - P_{\text{unaffected}}}{P_{\text{current}}}
$$
$$
\mathbb{E}[\text{Payoff}] = p \cdot (P_{\text{offer}} - P_{\text{current}}) - (1 - p) \cdot (P_{\text{current}} - P_{\text{unaffected}})
$$
$$
p^* = \frac{P_{\text{current}} - P_{\text{unaffected}}}{P_{\text{offer}} - P_{\text{unaffected}}}, \quad q^* = 1 - p^* = \frac{P_{\text{offer}} - P_{\text{current}}}{P_{\text{offer}} - P_{\text{unaffected}}}
$$
变量定义域与参数约束：
- $P_{\text{offer}} > P_{\text{current}} > P_{\text{unaffected}} > 0$：现金收购价格层次。
- $\text{Days to Close} \in [1, 730]$：预计交割所需日历天数。
- $p \in [0, 1]$：主观评估成功概率，$p^*$ 为盈亏平衡临界胜率，$q^*$ 为隐含破裂概率。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **监管审查死刑（CFIUS / FTC 否决）**：涉及国家安全、半导体核心技术或跨国地缘敏感领域的跨国并购，政治阻力不可量化，严禁参与此类‘高利差诱饵’交易。
2. **重大不利变化（MAC 条款）触发**：在漫长审批期内，若目标公司财务造假、核心客户流失或遭遇行业黑天鹅，收购方可合法援引 MAC 协议无责任毁约。
3. **换股收购单边多头裸露**：对于 Stock-for-Stock 并购，必须按换股比例严格做空收购方现货股票构造 Market-Neutral，绝对禁止裸做多目标公司。
:::

【思考题】
Q1: 为什么华尔街将并购套利（Merger Arbitrage）形象地比喻为“在压路机前捡硬币（Picking up nickels in front of a steamroller）”？从其收益分布的偏度（Skewness）与峰度（Kurtosis）角度进行推导。
Q2: 对于“换股收购（Stock-for-Stock Merger，即 1 股目标公司股票换兑收 0.8 股收购方股票）”，对冲基金如何通过配对交易（Pairs Trading）彻底消除收购方股票的系统性市场风险？
Q3: 为什么在反垄断监管趋紧的环境下（例如 FTC/DOJ 采取更加激进的反垄断诉讼态度），传统依赖“历史统计胜率（如 95%）”的并购套利模型会发生系统性灾难？

【Q1 深度参考答案】
- **[收益分布的极度负偏态（Extreme Left Skewness）]**：在正常完成的交易中，套利者仅能获取确定性但极薄弱的名义利差（如 3%~5%），如同弯腰捡起的一枚小硬币；然而一旦反垄断否决，标的在几分钟内断崖暴跌 20%~50% 跌回原价，如同被呼啸而来的压路机碾压。
- **[非对称赔率侵蚀复利]**：赚只赚 5 块，亏一次亏 20 块，盈亏比仅 0.25。哪怕破裂概率只有 5%，单次暴跌即可清空此前 8~10 笔成功交易的全部累计利润。
- **[峰度肥尾与伪夏普陷阱]**：月度净值序列平稳得如同一道直线（波动率极低、伪夏普比率极高），但在黑天鹅破裂年份直接发生断崖式深水下挫，呈现高尖厚尾分布。

【Q2 深度参考答案】
- **[换股收购的 Beta 暴露敞口]**：目标公司最终结算物为收购方股票而非现金，其价值不仅取决于并购成功与否，还随收购方股价同向沉浮。裸多目标公司将直接承受全额市场下行 Beta 风险。
- **[合成空头对冲结构搭建]**：设换股比例为 $\rho = 0.8$。基金在买入 1 股目标公司股票的同时，按市价融券做空 $\rho$ 股收购方股票。无论大盘暴跌抑或收购方股价重挫，该配对组合的总市值波动被完全锁死。
- **[交割时点的实物兑现闭环]**：交易交割当日，基金将持有的目标公司股票按约兑换为收购方新股，并无摩擦归还融券借入的空头现货平仓，彻底锁定建仓瞬间的固定折价利差，完全实现市场中性（Market-Neutral）。

【Q3 深度参考答案】
- **[监管体制转移（Regime Shift）打破平稳性假设]**：传统量化模型基于过去 20 年经验数据将先验成功率固定为 95%。然而当监管政策发生结构性严监管转向时，全行业真实破裂概率从 5% 激增至 25%~35%，静态模型因参数失真而产生灾难性高估。
- **[高杠杆放大与相关性陷阱]**：套利基金普遍施加 3~5 倍杠杆以增厚收益。在监管风暴下，原本被认为互不相关的多笔大宗科技并购同时面临审查受阻与流产威胁。
- **[特质风险异化为系统性违约]**：原本以为分散配置在不同个股的特质风险瞬间汇聚为单一维度的监管风暴，导致加杠杆的多策略基金在流动性踩踏中被迫去杠杆平仓，引发连锁踩踏。
"""

from typing import Dict, Any


def calculate_merger_arbitrage_metrics(
    offer_price: float,
    current_price: float,
    unaffected_price: float,
    days_to_close: int,
    estimated_success_prob: float = 0.90
) -> Dict[str, float]:
    """
    计算现金并购套利全套量化度量指标。
    """
    spread = offer_price - current_price
    gross_return = spread / current_price if current_price > 0 else 0.0

    ann_return = gross_return * (365.0 / days_to_close) if days_to_close > 0 else 0.0

    downside_loss = current_price - unaffected_price
    downside_pct = downside_loss / current_price if current_price > 0 else 0.0

    expected_payoff = estimated_success_prob * spread - (1.0 - estimated_success_prob) * downside_loss
    expected_return_pct = expected_payoff / current_price if current_price > 0 else 0.0

    total_range = offer_price - unaffected_price
    if total_range > 0:
        breakeven_p = downside_loss / total_range
    else:
        breakeven_p = 1.0

    implied_break_p = 1.0 - breakeven_p

    return {
        "gross_spread": round(spread, 4),
        "gross_return_pct": round(gross_return * 100.0, 2),
        "annualized_return_pct": round(ann_return * 100.0, 2),
        "downside_loss": round(downside_loss, 4),
        "downside_loss_pct": round(downside_pct * 100.0, 2),
        "expected_payoff": round(expected_payoff, 4),
        "expected_return_pct": round(expected_return_pct * 100.0, 2),
        "breakeven_success_prob": round(breakeven_p, 4),
        "implied_break_prob": round(implied_break_p, 4)
    }


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Merger Arbitrage Metrics Calculation...")
    metrics = calculate_merger_arbitrage_metrics(
        offer_price=105.0,
        current_price=100.0,
        unaffected_price=80.0,
        days_to_close=90,
        estimated_success_prob=0.95
    )

    assert metrics["gross_spread"] == 5.0
    assert metrics["gross_return_pct"] == 5.0
    assert metrics["annualized_return_pct"] == 20.28, f"Got {metrics['annualized_return_pct']}"
    assert metrics["downside_loss"] == 20.0
    assert metrics["downside_loss_pct"] == 20.0
    assert metrics["breakeven_success_prob"] == 0.8000
    assert metrics["implied_break_prob"] == 0.2000
    assert metrics["expected_payoff"] == 3.75

    print("All assertions passed! Module 09 Lesson 01 verification successful.")
