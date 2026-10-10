r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 3 课：经典多腿期权组合策略与 Payoff 收益矩阵

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握四大经典期权组合策略（Covered Call、Protective Put、Long Straddle、Iron Condor）的结构构造与适用场景；
2. 深刻理解多腿期权头寸到期损益（Payoff Diagram）的几何分段线性叠加原理；
3. 掌握希腊字母在多腿组合中的空间对冲效果（如铁秃鹰的 Delta 中性、正 Theta 与负 Vega）；
4. 编写通用多腿期权收益矩阵引擎，自动求解任意组合的到期损益曲线、盈亏平衡点（Breakeven Points）与最大风险收益比。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，阐述财报前后波动率崩塌（IV Crush）对多腿头寸的损益冲击。

---
## 核心心智模型与策略拓扑

### 1. 四大经典策略构造解析

```
 1. 备兑看涨 (Covered Call)           2. 保护性看跌 (Protective Put)
        收益 Payoff                           收益 Payoff
             |        ------- (封顶)               |          / (无限上涨)
             |       /                             |        /
             |      /                              |       /
   ----------+-----+--------- S_T        ----------+------+---------- S_T
            /|                                     |保底---|
           / |                                     |
 
 3. 买入跨式 (Long Straddle)           4. 铁秃鹰 (Iron Condor)
        收益 Payoff                           收益 Payoff
          \  |  / (做多波动率)                      |  +Credit  (收敛赚权利金)
           \ | /                                   |   ------
   ---------+-V-+------------ S_T        ----+-----+--+------+---+--- S_T
              | -Premium                           | /        \  |
              |                                 ---|            |--- (双边锁损)
```

- **备兑看涨（Covered Call）**：持有标的股票现货 + 卖出虚值 Call。
  - 核心目的：在温和上涨或震荡行情中，通过出让上方超额暴利空间，换取确定性的权利金增厚（Yield Enhancement）。
- **保护性看跌（Protective Put）**：持有标的股票现货 + 买入虚值/平值 Put。
  - 核心目的：相当于为股票资产购买下行财产保险，锁定最大回撤，保留上方无限收益潜力。
- **买入跨式（Long Straddle）**：同时买入相同到期日、相同行权价的平值 Call 和 Put。
  - 核心目的：纯粹做多波动率（Long Vega / Long Gamma），预期发生重大单边突破（无论暴涨或暴跌），只要价格跳出两侧盈亏平衡点即可获利。
- **铁秃鹰（Iron Condor）**：由四腿虚值期权构成的卖方组合：
  - 牛市看跌差价（Bull Put Spread）：买入深度虚值 Put ($K_1$) + 卖出虚值 Put ($K_2$)
  - 熊市看涨差价（Bear Call Spread）：卖出虚值 Call ($K_3$) + 买入深度虚值 Call ($K_4$)
  - 核心目的：在标的资产窄幅横盘时，两端收取净权利金（Net Credit），同时两端买入外挂保护，将极端暴涨暴跌的最大亏损严格锁定。
"""

from typing import List, Dict, Any, Tuple


class MultiLegOptionEngine:
    """
    通用多腿期权与现货组合收益分析引擎。
    """

    @staticmethod
    def calculate_single_leg_payoff(leg: Dict[str, Any], spot_price: float) -> float:
        """
        计算单腿头寸在到期时点 spot_price 下的净收益 (PnL)。
        
        合法 leg 类型：
        - STOCK: {"type": "STOCK", "side": "BUY"|"SELL", "quantity": 1, "price": 100.0}
        - CALL:  {"type": "CALL", "side": "BUY"|"SELL", "quantity": 1, "strike": 105.0, "premium": 3.0}
        - PUT:   {"type": "PUT", "side": "BUY"|"SELL", "quantity": 1, "strike": 95.0, "premium": 2.0}
        """
        leg_type = leg["type"].upper()
        side_mult = 1.0 if leg["side"].upper() == "BUY" else -1.0
        qty = leg.get("quantity", 1.0)

        if leg_type == "STOCK":
            entry_price = leg["price"]
            return side_mult * qty * (spot_price - entry_price)

        elif leg_type == "CALL":
            strike = leg["strike"]
            premium = leg["premium"]
            intrinsic = max(0.0, spot_price - strike)
            return side_mult * qty * (intrinsic - premium)

        elif leg_type == "PUT":
            strike = leg["strike"]
            premium = leg["premium"]
            intrinsic = max(0.0, strike - spot_price)
            return side_mult * qty * (intrinsic - premium)

        return 0.0

    @classmethod
    def calculate_portfolio_payoff(cls, legs: List[Dict[str, Any]], spot_price: float) -> float:
        """计算整个多腿组合在到期价格 spot_price 下的总净收益。"""
        total_pnl = sum(cls.calculate_single_leg_payoff(leg, spot_price) for leg in legs)
        return round(total_pnl, 4)

    @classmethod
    def analyze_payoff_profile(
        cls,
        legs: List[Dict[str, Any]],
        spot_grid: List[float]
    ) -> Dict[str, Any]:
        """
        在给定的标的价格网格 spot_grid 上分析组合收益轮廓：
        - 最大收益 (max_profit)
        - 最大亏损 (max_loss, 负数或绝对亏损)
        - 盈亏平衡点列表 (breakeven_points)
        - 网格各点收益字典 (payoffs)
        """
        payoffs = [cls.calculate_portfolio_payoff(legs, s) for s in spot_grid]

        max_profit = max(payoffs)
        max_loss = min(payoffs)

        # 线性插值寻找零点 (盈亏平衡点)
        breakevens = []
        for i in range(len(spot_grid) - 1):
            s1, s2 = spot_grid[i], spot_grid[i + 1]
            p1, p2 = payoffs[i], payoffs[i + 1]

            if abs(p1) < 1e-4:
                breakevens.append(round(s1, 2))
            elif p1 * p2 < 0:
                # 符号相异，线性插值寻找根
                # p(s) = p1 + (s - s1) / (s2 - s1) * (p2 - p1) = 0
                root_s = s1 - p1 * (s2 - s1) / (p2 - p1)
                breakevens.append(round(root_s, 2))

        # 去重并排序
        unique_bes = sorted(list(set(breakevens)))

        return {
            "max_profit": round(max_profit, 4),
            "max_loss": round(max_loss, 4),
            "breakeven_points": unique_bes,
            "min_spot": spot_grid[0],
            "max_spot": spot_grid[-1]
        }


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么在长周期回测中，长期机械性执行备兑看涨（Covered Call）策略在牛市主升浪中会严重跑输单纯持有股票指数（Buy-and-Hold）？

参考答案：
1. 收益分布的严重截断与非对称性（Asymmetric Upside Truncation）：
   - Covered Call 的收益结构本质上是：全盘承担标的股票的下行风险（仅有极薄的权利金安全垫缓冲），同时将上行暴利彻底截断封顶在行权价 $K$。
   - 在股票市场的长期复合收益中，极大部分指数涨幅由极少数几天或几周的极端单边暴涨贡献（肥尾正收益）。
   - 机械执行 Covered Call 的基金在暴涨行情中被动以行权价交割抛出了筹码，错失了指数 30%、50% 的主升浪；
     而在随后的熊市崩盘中，由于权利金不足以抵御腰斩式下跌，净值依然承受沉重回撤。这种“截断利润、承受亏损”的非对称结构导致长周期复利跑输指数。

### Q2：铁秃鹰（Iron Condor）策略四腿组合在居中平值附近的希腊字母特征（Delta, Gamma, Vega, Theta）是什么？应在何种市场环境中部署？

参考答案：
1. 居中区域的希腊字母全景：
   - **Delta 接近 0（Delta-Neutral）**：组合兼具 Bull Put 与 Bear Call，在中间平台区域，做空 Put 产生的正 Delta 与做空 Call 产生的负 Delta 完美相消，对现货微小波动不敏感。
   - **Theta 显著为正（Positive Theta）**：四腿中期权空头处于内侧（更靠近平值，时间价值更厚），多头处于外侧深度虚值（时间价值极薄），因此组合整体净赚取丰厚的时间衰减收益（天天收租）。
   - **Gamma 显著为负（Negative Gamma）**与 **Vega 显著为负（Negative Vega）**：组合惧怕大幅单边暴走与隐含波动率骤升。
2. 最佳部署环境：
   - 市场处于高隐含波动率后的均值回归期（IV Percentile > 70%~80%），但宏观基本面预期进入箱体震荡、缺乏强单边催化剂的真空期。此时卖出膨胀的高估波动率，收割波动率溢价与时间价值。

### Q3：什么是“波动率崩塌（IV Crush）”？为什么很多散户在重大财报或大选公布前买入跨式（Long Straddle），即便标的股票剧烈波动依然遭遇严重亏损？

参考答案：
1. 隐含波动率的事件驱动定价结构：
   在重大不确定性事件（如英伟达财报发布、FDA 新药审批、总统大选）前夕，市场避险与对冲情绪极度高涨，双向买入期权推升隐含波动率到极端高位（如 IV 从平时 30% 暴拉至 120%）。
   期权权利金中包含了极其昂贵的波动率风险溢价（VRP）。
2. 事件落地的方差不确定性消除（Variance Realization）：
   一旦财报公布，无论业绩超预期还是不及预期，“靴子落地”，未来的不确定性瞬间归零。
   做市商立刻调低报价，IV 发生垂直断崖式暴跌（例如从 120% 瞬间腰斩回 40%）。
3. Vega 暴跌掩盖了 Delta 盈利：
   Long Straddle 持有巨大的正 Vega（$\nu > 0$）。虽然股票跳空产生了一定程度的 Delta 收益，
   但由于 IV 断崖式暴跌引发的 Vega 账面亏损（$-\nu \times \Delta \sigma$）以及跨式期权原本支付的极高时间价值损耗，
   往往远大于现货跳空产生的内在价值收益，导致多头两头挨打，整体头寸严重亏损。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    engine = MultiLegOptionEngine()

    print("[Testing] Covered Call Payoff Profile...")
    # 买入现货成本 100, 卖出 105 Call 收取权利金 3.0
    covered_call_legs = [
        {"type": "STOCK", "side": "BUY", "quantity": 1, "price": 100.0},
        {"type": "CALL", "side": "SELL", "quantity": 1, "strike": 105.0, "premium": 3.0}
    ]
    # S_T = 110 -> 现货盈利 10 + 权利金 3 - 赔付 5 = 8.0 (封顶盈利)
    pnl_110 = engine.calculate_portfolio_payoff(covered_call_legs, 110.0)
    assert pnl_110 == 8.0, f"Expected 8.0, got {pnl_110}"

    # S_T = 90 -> 现货亏损 -10 + 权利金 3 = -7.0
    pnl_90 = engine.calculate_portfolio_payoff(covered_call_legs, 90.0)
    assert pnl_90 == -7.0, f"Expected -7.0, got {pnl_90}"

    # 盈亏平衡点: 100 - 3 = 97.0
    spot_range_cc = [float(x) for x in range(80, 130)]
    cc_profile = engine.analyze_payoff_profile(covered_call_legs, spot_range_cc)
    assert cc_profile["max_profit"] == 8.0
    assert 97.0 in cc_profile["breakeven_points"]

    print("[Testing] Protective Put Payoff Profile...")
    # 买入现货 100, 买入 95 Put 支付权利金 2.0
    protective_put_legs = [
        {"type": "STOCK", "side": "BUY", "quantity": 1, "price": 100.0},
        {"type": "PUT", "side": "BUY", "quantity": 1, "strike": 95.0, "premium": 2.0}
    ]
    # S_T = 80 -> 现货亏损 -20 + 行权收益 (95-80 - 2) 13 = -7.0 (锁定最大亏损: 100-95 + 2 = 7)
    pnl_pp_80 = engine.calculate_portfolio_payoff(protective_put_legs, 80.0)
    assert pnl_pp_80 == -7.0

    # S_T = 120 -> 现货盈利 20 - 权利金 2 = 18.0 (上方无封顶)
    pnl_pp_120 = engine.calculate_portfolio_payoff(protective_put_legs, 120.0)
    assert pnl_pp_120 == 18.0

    # 盈亏平衡点: 100 + 2 = 102.0
    pp_profile = engine.analyze_payoff_profile(protective_put_legs, spot_range_cc)
    assert 102.0 in pp_profile["breakeven_points"]

    print("[Testing] Long Straddle Payoff Profile...")
    # 买入 100 Call (权利金 4.0) + 买入 100 Put (权利金 3.0), 总成本 7.0
    straddle_legs = [
        {"type": "CALL", "side": "BUY", "quantity": 1, "strike": 100.0, "premium": 4.0},
        {"type": "PUT", "side": "BUY", "quantity": 1, "strike": 100.0, "premium": 3.0}
    ]
    # S_T = 100 -> 最大亏损 -7.0
    pnl_straddle_100 = engine.calculate_portfolio_payoff(straddle_legs, 100.0)
    assert pnl_straddle_100 == -7.0

    # S_T = 115 -> Call 盈利 (15 - 4) 11 - Put 亏损 3 = 8.0
    pnl_straddle_115 = engine.calculate_portfolio_payoff(straddle_legs, 115.0)
    assert pnl_straddle_115 == 8.0

    # 盈亏平衡点: 100 - 7 = 93.0 和 100 + 7 = 107.0
    straddle_profile = engine.analyze_payoff_profile(straddle_legs, spot_range_cc)
    assert straddle_profile["max_loss"] == -7.0
    assert 93.0 in straddle_profile["breakeven_points"]
    assert 107.0 in straddle_profile["breakeven_points"]

    print("[Testing] Iron Condor Payoff Profile...")
    # 铁秃鹰: 买 85P (1.0), 卖 90P (2.5), 卖 110C (2.5), 买 115C (1.0)
    # 净收取权利金 = (2.5 - 1.0) + (2.5 - 1.0) = 3.0
    # 最大亏损 = 翼宽 5.0 - 3.0 = 2.0
    iron_condor_legs = [
        {"type": "PUT", "side": "BUY", "quantity": 1, "strike": 85.0, "premium": 1.0},
        {"type": "PUT", "side": "SELL", "quantity": 1, "strike": 90.0, "premium": 2.5},
        {"type": "CALL", "side": "SELL", "quantity": 1, "strike": 110.0, "premium": 2.5},
        {"type": "CALL", "side": "BUY", "quantity": 1, "strike": 115.0, "premium": 1.0}
    ]
    # 中间平原 S_T = 100 -> 最大收益 3.0
    assert engine.calculate_portfolio_payoff(iron_condor_legs, 100.0) == 3.0
    # 左侧极端暴跌 S_T = 75 -> 最大亏损 -2.0
    assert engine.calculate_portfolio_payoff(iron_condor_legs, 75.0) == -2.0
    # 右侧极端暴涨 S_T = 125 -> 最大亏损 -2.0
    assert engine.calculate_portfolio_payoff(iron_condor_legs, 125.0) == -2.0

    # 盈亏平衡点: 90 - 3 = 87.0 与 110 + 3 = 113.0
    spot_range_ic = [float(x) for x in range(70, 130)]
    ic_profile = engine.analyze_payoff_profile(iron_condor_legs, spot_range_ic)
    assert ic_profile["max_profit"] == 3.0
    assert ic_profile["max_loss"] == -2.0
    assert 87.0 in ic_profile["breakeven_points"]
    assert 113.0 in ic_profile["breakeven_points"]

    print("All assertions passed! Module 08 Lesson 03 verification successful.")
