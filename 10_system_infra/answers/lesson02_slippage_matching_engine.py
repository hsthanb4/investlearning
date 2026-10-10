r"""
================================================================================
模块 10：量化回测避坑指南与实盘系统工程 · 第 2/4 课
第 2 课：真实微观撮合仿真：滑点、排队模型与交易摩擦成本 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：零滑点与无限流动性是回测中最隐蔽的自欺欺人
业余量化回测最致命的玩具级假设有二：“零滑点无限流动性”与“静态无门槛交易费”。现实中，任何策略指令送入交易所订单簿（LOB）都必须经历物理排队与对手盘消耗。大额订单不可避免地产生非线性市场冲击（Market Impact）；而中国 A 股特有的“券商佣金最低 5 元”、“双边十万分之一过户费”、“卖出单向千分之零点五印花税”以及涨跌停一字封板不可成交，共同构成了侵蚀高频高换手策略真实收益的摩擦黑洞。
:::

- **[平方根市场冲击定律（Square-Root Law）]**：根据 Almgren-Chriss 与微观结构理论，市场冲击成本与订单量占 Bar 成交量的平方根成正比。资金规模越大，单位滑点呈非线性加速恶化。
- **[订单排队与容量上限截断]**：在限价订单簿中，单 Bar 撮合量受制于参与率上限（通常 $\alpha = 10\% \sim 15\%$）。超过容量的订单必须部分成交（Partial Fill）并结转至下一 Bar，严禁瞬时全额无感吃单。
- **[极端行情物理封死判定]**：一字涨停板买单封死（成交为 0）、一字跌停板卖单封死（出逃为 0）、停牌拒绝撮合；任何假设在跌停板能够自由市价止损的回测均为造假。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了限价订单簿（LOB）微观排队机制与参与率上限截断流程。

```mermaid
flowchart TD
    Order["策略提交大额订单 (Order Volume)"] --> Check{"检查 Bar 状态与流动性"}
    Check -->|停牌 Volume=0 或 is_suspended| Reject["拒单: SUSPENSION (无法成交)"]
    Check -->|一字涨停且买入 / 一字跌停且卖出| LimitLock["拒单: LIMIT_LOCK (封板排队在队尾)"]
    Check -->|正常连续交易| Match["计算容量上限: Available = Bar_Volume × α (10%)"]
    Match --> Fill["本次成交 = min(剩余委托量, Available) ➔ 剩余结转下一期"]
```

- **[要点 1：价格优先与时间优先的残酷性]**：当策略大单到达盘口时，队列前排早已堆积了做市商与快速通道挂单，策略订单排在队尾无法瞬时消化。
- **[要点 2：参与率上限防范自成交易]**：若某股票 1 分钟仅成交 500 手，策略下单 2000 手若全部以当前价成交，本质是凭空虚构了 1500 手对手盘流动性。
- **[要点 3：部分成交状态流转]**：未成交部分保持 `PARTIALLY_FILLED` 状态，随时间序列推移继续等待后续 Bar 的流动性释放。

锚点指引：下图拆解了 A 股全套法定交易税费漏斗与非线性冲击滑点构成。

```mermaid
flowchart LR
    Trade["单笔成交金额 Amount = P_exec × Q_fill"] --> Fee1["券商佣金: max(5.0, Amount × 0.00025) [双边]"]
    Trade --> Fee2["过户费: Amount × 0.00001 [双边]"]
    Trade --> Fee3["印花税: Amount × 0.0005 [仅卖出]"]
    Trade --> Slip["冲击滑点: Amount × [Base_Slippage + η·√(Q_fill / Bar_Vol)]"]
    Fee1 & Fee2 & Fee3 & Slip --> Total["总摩擦损耗 Total Friction = 佣金 + 过户费 + 印花税 + 滑点"]
```

- **[要点 1：最低 5 元佣金的散户刺客]**：高频小单交易中，数千元成交额的实际佣金率可能高达千分之二（5元 / 2500元），远超名义万 2.5。
- **[要点 2：印花税的单边惩罚]**：卖出时万分之五的印花税属于不可避免的财政硬扣税，直接抬高了每一次换仓的获利门槛。
- **[要点 3：平方根滑点的资金容量天花板]**：随着策略资产规模膨胀，滑点开销呈超线性上升，导致策略出现著名的“规模是 Alpha 的敌人”容量衰竭。

【数学与估值模型】
真实 A 股微观撮合成交价与滑点公式（Almgren-Chriss）：
$$
\text{Slippage} = \text{Base\_Slippage} + \eta \cdot \sqrt{\frac{\text{Order\_Volume}}{\text{Bar\_Volume}}}
$$
$$
P_{\text{exec}} = \begin{cases}
P_{\text{bench}} \times (1 + \text{Slippage}), & \text{Direction} = \text{'BUY'} \\
P_{\text{bench}} \times (1 - \text{Slippage}), & \text{Direction} = \text{'SELL'}
\end{cases}
$$
变量定义域与参数约束：
- $\text{Base\_Slippage} \in [0.0001, 0.0005]$：通常设为 $0.0002$（2 bps，覆盖买卖最小跳价差）；
- $\eta \in [0.02, 0.15]$：市场冲击敏感系数，日频大盘取 $0.03$，分钟频小盘取 $0.08$；
- $\text{Fill\_Volume} \le \text{Bar\_Volume} \times \alpha$，$\alpha \in [0.05, 0.15]$。

A 股法定交易税费方程：
$$
\text{Commission} = \max(5.0, \; \text{Trade\_Amount} \times 0.00025)
$$
$$
\text{Transfer\_Fee} = \text{Trade\_Amount} \times 0.00001
$$
$$
\text{Stamp\_Duty} = \begin{cases}
\text{Trade\_Amount} \times 0.0005, & \text{Direction} = \text{'SELL'} \\
0.0, & \text{Direction} = \text{'BUY'}
\end{cases}
$$

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **高换手率的摩擦复利吞噬**：年化单边换手率 50 倍的策略，一年仅手续费与双边滑点即可吞噬 10%~15% 的总收益，回测中未加税费的高夏普属于虚无泡沫。
2. **限价单逆向选择（Adverse Selection）**：回测中挂单买入若轻易全额成交，实盘中通常意味着有剧烈的大卖单正在向下击穿盘口，成交后大概率立即面临浮亏。
3. **停牌与一字跌停不可撤销**：持有标的一旦暴雷停牌或一字跌停封死，实盘中卖单只能排在数亿封单队尾，回测中任何当日平仓成功的记录一律视为严重合规事故。
:::

【思考题】
Q1: 为什么小市值高换手策略（例如年化单边换手率 50~100 倍）在扣除万分之五滑点与真实交易成本后，纸面上 80% 的年化超额收益往往会断崖式暴跌至负收益？请从摩擦成本复利损耗的角度定量推导。
Q2: 在基于分钟 Bar 的事件驱动回测中，如果某个 Bar 内限价买单价格为 10.20 元，而该 Bar 的价格区间为 [Low=10.00, High=10.50]，真实市场成交量仅为 500 手（50,000 股），策略下单量为 2,000 手（200,000 股）。为什么绝不能允许这 2,000 手在当前 Bar 全部以 10.20 元成交？如何设计合理的局部成交与排队结转机制？
Q3: 什么是撮合中的“逆向选择（Adverse Selection）”？为什么在回测中限价单（Limit Order）成交往往意味着当前行情正朝着对该订单不利的方向剧烈运动？如何在仿真中刻画这一微观结构现象？

【Q1 深度参考答案】
- **[单笔全流程摩擦成本分解]**：一次完整的买入+卖出换仓，其不可规避的法定税费与微观滑点包含：双边券商佣金（$0.025\% \times 2 = 0.05\%$）、单向卖出印花税（$0.05\%$）、双边过户费（$0.001\% \times 2 = 0.002\%$）以及双边冲击滑点（假设保守取各 $0.05\% \times 2 = 0.10\%$）。单次换仓全摩擦成本约为 $0.202\%$。
- **[高换手率下的复利磨损放大]**：若策略年化单边换手率为 50 倍（即一年换仓 50 次），仅摩擦成本在时间序列上的机械性扣除就高达 $50 \times 0.202\% = 10.10\%$；若年化换手率达到 100 倍且规模较大导致滑点升至 $0.1\%$，摩擦损耗将飙升至 $25\% \sim 30\%$。
- **[容量天花板与 Alpha 衰减]**：当策略规模扩大时，冲击滑点呈 $O(\sqrt{\text{Size}})$ 非线性膨胀，而总超额收益仅呈常数或衰减，边际摩擦成本迅速抹平全部纸面 Alpha，导致实盘净利润断崖式归零。

【Q2 深度参考答案】
- **[物理流动性承载力违背]**：若整个分钟 Bar 市场真实总成交仅有 500 手，代表在 $[10.00, 10.50]$ 整个价格带上全市场所有参与者的博弈总和仅为 500 手。若允许策略单笔瞬时吃下 2000 手，相当于策略在回测中虚构了多达 1500 手的凭空对手盘流动性。
- **[参与率上限（Participation Cap）截断]**：工业级事件驱动引擎必须强制设定单 Bar 参与率上限（通常 $\alpha = 10\%$）。本例中该 Bar 最多撮合 $500 \times 10\% = 50$ 手，成交状态置为 `PARTIALLY_FILLED`。
- **[跨期排队结转架构（Order Walk-Forward）]**：剩余 1950 手作为在途活动委托留在撮合队列中。在下一分钟 Bar 到来时，重新判定价格区间（是否仍在 10.20 元以内）并根据新 Bar 的成交量配额继续撮合，直到全额成交或超时撤单。

【Q3 深度参考答案】
- **[做市商与限价单的逆向选择机制]**：作为流动性提供者（Maker）在盘口挂出限价买单，该订单被成交的充要条件是有知情交易者或激进的主动市价卖单（Taker）向下扫盘。当限价买单成交时，通常伴随着空头动量极强的毒性订单流（Toxic Flow），价格大概率会继续向下击穿。
- **[回测中盲目假设触价即成的偏误]**：如果价格仅仅触及委托价 10.20 元便立刻反弹，实盘中该限价单排在队列末尾大概率根本无法成交；回测若判定成交，则严重高估了逢低买入的成功率。
- **[微观仿真刻画方案]**：在 Bar 级撮合中引入“深度穿越阈值”或“逆向滑点惩罚”：仅当后续最低价显著低于委托价（例如 $P_{\text{low}} < P_{\text{limit}} - \text{TickSize}$）且成交量超过该挂单规模数倍时，才确认订单成交，以精准拟合微观结构中的逆向选择成本。
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import math


@dataclass
class Order:
    """订单对象"""
    order_id: str
    symbol: str
    direction: str       # 'BUY' 或 'SELL'
    order_type: str      # 'MARKET' (市价单) 或 'LIMIT' (限价单)
    price: float         # 委托限价 (市价单可传 0.0)
    volume: int          # 委托总股数 (100股的整数倍)
    filled_volume: int = 0
    status: str = 'PENDING'  # 'PENDING', 'PARTIALLY_FILLED', 'FILLED', 'REJECTED'


@dataclass
class BarData:
    """行情 Bar 对象"""
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int          # 市场该 Bar 真实成交股数
    limit_up: float      # 当日涨停价
    limit_down: float    # 当日跌停价
    is_suspended: bool = False


@dataclass
class ExecutionReport:
    """撮合成交回报"""
    order_id: str
    status: str
    filled_this_bar: int     # 本次 Bar 撮合成交股数
    cumulative_filled: int   # 累计已成交总股数
    remaining_volume: int    # 剩余未成交股数
    executed_price: float    # 本次成交均价 (包含滑点)
    commission: float        # 券商佣金 (含最低5元保底)
    transfer_fee: float      # 过户费
    stamp_duty: float        # 印花税 (仅卖出)
    slippage_cost: float     # 相比基准价产生的绝对滑点损失金额
    total_friction: float    # 总摩擦成本 = 佣金 + 过户费 + 印花税 + 滑点损失


class EventDrivenMatchingEngine:
    """
    工业级事件驱动微观撮合引擎模拟器:
    支持真实 A 股费用结构、流动性容量上限截断、平方根市场冲击滑点与极端行情不可成交判定。
    """

    def __init__(
        self,
        commission_rate: float = 0.00025,
        min_commission: float = 5.0,
        transfer_fee_rate: float = 0.00001,
        stamp_duty_rate: float = 0.0005,
        base_slippage: float = 0.0002,
        impact_coef: float = 0.05,
        max_volume_ratio: float = 0.10
    ):
        self.commission_rate = commission_rate
        self.min_commission = min_commission
        self.transfer_fee_rate = transfer_fee_rate
        self.stamp_duty_rate = stamp_duty_rate
        self.base_slippage = base_slippage
        self.impact_coef = impact_coef
        self.max_volume_ratio = max_volume_ratio

    def calculate_transaction_fees(self, trade_amount: float, direction: str) -> Tuple[float, float, float]:
        """
        计算法定交易规费：
        1. 券商佣金 (双边，最低 5 元)
        2. 过户费 (双边)
        3. 印花税 (仅卖出)
        """
        raw_comm = trade_amount * self.commission_rate
        commission = max(self.min_commission, raw_comm) if trade_amount > 0 else 0.0
        transfer_fee = trade_amount * self.transfer_fee_rate
        stamp_duty = trade_amount * self.stamp_duty_rate if direction.upper() == 'SELL' else 0.0
        return commission, transfer_fee, stamp_duty

    def calculate_impact_slippage(
        self,
        benchmark_price: float,
        direction: str,
        order_volume: int,
        bar_volume: int
    ) -> Tuple[float, float]:
        """
        计算平方根市场冲击滑点。
        """
        if bar_volume <= 0 or order_volume <= 0:
            return benchmark_price, 0.0

        part_ratio = order_volume / bar_volume
        slippage_rate = self.base_slippage + self.impact_coef * math.sqrt(part_ratio)

        if direction.upper() == 'BUY':
            exec_price = benchmark_price * (1.0 + slippage_rate)
            slippage_cost = (exec_price - benchmark_price) * order_volume
        else:
            exec_price = benchmark_price * (1.0 - slippage_rate)
            slippage_cost = (benchmark_price - exec_price) * order_volume

        return exec_price, slippage_cost

    def match(self, order: Order, bar: BarData) -> ExecutionReport:
        """
        执行单 Bar 粒度事件撮合逻辑。
        """
        rem_before = order.volume - order.filled_volume

        # 1. 停牌检查
        if bar.is_suspended or bar.volume <= 0:
            order.status = "REJECTED"
            return ExecutionReport(
                order_id=order.order_id,
                status=order.status,
                filled_this_bar=0,
                cumulative_filled=order.filled_volume,
                remaining_volume=rem_before,
                executed_price=0.0,
                commission=0.0,
                transfer_fee=0.0,
                stamp_duty=0.0,
                slippage_cost=0.0,
                total_friction=0.0
            )

        # 2. 涨跌停封板流动性截断
        if order.direction == "BUY" and bar.low >= bar.limit_up and bar.high >= bar.limit_up:
            return ExecutionReport(
                order_id=order.order_id,
                status=order.status,
                filled_this_bar=0,
                cumulative_filled=order.filled_volume,
                remaining_volume=rem_before,
                executed_price=0.0,
                commission=0.0,
                transfer_fee=0.0,
                stamp_duty=0.0,
                slippage_cost=0.0,
                total_friction=0.0
            )

        if order.direction == "SELL" and bar.low <= bar.limit_down and bar.high <= bar.limit_down:
            return ExecutionReport(
                order_id=order.order_id,
                status=order.status,
                filled_this_bar=0,
                cumulative_filled=order.filled_volume,
                remaining_volume=rem_before,
                executed_price=0.0,
                commission=0.0,
                transfer_fee=0.0,
                stamp_duty=0.0,
                slippage_cost=0.0,
                total_friction=0.0
            )

        # 3. 限价单触价判定
        if order.order_type == "LIMIT":
            if order.direction == "BUY" and bar.low > order.price:
                return ExecutionReport(
                    order_id=order.order_id,
                    status=order.status,
                    filled_this_bar=0,
                    cumulative_filled=order.filled_volume,
                    remaining_volume=rem_before,
                    executed_price=0.0,
                    commission=0.0,
                    transfer_fee=0.0,
                    stamp_duty=0.0,
                    slippage_cost=0.0,
                    total_friction=0.0
                )
            if order.direction == "SELL" and bar.high < order.price:
                return ExecutionReport(
                    order_id=order.order_id,
                    status=order.status,
                    filled_this_bar=0,
                    cumulative_filled=order.filled_volume,
                    remaining_volume=rem_before,
                    executed_price=0.0,
                    commission=0.0,
                    transfer_fee=0.0,
                    stamp_duty=0.0,
                    slippage_cost=0.0,
                    total_friction=0.0
                )

        # 4. 容量上限与局部撮合
        available_cap = int(bar.volume * self.max_volume_ratio)
        fill_qty = min(rem_before, available_cap)
        if fill_qty <= 0:
            return ExecutionReport(
                order_id=order.order_id,
                status=order.status,
                filled_this_bar=0,
                cumulative_filled=order.filled_volume,
                remaining_volume=rem_before,
                executed_price=0.0,
                commission=0.0,
                transfer_fee=0.0,
                stamp_duty=0.0,
                slippage_cost=0.0,
                total_friction=0.0
            )

        # 5. 基准价与滑点
        if order.order_type == "MARKET":
            bench_price = bar.open
        else:
            if order.direction == "BUY" and bar.open <= order.price:
                bench_price = bar.open
            elif order.direction == "SELL" and bar.open >= order.price:
                bench_price = bar.open
            else:
                bench_price = order.price

        exec_price, slippage_cost = self.calculate_impact_slippage(
            bench_price, order.direction, fill_qty, bar.volume
        )

        trade_amount = exec_price * fill_qty
        comm, trans, stamp = self.calculate_transaction_fees(trade_amount, order.direction)
        total_friction = comm + trans + stamp + slippage_cost

        # 6. 更新订单对象状态
        order.filled_volume += fill_qty
        if order.filled_volume >= order.volume:
            order.status = "FILLED"
        else:
            order.status = "PARTIALLY_FILLED"

        rem_after = order.volume - order.filled_volume

        return ExecutionReport(
            order_id=order.order_id,
            status=order.status,
            filled_this_bar=fill_qty,
            cumulative_filled=order.filled_volume,
            remaining_volume=rem_after,
            executed_price=exec_price,
            commission=comm,
            transfer_fee=trans,
            stamp_duty=stamp,
            slippage_cost=slippage_cost,
            total_friction=total_friction
        )


# ==============================================================================
# 自动化测试与参考答案解析
# ==============================================================================
if __name__ == "__main__":
    print("正在运行 10_system_infra / Lesson 02 参考实现断言验证...")

    engine = EventDrivenMatchingEngine(
        commission_rate=0.00025,
        min_commission=5.0,
        transfer_fee_rate=0.00001,
        stamp_duty_rate=0.0005,
        base_slippage=0.0002,
        impact_coef=0.05,
        max_volume_ratio=0.10
    )

    # 测试 1: 法定交易税费
    comm1, trans1, stamp1 = engine.calculate_transaction_fees(5000.0, 'BUY')
    assert comm1 == 5.0
    assert trans1 == 5000.0 * 0.00001
    assert stamp1 == 0.0

    comm2, trans2, stamp2 = engine.calculate_transaction_fees(200000.0, 'SELL')
    assert comm2 == 50.0
    assert trans2 == 2.0
    assert stamp2 == 100.0

    # 测试 2: 停牌与涨跌停截断
    suspended_bar = BarData(
        symbol="600000.SH", open=10.0, high=10.0, low=10.0, close=10.0,
        volume=0, limit_up=11.0, limit_down=9.0, is_suspended=True
    )
    buy_order = Order("O01", "600000.SH", "BUY", "MARKET", 0.0, 1000)
    rep_susp = engine.match(buy_order, suspended_bar)
    assert rep_susp.status == "REJECTED"
    assert rep_susp.filled_this_bar == 0

    limit_up_bar = BarData(
        symbol="600000.SH", open=11.0, high=11.0, low=11.0, close=11.0,
        volume=50000, limit_up=11.0, limit_down=9.0, is_suspended=False
    )
    rep_lup = engine.match(buy_order, limit_up_bar)
    assert rep_lup.filled_this_bar == 0

    limit_down_bar = BarData(
        symbol="600000.SH", open=9.0, high=9.0, low=9.0, close=9.0,
        volume=30000, limit_up=11.0, limit_down=9.0, is_suspended=False
    )
    sell_order = Order("O02", "600000.SH", "SELL", "MARKET", 0.0, 1000)
    rep_ldown = engine.match(sell_order, limit_down_bar)
    assert rep_ldown.filled_this_bar == 0

    # 测试 3: 流动性容量上限与平方根滑点
    normal_bar = BarData(
        symbol="600000.SH", open=10.0, high=10.5, low=9.8, close=10.2,
        volume=100000, limit_up=11.0, limit_down=9.0, is_suspended=False
    )
    big_order = Order("O03", "600000.SH", "BUY", "MARKET", 0.0, 25000)
    rep_part = engine.match(big_order, normal_bar)
    assert rep_part.status == "PARTIALLY_FILLED"
    assert rep_part.filled_this_bar == 10000
    assert rep_part.remaining_volume == 15000
    assert big_order.filled_volume == 10000
    assert rep_part.executed_price > 10.0
    assert rep_part.slippage_cost > 0.0

    # 测试 4: 限价单
    unhit_limit_order = Order("O04", "600000.SH", "BUY", "LIMIT", 9.50, 1000)
    rep_unhit = engine.match(unhit_limit_order, normal_bar)
    assert rep_unhit.filled_this_bar == 0

    hit_limit_order = Order("O05", "600000.SH", "BUY", "LIMIT", 10.30, 5000)
    rep_hit = engine.match(hit_limit_order, normal_bar)
    assert rep_hit.status == "FILLED"
    assert rep_hit.filled_this_bar == 5000
    assert rep_hit.remaining_volume == 0

    print("Lesson 02 参考实现全部断言通过 (Exit Code 0)！\n")
