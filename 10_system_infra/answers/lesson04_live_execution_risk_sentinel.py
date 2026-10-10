"""
================================================================================
模块 10：量化回测引擎避坑指南与实盘系统工程 · 第 4/4 课
第 4 课：实盘交易架构：订单有限状态机、网络心跳与风控熔断哨兵【参考实现】
================================================================================
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
        allowed = cls.VALID_TRANSITIONS.get(current_state, set())
        return target_state in allowed

    @classmethod
    def transition(cls, order: Order, target_state: OrderState) -> bool:
        """
        尝试执行状态转移:
        - 若合法: 更新 order.state = target_state 并返回 True
        - 若非法: 保持原状态，返回 False (禁止非法篡改)
        """
        if cls.can_transition(order.state, target_state):
            order.state = target_state
            return True
        return False


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
        self.active_orders: Dict[str, Order] = {} # order_id -> Order

    def update_heartbeat(self, current_timestamp: float) -> None:
        """更新最近一次心跳时间戳"""
        self.last_heartbeat_timestamp = current_timestamp

    def check_heartbeat(self, current_timestamp: float) -> Tuple[bool, str]:
        """
        心跳检查
        """
        if (current_timestamp - self.last_heartbeat_timestamp) > self.heartbeat_timeout_sec:
            return False, "HEARTBEAT_TIMEOUT_DISCONNECTED"
        return True, "HEARTBEAT_OK"

    def check_pre_trade_risk(
        self,
        order: Order,
        portfolio: PortfolioState,
        is_st_stock: bool
    ) -> Tuple[bool, str]:
        """
        前置硬风控流水线审查 (Pre-Trade Risk Inspection)
        """
        # 1. 熔断开关
        if self.is_kill_switch_active:
            return False, "REJECT_KILL_SWITCH_ACTIVE"

        order_value = order.price * order.volume

        # 2. 乌龙指单笔限额
        if order_value > self.max_single_order_value:
            return False, "REJECT_FAT_FINGER_LIMIT"

        # 3. ST 股票
        if is_st_stock:
            return False, "REJECT_ST_PROHIBITED"

        # 4. 单日亏损熔断
        if portfolio.daily_pnl_pct <= self.daily_loss_limit:
            self.trigger_emergency_kill_switch()
            return False, "REJECT_DAILY_LOSS_CIRCUIT_BREAKER"

        # 5. 最大回撤熔断
        drawdown = (portfolio.total_equity - portfolio.peak_equity) / portfolio.peak_equity
        if drawdown <= self.max_drawdown_limit:
            self.trigger_emergency_kill_switch()
            return False, "REJECT_MAX_DRAWDOWN_CIRCUIT_BREAKER"

        # 6. 单票集中度 (仅针对 BUY)
        if order.direction == "BUY":
            cur_pos_val = portfolio.positions.get(order.symbol, 0.0)
            new_pos_val = cur_pos_val + order_value
            if (new_pos_val / portfolio.total_equity) > self.max_stock_concentration:
                return False, "REJECT_CONCENTRATION_LIMIT"

            # 7. 全账户杠杆率 (仅针对 BUY)
            total_pos_val = sum(portfolio.positions.values()) + order_value
            if (total_pos_val / portfolio.total_equity) > self.max_leverage:
                return False, "REJECT_LEVERAGE_LIMIT"

        return True, "APPROVED"

    def trigger_emergency_kill_switch(self) -> List[str]:
        """
        触发紧急自毁熔断 (Emergency Kill Switch)
        """
        self.is_kill_switch_active = True
        cancelled_orders: List[str] = []

        for oid, ord_obj in self.active_orders.items():
            if ord_obj.state not in {OrderState.FILLED, OrderState.CANCELLED, OrderState.REJECTED}:
                OrderStateMachine.transition(ord_obj, OrderState.CANCELLED)
                cancelled_orders.append(oid)

        return cancelled_orders


# ==============================================================================
# 自动化测试与参考答案解析
# ==============================================================================

if __name__ == "__main__":
    print("正在运行 10_system_infra / Lesson 04 参考实现断言验证...")

    # 测试 1: 订单 FSM 状态机
    fsm = OrderStateMachine
    order = Order("ORD_01", "600519.SH", "BUY", 1800.0, 100)
    assert order.state == OrderState.PENDING_SUBMIT

    ok1 = fsm.transition(order, OrderState.SUBMITTED)
    assert ok1 is True and order.state == OrderState.SUBMITTED

    ok2 = fsm.transition(order, OrderState.ACCEPTED)
    assert ok2 is True and order.state == OrderState.ACCEPTED

    ok3 = fsm.transition(order, OrderState.PARTIALLY_FILLED)
    assert ok3 is True and order.state == OrderState.PARTIALLY_FILLED

    ok4 = fsm.transition(order, OrderState.FILLED)
    assert ok4 is True and order.state == OrderState.FILLED

    bad1 = fsm.transition(order, OrderState.CANCELLED)
    assert bad1 is False
    assert order.state == OrderState.FILLED

    # 测试 2: 前置风控多层拦截
    gateway = RiskSentinelGateway(
        max_single_order_value=1_000_000.0,
        max_stock_concentration=0.20,
        max_leverage=1.0,
        daily_loss_limit=-0.03,
        max_drawdown_limit=-0.08,
        heartbeat_timeout_sec=3.0
    )

    portfolio = PortfolioState(
        total_equity=10_000_000.0,
        cash=4_000_000.0,
        peak_equity=10_000_000.0,
        positions={"600519.SH": 1_500_000.0, "000858.SZ": 500_000.0},
        daily_pnl_pct=0.01
    )

    ord_normal = Order("ORD_A", "600519.SH", "BUY", 1000.0, 500)
    pass_a, msg_a = gateway.check_pre_trade_risk(ord_normal, portfolio, is_st_stock=False)
    assert pass_a is True and msg_a == "APPROVED"

    ord_fat = Order("ORD_B", "600519.SH", "BUY", 1000.0, 2000)
    pass_b, msg_b = gateway.check_pre_trade_risk(ord_fat, portfolio, is_st_stock=False)
    assert pass_b is False and "FAT_FINGER" in msg_b

    ord_st = Order("ORD_C", "*ST000001", "BUY", 10.0, 1000)
    pass_c, msg_c = gateway.check_pre_trade_risk(ord_st, portfolio, is_st_stock=True)
    assert pass_c is False and "ST_PROHIBITED" in msg_c

    ord_conc = Order("ORD_D", "600519.SH", "BUY", 1000.0, 600)
    pass_d, msg_d = gateway.check_pre_trade_risk(ord_conc, portfolio, is_st_stock=False)
    assert pass_d is False and "CONCENTRATION" in msg_d

    portfolio_high_lev = PortfolioState(
        total_equity=10_000_000.0,
        cash=500_000.0,
        peak_equity=10_000_000.0,
        positions={"600519.SH": 1_500_000.0, "000858.SZ": 1_500_000.0, "601318.SH": 1_500_000.0,
                   "000333.SZ": 1_500_000.0, "600036.SH": 1_500_000.0, "002594.SZ": 2_000_000.0},
        daily_pnl_pct=0.01
    )
    ord_lev = Order("ORD_E", "300750.SZ", "BUY", 800.0, 1000)
    pass_lev, msg_lev = gateway.check_pre_trade_risk(ord_lev, portfolio_high_lev, is_st_stock=False)
    assert pass_lev is False and "LEVERAGE" in msg_lev

    # 测试 3: 心跳保活
    gateway.update_heartbeat(current_timestamp=100.0)
    hb_ok, _ = gateway.check_heartbeat(current_timestamp=102.5)
    assert hb_ok is True

    hb_fail, hb_msg = gateway.check_heartbeat(current_timestamp=104.0)
    assert hb_fail is False and "TIMEOUT" in hb_msg

    # 测试 4: 回撤熔断与 Kill Switch
    active_ord1 = Order("ACT_01", "600519.SH", "BUY", 1800.0, 100, state=OrderState.ACCEPTED)
    active_ord2 = Order("ACT_02", "000858.SZ", "BUY", 150.0, 1000, state=OrderState.PARTIALLY_FILLED)
    gateway.active_orders["ACT_01"] = active_ord1
    gateway.active_orders["ACT_02"] = active_ord2

    crashed_portfolio = PortfolioState(
        total_equity=9_100_000.0,
        cash=2_000_000.0,
        peak_equity=10_000_000.0,
        positions={},
        daily_pnl_pct=-0.04
    )

    test_ord = Order("ORD_NEW", "600519.SH", "BUY", 1000.0, 100)
    pass_crash, crash_msg = gateway.check_pre_trade_risk(test_ord, crashed_portfolio, is_st_stock=False)
    assert pass_crash is False
    assert "CIRCUIT_BREAKER" in crash_msg
    assert gateway.is_kill_switch_active is True

    assert active_ord1.state == OrderState.CANCELLED
    assert active_ord2.state == OrderState.CANCELLED

    pass_locked, lock_msg = gateway.check_pre_trade_risk(test_ord, portfolio, is_st_stock=False)
    assert pass_locked is False and "KILL_SWITCH_ACTIVE" in lock_msg

    print("Lesson 04 参考实现全部断言通过 (Exit Code 0)！\n")

    print("=" * 80)
    print("【思考题标准答案深度解析 (Q1 ~ Q3)】")
    print("=" * 80)
    print("Q1 解析:")
    print("  (1) 光大证券乌龙指核心缺陷：")
    print("      策略系统代码中存在重试死循环逻辑漏洞（当买入订单回报超时未达时，代码判定下单失败并不断重复重发买单）；")
    print("      更致命的是，该机构内部为了追求超低延迟，绕过了柜台集中硬风控检查，且交易网关没有设置'单日累计报单总金额硬顶'和")
    print("      '高频连击报单熔断器'，导致 2 分钟内错误发单数百亿元并瞬间透支数十亿资本金。")
    print("  (2) 现代防范架构：")
    print("      ① 独立前置物理硬件风控 (Pre-Trade FPGA/Kernel Bypass Sentinel)：无论策略模型如何编写，所有报单进入券商/交易所柜台前，")
    print("         必须经由独立的风控节点进行配额递减核算，风控网关具备一票否决权且由风控部门独立运维，策略研发无权修改。")
    print("      ② 漏桶/令牌桶频控与总额度硬熔断 (Token Bucket Rate Limiting & Gross Notional Cap)：设置每秒报单笔数上限（如 200 笔/秒）")
    print("         与全账户单日总买入上限，一旦累计报单量达到阈值，硬件电路或网关层立即强行关闭 Socket 连接并锁定账户。")
    print("-" * 80)
    print("Q2 解析:")
    print("  (1) 撤单与完全成交的竞态冲突 (Race Condition)：")
    print("      在交易所撮合内核中，若在收到撤单指令前 0.1 毫秒，该订单恰好已被对手方大单吃掉撮合成交，交易所会首先生成成交回报（FILLED），")
    print("      随后处理撤单请求时判定该订单已不存在，返回撤单被拒回报（CANCEL_REJECTED）。")
    print("  (2) 状态机的确定性仲裁规则：")
    print("      ① 状态机必须遵循'终态不可逆'原则：一旦订单收到 FILLED 并转入 FILLED 状态，任何后续迟到的 CANCELLED 或 CANCEL_REJECTED")
    print("         回报均不得改变该订单的终态。")
    print("      ② 资金账本对账与幂等处理：以交易所成交回报中的实际成交价格和股数扣减账户可用现金并登记持仓，避免因撤单回报误入导致")
    print("         '幽灵解冻资金'引发的账户透支灾难。")
    print("-" * 80)
    print("Q3 解析:")
    print("  (1) 策略层'软风控'的脆弱性：")
    print("      将风控代码写在策略 Python/C++ 业务逻辑内部（如 `if my_loss > 0.05: return`），容易因为策略代码本身的运行时异常")
    print("      （如空指针、除零、死循环、多线程死锁、异常被未捕获的 try-except 吞掉）而被彻底穿透失效。")
    print("  (2) 网关层'独立前置硬风控'的必要性：")
    print("      遵循金融信息系统工程的'职责隔离与零信任架构'。网关层只关注合规契约（报单合法性、资金足额性、杠杆集中度、心跳健康度），")
    print("      它不依赖策略代码的正确性。即使策略逻辑完全失控疯跑（Rogue Algorithm），独立网关也能像坚固的保险丝一样在 1 毫秒内")
    print("      物理切断链路并保护整个机构的资产安全。")
    print("=" * 80)
