r"""
# 模块 09：特殊事件驱动与低风险套利 · 第 1 课：现金并购套利、年化利差与交易破裂概率模型

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

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
    # TODO:
    # 1. 计算名义利差 spread = offer_price - current_price, 名义收益率 gross_return = spread / current_price
    # 2. 计算简单年化收益率 annualized_return = gross_return * (365 / days_to_close)
    # 3. 计算破裂下行损失 downside_loss = current_price - unaffected_price, downside_pct = downside_loss / current_price
    # 4. 计算期望单股收益 expected_payoff = p * spread - (1 - p) * downside_loss, expected_return_pct = expected_payoff / current_price
    # 5. 计算盈亏平衡胜率 breakeven_p = downside_loss / (offer_price - unaffected_price) (若分母为0则为1.0), implied_break_p = 1 - breakeven_p
    pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么华尔街将并购套利（Merger Arbitrage）形象地比喻为“在压路机前捡硬币（Picking up nickels in front of a steamroller）”？从其收益分布的偏度（Skewness）与峰度（Kurtosis）角度进行推导。

**你的答案：**
[在此处写下你的分析：需对比成功时微薄确定的正收益，与破裂时暴跌回原价的巨额非对称亏损，推导其极度左偏、肥尾的分布特征]


### Q2：对于“换股收购（Stock-for-Stock Merger，即 1 股目标公司股票换兑收 0.8 股收购方股票）”，对冲基金如何通过配对交易（Pairs Trading）彻底消除收购方股票的系统性市场风险？

**你的答案：**
[在此处写下你的分析：需阐述按换股比例建立“做多目标公司 + 融券做空收购方”配对组合的运作机制，证明其完全隔离市场 Beta 风险]


### Q3：为什么在反垄断监管趋紧的环境下（例如 FTC/DOJ 采取更加激进的反垄断诉讼态度），传统依赖“历史统计胜率（如 95%）”的并购套利模型会发生系统性灾难？

**你的答案：**
[在此处写下你的分析：需从监管体制结构性转换（Regime Shift）、先验胜率失真以及多笔大宗科技并购在杠杆放大下的系统性相关性陷阱切入]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
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
    assert metrics["expected_return_pct"] == 3.75

    print("[Testing] Boundary Conditions (Zero Spread & Near-Certain Deal)...")
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
