r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 1/5 课
第 1 课：限价订单簿撮合机制与盘口深度动力学 (Limit Order Book Mechanics)
================================================================================

【课程定位与第一性原理】
连续竞价二级市场的物理核心是限价订单簿（Limit Order Book, LOB）。
股票的瞬时价格既非宏观经济公式的静态均衡解，亦非平滑的连续布朗运动，而是无数
被动挂单（Passive Limit Orders）与激进吃单（Aggressive Market Orders）在交易所
撮合主机内存中按纳秒时序推进的离散碰撞结果。

核心概念与物理结构：
1. 挂单簿队列双向结构：
   - 买方队列（Bids）：按价格由高到低降序排列，最高买入价为 Best Bid (买一价)；
   - 卖方队列（Asks）：按价格由低到高升序排列，最低卖出价为 Best Ask (卖一价)；
   - 买卖价差：Spread = Best_Ask - Best_Bid；中间价：Mid_Price = (Best_Ask + Best_Bid) / 2。
2. 撮合优先级公理（Price-Time Priority）：
   - 价格优先（Price Priority）：出价更高的买单优先于出价更低的买单；出价更低的卖单优先于出价更高的卖单；
   - 时间优先（Time Priority / FIFO）：在同等价格档位上，先到达交易所服务器的订单优先于后到达的订单排队成交。
3. 订单类型与撮合流：
   - 限价单（Limit Order）：指定最高买价或最低卖价。若与对手盘价格交叉（Crossed: Bid >= Best_Ask 或 Ask <= Best_Bid），
     则立即按对手盘最优价格撮合成交；未完全成交的剩余部分进入本方簿记挂单排队；
   - 市价单（Market Order）：无指定价格，直接以对手盘可用流动性由优至劣连续扫盘（Sweep the book），直至足额成交或流动性彻底枯竭；
   - 撤单（Cancel Order）：交易者在排队未成交前主动向交易所申请注销未撮合份额。
4. 微观价格（Micro-Price）：
   传统中间价未考虑盘口挂单量的不对称性。考虑挂单深度的微观价格能够提前反映下一跳跳跃方向：
       Micro_Price = (Bid_Size * Best_Ask + Ask_Size * Best_Bid) / (Bid_Size + Ask_Size)

【撮合引擎控制流图解】
```mermaid
flowchart TD
    InOrder["收到新委托订单 (Side, Type, Price, Volume)"] --> TypeCheck{"Order Type ?"}
    TypeCheck -->|Market Order| SweepBook["沿对手盘队列由优至劣顺序吃单撮合 ➔ 生成 Trade 记录 ➔ 扣减盘口深度"]
    TypeCheck -->|Limit Order| CrossCheck{"是否与对手盘价格交叉 ?"}
    CrossCheck -->|是 (Bid >= Ask / Ask <= Bid)| MatchCross["立即按对手盘最优价撮合成交"]
    MatchCross --> RemCheck{"委托单是否有剩余份额 ?"}
    RemCheck -->|是| AppendBook["剩余份额按价格插入本方挂单队列队尾 (时间优先)"]
    RemCheck -->|否| Done["撮合完成"]
    CrossCheck -->|否 (普通挂单)| AppendBook
```

【工业界实战场景与风控陷阱】
1. 闪崩（Flash Crash）与买卖价差失控：
   在做市商撤回流动性的极端时刻，盘口深度瞬间归零（如卖一价直接跳空暴涨 50%）。
   此时大额市价单会遭遇惨绝人寰的穿仓滑点（Slippage），瞬间吃穿数十档盘口，以极端不利价格成交。
2. 纳秒竞赛与队列插队（Queue Position）：
   高频交易（HFT）通过 FPGA 芯片硬件解析行情组播，在得知新单信息后以纳秒级速度抢先挂入最优买价队首，
   享受做市商买卖半价差，同时规避被大单砸盘的逆向选择风险（Adverse Selection）。
3. 虚假挂单撤单（Spoofing）的微观操纵：
   主力在买二/买三挂出数千万股假大单制造强支撑假象诱骗散户追高，在自己卖单一成交的瞬间秒速撤销买单。

【思考题】
Q1: 为什么在流动性匮乏或突发重大外生冲击（如地缘黑天鹅）瞬间，买卖价差（Spread）会急剧放大数十倍
    甚至发生“盘口闪崩”（Flash Crash）？这对提交市价单（Market Order）的交易者会造成怎样的灾难性后果？
Q2: 什么是订单簿的“价格优先、时间优先（Price-Time Priority / FIFO）”原则？做市商与高频交易商（HFT）
    如何利用微波链路（Microwave）、FPGA 硬件网卡以及交易所机房托管（Co-location）抢占队首以规避逆向选择风险？
Q3: 什么是“虚假挂撤单”（Spoofing）与“分层诱骗”（Layering）？投机庄家如何在深度远端挂出巨额虚假买单/卖单
    欺骗散户与跟风算法，并在成交前一瞬间撤单？现代量化监管如何利用“撤单率与挂单存活时间分布”进行自动化稽查？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现基础挂单管理与最优买卖价差计算 (1分)；
  2. 准确实现限价单交叉即时撮合与对手盘扣减 (1.5分)；
  3. 准确实现市价单连续扫盘吃单、VWAP均价计算与微观价格计算 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须阐释微观订单流物理撮合因果链，而非堆砌术语；
- 通过线：8/10 分。一票否决：撮合违背价格优先、市价单成交量漏算、删除断言。
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
        # 挂单结构: price -> total_volume
        # bids 降序排列，asks 升序排列
        self.bids: Dict[float, int] = {}
        self.asks: Dict[float, int] = {}
        self.trade_history: List[Trade] = []
        self._trade_counter = 0

    def get_best_bid_ask(self) -> Tuple[float, float]:
        """获取当前盘口最优买价 (Best Bid) 与最优卖价 (Best Ask)，若为空返回 0.0"""
        # TODO: 返回当前最优买价与卖价
        pass

    def get_spread_and_mid(self) -> Tuple[float, float]:
        """计算当前盘口的买卖价差 (Spread) 与算术中间价 (Mid Price)"""
        # TODO: 计算 (Spread, Mid_Price)
        pass

    def get_micro_price(self) -> float:
        """
        计算考虑顶层深度的加权微观价格 (Micro-Price):
            Micro_Price = (Bid_Size * Best_Ask + Ask_Size * Best_Bid) / (Bid_Size + Ask_Size)
        若盘口单边缺失，退化返回中间价或当前有效价格。
        """
        # TODO: 实现微观价格计算
        pass

    def add_limit_order(self, side: str, price: float, volume: int) -> List[Trade]:
        """
        添加限价单并执行撮合:
        1. 检查是否与对手盘交叉 (Crossed Order):
           - 若 side == 'bid' 且 price >= Best_Ask: 发生吃单撮合，按最低卖价升序逐步撮合
           - 若 side == 'ask' 且 price <= Best_Bid: 发生吃单撮合，按最高买价降序逐步撮合
        2. 撮合后若委托仍有未成交剩余 volume，则作为挂单存入己方队列排队。
        3. 返回本次撮合生成的成交记录列表。
        """
        # TODO: 实现交叉限价单撮合与剩余挂单排队逻辑
        pass

    def process_market_order(self, side: str, volume: int) -> Tuple[List[Trade], float, int]:
        """
        执行市价吃单 (Market Order Sweep):
        - side: 'bid' 表示市价买入 (吃掉 asks 队列), 'ask' 表示市价卖出 (吃掉 bids 队列)
        - volume: 请求买入/卖出股数

        返回:
            (trades, vwap_price, executed_volume):
            - trades: 成交列表
            - vwap_price: 成交均价 (成交总金额 / 成交总股数), 若未成交返回 0.0
            - executed_volume: 实际成交总股数
        """
        # TODO: 实现市价单连续吃单扫盘逻辑并计算成交均价
        pass

    def cancel_order(self, side: str, price: float, volume: int) -> int:
        """
        撤销指定价格档位的排队挂单:
        扣减该价格处的 volume，若扣减后挂单量 <= 0 则删除该价格档位。
        返回实际成功撤销的数量。
        """
        # TODO: 实现撤单逻辑
        pass


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

    # 微观价格校验:
    # Bid_Size = 300, Ask_Size = 200
    # Micro_Price = (300 * 101.5 + 200 * 100.5) / 500 = (30450 + 20100) / 500 = 101.1
    micro_p = lob.get_micro_price()
    assert abs(micro_p - 101.1) < 1e-4, f"Micro price 期望 101.1, 实际 {micro_p}"

    # ---------------- 基础测试 2: 市价单吃单扫盘与 VWAP ----------------
    # 此时卖方盘口: 101.5 挂 200 股; 102.0 挂 600 股
    # 提交市价买单 350 股: 将全部吃掉 101.5 的 200 股，并吃掉 102.0 的 150 股
    # 期望 VWAP = (200 * 101.5 + 150 * 102.0) / 350 = (20300 + 15300) / 350 = 35600 / 350 = 101.7142857...
    trades, vwap, exec_vol = lob.process_market_order('bid', 350)
    assert exec_vol == 350, f"应全部成交 350 股, 实际成交 {exec_vol}"
    assert len(trades) == 2, f"应跨两档成交 2 笔, 实际 {len(trades)}"
    assert abs(vwap - (35600.0 / 350.0)) < 1e-4, f"VWAP 均价偏差: {vwap}"

    # 验证扫盘后订单簿盘口状态:
    # 101.5 档位已被吃空，卖一价应变为 102.0，且剩余 600 - 150 = 450 股
    best_b, best_a = lob.get_best_bid_ask()
    assert best_a == 102.0, f"新卖一价应为 102.0, 实际 {best_a}"
    assert lob.asks[102.0] == 450, f"102.0 档位剩余量应为 450, 实际 {lob.asks[102.0]}"

    # ---------------- 基础测试 3: 交叉限价单撮合与剩余排队 ----------------
    # 此时卖方有 102.0 (450股)。提交买入限价单: 价格 102.5，数量 500 股 (具有价格侵略性)
    # 应以 102.0 成交 450 股，剩余 50 股挂在买一 102.5
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

    print("Lesson 01 (LOB) Exercise Passed!")
