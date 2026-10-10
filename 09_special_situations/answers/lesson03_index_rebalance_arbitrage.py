r"""
================================================================================
模块 09：特殊事件驱动与低风险套利 · 第 3/4 课
第 3 课：指数成分股定期调整与被动资金流动性冲击套利 (Index Rebalancing Arbitrage) - 参考答案版
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：被动投资刚性契约创造的确定性流动性挤兑
现代资产管理行业中最庞大的机械性买卖力量并非来自主观基金经理，而是来自于被动跟踪主流宽基指数（沪深300、中证500、标普500、MSCI）的数万亿 ETF 与指数增强基金。被动基金经理受制于严苛的契约考核：其终极目标是将相对于标的指数的跟踪偏离度（Tracking Error）降至绝对极小值（<0.1%）。为了在指数调整生效日（Implementation Date）消除时间错配，被动基金必须且只能在生效日最后一刻（收盘集合竞价 MOC）以不计成本的市价顶格买齐调入股、抛尽调出股。这种非弹性的刚性买卖需求，为量化对冲基金提供了物理规律般可靠的跨期流动性套利沃土。
:::

- **[被动买盘的微观物理冲击]**：根据市场微观结构与平方根冲击定律（Square-Root Law），大额确定性买盘对股价的推升弹性与被动需求占该股日均成交量（Days of ADV）的平方根成正比。
- **[跨期套利生命周期的四幕剧]**：从‘指数规则推算名单（提前抢跑）’到‘官方名单发布（散户抬轿）’，再到‘生效日尾盘收盘价集合竞价倒手（MOC 平仓）’，最后是‘次日买盘真空均值反转’，各阶段资金博弈具有明确的马尔可夫转移路径。
- **[拥挤度反噬与利好出尽陷阱]**：当抢跑资金过度拥挤时，预期在官方公告日前已被过度透支，往往在公布日当天出现‘利好兑现成利空’的踩踏反转。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了指数成分股调整套利的完整四阶段生命周期与资金对手盘演化。

```mermaid
flowchart LR
    S1["阶段 1: 规则预测 (T-60d)<br/>量化追踪市值成交排名 ➔ 悄悄抢跑建仓"] --> S2["阶段 2: 官方公告 (T-14d)<br/>名单官宣 / 散户游资跟风抬轿"]
    S2 --> S3["阶段 3: 生效日交割 (T_eff)<br/>ETF 尾盘集合竞价不计成本无脑买齐 ➔ 套利者精准高位倒手"]
    S3 --> S4["阶段 4: 均值反转 (T+1d)<br/>人工流动性买盘消失 / 股价超额回落"]
```

- **[要点 1：规则透明带来的可预测性]**：宽基指数编制规则（流通市值占比、流动性分位数、扣除非经常损益）完全公开，量化模型可提前 1~2 个月推算出 90% 以上准确度的候选名单。
- **[要点 2：生效日尾盘流动性盛宴]**：被动资金在生效日 14:57~15:00 集中释放巨额买单，套利资金利用这一确定性买盘流动性实现全身而退。
- **[要点 3：均值反转的负向 Alpha]**：生效日次日人工流动性买盘瞬间归零，调入股通常在随后数周内跑输大盘，形成经典的‘买入抢跑、卖给指数、反手做空’策略。

锚点指引：下图展示了平方根市场冲击定律与被动资金日均成交吸收天数（Days of ADV）的非线性映射。

```mermaid
flowchart TD
    Flow["被动资金净流入 V_buy = AUM_passive × Weight"] --> ADV["计算吸收天数: Days of ADV = V_buy / ADV_dollar"]
    ADV --> Impact["平方根冲击定律: Impact(%) = η · σ · √(Days of ADV)"]
    Impact --> Class{"流动性弹性分层"}
    Class -->|Days of ADV >= 3.0 天| High["高弹性套利核心池 (预期冲击 > 5%)"]
    Class -->|Days of ADV < 1.0 天| Low["低弹性噪音池 (大盘蓝筹容量充裕 / 冲击微弱)"]
```

- **[要点 1：日均成交吸收天数的衡量标准]**：若某股票所需被动买入金额超过其 3 天的全部市场成交量（Days of ADV ≥ 3.0），盘口供需极度失衡，价格上扬弹性最高。
- **[要点 2：大市值蓝筹的冲击钝化]**：超大市值调入股虽然权重高，但自身日均流动性充沛（Days of ADV < 0.5），价格冲击往往不足以覆盖交易佣金与借券成本。
- **[要点 3：市场弹性系数 $\eta$ 的状态依赖]**：在牛市流动性过剩期，冲击系数相对平缓；在熊市流动性真空期，微小的被动扫盘即可引发股价涨停。

【数学与估值模型】
被动流动性冲击与平方根冲击定律方程：
$$
V_{\text{flow}, i} = \text{AUM}_{\text{passive}} \times w_i, \quad \text{Days of ADV}_i = \frac{V_{\text{flow}, i}}{\text{ADV}_i}
$$
$$
\text{Impact Pct}_i = \text{Sign}_i \times \eta \times \sqrt{\text{Days of ADV}_i}
$$
$$
P_{\text{target}, i} = P_{\text{current}, i} \times (1 + \text{Impact Pct}_i)
$$
变量定义域与参数约束：
- $\text{AUM}_{\text{passive}} > 0$：跟踪该指数的全市场被动公募基金与 ETF 资产管理总规模（USD 或 RMB）。
- $w_i \in (0, 1)$：标的股票在新指数中的理论权重。
- $\text{ADV}_i > 0$：过去 20~60 个交易日的日均成交金额（Dollar Volume）。
- $\text{Sign}_i \in \{+1, -1\}$：调入股（INCLUSION）为 $+1$，调出股（EXCLUSION）为 $-1$。
- $\eta \in [0.015, 0.05]$：市场流动性微观冲击弹性参数，A 股经验均值常取 $0.03$。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **多头抢跑过度拥挤踩踏**：若市场上多家头部量化均运行同源预测模型，调入股在官宣前夕已累积过大涨幅，官宣日极易诱发‘踩踏式提前获利砸盘’。
2. **调出股跌停无法出逃风险**：对于被剔除的垃圾调出股，若其在生效日前夕连续一字跌停或停牌，套利做空单或底仓可能面临无法平仓的巨大流动性违约。
3. **跨市场汇率与节假日错配**：MSCI 或富时指数调整涉及离岸北向资金跨境结售汇，若逢陆股通休市或汇率极端波动，生效日尾盘可能发生脉冲异常漂移。
:::

【思考题】
Q1: 为什么随着量化对冲基金普遍建立“指数调整预测模型”，提前数周甚至数月抢跑（Front-running），导致指数调整官方公布日反而经常出现“利好兑现成利空（Sell the News）”的诡异暴跌？
Q2: 在生效日（Implementation Date）收盘集合竞价（MOC - Market-on-Close）阶段，为什么被动 ETF 基金经理即便明知股价被严重拉高，也必须不计成本挂涨停价甚至市价扫盘买齐？
Q3: 比较中国 A 股（如沪深 300 / 中证 500）与全球跨市场指数（如 MSCI 新兴市场指数）在成分股调整执行机制与流动性冲击上的本质区别。

【Q1 深度参考答案】
- **[编制规则公开度促成预期超级透支]**：主流宽基指数的选股规则（日均成交金额前 50% 排他性筛选、总市值加权、剔除 ST 股票与扣非连续亏损企业）完全公式化透明。量化投研团队在考察截止日前 60 天即可推算出确定性名单，低位建立潜伏多头底仓。
- **[抢跑资本在时间序列上的逐级接力]**：随着官宣日临近，次级机构与散户陆续跟风，将调入股估值推升 15%~30%，使得预期利好在官宣前夕已被完全价格化。
- **[官宣日流动性对手盘逆转]**：官方名单发布当天，大众媒体铺天盖地报道，散户资金最亢奋地涌入买入。然而前期潜伏的庞大套利基金将其视为绝佳的高位出货对手盘，集体集中平仓了结，巨额卖单瞬间砸穿买盘挂单，形成“官宣日反向暴跌”的利好出尽形态。

【Q2 深度参考答案】
- **[跟踪偏离度（Tracking Error）的刚性契约一票否决]**：被动指数 ETF 的唯一受托人考核指标是跟踪偏离度极小化（通常契约规定日均跟踪误差不得超过 0.1%）。指数公司官方在计算指数基准收盘点位时，一律以生效日当天的“收盘价（Closing Price）”作为新成分股计入基准。
- **[时间错配导致的永久性超额亏损不可逆]**：若 ETF 基金经理主观认为股价过高而延迟到次日开盘买入或日内分批建仓，一旦股价在盘中剧烈跳升，ETF 实际建仓成本将大幅脱离官方收盘基准，产生永久性且不可弥补的跟踪偏离，面临监管通报与资金赎回挤兑。
- **[制度性无弹性买盘为套利者兜底]**：因此，ETF 必须且只能在生效日 14:57~15:00 集合竞价将所有再平衡买单以 MOC 形式无脑提交，哪怕被套利资金高位截胡也在所不惜。

【Q3 深度参考答案】
- **[资金体量与跨境资本管制约束]**：沪深 300 调整影响的是境内人民币公募 ETF 与量化对冲融券池，资金交收在 T+1 闭环内完成，无外汇管制阻碍；而 MSCI 新兴市场指数调整调动的是数万亿美元全球主权财富基金与离岸养老金，必须通过陆股通（北向通道）实时跨境兑换离岸人民币（CNH），受到每日配额限制与跨境结算时差约束。
- **[尾盘脉冲幅度与反转弹性差异]**：境内 ETF 调仓日内平滑度相对较好；而 MSCI 生效日的最后 3 分钟，北向资金往往在收盘前瞬间脉冲净流入数百亿元人民币（形成著名的“北向黄金三分钟”）。
- **[次日均值反转的统计套利机会]**：MSCI 调入股在 14:59 经常被机械性爆买拉升 3%~5%，但由于这一买盘完全是制度性产物而非企业基本面驱动，次日开盘后人工买盘瞬间退潮，股价往往在开盘后 30 分钟内发生 2%~4% 的急速均值回归，为日内高频统计套利提供了极高胜率的反转收割窗口。
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
        """
        results = []
        for stock in stock_records:
            symbol = stock["symbol"]
            name = stock["name"]
            action = stock["action"].upper()
            weight = stock["index_weight"]
            adv = stock["adv_dollar"]
            curr_p = stock["current_price"]

            passive_flow = self.passive_aum * weight
            days_of_adv = passive_flow / adv if adv > 0 else 0.0

            base_impact = self.impact_coefficient * math.sqrt(days_of_adv)
            sign = 1.0 if action == "INCLUSION" else -1.0
            expected_impact_pct = sign * base_impact

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
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] IndexRebalanceArbitrageEngine Liquidity Impact Calculation...")
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

    impact_res = engine.estimate_liquidity_impact(test_stocks)

    # 验证 A公司: passive_flow = 1.5 亿, days_of_adv = 5.0
    # expected_impact = 0.03 * sqrt(5.0) ≈ 0.03 * 2.236068 ≈ 0.0671 (6.71%)
    # target_price = 20.0 * 1.067082 ≈ 21.34
    stock_a = impact_res[0]
    assert stock_a["passive_flow"] == 150000000.0
    assert stock_a["days_of_adv"] == 5.0
    assert stock_a["expected_impact_pct"] == 6.71
    assert stock_a["expected_target_price"] == 21.34

    # 验证 B公司: days_of_adv = 1.0, impact = 0.03 * 1.0 = 3.0% -> target = 15.0 * 1.03 = 15.45
    stock_b = impact_res[1]
    assert stock_b["days_of_adv"] == 1.0
    assert stock_b["expected_impact_pct"] == 3.00
    assert stock_b["expected_target_price"] == 15.45

    # 验证 C公司 (调出): days_of_adv = 4.0, impact = -0.03 * 2.0 = -6.0% -> target = 10.0 * 0.94 = 9.40
    stock_c = impact_res[2]
    assert stock_c["days_of_adv"] == 4.0
    assert stock_c["expected_impact_pct"] == -6.00
    assert stock_c["expected_target_price"] == 9.40

    print("[Testing] High Impact Targets Screening...")
    high_impact = engine.screen_high_impact_arbitrage_targets(test_stocks, min_days_of_adv=3.0)
    # 应筛选出 A公司 (5.0 天) 与 C公司 (4.0 天)，降序排列
    assert len(high_impact) == 2
    assert high_impact[0]["symbol"] == "600100"
    assert high_impact[1]["symbol"] == "600300"

    print("All assertions passed! Module 09 Lesson 03 verification successful.")
