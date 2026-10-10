"""
================================================================================
模块 10：量化回测引擎避坑指南与实盘系统工程 · 第 2/4 课
第 2 课：真实微观撮合仿真：滑点、排队模型与交易摩擦成本
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 思考题深入分析并达到工业级认知线：各 2 分（共 6 分）
- 综合及格线：8/10 分

【理论精讲】
在教科书或玩具级量化回测中，往往存在两个虚假的“完美假设”：
1. “零滑点与无限流动性”：假定策略在任何时刻都能以当前 Bar 的收盘价或开盘价瞬间全额成交，哪怕下单量高达数亿元，而该股票当日总成交仅几千万元。
2. “静态交易成本”：忽略了中国 A 股真实交易中券商佣金的“最低 5 元门槛”、双边过户费、单向卖出印花税以及非线性市场冲击成本。

工业级事件驱动撮合引擎（Event-Driven Matching Engine）必须严格仿真真实交易所的微观物理现实：

1. 订单排队与成交量容量限制 (Volume Participation Rate & Queueing)：
   - 在限价订单簿（Limit Order Book, LOB）中，撮合遵循“价格优先、时间优先”原则。
   - 在 Bar 粒度（分钟或日线）回测中，单笔策略订单成交量不得超过该 Bar 市场真实成交量的上限（通常设定参与率上限 $\alpha = 10\% \sim 15\%$）。超过该容量的大单只能部分成交（Partially Filled），剩余部分保留在订单簿中等待下一期撮合或被取消。
   - 极端行情流动性枯竭：
     * 停牌（Volume = 0 或 is_suspended = True）：拒绝撮合。
     * 一字涨停（Low == High == Limit_Up）：买盘封死，策略买单排在队尾无法成交（成交量为 0）。
     * 一字跌停（Low == High == Limit_Down）：卖盘封死，策略卖单排在队尾无法出逃（成交量为 0）。

2. 滑点与非线性市场冲击（Square-Root Law of Market Impact）：
   - 机构大单在买入时会推高对手方卖盘报价，卖出时会打压买盘报价。
   - 根据 Almgren-Chriss 与经典的物理学平方根定律（Square-Root Law），市场冲击滑点率满足：
     $$Slippage = Base\_Slippage + \eta \cdot \sqrt{\frac{Order\_Volume}{Bar\_Volume}}$$
     其中：
     - $Base\_Slippage$ 为买卖最小跳价（Tick Size）带来的固定点差滑点（如 2 bps）；
     - $\eta$ 为市场冲击系数（通常取 0.05 ~ 0.15）；
     - 买入成交价：$P_{exec} = P_{bench} \times (1 + Slippage)$；
     - 卖出成交价：$P_{exec} = P_{bench} \times (1 - Slippage)$。

3. 中国 A 股真实法定交易费用体系：
   - 券商佣金 (Commission)：双边征收，费率通常为万分之二点五（0.00025），且单笔必须满足最低 5 元人民币（不足 5 元按 5 元收取）。
   - 过户费 (Transfer Fee)：双边征收，按成交金额的 0.001%（十万分之一）收取。
   - 印花税 (Stamp Duty)：仅卖出单向征收，现行法定税率为 0.05%（千分之零点五）；买入免征。

【三个思考题 (Q1~Q3)】
Q1: 为什么小市值高换手策略（例如年化单边换手率 50~100 倍）在扣除万分之五滑点与真实交易成本后，纸面上 80% 的年化超额收益往往会断崖式暴跌至负收益？请从摩擦成本复利损耗的角度定量推导。
Q2: 在基于分钟 Bar 的事件驱动回测中，如果某个 Bar 内限价买单价格为 10.20 元，而该 Bar 的价格区间为 [Low=10.00, High=10.50]，真实市场成交量仅为 500 手（50,000 股），策略下单量为 2,000 手（200,000 股）。为什么绝不能允许这 2,000 手在当前 Bar 全部以 10.20 元成交？如何设计合理的局部成交与排队结转机制？
Q3: 什么是撮合中的“逆向选择（Adverse Selection）”？为什么在回测中限价单（Limit Order）成交往往意味着当前行情正朝着对该订单不利的方向剧烈运动？如何在仿真中刻画这一微观结构现象？
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
        commission_rate: float = 0.00025,   # 佣金率 万分之2.5
        min_commission: float = 5.0,        # 佣金最低 5 元
        transfer_fee_rate: float = 0.00001, # 过户费率 十万分之一 (0.001%)
        stamp_duty_rate: float = 0.0005,    # 印花税率 千分之0.5 (仅卖出)
        base_slippage: float = 0.0002,      # 基础固定滑点 2 bps
        impact_coef: float = 0.08,          # 平方根冲击系数
        max_volume_ratio: float = 0.10      # 单 Bar 最大成交量参与率上限 10%
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
        计算交易法定规费:
        返回: (commission, transfer_fee, stamp_duty)
        - commission: max(min_commission, trade_amount * commission_rate)
        - transfer_fee: trade_amount * transfer_fee_rate
        - stamp_duty: trade_amount * stamp_duty_rate (仅当 direction == 'SELL' 时征收，BUY 为 0)
        """
        # TODO: 实现费用计算公式
        pass

    def calculate_impact_slippage(
        self,
        benchmark_price: float,
        direction: str,
        fill_volume: int,
        bar_volume: int
    ) -> Tuple[float, float]:
        """
        基于平方根定律 (Square-Root Law) 计算非线性冲击滑点与实际执行价格:
        
        公式:
            slippage_pct = base_slippage + impact_coef * sqrt(fill_volume / bar_volume)
            若 direction == 'BUY':
                executed_price = benchmark_price * (1.0 + slippage_pct)
            若 direction == 'SELL':
                executed_price = benchmark_price * (1.0 - slippage_pct)
            slippage_cost = abs(executed_price - benchmark_price) * fill_volume
            
        返回: (executed_price, slippage_cost)
        """
        # TODO: 实现滑点与成交价格计算
        pass

    def match(self, order: Order, bar: BarData) -> ExecutionReport:
        """
        核心撮合内核:
        1. 检查标的是否停牌 (is_suspended == True 或 bar.volume <= 0):
           若停牌，直接判定无法成交，order.status 设为 'REJECTED'，返回成交量为 0 的回报。
        2. 检查极端封板流动性截断:
           - 若 direction == 'BUY' 且 bar.low >= bar.limit_up (一字涨停): 无法买入，保持未成交。
           - 若 direction == 'SELL' 且 bar.high <= bar.limit_down (一字跌停): 无法卖出，保持未成交。
        3. 限价单可撮合性判定 (OrderType == 'LIMIT'):
           - 若 direction == 'BUY' 且 bar.low > order.price: 价格未触及委托买价，无法成交。
           - 若 direction == 'SELL' 且 bar.high < order.price: 价格未触及委托卖价，无法成交。
        4. 成交量容量上限约束 (Liquidity Cap):
           - 本 Bar 允许的最大成交股数 = int(bar.volume * max_volume_ratio)
           - 本次撮合成交股数 fill_qty = min(order.volume - order.filled_volume, available_cap)
           - 若 fill_qty <= 0: 返回成交量为 0 的回报。
        5. 基准价格确定与滑点冲击:
           - 市价单: 以 bar.open 为基准价格，叠加平方根冲击滑点。
           - 限价单: 若 BUY 且 bar.open <= order.price，以 bar.open 为基准；否则以 order.price 为基准，叠加冲击滑点 (执行价不能劣于限价)。
        6. 结算税费并更新订单状态 (全部成交 FILLED 或部分成交 PARTIALLY_FILLED)。
        """
        # TODO: 实现完整撮合判定与结算逻辑
        pass


# ==============================================================================
# 自动化测试断言
# ==============================================================================

if __name__ == "__main__":
    print("正在运行 10_system_infra / Lesson 02 单元测试...")

    engine = EventDrivenMatchingEngine(
        commission_rate=0.00025,
        min_commission=5.0,
        transfer_fee_rate=0.00001,
        stamp_duty_rate=0.0005,
        base_slippage=0.0002,
        impact_coef=0.05,
        max_volume_ratio=0.10
    )

    # -------------------------------------------------------------------------
    # 测试 1: 法定交易税费精准计算 (买入免印花税，卖出征收千分之0.5，最低5元佣金)
    # -------------------------------------------------------------------------
    # 小额交易 5,000 元: 佣金 5000 * 0.00025 = 1.25 元 -> 触发 5 元保底
    comm1, trans1, stamp1 = engine.calculate_transaction_fees(5000.0, 'BUY')
    assert comm1 == 5.0, f"小额买入佣金保底预期 5.0，实际 {comm1}"
    assert trans1 == 5000.0 * 0.00001, f"过户费计算不符: {trans1}"
    assert stamp1 == 0.0, f"买入不应征收印花税，实际 {stamp1}"

    # 大额卖出 200,000 元: 佣金 50 元，过户费 2 元，印花税 100 元
    comm2, trans2, stamp2 = engine.calculate_transaction_fees(200000.0, 'SELL')
    assert comm2 == 50.0, f"大额佣金预期 50.0，实际 {comm2}"
    assert trans2 == 2.0, f"大额过户费预期 2.0，实际 {trans2}"
    assert stamp2 == 100.0, f"卖出印花税预期 100.0，实际 {stamp2}"
    print("✅ 测试 1 (A 股法定税费与 5 元保底佣金) 通过！")

    # -------------------------------------------------------------------------
    # 测试 2: 停牌与一字涨跌停流动性截断
    # -------------------------------------------------------------------------
    # 停牌日 Bar
    suspended_bar = BarData(
        symbol="600000.SH", open=10.0, high=10.0, low=10.0, close=10.0,
        volume=0, limit_up=11.0, limit_down=9.0, is_suspended=True
    )
    buy_order = Order("O01", "600000.SH", "BUY", "MARKET", 0.0, 1000)
    rep_susp = engine.match(buy_order, suspended_bar)
    assert rep_susp.status == "REJECTED", "停牌股票撮合应返回 REJECTED"
    assert rep_susp.filled_this_bar == 0, "停牌股票成交股数应为 0"

    # 一字涨停 Bar: 买入无法成交
    limit_up_bar = BarData(
        symbol="600000.SH", open=11.0, high=11.0, low=11.0, close=11.0,
        volume=50000, limit_up=11.0, limit_down=9.0, is_suspended=False
    )
    rep_lup = engine.match(buy_order, limit_up_bar)
    assert rep_lup.filled_this_bar == 0, "一字涨停板买单成交量必须为 0"

    # 一字跌停 Bar: 卖出无法成交
    limit_down_bar = BarData(
        symbol="600000.SH", open=9.0, high=9.0, low=9.0, close=9.0,
        volume=30000, limit_up=11.0, limit_down=9.0, is_suspended=False
    )
    sell_order = Order("O02", "600000.SH", "SELL", "MARKET", 0.0, 1000)
    rep_ldown = engine.match(sell_order, limit_down_bar)
    assert rep_ldown.filled_this_bar == 0, "一字跌停板卖单成交量必须为 0"
    print("✅ 测试 2 (停牌与极限一字涨跌停截断) 通过！")

    # -------------------------------------------------------------------------
    # 测试 3: 流动性容量上限 (10% 参与率) 与部分成交排队
    # -------------------------------------------------------------------------
    # Bar 真实成交总量 100,000 股，单 Bar 最大容纳 10% = 10,000 股
    normal_bar = BarData(
        symbol="600000.SH", open=10.0, high=10.5, low=9.8, close=10.2,
        volume=100000, limit_up=11.0, limit_down=9.0, is_suspended=False
    )
    # 策略下单 25,000 股市价买单
    big_order = Order("O03", "600000.SH", "BUY", "MARKET", 0.0, 25000)
    rep_part = engine.match(big_order, normal_bar)
    
    assert rep_part.status == "PARTIALLY_FILLED", "大单首个 Bar 应为部分成交"
    assert rep_part.filled_this_bar == 10000, f"参与率上限 10% 预期成交 10000 股，实际 {rep_part.filled_this_bar}"
    assert rep_part.remaining_volume == 15000, f"剩余待成交预期 15000 股，实际 {rep_part.remaining_volume}"
    assert big_order.filled_volume == 10000, "订单累计成交量应更新为 10000"
    
    # 验证平方根滑点: 基准价 10.0，买入滑点率 = 0.0002 + 0.05 * sqrt(10000 / 100000) = 0.0002 + 0.05 * 0.3162277 = 0.016011
    # 成交均价预期 > 10.0
    assert rep_part.executed_price > 10.0, f"买单滑点后成交价必须高于基准价 10.0，实际 {rep_part.executed_price}"
    assert rep_part.slippage_cost > 0.0, "滑点摩擦成本应大于 0"
    print(f"  大单撮合验证: 委托 25,000 股 -> 首 Bar 成交 {rep_part.filled_this_bar} 股，成交均价: {rep_part.executed_price:.4f} 元")
    print(f"  摩擦成本账本: 佣金={rep_part.commission:.2f}元, 过户费={rep_part.transfer_fee:.2f}元, 滑点损失={rep_part.slippage_cost:.2f}元")
    print("✅ 测试 3 (流动性容量上限与非线性平方根滑点) 通过！")

    # -------------------------------------------------------------------------
    # 测试 4: 限价单价格未触及与完全成交
    # -------------------------------------------------------------------------
    # 委托价格 9.50 买入，而当日最低价 9.80，价格未触及
    unhit_limit_order = Order("O04", "600000.SH", "BUY", "LIMIT", 9.50, 1000)
    rep_unhit = engine.match(unhit_limit_order, normal_bar)
    assert rep_unhit.filled_this_bar == 0, "未触及限价的买单不可成交"

    # 委托价格 10.30 买入，正常成交 (委托 5,000 股 <= 容量 10,000 股)
    hit_limit_order = Order("O05", "600000.SH", "BUY", "LIMIT", 10.30, 5000)
    rep_hit = engine.match(hit_limit_order, normal_bar)
    assert rep_hit.status == "FILLED", "满足限价且在容量范围内的订单应完全成交"
    assert rep_hit.filled_this_bar == 5000
    assert rep_hit.remaining_volume == 0
    print("✅ 测试 4 (限价单价格判定与全额成交) 通过！")

    print("\n🎉 Lesson 02 全部单元测试顺利通过！")
"""
