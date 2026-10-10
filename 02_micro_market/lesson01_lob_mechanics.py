r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 1/5 课
第 1 课：限价订单簿撮合机制与盘口深度动力学 (Limit Order Book Mechanics)
================================================================================

::: {.callout-note}
### 投决会微观物理学公理：价格不是连续函数，而是离散挂单在交易所内存中的碰撞残差
- **[微观物理本质]**：二级市场的物理真实既非宏观经济公式的静态均衡解，亦非连续时间几何布朗运动。盘口价格是无数被动挂单（Passive Limit Orders）与激进吃单（Aggressive Market Orders）在交易所撮合主机内存中按纳秒时序推进的离散碰撞结果。
- **[买卖队列双向拓扑]**：买方队列（Bids）按价格由高到低降序排列，最优买入价为 Best Bid；卖方队列（Asks）按价格由低到高升序排列，最优卖出价为 Best Ask。
- **[无套利价差约束]**：在无交叉连续竞价阶段，严格满足 $P^{\text{ask}}_1 > P^{\text{bid}}_1$，买卖半价差即为做市商为全市场提供即时流动性所索取的风险溢价报酬。
:::

- **[盘口微观价格 (Micro-Price) 数学推导]**：
  - 传统中间价 $P^{\text{mid}} = (P^{\text{ask}}_1 + P^{\text{bid}}_1) / 2$ 忽略了买卖盘口委托量的不对称性。考虑一档深度的微观价格能够对下一跳价格变动方向提供无偏估计：

$$
P^{\text{micro}}_t = \frac{q^b_1 \cdot P^a_1 + q^a_1 \cdot P^b_1}{q^b_1 + q^a_1} = P^b_1 + \frac{q^b_1}{q^b_1 + q^a_1} (P^a_1 - P^b_1)
$$

- **[变量定义域与物理意义]**：
  - $P^a_1, P^b_1 \in \mathbb{R}^+$：最优卖一价与买一价，满足 $P^a_1 > P^b_1$。
  - $q^a_1, q^b_1 \in \mathbb{N}^+$：卖一档与买一档的挂单股数（或手数）。
  - 若 $q^b_1 \gg q^a_1$（买盘厚实而卖盘菲薄），微观价格无限逼近 $P^a_1$，表明卖一档极易被市价买单快速吃穿而引发向上跳跃。

- **[引导句锚点 1]**：如下架构拓扑所示，限价订单簿的双向挂单梯队与中间价分布构成了二级市场的底层微观骨架：

```mermaid
flowchart LR
    subgraph BidSide["买方挂单队列 (Bids 降序)"]
        B1["Bid 1: 最优买价 (最高) [+]"]
        B2["Bid 2: 次优买价"]
        B3["Bid 3: 深端挂单"]
    end
    subgraph SpreadGap["价差真空区 (Spread)"]
        MidPrice["公允中间价 (Mid Price)"]
    end
    subgraph AskSide["卖方挂单队列 (Asks 升序)"]
        A1["Ask 1: 最优卖价 (最低) [-]"]
        A2["Ask 2: 次优卖价"]
        A3["Ask 3: 深端挂单"]
    end
    B1 --> MidPrice
    MidPrice --> A1
```

- **[架构要点拆解 1]**：
  - **[1. 价格优先公理]**：出价更高的买单必定优先于出价更低的买单成交；出价更低的卖单必定优先于出价更高的卖单成交。
  - **[2. 时间优先公理 (FIFO)]**：在同一价位档位上，先到达交易所撮合服务器的订单严格排在队首，享受最优被动撮合权。
  - **[3. 价差动态弹性]**：在平静市况下做市商提供充沛挂单，Spread 维持极窄；一旦突发重大外生冲击，做市商本能撤单，Spread 瞬间被动放大数十倍。

- **[连续撮合引擎状态机与扫盘机制]**：
  - 市价单（Market Order）以对手盘可用流动性由优至劣连续扫盘（Sweep the book），其实际成交均价服从成交量加权：

$$
\text{VWAP}_{\text{Sweep}} = \frac{\sum_{i=1}^k P_i \cdot V_i}{\sum_{i=1}^k V_i}
$$

- **[引导句锚点 2]**：交易所撮合主机的价格-时间优先执行控制流如下拓扑所示：

```mermaid
flowchart TD
    InOrder["收到新委托订单 (Side, Type, Price, Volume)"] --> TypeCheck{"订单类型 Order Type ?"}
    TypeCheck -->|Market Order 市价单| SweepBook["沿对手盘由优至劣连续吃单扫盘 ➔ 扣减挂单量 ➔ 输出成交回报 Trade"]
    TypeCheck -->|Limit Order 限价单| CrossCheck{"是否与对手盘价格交叉 (Bid >= Ask / Ask <= Bid) ?"}
    CrossCheck -->|是 (可即时成交)| ExecCross["立即按对手盘最优价撮合成交"]
    ExecCross --> RemCheck{"委托单是否有未成交剩余份额 ?"}
    RemCheck -->|是| InsertQueue["剩余份额作为被动挂单插入本方队列队尾 (FIFO 时间优先)"]
    RemCheck -->|否| Done["撮合完毕"]
    CrossCheck -->|否 (普通被动挂单)| InsertQueue
```

- **[架构要点拆解 2]**：
  - **[1. 交叉即撮合]**：限价单买价若 $\ge$ 卖一价，立即按卖一价撮合成交（作为 Taker）；若未能完全吃完，剩余股数按原限价挂入买方队首（转为 Maker）。
  - **[2. 市价单穿仓风险]**：大单若以市价单形式打出，将瞬间吃干前三档深度，使自身在不利的高价位非线性成交。
  - **[3. 撤单流信息含量]**：高频取消订单（Cancel Order）占全市场委托的 80% 以上，撤单的微观空间分布反映了知情交易者的撤退意图。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[市价单穿仓陷阱]**：严禁在集合竞价尾盘、涨跌停开板或黑天鹅突发时使用市价单交易。做市商撤单导致的深度真空会引发 5%~10% 的即时非理性穿仓滑点。
- **[假大单诱骗陷阱 (Spoofing)]**：深度买二或买三挂出的数万手巨额买单往往是主力资金制造的支撑假象，一旦上方卖单成交完毕，该假单将在数毫秒内撤销。
:::

【思考题】
Q1: 为什么在流动性匮乏或突发重大外生冲击（如地缘黑天鹅）瞬间，买卖价差（Spread）会急剧放大数十倍甚至发生“盘口闪崩”（Flash Crash）？这对提交市价单（Market Order）的交易者会造成怎样的灾难性后果？
Q2: 什么是订单簿的“价格优先、时间优先（Price-Time Priority / FIFO）”原则？做市商与高频交易商（HFT）如何利用微波链路（Microwave）、FPGA 硬件网卡以及交易所机房托管（Co-location）抢占队首以规避逆向选择风险？
Q3: 什么是“虚假挂撤单”（Spoofing）与“分层诱骗”（Layering）？投机庄家如何在深度远端挂出巨额虚假买单/卖单欺骗散户与跟风算法，并在成交前一瞬间撤单？现代量化监管如何利用“撤单率与挂单存活时间分布”进行自动化稽查？

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
