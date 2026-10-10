r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 1/5 课
第 1 课：限价订单簿撮合机制与盘口深度动力学 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么在流动性匮乏或突发重大外生冲击（如地缘黑天鹅）瞬间，买卖价差（Spread）会急剧放大数十倍甚至发生“盘口闪崩”（Flash Crash）？这对提交市价单（Market Order）的交易者会造成怎样的灾难性后果？
- **[做市商库存规避与逆向选择模型推导]**：
  - **[1. 做市商被动单的期权属性]**：做市商挂在订单簿上的限价单本质上是向全市场免费派发的一张看跌/看涨期权。当外生重大利空爆发时，知情交易者（Informed Traders）会第一时间以极速吃掉做市商的买单挂单，做市商承担巨额逆向选择损失（Adverse Selection Loss）。
  - **[2. 极速撤单与流动性真空]**：为了规避毒性订单流（Toxic Order Flow）的无情收割，做市商算法会依据内生风控在纳秒级时间内撤销所有本方挂单。盘口原本充裕的挂单瞬间蒸发，买一价与卖一价之间的价差（Spread）被动拉大数十倍至数百倍。
  - **[3. 市价单的灾难性滑点]**：缺乏微观微结构风控保护的市价单（Market Order）在提交给交易所后，交易所主机强制执行“无条件扫盘（Sweep the Book）”。市价单将依次吃穿数档仅剩的零星散户挂单，直接以偏离公允价值 10%~30% 的极端价格完成撮合。在 2010 年美股闪崩事件中，大量优质蓝筹股的市价止损单直接以 1 美分成交，瞬间引发毁灭性穿仓。

【Q2 投决会深度解析】
什么是订单簿的“价格优先、时间优先（Price-Time Priority / FIFO）”原则？做市商与高频交易商（HFT）如何利用微波链路（Microwave）、FPGA 硬件网卡以及交易所机房托管（Co-location）抢占队首以规避逆向选择风险？
- **[物理纳秒竞赛与队列博弈机制]**：
  - **[1. 优先原则的物理排队本质]**：价格优先保证了最具竞争力的价格拥有绝对优先撮合权；而在同一价位档位上，严格依据物理数据包到达交易所撮合服务器网络端口的时间戳先后排队（First-In, First-Out）。
  - **[2. 队首做市商的无风险优势]**：在买一档排在队首（Queue Position 1）的挂单拥有最高概率以最优价格被市价单动量吃掉，从而赚取买卖半价差（Half-Spread）；而排在队尾的挂单往往只有在发生大额大单砸盘、价格即将向下破位时才会被成交，面临极高的套牢亏损概率。
  - **[3. 硬件与物理基础设施重构]**：为了争夺毫微秒级的队首排位并抢先撤单：
    - **机房托管（Co-location）**：将服务器机柜直接搬进交易所机房，利用等长光纤消除光速传播的时延差；
    - **FPGA 芯片直接解包**：跳过操作系统内核与 TCP/IP 协议栈，硬件直接解析交易所行情组播（Multicast）并瞬间触发委托；
    - **微波无线传输（Microwave）**：在芝加哥与纽约之间建立视距微波塔，利用空气中无线电波速度比光纤快约 30% 的物理特性，抢先对手盘几十微秒完成挂撤单。

【Q3 投决会深度解析】
什么是“虚假挂撤单”（Spoofing）与“分层诱骗”（Layering）？投机庄家如何在深度远端挂出巨额虚假买单/卖单欺骗散户与跟风算法，并在成交前一瞬间撤单？现代量化监管如何利用“撤单率与挂单存活时间分布”进行自动化稽查？
- **[市场操纵微观机理与量化稽查维度]**：
  - **[1. 虚假挂单的心理与算法操纵]**：庄家在买二、买三或更深的非即时成交档位挂出数万手的非真实意图大买单（制造买盘极其雄厚、即将暴涨的假象）。跟风的趋势跟踪算法与散户交易员被虚假深度欺骗，纷纷以市价单或最优买价抢筹。
  - **[2. 暗度陈仓与光速撤单]**：就在散户买单推升价格、庄家自身位于卖一档的真实小额出货单成交完毕的纳秒瞬间，庄家算法以极高频率向交易所发送撤单指令（Cancel Order），将原本挂在下方的巨额虚假买单全部撤销。
  - **[3. 监管量化指标穿透]**：现代交易所反操纵引擎（如中国证监会与美国 CFTC 系统）通过以下微观特征进行自动化特征识别：
    - **订单存活时间（Order Lifetime）**：虚假挂单的中位数存活时间通常低于数毫秒至数百毫秒，显著短于正常配置型委托；
    - **撤单率（Cancellation Ratio）**：操纵账户的挂撤比（Cancel-to-Fill Ratio）极度反常，往往超过 95%~99%；
    - **盘口对称性背离**：观察在特定价格档位撤单与对手盘成交在纳秒时间戳上的强因果协变特征，对恶意撤单实施精确法律穿透与自动化冻结。
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
