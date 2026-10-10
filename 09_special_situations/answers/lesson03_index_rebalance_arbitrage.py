r"""
# 模块 09：特殊事件驱动与低风险套利 · 第 3 课：指数成分股定期调整与被动资金配置套利

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握主流宽基指数（沪深300、中证500、标普500、MSCI）成分股定期调整（Index Rebalancing）的编制规则与时间表；
2. 深刻理解被动跟踪资金（Passive AUM / ETF / 指数增强基金）在调仓生效日的机械性交易行为与流动性挤兑效应；
3. 掌握基于市场微观结构的平方根市场冲击定律（Square-Root Law of Market Impact）与“日均成交量吸收天数（Days of ADV）”度量模型；
4. 编写代码实现指数调仓被动流动性冲击测算引擎，筛选高弹性套利标的，并评估开仓抢跑与收盘倒手（MOC）的期望收益。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，阐述跨期套利拥挤度与生效日“尾盘集合竞价流动性反转”现象。

---
## 核心心智模型与数理推导

### 1. 指数调整套利的生命周期与时间拓扑

```
        考察截止日                    官方公告日                    生效实施日 (T_eff)
            │                            │                               │
            ▼                            ▼                               ▼
    ┌───────────────┐            ┌───────────────┐               ┌───────────────┐
    │ 步骤 1：名单预测│───────────►│ 步骤 2：抢跑建仓│──────────────►│ 步骤 3：尾盘交割│
    └───────────────┘            └───────────────┘               └───────────────┘
     量化团队依据公开规则          公募与散户跟风买入               被动 ETF 必须在收盘
     提前 1~2 个月推算名单        推动调入股继续上涨               集合竞价不计成本无脑买齐;
     低位悄悄建立多头底仓         调出股承压下跌                  套利者高位精准倒手了结！
                                                                         │
                                                                         ▼
                                                                 ┌───────────────┐
                                                                 │ 步骤 4：均值反转│
                                                                 └───────────────┘
                                                                  人工流动性买盘消失，
                                                                  调入股大概率回落超跌
```

### 2. 被动资金流动性冲击模型 (Market Impact)

假设跟踪目标指数的被动资金资产总规模为 $\text{AUM}_{\text{passive}}$：
- **调入股票 $i$ 的目标被动买入金额**：
  $$V_{\text{buy}, i} = \text{AUM}_{\text{passive}} \times w_i$$
  其中 $w_i$ 为该股票在新指数中的理论权重。
- **日均成交金额吸收天数（Days of ADV）**：
  $$\text{Days of ADV}_i = \frac{V_{\text{buy}, i}}{\text{ADV}_i}$$
  其中 $\text{ADV}_i$ 为该股票近 20~60 个交易日的日均成交额（Average Daily Dollar Volume）。
  - 若 $\text{Days of ADV} \ge 3.0$：说明被动资金需要吃掉该股整整 3 天以上的全部市场交易量，必然形成显著的供需失衡与价格上推冲击！

- **平方根市场冲击定律（Square-Root Law）**：
  根据 Barra 与 Almgren-Chriss 微观结构理论，大额被动资金强行买入引发的相对价格冲击百分比与订单规模占 ADV 比例的平方根成正比：
  $$\text{Impact Pct} = \text{Sign} \times \eta \times \sqrt{\text{Days of ADV}}$$
  - 调入股（INCLUSION）：$\text{Sign} = +1$
  - 调出股（EXCLUSION）：$\text{Sign} = -1$
  - $\eta$ 为市场流动性冲击弹性系数（A股通常在 0.02~0.04 之间）。
"""

import math
from typing import List, Dict, Any


class IndexRebalanceArbitrageEngine:
    """
    指数成分股调整被动资金流动性冲击测算与套利分析引擎。
    """

    def __init__(self, passive_aum: float, impact_coefficient: float = 0.03):
        """
        :param passive_aum: 跟踪该指数的被动资金总规模 (美元或元)
        :param impact_coefficient: 平方根市场冲击弹性系数 eta (默认 0.03)
        """
        self.passive_aum = passive_aum
        self.impact_coefficient = impact_coefficient

    def estimate_liquidity_impact(self, stock_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        测算每只调入/调出股票的被动资金流动性冲击。
        
        输入记录格式：
        stock_records = [
            {
                "symbol": "600100",
                "name": "A公司",
                "action": "INCLUSION",  # INCLUSION (调入) 或 EXCLUSION (调出)
                "index_weight": 0.015,  # 指数目标权重
                "adv_dollar": 30000000.0, # 近期日均成交金额
                "current_price": 20.0   # 消息前基准市价
            },
            ...
        ]
        """
        results = []
        for stock in stock_records:
            symbol = stock["symbol"]
            name = stock.get("name", symbol)
            action = stock["action"].upper()
            weight = stock["index_weight"]
            adv = stock["adv_dollar"]
            curr_p = stock["current_price"]

            # 1. 被动资金买入/卖出总额
            passive_flow = self.passive_aum * weight

            # 2. ADV 吸收天数 (Days of ADV)
            days_of_adv = passive_flow / adv if adv > 0 else 0.0

            # 3. 基于平方根法则计算预期相对价格冲击 (%)
            base_impact = self.impact_coefficient * math.sqrt(days_of_adv)
            sign = 1.0 if action == "INCLUSION" else -1.0
            expected_impact_pct = sign * base_impact

            # 4. 预期目标价格
            target_price = curr_p * (1.0 + expected_impact_pct)

            results.append({
                "symbol": symbol,
                "name": name,
                "action": action,
                "passive_flow": round(passive_flow, 2),
                "days_of_adv": round(days_of_adv, 2),
                "expected_impact_pct": round(expected_impact_pct * 100.0, 2),
                "expected_target_price": round(target_price, 2)
            })

        return results

    def screen_high_impact_arbitrage_targets(
        self,
        stock_records: List[Dict[str, Any]],
        min_days_of_adv: float = 3.0
    ) -> List[Dict[str, Any]]:
        """
        筛选具备高确定性流动性挤兑的重点套利标的 (Days of ADV >= min_days_of_adv)。
        按 days_of_adv 降序排列。
        """
        all_impacts = self.estimate_liquidity_impact(stock_records)
        screened = [s for s in all_impacts if s["days_of_adv"] >= min_days_of_adv]
        screened.sort(key=lambda x: x["days_of_adv"], reverse=True)
        return screened


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么随着量化对冲基金普遍建立“指数调整预测模型”，提前数周甚至数月抢跑（Front-running），导致指数调整官方公布日反而经常出现“利好兑现成利空（Sell the News）”的诡异暴跌？

参考答案：
1. 预测透明度与超前预期消化：
   指数公司（如中证指数公司、标普道琼斯）的成分股编制规则（如过去一年日均成交额前 50%、总市值排序、财务扣非利润等）是完全公开透明的。
   专业的量化团队可以在考察期截止前 1~2 个月精确推算出 90% 以上的调入调出名单，并在低位大举建仓抢跑。
2. 拥挤度爆炸与流动性反噬：
   当官方正式公布调仓名单时，该股票已经在抢跑资金推升下积累了 15%~30% 的巨额浮盈，估值显著透支。
   此时市场上的主流散户和次级机构才看到新闻蜂拥买入，而原本埋伏已久的多头套利资金将其视为完美的“高位对手盘流动性”，
   集中抛售获利了结，导致“官宣公布日”不仅不大涨，反而遭遇沉重的获利盘砸盘暴跌。

### Q2：在生效日（Implementation Date）收盘集合竞价（MOC - Market-on-Close）阶段，为什么被动 ETF 基金经理即便明知股价被严重拉高，也必须不计成本挂涨停价甚至市价扫盘买齐？

参考答案：
1. 跟踪误差（Tracking Error）是一票否决的刚性考核红线：
   被动指数型 ETF 的基金合同明确规定：其核心投资目标不是战胜大盘，而是将相对于标的指数的跟踪偏离度（Tracking Error）降至极致（通常要求日均偏离 < 0.1%）。
   指数公司官方计算指数收盘点位时，一律采用生效日当天的“收盘价（Closing Price）”。
2. 任何时间错配都会造成永久性跟踪误差：
   如果 ETF 基金经理为了“省成本”而在盘中分批买入，或者在第二天开盘买入，一旦该股在盘中大幅波动，
   ETF 的实际成交均价就会与指数官方收盘基准价产生不可逆的巨大价差，导致基金出现严重的跟踪偏离而被交易所问询或基民赎回。
   因此，ETF 必须且只能在生效日最后一刻（14:57~15:00 集合竞价）将所有调仓订单以 MOC 形式一次性提交，宁可承受短期高价买入，也绝不承担跟踪误差违约风险。
   套利资金正是精准利用这一“制度性被动刚需”，在集合竞价把筹码倾销给 ETF。

### Q3：比较中国 A 股（如沪深 300 / 中证 500）与全球跨市场指数（如 MSCI 新兴市场指数）在成分股调整执行机制与流动性冲击上的本质区别。

参考答案：
1. 资金体量与跨境流动限制：
   - 沪深 300 调整主要影响境内公募 ETF、量化中性基金与融券对冲池，资金交收在 T+1 内于中登公司闭环完成，无汇率与外汇配额约束。
   - MSCI 新兴市场指数调整影响的是遍布全球数万亿美元的离岸主权财富基金、跨国养老金与国际 ETF。
     国际资金必须通过沪深港通（北向资金 QFII）跨境调拨美元并实时兑换离岸人民币（CNH），受限于陆股通每日额度、外汇即期流动性以及两地结算交收假期差异。
2. 冲击时点与波幅放大：
   - MSCI 每次季度调整生效日的最后 5 分钟，北向资金往往会在收盘集合竞价瞬间产生数十亿甚至数百亿元人民币的极端脉冲放量（俗称“北向黄金三分钟”）；
   - 相关标的股票常在 14:59 出现直线拉升 3%~5% 或瞬间跳水 3%~5% 的壮观异动，次日早盘又快速均值回归修复，为高频统计套利提供了极高夏普的脉冲反转交易机会。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] IndexRebalanceArbitrageEngine Liquidity Impact Calculation...")
    # 模拟指数被动跟踪资金 AUM = 100 亿元 (1e10)
    engine = IndexRebalanceArbitrageEngine(passive_aum=10000000000.0, impact_coefficient=0.03)

    test_stocks = [
        {
            "symbol": "600100",
            "name": "A公司",
            "action": "INCLUSION",  # 调入
            "index_weight": 0.015,  # 目标权重 1.5% -> 买入 1.5 亿
            "adv_dollar": 30000000.0, # 日均成交 0.3 亿 -> 需要 5.0 天 ADV
            "current_price": 20.0
        },
        {
            "symbol": "000200",
            "name": "B公司",
            "action": "INCLUSION",  # 调入
            "index_weight": 0.005,  # 目标权重 0.5% -> 买入 0.5 亿
            "adv_dollar": 50000000.0, # 日均成交 0.5 亿 -> 需要 1.0 天 ADV
            "current_price": 15.0
        },
        {
            "symbol": "600300",
            "name": "C公司",
            "action": "EXCLUSION",  # 调出
            "index_weight": 0.008,  # 原权重 0.8% -> 卖出 0.8 亿
            "adv_dollar": 20000000.0, # 日均成交 0.2 亿 -> 需要 4.0 天 ADV
            "current_price": 10.0
        }
    ]

    impacts = engine.estimate_liquidity_impact(test_stocks)

    # 1. 验证 A公司:
    # 买入金额 = 100亿 * 0.015 = 1.5亿
    # Days of ADV = 1.5亿 / 0.3亿 = 5.0 天
    # 冲击百分比 = +0.03 * sqrt(5.0) ≈ +0.03 * 2.236068 ≈ +6.71%
    # 目标价 = 20.0 * (1 + 0.0671) = 21.34
    res_a = impacts[0]
    assert res_a["passive_flow"] == 150000000.0
    assert res_a["days_of_adv"] == 5.0
    assert res_a["expected_impact_pct"] == 6.71
    assert res_a["expected_target_price"] == 21.34

    # 2. 验证 B公司:
    # Days of ADV = 0.5亿 / 0.5亿 = 1.0 天
    # 冲击 = +0.03 * sqrt(1.0) = +3.00%
    # 目标价 = 15.0 * 1.03 = 15.45
    res_b = impacts[1]
    assert res_b["days_of_adv"] == 1.0
    assert res_b["expected_impact_pct"] == 3.00
    assert res_b["expected_target_price"] == 15.45

    # 3. 验证 C公司 (调出):
    # Days of ADV = 0.8亿 / 0.2亿 = 4.0 天
    # 冲击 = -0.03 * sqrt(4.0) = -6.00%
    # 目标价 = 10.0 * 0.94 = 9.40
    res_c = impacts[2]
    assert res_c["days_of_adv"] == 4.0
    assert res_c["expected_impact_pct"] == -6.00
    assert res_c["expected_target_price"] == 9.40

    print("[Testing] High Impact Arbitrage Screening...")
    # 筛选 Days of ADV >= 3.0 的高冲击品种
    screened = engine.screen_high_impact_arbitrage_targets(test_stocks, min_days_of_adv=3.0)
    # 应筛选出 A公司 (5.0天) 与 C公司 (4.0天)，且 A公司排在前面
    assert len(screened) == 2
    assert screened[0]["symbol"] == "600100"
    assert screened[1]["symbol"] == "600300"
    assert screened[0]["days_of_adv"] > screened[1]["days_of_adv"]

    print("All assertions passed! Module 09 Lesson 03 verification successful.")
