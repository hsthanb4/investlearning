r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 2/5 课
第 2 课：交易制度差异、涨跌停流动性枯竭与隔夜风险对冲 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么 A 股的 T+1 交易制度设立初衷是为了抑制日内过度投机并“保护中小散户”，但在微观实战中，散户反而更容易在 T+1 制度下遭遇“追高日内被套、次日开盘遭遇核按钮跌停割肉”的单边杀伤？
- **[流动性退出期权剥夺与非对称博弈链]**：
  - **[1. 流动性期权的价值消亡]**：在金融衍生品理论中，“即时平仓止损权”是一张极具价值的美式实物看跌期权（American Put Option）。T+1 制度人为剥离了日内买入者的这一期权，使得买入者在成交的瞬间即丧失了防御能力，必须被动承受日内 4 小时与盘后 15 小时的全部未知市场波动。
  - **[2. 庄家与融券大户的非对称优势]**：资金实力雄厚的主力游资或底仓机构可通过持有多头底仓（或利用转融通借入券源），在日内先买后卖变相实现“变相 T+0”，从而在日内见顶时从容卖出底仓锁定利润；而中小散户只能眼睁睁看着浮盈变为深亏，无法执行任何止损操作。
  - **[3. 次日踩踏与核按钮陷阱]**：由于日内被套筹码全部积压至次日开盘，次日早间 09:15 集合竞价阶段，无数恐慌性止损盘竞相以跌停板价格挂单抢跑出逃（即“核按钮”），直接引发个股大幅低开甚至一字跌停，使散户遭受最大幅度的不可逆本金清算。

【Q2 投决会深度解析】
什么是暗池（Dark Pool）与内部化（Internalization）？大型量化做市商（如 Citadel Securities、Virtu）为何偏好在公开交易所（Lit Exchange）之外与散户订单进行撮合？这对公开市场的价格发现效率与点差（Spread）构成了怎样的外部性？
- **[订单流分流与逆向选择剥离机制]**：
  - **[1. 订单流性质的二元分化]**：做市商面对两种交易者：知情交易者（Informed Traders，如掌握基本面或高频动量的大型对冲基金，带来毒性订单流）与不知情交易者（Uninformed Traders，如普通零售散户，其订单属于非相关的随机噪音）。
  - **[2. 内部化吃下无害订单（Cream-skimming）]**：零售券商（如 Robinhood、Schwab）通过“订单流支付”（Payment for Order Flow, PFOF）将毫无毒性的散户订单直接导流给 Citadel 等批发做市商。做市商在暗池或内部化撮合中充当对手盘，几乎零风险地稳定赚取散户买卖的半价差（Spread），完全没有被大资金击穿盘口的逆向选择风险。
  - **[3. 公开交易所的负外部性]**：公开交易所（如纽交所、纳斯达克）被抽离了优质的散户流动性，留在公开盘口上的几乎全部是机构互砍的毒性知情大单。公开市场的做市商为了自保，被迫大幅放宽买卖报价点差（Spread），降低挂单深度，直接损害了全市场的价格发现效率。

【Q3 投决会深度解析】
为什么当一只重仓股陷入“一字跌停、封单比极高”时，使用股指期货（如中证1000 IM / 中证500 IC）进行交叉对冲会面临严重的“基差贴水走阔风险（Basis Bleed）”与“Alpha-Beta 解耦风险”？量化风控应如何设置对冲损耗上限？
- **[交叉对冲缺陷与基差摩擦控制]**：
  - **[1. 负基差贴水滚仓摩擦 (Basis Bleed)]**：由于 A 股市场存在大量的量化中性策略（股票多头 + 股指空头）对冲需求，导致中证500（IC）和中证1000（IM）期货合约长期处于深幅贴水（Discount）状态（年化负基差率常在 6%~15%）。空头头寸在合约到期换月时必须“低买高卖”平仓并移仓至远月，基差收敛带来的机械性损耗将持续蚕食投资组合净值。
  - **[2. Alpha-Beta 解耦与特质风险灾难]**：个股一字跌停往往由公司特质暴雷引发（如财务欺诈被立案调查、核心技术被制裁），属于个股特质非系统性风险（Idiosyncratic Risk）。若此时大盘宏观指数在稳增长利好下大幅上涨，股指期货空头端将产生剧烈亏损，而现货股票端却受困于一字跌停无法止损，导致对冲组合遭受“现货天天跌停 + 期货大幅空头逼仓”的双向爆仓惨剧。
  - **[3. 量化风控准则与损耗熔断]**：风控系统必须预先设定对冲存续时间上限（如最多对冲 3 个交易日）；若在对冲期内个股依然毫无开板迹象且基差快速走阔超 200 bps，系统必须强制按预设对冲敞口止损线（如组合净值损失达 3%）解除期货空头，不再做无效交叉对冲。
"""

from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd


def is_liquidity_locked(current_price: float, prev_close: float, limit_pct: float, bid_volume: int) -> bool:
    """
    判断个股是否处于跌停且流动性锁死状态:
        跌停价 = round(prev_close * (1.0 - limit_pct), 2)
        若 current_price <= 跌停价 且 bid_volume == 0，则为流动性锁死状态。
    """
    down_limit = round(prev_close * (1.0 - limit_pct), 2)
    return (current_price <= down_limit) and (bid_volume == 0)


def calculate_limit_prices(prev_close: float, limit_pct: float = 0.10) -> Tuple[float, float]:
    """
    计算 A 股合规的涨跌停板价格 (按分位 0.01 元四舍五入)
    """
    up_limit = round(prev_close * (1.0 + limit_pct), 2)
    down_limit = round(prev_close * (1.0 - limit_pct), 2)
    return float(up_limit), float(down_limit)


def calculate_overnight_hedge_ratio(
    locked_market_value: float,
    stock_beta: float,
    futures_price: float,
    contract_multiplier: float = 200.0,
) -> Dict[str, float]:
    """
    计算现货流动性锁死时的股指期货替代对冲策略
    """
    target_hedge_notional = locked_market_value * stock_beta
    contract_val = futures_price * contract_multiplier
    num_contracts = int(round(target_hedge_notional / contract_val))
    actual_hedge_notional = float(num_contracts * contract_val)

    # 剩余未完全对冲等效市值
    if stock_beta > 1e-6:
        net_unhedged_val = float(locked_market_value - (actual_hedge_notional / stock_beta))
    else:
        net_unhedged_val = float(locked_market_value)

    return {
        "num_contracts": int(num_contracts),
        "contract_value": float(contract_val),
        "actual_hedge_notional": float(actual_hedge_notional),
        "net_unhedged_value": float(net_unhedged_val),
    }


def simulate_lockup_hedge_payoff(
    locked_value: float,
    days_locked: int,
    daily_stock_loss_pct: float,
    hedge_notional: float,
    daily_futures_return: float,
) -> Dict[str, float]:
    """
    模拟连续跌停锁死期间，未对冲现货损失 vs 期货空头对冲组合收益
    """
    # 现货端复利亏损
    stock_mult = (1.0 - daily_stock_loss_pct) ** days_locked
    stock_pnl = float(locked_value * (stock_mult - 1.0))

    # 期货做空收益: 空头在指数下跌时获利
    # 期货指数累计收益率 = (1 + daily_futures_return)^days - 1
    # 做空 PnL = - hedge_notional * (期货指数累计收益率)
    futures_mult = (1.0 + daily_futures_return) ** days_locked
    futures_cum_ret = futures_mult - 1.0
    futures_pnl = float(-hedge_notional * futures_cum_ret)

    net_pnl = float(stock_pnl + futures_pnl)

    # 对冲效率: 1 - |净损益| / |现货单边亏损|
    if abs(stock_pnl) > 1e-6:
        hedge_eff = float(1.0 - abs(net_pnl) / abs(stock_pnl))
    else:
        hedge_eff = 0.0

    return {
        "stock_pnl": float(stock_pnl),
        "futures_pnl": float(futures_pnl),
        "net_pnl": float(net_pnl),
        "hedge_efficiency": float(hedge_eff),
    }


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
    sim = simulate_lockup_hedge_payoff(
        locked_value=10_000_000.0,
        days_locked=3,
        daily_stock_loss_pct=0.10,
        hedge_notional=12_000_000.0,
        daily_futures_return=-0.06,
    )
    assert abs(sim["stock_pnl"] - (-2_710_000.0)) < 1.0
    assert sim["futures_pnl"] > 0
    assert sim["hedge_efficiency"] > 0.65, f"对冲减亏效率应大于65%, 实际为: {sim['hedge_efficiency']}"

    print("Lesson 02 Answer Verified!")
