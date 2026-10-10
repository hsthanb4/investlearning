r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 1/5 课
第 1 课：限价订单簿撮合机制与盘口深度动力学 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么在流动性匮乏或突发重大外生冲击（如地缘黑天鹅）瞬间，买卖价差（Spread）会急剧放大数十倍
甚至发生“盘口闪崩”（Flash Crash）？这对提交市价单（Market Order）的交易者会造成怎样的灾难性后果？
- **做市商撤单与流动性真空传导**：
  1. **做市商库存风险与逆向选择模型（Glosten-Milgrom 效应）**：做市商盈利依托于撮合买卖双方赚取半价差（Half-Spread）。
     当突发重大利空时，所有新到达的激进卖单几乎 100% 属于“知情交易者”（Informed Traders）。
     做市商如果继续在买一口挂单垫单，其买单将被无情吃穿并被迫承受巨额现货存货跌价损失（Inventory Loss）。
  2. **自动化流动性撤回（Liquidity Withdrawal）**：主流做市商算法（如 Citadel, Virtu）均内置波动率硬阈值。
     一旦监测到毒性订单流（Toxic Order Flow）或外生突发事件，算法在几微秒内执行批量撤单（Cancel All Passive Bids），
     导致订单簿买方前十档挂单瞬间凭空蒸发，形成买方“流动性黑洞”。
  3. **市价单的灾难性穿仓穿透**：市价单本质上是“不计代价购买流动性”。当挂单深度归零、买卖价差从 0.01 美元
     拉大到 5.00 美元甚至更宽时，提交市价卖单的程序将沿着极端稀疏的买盘逐档向下穿透吃单，
     可能在平时 100 元的标的上以 10 元甚至 1 分钱撮生成交，瞬间引发不可逆的巨额真实亏损（穿仓穿盘）。

【Q2 深度参考答案】
什么是订单簿的“价格优先、时间优先（Price-Time Priority / FIFO）”原则？做市商与高频交易商（HFT）
如何利用微波链路（Microwave）、FPGA 硬件网卡以及交易所机房托管（Co-location）抢占队首以规避逆向选择风险？
- **纳秒级物理优势与队首期权价值**：
  1. **队首（Front of the Queue）的期权属性**：在相同价格档位上，排在队列第一位（Queue Position #1）的挂单
     拥有最高的成交概率；而排在队尾的挂单在被成交时，往往是因为有超大激进订单吃穿了整个档位，
     这意味着排在队尾成交意味着很大概率即将承受下一档位的逆向价格跳跃。
  2. **极速取消权（Fast Cancellation）**：排在队首的做市商若拥有超高速度，一旦通过芝加哥-纽约的微波通信网络
     （Microwave Link）比普通机构提前 3 微秒得知先导资产（如 S&P E-mini 期货）发生跳变，便可在现货市场
     知情市价单到达前的最后 500 纳秒将自己的挂单精准撤销（Cancel），实现“只在安全时被动赚利差，在危险时毫秒隐身”。
  3. **硬件级端到端优化**：高频做市商将撮合网络协议直接烧录入 FPGA（现场可编程门阵列）硬件网卡，
     绕过操作系统内核（Kernel-bypass），将交易延迟压制在 100 纳秒以内，从而筑起牢不可破的做市垄断护城河。

【Q3 深度参考答案】
什么是“虚假挂撤单”（Spoofing）与“分层诱骗”（Layering）？投机庄家如何在深度远端挂出巨额虚假买单/卖单
欺骗散户与跟风算法，并在成交前一瞬间撤单？现代量化监管如何利用“撤单率与挂单存活时间分布”进行自动化稽查？
- **微观欺诈机制与量化稽查特征工程**：
  1. **Spoofing / Layering 物理操作拆解**：
     - 诱导阶段：操纵者想在高位出货卖出 10 万股，他并不直接挂卖单，而是在买二、买三、买四连续分层挂出
       数百万股的虚假大额买单（Non-bona fide orders）；
     - 欺骗阶段：散户与被动跟随的趋势算法观测到订单簿买盘深度（Depth）暴增，误判有强力主力资金托底护盘，
       纷纷在买一价抢买挂单，推高微观价格；
     - 偷袭阶段：操纵者趁机在买一口通过小额限价单或市价单分批将真实的 10 万股卖出给跟风散户；
     - 撤单阶段：在真实卖单成交的瞬间，操纵者以毫秒级速度将买二至买四的虚假巨额买单全部撤销（Cancel），
       失去支撑的盘口瞬间坍塌。
  2. **量化稽查与特征工程检测**：
     - **挂单撤单比率（Order-to-Trade Ratio, OTR）**：正常交易者的 OTR 通常在 5:1 至 30:1，
       而 Spoofing 账户在操纵档位的 OTR 往往高达 500:1 以上；
     - **挂单存活寿命分布（Order Lifetime Distribution）**：分析订单的生存周期，Spoofing 挂单呈现
       极高的“近成交瞬间撤单（Cancellation right before execution）”峰值；
     - **非对称交互特征（Asymmetric Book Activity）**：同一账户在买方发生高频巨额挂撤单的同时，
       在卖方频繁发生单边真实成交，构成确凿的市场操纵量化证据链。
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class Trade:
    trade_id: int
    price: float
    volume: int
    maker_side: str  # 被吃单方: 'bid' or 'ask'


class SimpleLOB:
    """
    高仿真双向限价订单簿 (Limit Order Book) 连续撮合引擎
    """

    def __init__(self):
        self.bids: Dict[float, int] = {}
        self.asks: Dict[float, int] = {}
        self.trade_history: List[Trade] = []
        self._trade_counter = 0

    def get_best_bid_ask(self) -> Tuple[float, float]:
        """获取当前盘口最优买价 (Best Bid) 与最优卖价 (Best Ask)"""
        best_bid = max(self.bids.keys()) if self.bids else 0.0
        best_ask = min(self.asks.keys()) if self.asks else 0.0
        return float(best_bid), float(best_ask)

    def get_spread_and_mid(self) -> Tuple[float, float]:
        """计算 (Spread, Mid_Price)"""
        bb, ba = self.get_best_bid_ask()
        if bb <= 0.0 or ba <= 0.0:
            return 0.0, max(bb, ba)
        spread = ba - bb
        mid = (ba + bb) / 2.0
        return float(spread), float(mid)

    def get_micro_price(self) -> float:
        """
        计算考虑顶层深度的加权微观价格 (Micro-Price):
            Micro_Price = (Bid_Size * Best_Ask + Ask_Size * Best_Bid) / (Bid_Size + Ask_Size)
        """
        bb, ba = self.get_best_bid_ask()
        if bb <= 0.0 or ba <= 0.0:
            return float(max(bb, ba))
        b_size = self.bids.get(bb, 0)
        a_size = self.asks.get(ba, 0)
        if b_size + a_size == 0:
            return float((bb + ba) / 2.0)
        return float((b_size * ba + a_size * bb) / (b_size + a_size))

    def add_limit_order(self, side: str, price: float, volume: int) -> List[Trade]:
        """
        添加限价单并执行撮合
        """
        trades: List[Trade] = []
        rem_volume = volume

        if side == 'bid':
            # 买单撮合: 只要价格 >= 最低卖价，即刻撮合
            while rem_volume > 0 and self.asks:
                best_ask = min(self.asks.keys())
                if price >= best_ask:
                    avail = self.asks[best_ask]
                    match_vol = min(rem_volume, avail)
                    self._trade_counter += 1
                    t = Trade(self._trade_counter, best_ask, match_vol, 'ask')
                    trades.append(t)
                    self.trade_history.append(t)
                    rem_volume -= match_vol
                    if match_vol == avail:
                        del self.asks[best_ask]
                    else:
                        self.asks[best_ask] -= match_vol
                else:
                    break
            if rem_volume > 0:
                self.bids[price] = self.bids.get(price, 0) + rem_volume

        elif side == 'ask':
            # 卖单撮合: 只要价格 <= 最高买价，即刻撮合
            while rem_volume > 0 and self.bids:
                best_bid = max(self.bids.keys())
                if price <= best_bid:
                    avail = self.bids[best_bid]
                    match_vol = min(rem_volume, avail)
                    self._trade_counter += 1
                    t = Trade(self._trade_counter, best_bid, match_vol, 'bid')
                    trades.append(t)
                    self.trade_history.append(t)
                    rem_volume -= match_vol
                    if match_vol == avail:
                        del self.bids[best_bid]
                    else:
                        self.bids[best_bid] -= match_vol
                else:
                    break
            if rem_volume > 0:
                self.asks[price] = self.asks.get(price, 0) + rem_volume

        return trades

    def process_market_order(self, side: str, volume: int) -> Tuple[List[Trade], float, int]:
        """
        执行市价吃单扫盘
        """
        trades: List[Trade] = []
        rem_vol = volume
        total_cost = 0.0
        exec_vol = 0

        if side == 'bid':
            # 市价买入: 吃 asks 队列
            while rem_vol > 0 and self.asks:
                best_ask = min(self.asks.keys())
                avail = self.asks[best_ask]
                match_vol = min(rem_vol, avail)
                self._trade_counter += 1
                t = Trade(self._trade_counter, best_ask, match_vol, 'ask')
                trades.append(t)
                self.trade_history.append(t)
                total_cost += match_vol * best_ask
                exec_vol += match_vol
                rem_vol -= match_vol
                if match_vol == avail:
                    del self.asks[best_ask]
                else:
                    self.asks[best_ask] -= match_vol

        elif side == 'ask':
            # 市价卖出: 吃 bids 队列
            while rem_vol > 0 and self.bids:
                best_bid = max(self.bids.keys())
                avail = self.bids[best_bid]
                match_vol = min(rem_vol, avail)
                self._trade_counter += 1
                t = Trade(self._trade_counter, best_bid, match_vol, 'bid')
                trades.append(t)
                self.trade_history.append(t)
                total_cost += match_vol * best_bid
                exec_vol += match_vol
                rem_vol -= match_vol
                if match_vol == avail:
                    del self.bids[best_bid]
                else:
                    self.bids[best_bid] -= match_vol

        vwap = float(total_cost / exec_vol) if exec_vol > 0 else 0.0
        return trades, vwap, exec_vol

    def cancel_order(self, side: str, price: float, volume: int) -> int:
        """
        撤销挂单
        """
        target = self.bids if side == 'bid' else self.asks
        if price not in target:
            return 0
        current_vol = target[price]
        canceled = min(volume, current_vol)
        if canceled == current_vol:
            del target[price]
        else:
            target[price] -= canceled
        return canceled


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础挂单与盘口特征 ----------------
    lob = SimpleLOB()
    lob.add_limit_order('bid', 100.0, 500)
    lob.add_limit_order('bid', 100.5, 300)
    lob.add_limit_order('ask', 101.5, 200)
    lob.add_limit_order('ask', 102.0, 600)

    best_b, best_a = lob.get_best_bid_ask()
    assert best_b == 100.5, f"Expected best bid 100.5, got {best_b}"
    assert best_a == 101.5, f"Expected best ask 101.5, got {best_a}"

    spread, mid = lob.get_spread_and_mid()
    assert abs(spread - 1.0) < 1e-4, f"Spread 偏差: {spread}"
    assert abs(mid - 101.0) < 1e-4, f"Mid price 偏差: {mid}"

    micro_p = lob.get_micro_price()
    assert abs(micro_p - 101.1) < 1e-4, f"Micro price 期望 101.1, 实际 {micro_p}"

    # ---------------- 基础测试 2: 市价单吃单扫盘与 VWAP ----------------
    trades, vwap, exec_vol = lob.process_market_order('bid', 350)
    assert exec_vol == 350, f"应全部成交 350 股, 实际成交 {exec_vol}"
    assert len(trades) == 2, f"应跨两档成交 2 笔, 实际 {len(trades)}"
    assert abs(vwap - (35600.0 / 350.0)) < 1e-4, f"VWAP 均价偏差: {vwap}"

    best_b, best_a = lob.get_best_bid_ask()
    assert best_a == 102.0, f"新卖一价应为 102.0, 实际 {best_a}"
    assert lob.asks[102.0] == 450, f"102.0 档位剩余量应为 450, 实际 {lob.asks[102.0]}"

    # ---------------- 基础测试 3: 交叉限价单撮合与剩余排队 ----------------
    trades_l = lob.add_limit_order('bid', 102.5, 500)
    assert len(trades_l) == 1
    assert trades_l[0].price == 102.0 and trades_l[0].volume == 450
    assert 102.0 not in lob.asks, "102.0 卖盘应已完全清空"

    best_b, best_a = lob.get_best_bid_ask()
    assert best_b == 102.5, f"买一价应变为 102.5, 实际 {best_b}"
    assert lob.bids[102.5] == 50, f"买一 102.5 挂单量应为 50, 实际 {lob.bids[102.5]}"

    # ---------------- 基础测试 4: 撤单操作 ----------------
    canceled = lob.cancel_order('bid', 102.5, 30)
    assert canceled == 30
    assert lob.bids[102.5] == 20
    lob.cancel_order('bid', 102.5, 20)
    assert 102.5 not in lob.bids, "完全撤销后价位应被清理"

    print("Lesson 01 (LOB) Answer Verified!")
