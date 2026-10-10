r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 2/5 课
第 2 课：交易制度差异、涨跌停流动性枯竭与隔夜风险对冲 (Market Rules & Liquidity Freeze)
================================================================================

::: {.callout-note}
### 投决会交易制度公理：制度摩擦直接剥夺流动性退出期权，制造非对称尾部风险
- **[制度边界公理]**：交易制度是二级市场微观博弈的底层“物理法则”。制度差异决定了流动性供给的边界以及极端风险发生时的逃生通道。
- **[T+1 制度的单边风险暴露]**：A 股 T+1 制度剥夺了日内买入者的即时平仓选择权，投资者在买入后必须无条件承担长达 4 小时日内暴跌与 15 小时隔夜外生冲击的完全单边敞口。
- **[涨跌停物理锁死黑洞]**：当重大利空导致个股一字跌停（Limit Down）时，盘口买一挂单量为 0，卖一封单动辄数十万手。真实公允价值虽然已折价 30%，但制度限制使持仓者无法撮合成交，流动性降为绝对零度。
:::

- **[价格上下限四舍五入规则模型]**：
  - A 股以昨收盘价（Prev Close）为基准，最小价格变动单位严格限制在 0.01 元：

$$
P^{\text{Up}} = \text{round}(P_{\text{prev}} \times (1 + \rho), 2), \quad P^{\text{Down}} = \text{round}(P_{\text{prev}} \times (1 - \rho), 2)
$$

- **[变量定义域与参数]**：
  - $P_{\text{prev}} \in \mathbb{R}^+$：上一交易日官方除权除息收盘价。
  - $\rho \in \{0.10, 0.20, 0.30\}$：主板取 0.10（ST 取 0.05），创业板/科创板取 0.20，北交所取 0.30。
  - 流动性锁死判据：$P \le P^{\text{Down}} \land Q^{\text{Bid}}_1 = 0 \implies \text{Liquidity Locked (流动性归零)}$。

- **[跨市场衍生品做空对冲张数模型]**：
  - 当重仓个股陷入跌停锁死无法卖出时，必须在股指期货（如中证1000 IM、中证500 IC）建立空头头寸以中和系统性 Beta 敞口：

$$
N_{\text{Futures}} = \text{round}\left( \frac{\text{Equity Notional} \times \beta_{\text{Stock}}}{P_{\text{Futures}} \times \text{Multiplier}} \right)
$$

- **[变量定义域与物理意义]**：
  - $\text{Equity Notional}$：被困现货标的的市值规模。
  - $\beta_{\text{Stock}}$：该标的相对于对冲股指的回归敏感度。
  - $P_{\text{Futures}} \times \text{Multiplier}$：单张股指期货名义价值（IC/IM 每点乘数均为 200 元）。

- **[引导句锚点 1]**：如下架构拓扑所示，现货跌停被困与股指期货跨市场对冲构建了风险隔离防线：

```mermaid
flowchart TD
    BadNews["突发重大利空爆发 (戴帽/欺诈/地缘黑天鹅)"] --> LimitDown["个股一字跌停 (价格 <= 跌停价 且 买一挂单量 = 0)"]
    LimitDown --> Locked["现货卖出通路被物理封死 ➔ 流动性彻底归零 (Liquidity Freeze)"]
    Locked --> OvernightRisk["持仓者被迫承担隔夜连环跌停风险 (每日 -10% 复利缩水)"]
    OvernightRisk --> CrossHedge["启动量化跨市场对冲: 股指期货做空 (IM/IC) 或买入虚值认沽期权 (Put)"]
    CrossHedge --> BetaNeutral["构建 Beta 中性组合: 衍生品空头盈利完全抵消现货跌停损失"]
```

- **[架构要点拆解 1]**：
  - **[1. 现货通道封死]**：一字跌停时，任何以跌停价挂出的卖单因时间优先（FIFO）排在数十万手大机构队尾，成交概率几乎为零。
  - **[2. 衍生品流动性替换]**：股指期货市场具备连续 T+0 交易与双向多空机制，流动性充裕，可瞬间承接系统性对冲敞口。
  - **[3. 下行风险锁死]**：对冲组合在连环跌停期间，期货空头浮盈对冲现货资产缩水，使组合整体净值最大回撤收敛在可控区间。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[基差贴水走阔风险 (Basis Bleed)]**：股指期货通常存在显著的远月贴水（Discount），长期持有空头对冲头寸将承受年化 8%~15% 的负基差收敛摩擦成本。
- **[Alpha-Beta 解耦风险]**：若跌停个股属于个股特质爆雷（Idiosyncratic Risk），大盘指数未跌甚至上涨，期货做空端将出现亏损，引发“现货跌停割肉无门 + 期货做空倒贴”的双向灾难。
:::

【思考题】
Q1: 为什么 A 股的 T+1 交易制度设立初衷是为了抑制日内过度投机并“保护中小散户”，但在微观实战中，散户反而更容易在 T+1 制度下遭遇“追高日内被套、次日开盘遭遇核按钮跌停割肉”的单边杀伤？请从流动性选择权（Liquidity Optionality）与日内风险敞口暴露的角度推导。
Q2: 什么是暗池（Dark Pool）与内部化（Internalization）？大型量化做市商（如 Citadel Securities、Virtu）为何偏好在公开交易所（Lit Exchange）之外与散户订单进行撮合？这对公开市场的价格发现效率与点差（Spread）构成了怎样的外部性？
Q3: 为什么当一只重仓股陷入“一字跌停、封单比极高”时，使用股指期货（如中证1000 IM / 中证500 IC）进行交叉对冲会面临严重的“基差贴水走阔风险（Basis Bleed）”与“Alpha-Beta 解耦风险”？量化风控应如何设置对冲损耗上限？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现跌停锁死与涨跌停价精度计算 (1分)；
  2. 准确实现隔夜锁死风险的股指期货对冲张数与敞口计算 (1.5分)；
  3. 准确模拟连环跌停下对冲组合的净损益与风险平抑效率 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须深入剖析制度微观摩擦与对冲基差机制；
- 通过线：8/10 分。一票否决：跌停判定条件颠倒、对冲方向反向开多、删除断言。
"""

from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd


def is_liquidity_locked(current_price: float, prev_close: float, limit_pct: float, bid_volume: int) -> bool:
    """
    判断个股是否处于跌停且流动性锁死状态:
        跌停价 = round(prev_close * (1.0 - limit_pct), 2)
        若 current_price <= 跌停价 且 bid_volume == 0，则为流动性锁死状态。

    参数:
        current_price: 当前撮合/盘口价格 (元)
        prev_close: 昨收盘价 (元)
        limit_pct: 跌停幅度比例 (例如 0.10 代表 10%)
        bid_volume: 买一挂单量 (股)

    返回:
        bool: True 表示流动性已锁死
    """
    # TODO: 实现跌停锁死判断
    pass


def calculate_limit_prices(prev_close: float, limit_pct: float = 0.10) -> Tuple[float, float]:
    """
    计算 A 股合规的涨跌停板价格:
    根据交易所规则，股票价格最小变动单位为 0.01 元，采用四舍五入。
        up_limit = round(prev_close * (1.0 + limit_pct), 2)
        down_limit = round(prev_close * (1.0 - limit_pct), 2)

    返回:
        (up_limit, down_limit)
    """
    # TODO: 计算涨跌停价格
    pass


def calculate_overnight_hedge_ratio(
    locked_market_value: float,
    stock_beta: float,
    futures_price: float,
    contract_multiplier: float = 200.0,
) -> Dict[str, float]:
    """
    计算现货流动性锁死时的股指期货替代对冲策略:
    当底层股票锁死无法卖出时，通过做空中证500/1000等股指期货对冲系统性风险。
        目标对冲市值: Target_Hedge_Notional = locked_market_value * stock_beta
        单张期货合约价值: Contract_Value = futures_price * contract_multiplier
        所需空头合约张数: Num_Contracts = round(Target_Hedge_Notional / Contract_Value)
        实际对冲名义市值: Actual_Hedge_Notional = Num_Contracts * Contract_Value
        剩余净暴露市值: Net_Exposure = locked_market_value - (Actual_Hedge_Notional / stock_beta)

    返回字典:
        {
            "num_contracts": int 整数张数,
            "contract_value": float 单张合约面值,
            "actual_hedge_notional": float 实际对冲总面值,
            "net_unhedged_value": float 剩余未完全对冲现货市值
        }
    """
    # TODO: 计算期货对冲张数与剩余净敞口
    pass


def simulate_lockup_hedge_payoff(
    locked_value: float,
    days_locked: int,
    daily_stock_loss_pct: float,
    hedge_notional: float,
    daily_futures_return: float,
) -> Dict[str, float]:
    """
    模拟连续跌停锁死期间，未对冲现货损失 vs 期货空头对冲组合收益:
    现货损失: stock_pnl = locked_value * ((1.0 - daily_stock_loss_pct) ** days_locked - 1.0)
    空头期货收益: futures_pnl = -hedge_notional * ((1.0 + daily_futures_return) ** days_locked - 1.0)
    净损益: net_pnl = stock_pnl + futures_pnl
    对冲效率: hedge_efficiency = 1.0 - abs(net_pnl) / abs(stock_pnl)

    返回字典:
        {
            "stock_pnl": 股票端亏损金额 (负数),
            "futures_pnl": 期货空头端收益 (若期货跟随下跌则为正数),
            "net_pnl": 组合净损益,
            "hedge_efficiency": 对冲减亏效率 [0.0, 1.0]
        }
    """
    # TODO: 模拟复利跌幅与期货对冲收益并计算减亏效率
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 跌停锁死与涨跌停价 ----------------
    prev = 10.0
    limit = 0.10  # 10% 跌停
    assert is_liquidity_locked(9.0, prev, limit, 0) is True
    assert is_liquidity_locked(9.0, prev, limit, 500) is False
    assert is_liquidity_locked(9.5, prev, limit, 0) is False

    up_p, down_p = calculate_limit_prices(10.0, 0.10)
    assert up_p == 11.00 and down_p == 9.00
    up_20, down_20 = calculate_limit_prices(25.43, 0.20)
    assert up_20 == 30.52 and down_20 == 20.34

    # ---------------- 基础测试 2: 隔夜期货对冲合约数计算 ----------------
    # 假设跌停锁死个股现货市值 1000 万元，Beta = 1.2
    # 股指期货点位 6000 点，合约乘数 200 元/点 ➔ 单张面值 120 万元
    # 目标对冲市值 = 1000万 * 1.2 = 1200 万元
    # 期望张数 = round(1200万 / 120万) = 10 张
    res_hedge = calculate_overnight_hedge_ratio(
        locked_market_value=10_000_000.0,
        stock_beta=1.2,
        futures_price=6000.0,
        contract_multiplier=200.0,
    )
    assert res_hedge["num_contracts"] == 10
    assert abs(res_hedge["contract_value"] - 1_200_000.0) < 1e-4
    assert abs(res_hedge["actual_hedge_notional"] - 12_000_000.0) < 1e-4
    assert abs(res_hedge["net_unhedged_value"]) < 1e-4

    # ---------------- 基础测试 3: 连环跌停模拟与对冲效率 ----------------
    # 现货市值 1000 万元，遭遇连续 3 个跌停 (-10%/天)
    # 期货端空头持有 1200 万元，同期股指每日下跌 -6%
    sim = simulate_lockup_hedge_payoff(
        locked_value=10_000_000.0,
        days_locked=3,
        daily_stock_loss_pct=0.10,
        hedge_notional=12_000_000.0,
        daily_futures_return=-0.06,
    )
    # 3天跌停现货亏损: 1000万 * (0.9^3 - 1) = 1000万 * (0.729 - 1) = -271 万元
    assert abs(sim["stock_pnl"] - (-2_710_000.0)) < 1.0
    # 期货做空收益为正，成功对冲现货亏损
    assert sim["futures_pnl"] > 0
    assert sim["hedge_efficiency"] > 0.65, f"对冲减亏效率应大于65%, 实际为: {sim['hedge_efficiency']}"

    print("Lesson 02 Exercise Passed!")
