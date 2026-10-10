"""
================================================================================
模块 10：量化回测引擎避坑指南与实盘系统工程 · 第 2/4 课
第 2 课：真实微观撮合仿真：滑点、排队模型与交易摩擦成本【参考实现】
================================================================================
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
        commission = max(self.min_commission, trade_amount * self.commission_rate)
        transfer_fee = trade_amount * self.transfer_fee_rate
        stamp_duty = trade_amount * self.stamp_duty_rate if direction == "SELL" else 0.0
        return commission, transfer_fee, stamp_duty

    def calculate_impact_slippage(
        self,
        benchmark_price: float,
        direction: str,
        fill_volume: int,
        bar_volume: int
    ) -> Tuple[float, float]:
        """
        基于平方根定律 (Square-Root Law) 计算非线性冲击滑点与实际执行价格
        """
        vol_ratio = fill_volume / max(bar_volume, 1)
        slippage_pct = self.base_slippage + self.impact_coef * math.sqrt(vol_ratio)

        if direction == "BUY":
            executed_price = benchmark_price * (1.0 + slippage_pct)
        else:
            executed_price = benchmark_price * (1.0 - slippage_pct)

        slippage_cost = abs(executed_price - benchmark_price) * fill_volume
        return executed_price, slippage_cost

    def match(self, order: Order, bar: BarData) -> ExecutionReport:
        """
        核心撮合内核实现
        """
        rem_before = order.volume - order.filled_volume

        # 1. 停牌检查
        if bar.is_suspended or bar.volume <= 0:
            order.status = "REJECTED"
            return ExecutionReport(
                order_id=order.order_id,
                status="REJECTED",
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
        if order.direction == "BUY" and bar.low >= bar.limit_up:
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
        if order.direction == "SELL" and bar.high <= bar.limit_down:
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

        # 3. 限价单价格未触及判定
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

    print("=" * 80)
    print("【思考题标准答案深度解析 (Q1 ~ Q3)】")
    print("=" * 80)
    print("Q1 解析:")
    print("  (1) 摩擦成本对高换手策略的复利毁灭：")
    print("      假设策略单边年换手率为 50 倍（双边 100 次买卖）。每次买入+卖出的单次全摩擦成本约为：")
    print("      双边佣金 (0.025% * 2) + 卖出印花税 (0.05%) + 双边过户费 (0.001% * 2) + 双边滑点 (0.05% * 2) ≈ 0.202%。")
    print("      一年仅交易成本总损耗就高达：50 × 0.202% ≈ 10.10%！若滑点因规模扩大上升至 0.1%，年化损耗将飙升至 15%~20%。")
    print("  (2) 资金容量 (Capacity) 惩罚推导：")
    print("      根据 Square-Root 冲击定律，滑点成本随交易规模增长以 $O(\\sqrt{Capital})$ 乃至超线性增长，而策略的纯 Alpha 收益")
    print("      随资金规模仅呈常数或次线性增长。当资金规模达到临界阈值时，边际摩擦成本将完全吞噬边际超额，导致净夏普比率迅速归零。")
    print("-" * 80)
    print("Q2 解析:")
    print("  (1) 物理现实违背：如果一个 Bar 的总成交量仅有 500 手，说明在 10.00 到 10.50 整个价格带上，市场上所有参与者")
    print("      累计成交才 500 手。若允许策略一人瞬间买入 2,000 手，相当于策略创造了不存在的对手盘，是极端的伪流动性。")
    print("  (2) 参与率截断与排队结转机制：")
    print("      工业级回测引擎必须强制实施参与率上限（Participation Cap, 常用 10%）。")
    print("      本例中该 Bar 最多成交 500 × 10% = 50 手，剩余 1,950 手作为未完成订单保留在撮合引擎等待队列中。")
    print("      在下一个分钟 Bar 到来时，重新判定价格条件与容量，实现连续部分成交（Partial Fill Walk-Forward）。")
    print("-" * 80)
    print("Q3 解析:")
    print("  (1) 逆向选择效应 (Adverse Selection)：")
    print("      在限价订单簿中，作为流动性提供者（Maker）挂单买入，当且仅当市场上有更激进的主动大卖单砸盘时，你的买单才会被吃掉。")
    print("      这意味着：当你的限价买单成交时，往往预示着空头动量极强，短期价格极大概率会继续向下击穿你的买价。")
    print("  (2) 回测仿真刻画：")
    print("      不能假设限价单永远以委托价成交；工业引擎中常引入'逆向滑点惩罚'或'成交概率衰减函数'：")
    print("      当行情仅触及委托价即反弹时，判定未排到队；只有当后续成交量充分穿越委托价达一定深度时，才确认成交。")
    print("=" * 80)
