r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 3 课：经典多腿期权组合策略与 Payoff 收益矩阵

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

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
        # TODO: 根据 leg 类型计算内在收益并扣除/增加权利金或现货成本，乘以 side 方向系数与头寸数量 quantity
        pass

    @classmethod
    def calculate_portfolio_payoff(cls, legs: List[Dict[str, Any]], spot_price: float) -> float:
        """计算整个多腿组合在到期价格 spot_price 下的总净收益。"""
        # TODO: 累加所有 leg 的到期收益并保留 4 位小数
        pass

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
        # TODO:
        # 1. 遍历 spot_grid，计算所有点的 payoff
        # 2. 统计 max_profit 与 max_loss
        # 3. 线性插值寻找穿零的盈亏平衡点 (breakeven_points)
        pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么在长周期回测中，长期机械性执行备兑看涨（Covered Call）策略在牛市主升浪中会严重跑输单纯持有股票指数（Buy-and-Hold）？

**你的答案：**
[在此处写下你的分析：需阐述极端肥尾暴涨收益被行权价封顶截断、下行熊市时仅有微薄权利金保护的非对称损益特征]


### Q2：铁秃鹰（Iron Condor）策略四腿组合在居中平值附近的希腊字母特征（Delta, Gamma, Vega, Theta）是什么？应在何种市场环境中部署？

**你的答案：**
[在此处写下你的分析：需推导居中平原区域的 Delta 中性、正 Theta 每日收租特征，以及负 Vega/负 Gamma 风险属性，并说明高 IV 震荡市的适用逻辑]


### Q3：什么是“波动率崩塌（IV Crush）”？为什么很多散户在重大财报或大选公布前买入跨式（Long Straddle），即便标的股票剧烈波动依然遭遇严重亏损？

**你的答案：**
[在此处写下你的分析：需从事件驱动不确定性消除导致 IV 断崖暴跌切入，对比 Vega 账面亏损与 Delta 收益的相对强弱]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
# ==============================================================================
if __name__ == "__main__":
    engine = MultiLegOptionEngine()

    print("[Testing] Covered Call Payoff Profile...")
    covered_call_legs = [
        {"type": "STOCK", "side": "BUY", "quantity": 1, "price": 100.0},
        {"type": "CALL", "side": "SELL", "quantity": 1, "strike": 105.0, "premium": 3.0}
    ]
    pnl_110 = engine.calculate_portfolio_payoff(covered_call_legs, 110.0)
    assert pnl_110 == 8.0, f"Expected 8.0, got {pnl_110}"

    pnl_90 = engine.calculate_portfolio_payoff(covered_call_legs, 90.0)
    assert pnl_90 == -7.0, f"Expected -7.0, got {pnl_90}"

    spot_range_cc = [float(x) for x in range(80, 130)]
    cc_profile = engine.analyze_payoff_profile(covered_call_legs, spot_range_cc)
    assert cc_profile["max_profit"] == 8.0
    assert 97.0 in cc_profile["breakeven_points"]

    print("[Testing] Protective Put Payoff Profile...")
    protective_put_legs = [
        {"type": "STOCK", "side": "BUY", "quantity": 1, "price": 100.0},
        {"type": "PUT", "side": "BUY", "quantity": 1, "strike": 95.0, "premium": 2.0}
    ]
    pnl_pp_80 = engine.calculate_portfolio_payoff(protective_put_legs, 80.0)
    assert pnl_pp_80 == -7.0

    pnl_pp_120 = engine.calculate_portfolio_payoff(protective_put_legs, 120.0)
    assert pnl_pp_120 == 18.0

    pp_profile = engine.analyze_payoff_profile(protective_put_legs, spot_range_cc)
    assert 102.0 in pp_profile["breakeven_points"]

    print("[Testing] Long Straddle Payoff Profile...")
    straddle_legs = [
        {"type": "CALL", "side": "BUY", "quantity": 1, "strike": 100.0, "premium": 4.0},
        {"type": "PUT", "side": "BUY", "quantity": 1, "strike": 100.0, "premium": 3.0}
    ]
    pnl_straddle_100 = engine.calculate_portfolio_payoff(straddle_legs, 100.0)
    assert pnl_straddle_100 == -7.0

    pnl_straddle_115 = engine.calculate_portfolio_payoff(straddle_legs, 115.0)
    assert pnl_straddle_115 == 8.0

    straddle_profile = engine.analyze_payoff_profile(straddle_legs, spot_range_cc)
    assert straddle_profile["max_loss"] == -7.0
    assert 93.0 in straddle_profile["breakeven_points"]
    assert 107.0 in straddle_profile["breakeven_points"]

    print("[Testing] Iron Condor Payoff Profile...")
    iron_condor_legs = [
        {"type": "PUT", "side": "BUY", "quantity": 1, "strike": 85.0, "premium": 1.0},
        {"type": "PUT", "side": "SELL", "quantity": 1, "strike": 90.0, "premium": 2.5},
        {"type": "CALL", "side": "SELL", "quantity": 1, "strike": 110.0, "premium": 2.5},
        {"type": "CALL", "side": "BUY", "quantity": 1, "strike": 115.0, "premium": 1.0}
    ]
    assert engine.calculate_portfolio_payoff(iron_condor_legs, 100.0) == 3.0
    assert engine.calculate_portfolio_payoff(iron_condor_legs, 75.0) == -2.0
    assert engine.calculate_portfolio_payoff(iron_condor_legs, 125.0) == -2.0

    spot_range_ic = [float(x) for x in range(70, 130)]
    ic_profile = engine.analyze_payoff_profile(iron_condor_legs, spot_range_ic)
    assert ic_profile["max_profit"] == 3.0
    assert ic_profile["max_loss"] == -2.0
    assert 87.0 in ic_profile["breakeven_points"]
    assert 113.0 in ic_profile["breakeven_points"]

    print("All assertions passed! Module 08 Lesson 03 verification successful.")
