"""
================================================================================
模块 10：量化回测引擎避坑指南与实盘系统工程 · 第 4/4 课
第 4 课：实盘交易架构：订单有限状态机、网络心跳与风控熔断哨兵
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 思考题深入分析并达到工业级认知线：各 2 分（共 6 分）
- 综合及格线：8/10 分

【理论精讲】
量化交易从“离线研发”走向“实盘生产”的最大跃迁，是从“确定性计算”走向“分布式不确定性处理”。
在实盘生产环境中，网络抖动、丢包、交易所回报延迟、行情突发断流、策略逻辑死循环或乌龙指等灾难无处不在。
一个军规级的量化交易执行系统，必须在策略与交易所柜台之间筑牢两道防线：
**严谨的订单生命周期有限状态机 (Finite State Machine, FSM)** 与 **前置硬风控熔断哨兵网关 (Risk Sentinel Gateway)**。

1. 订单有限状态机 (Order Lifecycle FSM)：
   - 订单状态转移遵循严格的单向因果图：
     ```
     [PENDING_SUBMIT] ──► [SUBMITTED] ──► [ACCEPTED] ──► [PARTIALLY_FILLED] ──► [FILLED]
             │                    │             │               │
             ▼                    ▼             ▼               ▼
        [REJECTED]           [REJECTED]    [CANCELLED]     [CANCELLED]
     ```
   - 终态原则 (Terminal States)：`FILLED`, `CANCELLED`, `REJECTED` 为终态，一旦进入终态，严禁发生任何次级状态转移。
   - 竞态仲裁 (Race Conditions)：在撤单（Cancel）在途期间若收到交易所完全成交（Filled），状态机必须依据交易所时间戳以成交为准，将后续到达的撤单确认标记为拒绝（Cancel Rejected），防止产生幽灵持仓。

2. 前置多维硬风控规则链 (Pre-Trade Multi-Layer Risk Sentinel)：
   - 层级 1 (乌龙指与单笔拦截)：单笔报单金额硬顶 (如 100 万元)，单笔报单股数硬顶，超过即刻在网关层硬拦截。
   - 层级 2 (标的合规白名单)：禁止买入 ST、*ST 或停牌退市警示股票。
   - 层级 3 (头寸与杠杆敞口)：
     * 单票持仓集中度上限：单个股票持仓市值 / 账户总净资产 $\le 20\%$。
     * 全账户总杠杆率上限：所有多头持仓总市值 / 账户总净资产 $\le 1.0$ (严禁非预期借贷加杠杆)。
   - 层级 4 (动态回撤与亏损熔断)：
     * 日内动态亏损熔断：当日净亏损率 $\le -3\%$ 时触发。
     * 历史高点最大回撤熔断：相对历史最高净值 (Peak Equity) 回撤 $\le -8\%$ 时触发。

3. 网络心跳与紧急熔断切断机制 (Heartbeat, COD & Kill Switch)：
   - 心跳协议 (Heartbeat & Keep-Alive)：策略客户端与交易网关每秒保持心跳同步。一旦心跳丢失超过设定的超时时间（如 3.0 秒），网关判定网络中断。
   - 断线自动撤单 (Cancel-On-Disconnect, COD)：网络断开时，网关自动向交易所广播撤销该策略的所有在途活动挂单，防止断网裸暴露。
   - 终极自毁熔断开关 (Emergency Kill Switch)：一旦日内亏损、最大回撤触限或管理员下发人工切断指令，网关立即进入锁定状态：
     * 永久拒绝所有新开仓订单 (Reject All New Orders)；
     * 批量自动撤回全市场未成交活动挂单 (Mass Cancel Active Orders)；
     * 触发 P0 级监控告警。

【三个思考题 (Q1~Q3)】
Q1: 2013 年著名的“光大证券 816 乌龙指事件”（累计错误报单 234 亿元，成交 72.7 亿元）在系统架构与风控网关设计上暴露出哪些致命缺陷？如果在现代量化网关中，如何从“物理隔离前置硬风控”与“总额度熔断器”设计上彻底杜绝此类灾难？
Q2: 在异步分布式微服务交易架构中，如果策略发送了撤单请求（Cancel Request），但由于网络抖动，撤单回报（Cancelled）与交易所的完全成交回报（Filled）在极微小的时差内同时或乱序到达，订单状态机该如何处理这种竞态条件（Race Condition）以避免账本资金状态错乱？
Q3: 为什么实盘量化交易系统严禁使用“软风控（即在策略模型代码内部用 if-else 判定）”，而必须在独立的订单网关层（Execution Gateway）部署强隔离的“前置硬风控哨兵（Pre-Trade Hard Sentinel）”？
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Set, Optional


class OrderState(Enum):
    """订单生命周期状态枚举"""
    PENDING_SUBMIT = "PENDING_SUBMIT"     # 本地准备提交
    SUBMITTED = "SUBMITTED"               # 已发送至柜台
    ACCEPTED = "ACCEPTED"                 # 交易所已受理解挂
    PARTIALLY_FILLED = "PARTIALLY_FILLED" # 部分成交
    FILLED = "FILLED"                     # 完全成交 (终态)
    CANCELLED = "CANCELLED"               # 已撤单 (终态)
    REJECTED = "REJECTED"                 # 被风控或交易所拒绝 (终态)


@dataclass
class Order:
    """实盘订单对象"""
    order_id: str
    symbol: str
    direction: str          # 'BUY' 或 'SELL'
    price: float            # 委托价格
    volume: int             # 委托数量 (股)
    filled_volume: int = 0  # 已成交数量
    state: OrderState = OrderState.PENDING_SUBMIT


@dataclass
class PortfolioState:
    """账户资产与头寸实时状态"""
    total_equity: float                  # 当前账户总净资产 (元)
    cash: float                          # 可用现金 (元)
    peak_equity: float                   # 账户历史最高净资产 (用于计算回撤)
    positions: Dict[str, float] = field(default_factory=dict) # 标的代码 -> 当前持仓市值 (元)
    daily_pnl_pct: float = 0.0           # 当日收益率 (例如 -0.02 表示 -2%)


class OrderStateMachine:
    """
    订单生命周期有限状态机 (FSM):
    严格校验状态转移的因果合法性，拦截任何非法跃迁与终态篡改。
    """

    # 合法状态转移映射表
    VALID_TRANSITIONS: Dict[OrderState, Set[OrderState]] = {
        OrderState.PENDING_SUBMIT: {OrderState.SUBMITTED, OrderState.REJECTED},
        OrderState.SUBMITTED: {OrderState.ACCEPTED, OrderState.REJECTED},
        OrderState.ACCEPTED: {OrderState.PARTIALLY_FILLED, OrderState.FILLED, OrderState.CANCELLED},
        OrderState.PARTIALLY_FILLED: {OrderState.PARTIALLY_FILLED, OrderState.FILLED, OrderState.CANCELLED},
        OrderState.FILLED: set(),       # 终态不可转移
        OrderState.CANCELLED: set(),    # 终态不可转移
        OrderState.REJECTED: set(),     # 终态不可转移
    }

    @classmethod
    def can_transition(cls, current_state: OrderState, target_state: OrderState) -> bool:
        """检查从 current_state 转移到 target_state 是否合法"""
        # TODO: 依据 VALID_TRANSITIONS 返回是否允许转移
        pass

    @classmethod
    def transition(cls, order: Order, target_state: OrderState) -> bool:
        """
        尝试执行状态转移:
        - 若合法: 更新 order.state = target_state 并返回 True
        - 若非法: 保持原状态，返回 False (禁止非法篡改)
        """
        # TODO: 实现状态转移逻辑
        pass


class RiskSentinelGateway:
    """
    前置硬风控熔断哨兵网关 (Risk Sentinel Gateway):
    在订单进入柜台/交易所之前执行硬性风控预检、心跳保活检测与紧急熔断切断 (Kill Switch)。
    """

    def __init__(
        self,
        max_single_order_value: float = 1_000_000.0, # 单笔最大报单金额 (元)
        max_stock_concentration: float = 0.20,       # 单票持仓集中度上限 20%
        max_leverage: float = 1.0,                   # 全账户杠杆率上限 100%
        daily_loss_limit: float = -0.03,             # 单日亏损熔断阈值 -3%
        max_drawdown_limit: float = -0.08,           # 最大回撤熔断阈值 -8%
        heartbeat_timeout_sec: float = 3.0           # 心跳超时阈值 (秒)
    ):
        self.max_single_order_value = max_single_order_value
        self.max_stock_concentration = max_stock_concentration
        self.max_leverage = max_leverage
        self.daily_loss_limit = daily_loss_limit
        self.max_drawdown_limit = max_drawdown_limit
        self.heartbeat_timeout_sec = heartbeat_timeout_sec

        # 网关运行时状态
        self.is_kill_switch_active: bool = False
        self.last_heartbeat_timestamp: float = 0.0
        self.active_orders: Dict[str, Order] = {} # order_id -> Order (当前在途活跃订单)

    def update_heartbeat(self, current_timestamp: float) -> None:
        """更新最近一次心跳时间戳"""
        self.last_heartbeat_timestamp = current_timestamp

    def check_heartbeat(self, current_timestamp: float) -> Tuple[bool, str]:
        """
        心跳检查:
        若 current_timestamp - last_heartbeat_timestamp > heartbeat_timeout_sec:
            心跳超时，返回 (False, "HEARTBEAT_TIMEOUT_DISCONNECTED")
        否则返回 (True, "HEARTBEAT_OK")
        """
        # TODO: 实现心跳检测判定
        pass

    def check_pre_trade_risk(
        self,
        order: Order,
        portfolio: PortfolioState,
        is_st_stock: bool
    ) -> Tuple[bool, str]:
        """
        前置硬风控流水线审查 (Pre-Trade Risk Inspection):
        
        校验规则链:
        1. 熔断开关检查:
           若 is_kill_switch_active 为 True，直接拦截 -> (False, "REJECT_KILL_SWITCH_ACTIVE")
        2. 乌龙指单笔金额硬限制:
           order_value = order.price * order.volume
           若 order_value > max_single_order_value -> (False, "REJECT_FAT_FINGER_LIMIT")
        3. 标的合规性检查:
           若 is_st_stock 为 True -> (False, "REJECT_ST_PROHIBITED")
        4. 动态日内亏损熔断判定:
           若 portfolio.daily_pnl_pct <= daily_loss_limit:
               自动触发 trigger_emergency_kill_switch()
               返回 (False, "REJECT_DAILY_LOSS_CIRCUIT_BREAKER")
        5. 历史最高净值最大回撤熔断判定:
           drawdown = (portfolio.total_equity - portfolio.peak_equity) / portfolio.peak_equity
           若 drawdown <= max_drawdown_limit:
               自动触发 trigger_emergency_kill_switch()
               返回 (False, "REJECT_MAX_DRAWDOWN_CIRCUIT_BREAKER")
        6. 买单头寸集中度约束 (仅针对 BUY 买入订单):
           current_pos_val = portfolio.positions.get(order.symbol, 0.0)
           new_pos_val = current_pos_val + order_value
           若 (new_pos_val / portfolio.total_equity) > max_stock_concentration:
               返回 (False, "REJECT_CONCENTRATION_LIMIT")
        7. 全账户总杠杆率约束 (仅针对 BUY 买入订单):
           total_pos_val = sum(portfolio.positions.values()) + order_value
           若 (total_pos_val / portfolio.total_equity) > max_leverage:
               返回 (False, "REJECT_LEVERAGE_LIMIT")
               
        全部通过:
           返回 (True, "APPROVED")
        """
        # TODO: 编写完整前置风控规则链
        pass

    def trigger_emergency_kill_switch(self) -> List[str]:
        """
        触发紧急自毁熔断 (Emergency Kill Switch):
        1. 将 is_kill_switch_active 置为 True，锁定交易网关。
        2. 遍历 active_orders 中所有非终态订单，执行状态转移至 CANCELLED。
        3. 返回所有被紧急撤销的 order_id 列表。
        """
        # TODO: 实现硬熔断切断与批量紧急撤单
        pass


# ==============================================================================
# 自动化测试断言
# ==============================================================================

if __name__ == "__main__":
    print("正在运行 10_system_infra / Lesson 04 单元测试...")

    # -------------------------------------------------------------------------
    # 测试 1: 订单有限状态机 (FSM) 合法转移与终态不可逆拦截
    # -------------------------------------------------------------------------
    fsm = OrderStateMachine
    order = Order("ORD_01", "600519.SH", "BUY", 1800.0, 100)
    assert order.state == OrderState.PENDING_SUBMIT

    # 合法转移 1: PENDING_SUBMIT -> SUBMITTED
    ok1 = fsm.transition(order, OrderState.SUBMITTED)
    assert ok1 is True and order.state == OrderState.SUBMITTED

    # 合法转移 2: SUBMITTED -> ACCEPTED
    ok2 = fsm.transition(order, OrderState.ACCEPTED)
    assert ok2 is True and order.state == OrderState.ACCEPTED

    # 合法转移 3: ACCEPTED -> PARTIALLY_FILLED
    ok3 = fsm.transition(order, OrderState.PARTIALLY_FILLED)
    assert ok3 is True and order.state == OrderState.PARTIALLY_FILLED

    # 合法转移 4: PARTIALLY_FILLED -> FILLED (进入终态)
    ok4 = fsm.transition(order, OrderState.FILLED)
    assert ok4 is True and order.state == OrderState.FILLED

    # 非法转移测试: FILLED 终态不可撤单或被拒绝
    bad1 = fsm.transition(order, OrderState.CANCELLED)
    assert bad1 is False, "已完全成交 FILLED 的订单绝不可被转移至 CANCELLED"
    assert order.state == OrderState.FILLED, "非法转移尝试不得篡改原终态"
    print("✅ 测试 1 (订单生命周期 FSM 状态机转移与终态保护) 通过！")

    # -------------------------------------------------------------------------
    # 测试 2: 前置多层硬风控规则链预检
    # -------------------------------------------------------------------------
    gateway = RiskSentinelGateway(
        max_single_order_value=1_000_000.0,
        max_stock_concentration=0.20,
        max_leverage=1.0,
        daily_loss_limit=-0.03,
        max_drawdown_limit=-0.08,
        heartbeat_timeout_sec=3.0
    )

    portfolio = PortfolioState(
        total_equity=10_000_000.0, # 1000 万元总净资产
        cash=4_000_000.0,          # 400 万元现金
        peak_equity=10_000_000.0,  # 历史峰值 1000 万元
        positions={"600519.SH": 1_500_000.0, "000858.SZ": 500_000.0}, # 已有 200 万股票
        daily_pnl_pct=0.01         # 当日盈利 +1%
    )

    # 场景 A: 正常买单 (500股 * 1000元 = 50万元 <= 100万，增持后茅台持仓 200万/1000万 = 20% <= 20%) -> 准入
    ord_normal = Order("ORD_A", "600519.SH", "BUY", 1000.0, 500)
    pass_a, msg_a = gateway.check_pre_trade_risk(ord_normal, portfolio, is_st_stock=False)
    assert pass_a is True and msg_a == "APPROVED"

    # 场景 B: 乌龙指超额买单 (2000股 * 1000元 = 200万元 > 100万元) -> 拦截
    ord_fat = Order("ORD_B", "600519.SH", "BUY", 1000.0, 2000)
    pass_b, msg_b = gateway.check_pre_trade_risk(ord_fat, portfolio, is_st_stock=False)
    assert pass_b is False and "FAT_FINGER" in msg_b

    # 场景 C: ST 股票违规交易 -> 拦截
    ord_st = Order("ORD_C", "*ST000001", "BUY", 10.0, 1000)
    pass_c, msg_c = gateway.check_pre_trade_risk(ord_st, portfolio, is_st_stock=True)
    assert pass_c is False and "ST_PROHIBITED" in msg_c

    # 场景 D: 单票持仓集中度超限 (已有茅台 150万，再买 60万 -> 210万/1000万 = 21% > 20%) -> 拦截
    ord_conc = Order("ORD_D", "600519.SH", "BUY", 1000.0, 600)
    pass_d, msg_d = gateway.check_pre_trade_risk(ord_conc, portfolio, is_st_stock=False)
    assert pass_d is False and "CONCENTRATION" in msg_d

    # 场景 E: 杠杆率超限 (全账户已有持仓 950万，再买 80万 -> 1030万/1000万 = 1.03 > 1.0，且单笔80万<=100万，集中度8%<=20%) -> 拦截
    portfolio_high_lev = PortfolioState(
        total_equity=10_000_000.0,
        cash=500_000.0,
        peak_equity=10_000_000.0,
        positions={"600519.SH": 1_500_000.0, "000858.SZ": 1_500_000.0, "601318.SH": 1_500_000.0,
                   "000333.SZ": 1_500_000.0, "600036.SH": 1_500_000.0, "002594.SZ": 2_000_000.0},
        daily_pnl_pct=0.01
    )
    ord_lev = Order("ORD_E", "300750.SZ", "BUY", 800.0, 1000) # 80 万元
    pass_lev, msg_lev = gateway.check_pre_trade_risk(ord_lev, portfolio_high_lev, is_st_stock=False)
    assert pass_lev is False and "LEVERAGE" in msg_lev
    print("✅ 测试 2 (多层前置风控: 乌龙指、ST股、集中度与杠杆率硬拦截) 通过！")

    # -------------------------------------------------------------------------
    # 测试 3: 网络心跳检测与断线保护
    # -------------------------------------------------------------------------
    gateway.update_heartbeat(current_timestamp=100.0)
    hb_ok, _ = gateway.check_heartbeat(current_timestamp=102.5) # 间隔 2.5 秒 <= 3.0 秒
    assert hb_ok is True

    hb_fail, hb_msg = gateway.check_heartbeat(current_timestamp=104.0) # 间隔 4.0 秒 > 3.0 秒
    assert hb_fail is False and "TIMEOUT" in hb_msg
    print("✅ 测试 3 (毫秒级网络心跳保活与超时预警) 通过！")

    # -------------------------------------------------------------------------
    # 测试 4: 日内大亏/最大回撤自动熔断 (Kill Switch) 与全撤单切断
    # -------------------------------------------------------------------------
    # 注册两笔活跃挂单
    active_ord1 = Order("ACT_01", "600519.SH", "BUY", 1800.0, 100, state=OrderState.ACCEPTED)
    active_ord2 = Order("ACT_02", "000858.SZ", "BUY", 150.0, 1000, state=OrderState.PARTIALLY_FILLED)
    gateway.active_orders["ACT_01"] = active_ord1
    gateway.active_orders["ACT_02"] = active_ord2

    # 账户净值从历史高点 1000 万跌至 910 万 (回撤 -9% <= -8% 熔断线)
    crashed_portfolio = PortfolioState(
        total_equity=9_100_000.0,
        cash=2_000_000.0,
        peak_equity=10_000_000.0,
        positions={},
        daily_pnl_pct=-0.04 # 单日暴跌 -4% <= -3% 熔断线
    )

    test_ord = Order("ORD_NEW", "600519.SH", "BUY", 1000.0, 100)
    pass_crash, crash_msg = gateway.check_pre_trade_risk(test_ord, crashed_portfolio, is_st_stock=False)
    
    assert pass_crash is False
    assert ("CIRCUIT_BREAKER" in crash_msg)
    assert gateway.is_kill_switch_active is True, "熔断开关必须被硬激活"

    # 校验所有活跃挂单是否被自动硬撤销
    assert active_ord1.state == OrderState.CANCELLED, "活动订单 1 必须被紧急撤回"
    assert active_ord2.state == OrderState.CANCELLED, "活动订单 2 必须被紧急撤回"

    # 网关锁定后，后续任何普通报单均直接拒单
    pass_locked, lock_msg = gateway.check_pre_trade_risk(test_ord, portfolio, is_st_stock=False)
    assert pass_locked is False and "KILL_SWITCH_ACTIVE" in lock_msg
    print("✅ 测试 4 (动态最大回撤熔断、紧急全撤单与网关切断锁定) 通过！")

    print("\n🎉 Lesson 04 全部单元测试顺利通过！")
"""
