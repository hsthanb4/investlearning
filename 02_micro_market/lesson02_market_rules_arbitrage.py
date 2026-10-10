r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 2/5 课
第 2 课：交易制度差异、涨跌停流动性枯竭与隔夜风险对冲 (Market Rules & Liquidity Freeze)
================================================================================

【课程定位与第一性原理】
交易制度是二级市场微观博弈的底层“物理法则”。制度差异决定了流动性供给的边界以及极端风险发生时的逃生通道：

1. A 股市场三大核心制度约束：
   - T+1 交易制度：当日买入的股票在次日（T+1）开盘前无法卖出，剥夺了日内止损的“即时流动性选择权”；
   - 价格涨跌幅限制（Price Limit）：主板 ±10%（ST ±5%），创业板/科创板 ±20%，北交所 ±30%。
   - 融券做空约束：融券券源紧缺、转融通借贷成本高，无法实现无摩擦做空，价格发现容易单边化。
2. 港美股市场对比特征：
   - T+0 连续回转交易：日内可无限次平仓锁定风险；
   - 弹性价格熔断机制：美股无涨跌停板，采用大盘三级熔断（7%, 13%, 20%）与个股 LULD（Limit Up-Limit Down，5分钟暂停交易）；
   - 做市商与暗池（Dark Pools / Internalizers）：大量散户散单在场外被内部化撮合，主交易所（Lit Exchanges）承担大单博弈。
3. 涨跌停流动性枯竭（Liquidity Freeze & Black Hole）：
   当个股突发重大利空遭遇“一字跌停板”时：
   - 盘口买一挂单量为 0，卖一封单量动辄数十万手；
   - 真实市场公允估值（Fair Value）可能早已跌去 30%~50%，但在 ±10% 规则限制下，持仓者想以任何价格割肉都无法撮合成交；
   - 流动性完全降为零，形成“关门打狗”的流动性黑洞与隔夜连环跌停风险。

【微观锁死与跨市场衍生品对冲流】
```mermaid
flowchart TD
    BadNews["重大利空爆发 (如造假戴帽/地缘制裁)"] --> DownLimit["个股一字跌停 (价格 <= 跌停价 且 买一挂单量 = 0)"]
    DownLimit --> Freeze["现货卖出通路被物理封死 ➔ 流动性彻底枯竭 (Liquidity Locked)"]
    Freeze --> OvernightRisk["持仓者被迫承担隔夜连环跌停风险 (每日 -10% 复利缩水)"]
    OvernightRisk --> CrossHedge["量化对冲防线: 跨市场衍生品做空对冲 (股指期货 IC/IM / 期权 Put)"]
    CrossHedge --> DeltaNeutral["构建对冲头寸: 抵消现货跌停损失，锁定组合最大下行敞口"]
```

【思考题】
Q1: 为什么 A 股的 T+1 交易制度设立初衷是为了抑制日内过度投机并“保护中小散户”，但在微观实战中，
    散户反而更容易在 T+1 制度下遭遇“追高日内被套、次日开盘遭遇核按钮跌停割肉”的单边杀伤？
    请从流动性选择权（Liquidity Optionality）与日内风险敞口暴露的角度推导。
Q2: 什么是暗池（Dark Pool）与内部化（Internalization）？大型量化做市商（如 Citadel Securities、Virtu）
    为何偏好在公开交易所（Lit Exchange）之外与散户订单进行撮合？这对公开市场的价格发现效率与点差（Spread）构成了怎样的外部性？
Q3: 为什么当一只重仓股陷入“一字跌停、封单比极高”时，使用股指期货（如中证1000 IM / 中证500 IC）进行交叉对冲
    会面临严重的“基差贴水走阔风险（Basis Bleed）”与“Alpha-Beta 解耦风险”？量化风控应如何设置对冲损耗上限？

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
