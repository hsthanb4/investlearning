r"""
# 模块 09：特殊事件驱动与低风险套利 · 第 1 课：现金并购套利、年化利差与交易破裂概率模型

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握现金要约收购（Cash Tender Offer）与并购套利（Merger Arbitrage）的微观运作机理与利差（Spread）定价逻辑；
2. 熟练计算名义利差、年化收益率、未受干扰基准价（Unaffected Price）以及交易破裂潜在下行亏损；
3. 掌握并购期望收益模型，精准反推市场交易价格中隐含的交易破裂概率（Implied Break Probability）与盈亏平衡胜率；
4. 编写代码实现并购套利度量模型，并在不同监管审批情境与下行假设下进行参数敏感性压力测试。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，剖析“在压路机前捡硬币”的负偏斜肥尾风险与换股套利对冲架构。

---
## 核心心智模型与数理推导

### 1. 并购利差与年化收益率公式

当收购方宣布以固定现金价格 $P_{\text{offer}}$ 收购目标公司时，目标公司的股票市价 $P_{\text{current}}$ 通常会迅速跳涨至接近但略低于 $P_{\text{offer}}$ 的水平：
$$
P_{\text{unaffected}} < P_{\text{current}} < P_{\text{offer}}
$$
存在折价价差（Gross Spread）的原因是：市场认为交易存在不能在预期日期完成甚至彻底破裂的风险（反垄断否决、地缘政治审查、融资暴雷、重大不利变化 MAC 条款触发等）。
- **绝对名义利差（Gross Spread）**：
  $$S = P_{\text{offer}} - P_{\text{current}}$$
- **绝对名义收益率（Gross Return）**：
  $$R_{\text{gross}} = \frac{P_{\text{offer}} - P_{\text{current}}}{P_{\text{current}}}$$
- **简单年化收益率（Annualized Return）**：
  $$R_{\text{ann}} = R_{\text{gross}} \times \frac{365}{\text{Days to Close}}$$

### 2. 交易破裂下行幅度与期望收益模型

若交易最终破裂（Deal Breaks），标的资产价格通常会迅速跌回未受干扰价格 $P_{\text{unaffected}}$（即收购要约公布前的基准价格）：
- **交易破裂单股下行损失（Downside Loss）**：
  $$D = P_{\text{current}} - P_{\text{unaffected}}$$
- **交易破裂跌幅比例**：
  $$\text{Loss}_{\text{pct}} = \frac{P_{\text{current}} - P_{\text{unaffected}}}{P_{\text{current}}}$$

假设交易成功概率为 $p$，破裂概率为 $1 - p$：
- **单股期望收益（Expected Payoff）**：
  $$\mathbb{E}[\text{Payoff}] = p \times S - (1 - p) \times D = p \times (P_{\text{offer}} - P_{\text{current}}) - (1 - p) \times (P_{\text{current}} - P_{\text{unaffected}})$$
- **盈亏平衡临界成功概率（Breakeven Probability, $p^*$）**：
  令 $\mathbb{E}[\text{Payoff}] = 0$：
  $$p^* \times S = (1 - p^*) \times D \implies p^* \times (S + D) = D$$
  $$p^* = \frac{D}{S + D} = \frac{P_{\text{current}} - P_{\text{unaffected}}}{P_{\text{offer}} - P_{\text{unaffected}}}$$
- **市场隐含交易破裂概率（Implied Break Probability, $q^*$）**：
  $$q^* = 1 - p^* = \frac{S}{S + D} = \frac{P_{\text{offer}} - P_{\text{current}}}{P_{\text{offer}} - P_{\text{unaffected}}}$$
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
    
    :param offer_price: 收购方现金要约价 (P_offer)
    :param current_price: 目标公司当前二级市场交易价 (P_current)
    :param unaffected_price: 收购消息发布前的未受干扰参考价 (P_unaffected)
    :param days_to_close: 预计交易最终交割交收所需天数
    :param estimated_success_prob: 操盘手/研究员基于反垄断评估主观估计的交易成功概率 (p)
    :return: 包含利差、年化收益率、下行敞口、期望收益及隐含胜率阈值的量化结果字典
    """
    spread = offer_price - current_price
    gross_return = spread / current_price
    ann_return = gross_return * (365.0 / days_to_close)

    downside_loss = current_price - unaffected_price
    downside_pct = downside_loss / current_price

    expected_payoff = estimated_success_prob * spread - (1.0 - estimated_success_prob) * downside_loss
    expected_return_pct = expected_payoff / current_price

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
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么华尔街将并购套利（Merger Arbitrage）形象地比喻为“在压路机前捡硬币（Picking up nickels in front of a steamroller）”？从其收益分布的偏度（Skewness）与峰度（Kurtosis）角度进行推导。

参考答案：
1. 非对称赔率与左偏肥尾（Extreme Left Skewness）：
   - 在正常成功的并购案中，套利者只能获得微薄但确定的利差（例如 3%~5% 的价差，折合年化 8%~15%），这就是那枚“硬币（Nickels）”；
   - 然而，一旦交易因监管反垄断否决、国家安全审查（如 CFIUS）或收购方暴雷而破裂，标的股票通常会在数分钟内暴跌 20%~50%（跌回甚至跌破 $P_{\text{unaffected}}$），这就是那台呼啸而来的“压路机（Steamroller）”；
   - 赔率特征：赚只赚 3 美元，亏一次亏 25 美元。哪怕发生概率仅 5%，一次意外暴跌就会吞噬此前 8~10 笔成功交易的全部累计利润。
2. 收益统计分布异化：
   并购套利基金的月度收益序列在大多数平稳月份呈现极小的正收益、近乎为零的低波动率（形似无风险国债）；
   但其收益率分布具有极高负偏度（Negative Skewness < -3）与厚尾峰度（Fat Tails / High Kurtosis），在危机年份表现为断崖式的深水回撤。

### Q2：对于“换股收购（Stock-for-Stock Merger，即 1 股目标公司股票换兑收 0.8 股收购方股票）”，对冲基金如何通过配对交易（Pairs Trading）彻底消除收购方股票的系统性市场风险？

参考答案：
1. 换股比例与合成空头敞口：
   - 在换股收购中，目标公司股东最终拿到的是收购方的股票而非现金。因此，目标公司股价不仅取决于并购成功与否，还直接随收购方股票价格同向涨跌。
   - 套利基金若单纯买入目标公司股票，将直接暴露于收购方的市场 Beta 风险（若大盘暴跌导致收购方股价腰斩，目标公司亦将腰斩）。
2. 无风险价差对冲架构：
   - 设换股比例为 $\rho$（例如 $\rho = 0.8$）。
   - 套利基金在买入 1 股目标公司股票的同时，在现货市场以市价融券做空 $\rho$ 股收购方的股票；
   - 无论未来宏观市场如何暴跌、收购方股价如何剧烈下挫，该配对多空组合的总市值波动被完全锁死；
   - 一旦交易正式完成交割，套利基金将持有的 1 股目标公司股票按约兑换为 $\rho$ 股收购方新股，并直接用于归还融券借入的空头现货平仓。
   - 基金最终稳稳锁定建仓瞬间的固定折价利差：$\text{Profit} = \rho \cdot P_{\text{acquirer}} - P_{\text{target}}$，完全实现 Market-Neutral。

### Q3：为什么在反垄断监管趋紧的环境下（例如 FTC/DOJ 采取更加激进的反垄断诉讼态度），传统依赖“历史统计胜率（如 95%）”的并购套利模型会发生系统性灾难？

参考答案：
1. 监管体制转换（Regime Shift）破坏了样本历史分布的平稳性假设：
   传统量化模型往往基于过去 20 年全球数千宗并购案的经验统计（历史交易成功率高达 92%~95%），并将先验成功概率设为 0.95。
   然而，一旦监管政策发生结构性转向（例如出台全新的反垄断指南、对大型科技并购采取“凡申报必严审甚至直接诉讼阻止”的激进姿态），
   行业真实破裂概率从历史的 5% 激增至 25%~35%。
2. 杠杆放大与相关性陷阱：
   许多套利基金为了将 5% 的名义利差增厚至 15%~20% 的对冲基金收益率，普遍施加了 3~5 倍的杠杆。
   在监管风暴下，原本被认为互不相关的多笔大宗科技并购案（例如微软收购动视暴雪、博通收购威睿、Adobe 收购 Figma）同时面临审查受阻与破裂威胁。
   原本以为是独立分散的特质风险（Idiosyncratic Risk），瞬间异化为系统性监管关联风险，引发巨额连环亏损与被迫去杠杆平仓潮。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Merger Arbitrage Metrics Calculation...")
    # 案例：现金要约收购
    # 要约收购价 105.0, 当前市价 100.0, 消息公布前未受干扰价 80.0
    # 预计 90 天完成交割, 操盘手主观评估成功率 95% (0.95)
    metrics = calculate_merger_arbitrage_metrics(
        offer_price=105.0,
        current_price=100.0,
        unaffected_price=80.0,
        days_to_close=90,
        estimated_success_prob=0.95
    )

    # 1. 绝对利差 = 105 - 100 = 5.0, 名义收益率 5.0%
    assert metrics["gross_spread"] == 5.0
    assert metrics["gross_return_pct"] == 5.0

    # 2. 简单年化收益率 = 5.0% * (365 / 90) ≈ 20.28%
    assert metrics["annualized_return_pct"] == 20.28, f"Got {metrics['annualized_return_pct']}"

    # 3. 破裂下行损失 = 100 - 80 = 20.0 (跌幅 20.0%)
    assert metrics["downside_loss"] == 20.0
    assert metrics["downside_loss_pct"] == 20.0

    # 4. 盈亏平衡临界胜率 = 20 / (5 + 20) = 20 / 25 = 0.8000 (80.0%)
    assert metrics["breakeven_success_prob"] == 0.8000
    assert metrics["implied_break_prob"] == 0.2000

    # 5. 期望每股收益 = 0.95 * 5.0 - 0.05 * 20.0 = 4.75 - 1.00 = 3.75 美元 (3.75%)
    assert metrics["expected_payoff"] == 3.75
    assert metrics["expected_return_pct"] == 3.75

    print("[Testing] Boundary Conditions (Zero Spread & Near-Certain Deal)...")
    # 当交易毫无利差时 (current_price == offer_price)
    zero_spread = calculate_merger_arbitrage_metrics(
        offer_price=100.0,
        current_price=100.0,
        unaffected_price=70.0,
        days_to_close=30,
        estimated_success_prob=0.99
    )
    assert zero_spread["gross_spread"] == 0.0
    assert zero_spread["annualized_return_pct"] == 0.0
    assert zero_spread["breakeven_success_prob"] == 1.0
    assert zero_spread["implied_break_prob"] == 0.0

    print("All assertions passed! Module 09 Lesson 01 verification successful.")
