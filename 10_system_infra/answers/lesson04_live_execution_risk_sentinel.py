r"""
================================================================================
模块 10：量化回测避坑指南与实盘系统工程 · 第 4/4 课
第 4 课：实盘交易架构：订单有限状态机、网络心跳与风控熔断哨兵 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：实盘工程的核心不是收益计算，而是分布式故障防线与硬熔断
量化交易从离线投研走向实盘生产的最惊险跃迁，是从确定性离线矩阵计算切入非确定性分布式网络博弈。在实盘环境中，交易所网关超时、光缆抖动断流、回报乱序竞争、策略死循环及乌龙指等灾难在统计学上必然发生。军规级量化交易系统绝不把风控寄托于策略研发代码的自觉，而是在策略客户端与交易所撮合引擎之间筑牢两道不可逾越的物理城墙：严格遵循吸收态的订单全生命周期有限状态机（FSM），与独立部署的前置多维硬风控熔断哨兵网关（Pre-Trade Risk Sentinel）。
:::

- **[订单状态机的吸收态终态原则]**：订单生命周期满足严格单向转移图，`FILLED`、`CANCELLED`、`REJECTED` 为马尔可夫吸收终态。一旦确立终态，系统在硬件与内存级别彻底冻结该订单状态，任何迟到或乱序的网络回报均不得改变终态。
- **[前置硬风控与软风控的物理隔离]**：严禁在策略逻辑内部通过 `if-else` 实现风控（软风控极易因除零、死循环或未捕获异常而被击穿）。风控哨兵必须作为独立网关进程运行在交易核心入口，拥有单笔额度、标的白名单、杠杆集中度与动态回撤的一票否决权。
- **[网络心跳与断线自动撤单（COD）]**：网关维持每秒心跳同步。一旦心跳丢失超过 3.0 秒，触发 Cancel-On-Disconnect (COD) 协议，自动向交易所广播撤回全部在途挂单，防范无主飞车盘。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了订单生命周期有限状态机（Order FSM）的合法跃迁因果图与竞态仲裁机制。

```mermaid
flowchart TD
    Init["PENDING_SUBMIT (待报单)"] --> Sub["SUBMITTED (已报送柜台)"]
    Sub --> Acc["ACCEPTED (交易所受理解挂)"]
    Acc --> Part["PARTIALLY_FILLED (部分撮合成交)"]
    Part --> Fill["FILLED (完全成交 ➔ ★终态)"]
    Acc --> Fill
    Init --> Rej["REJECTED (风控/交易所拒单 ➔ ★终态)"]
    Sub --> Rej
    Acc --> Can["CANCELLED (成功撤销 ➔ ★终态)"]
    Part --> Can
```

- **[要点 1：因果律状态单向流转]**：严禁从未提交状态直接跳跃至成交状态，严禁已完全成交订单退回至撤单状态。
- **[要点 2：成交与撤单在途的竞态仲裁]**：若撤单请求发出时交易所已成交，系统以交易所成交回报时间戳为最高权威判据，将迟到的撤单确认置为被拒，彻底消除幽灵持仓。
- **[要点 3：内存状态原子化更新]**：状态机采用互斥锁与内存 CAS 原子操作，杜绝多线程或分布式异步并发产生的不一致账本。

锚点指引：下图展示了前置风控哨兵网关的四层阶梯式硬拦截与紧急自毁 Kill-Switch 架构。

```mermaid
flowchart LR
    Order["策略发起下单指令"] --> L1{"层级 1: 乌龙指与单笔上限 (<=100万) ?"}
    L1 -->|超限| R1["拦截: SINGLE_ORDER_LIMIT_EXCEEDED"]
    L1 -->|通过| L2{"层级 2: 标的池白名单 (非ST/非停牌) ?"}
    L2 -->|违规| R2["拦截: ILLEGAL_SYMBOL_ST_OR_SUSPENDED"]
    L2 -->|通过| L3{"层级 3: 敞口与集中度 (单票<=20% 杠杆<=1.0x) ?"}
    L3 -->|超限| R3["拦截: LEVERAGE_OR_CONCENTRATION_EXCEEDED"]
    L3 -->|通过| L4{"层级 4: 回撤熔断 (日亏<=-3% 回撤<=-8%) ?"}
    L4 -->|触限| R4["激活 Kill-Switch: 自动批量撤销全市场在途单 ➔ 关机"]
    L4 -->|安全| Pass["✔ 放行订单进入交易所撮合"]
```

- **[要点 1：乌龙指第一道防线]**：单笔报单金额设置绝对物理天花板（如 100 万元），从底层彻底封死手误敲错两个零引发百亿灾难的通道。
- **[要点 2：单票持仓集中度硬卡口]**：单票市值占总资产比重严格限制在 20% 以内，防止策略因特质黑天鹅连环跌停引发整个基金清盘。
- **[要点 3：全自动自毁熔断器（Kill Switch）]**：当触发日内亏损或回撤警戒线，网关不仅拒绝新开仓，更在毫秒内批量广播撤回所有已挂单委托，防止已挂买单继续被动成交放大众人亏损。

【数学与估值模型】
前置风控约束矩阵方程：
$$
\text{OrderValue} = P_{\text{order}} \times Q_{\text{order}} \le \text{MaxSingleOrderValue}
$$
$$
\text{Concentration}_i = \frac{\text{PositionValue}_i + \text{OrderValue}_i}{\text{TotalEquity}} \le \gamma_{\text{stock}} \quad (\gamma_{\text{stock}} = 0.20)
$$
$$
\text{GrossLeverage} = \frac{\sum_j \text{PositionValue}_j + \text{OrderValue}}{\text{TotalEquity}} \le \text{MaxLeverage} \quad (\text{MaxLeverage} = 1.0)
$$
动态回撤与亏损熔断判定：
$$
\text{Drawdown}_t = \frac{\text{TotalEquity}_t - \text{PeakEquity}}{\text{PeakEquity}} \le \text{DD}_{\text{limit}} \implies \text{KillSwitch} \leftarrow \text{True}
$$
$$
\text{DailyPnL}_t \le \text{DailyLossLimit} \implies \text{KillSwitch} \leftarrow \text{True}
$$
变量定义域与参数约束：
- $\text{TotalEquity} > 0$；$\text{PeakEquity} \ge \text{TotalEquity}$；
- $\text{DailyLossLimit} = -0.03$（$-3\%$）；$\text{DD}_{\text{limit}} = -0.08$（$-8\%$）；
- $\Delta t_{\text{heartbeat}} \le 3.0 \text{ s}$。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **策略内软风控被异常绕过**：2013 年光大证券“816 乌龙指”由于策略系统内部逻辑死循环不断重发错误买单，且柜台风控被设为直通模式，2 分钟内错误发单 234 亿元。
2. **断线在途单成为无主幽灵**：策略机房断电或网络中断若无 COD（Cancel-on-Disconnect）保护，已挂在交易所的限价买单将被对手盘恶意扫货成交，交易员在失联中被动加满高杠杆。
3. **撤单未确认即重复发单**：网络拥塞时连续发送多笔撤单并再次开仓，极易引发资金双重占用甚至穿仓透支。
:::

【思考题】
Q1: 2013 年著名的“光大证券 816 乌龙指事件”（累计错误报单 234 亿元，成交 72.7 亿元）在系统架构与风控网关设计上暴露出哪些致命缺陷？如果在现代量化网关中，如何从“物理隔离前置硬风控”与“总额度熔断器”设计上彻底杜绝此类灾难？
Q2: 在异步分布式微服务交易架构中，如果策略发送了撤单请求（Cancel Request），但由于网络抖动，撤单回报（Cancelled）与交易所的完全成交回报（Filled）在极微小的时差内同时或乱序到达，订单状态机该如何处理这种竞态条件（Race Condition）以避免账本资金状态错乱？
Q3: 为什么实盘量化交易系统严禁使用“软风控（即在策略模型代码内部用 if-else 判定）”，而必须在独立的订单网关层（Execution Gateway）部署强隔离的“前置硬风控哨兵（Pre-Trade Hard Sentinel）”？

【Q1 深度参考答案】
- **[系统架构与风控绕过的致命缺陷剖析]**：光大证券策略系统在订单重试机制上存在严重代码缺陷（订单超时未回报即死循环重复重发买单）；更致命的是，为了追求极低网络延迟，机构内部将核心交易通道设为了“绕过柜台检查的直通模式”，交易网关完全缺乏单笔金额上限与全日累计报单总额度的刚性熔断阀门，导致在短短两分钟内错误报单吞噬数十亿可用资本。
- **[现代前置硬件隔离风控方案（Pre-Trade FPGA Sentinel）]**：在策略服务器与交易所柜台的光纤链路之间部署独立的硬件级或无旁路风控哨兵网关。风控网关由风控合规团队独立配置与运维，策略代码在逻辑上完全不可穿透或覆写网关规则，拥有不可逾越的一票否决权。
- **[令牌桶频控与全日额度硬熔断（Token Bucket & Gross Notional Cap）]**：网关内置高频令牌桶，单秒报单笔数超过阈值（如 200 笔/秒）立即强行截断连接；同时设定全账户单日总名义买入额度硬顶，一旦触及，硬件直接断开网口并锁死交易席位。

【Q2 深度参考答案】
- **[撮合引擎竞态仲裁机制]**：在微秒级高频博弈中，若撤单请求到达撮合主机前 0.1 毫秒该挂单已被对手盘市价单吃掉，交易所内核会先生成成交回报（FILLED），随后处理撤单时判定该单已无剩余可撤股份，返回撤单被拒回报（CANCEL_REJECTED）。
- **[吸收终态锁定与幂等性保障]**：订单有限状态机（Order FSM）必须严格遵循“终态不可篡改原则”：一旦订单收到成交回报并跃迁进入 `FILLED`，该订单在内存数据库中的状态永久锁死为终态。任何随后延迟到达的 `CANCELLED` 或 `CANCEL_REJECTED` 回报均作为幂等过时事件忽略。
- **[账本资金流水按实际成交对账]**：清算账本严格以交易所官方撮合时间戳与成交回报中的实际成交价格和股数扣减保证金并登记持仓，彻底规避因撤单确认错序导致“幽灵解冻资金”进而引发透支穿仓的灾难。

【Q3 深度参考答案】
- **[策略代码软风控的脆弱性与单点失效]**：将风控规则写在策略 Python/C++ 业务逻辑内部（如 `if loss > 0.05: return`），极易因为策略代码自身的运行时异常（空指针解引用、数组越界、数值除零、死锁挂起或未捕获的全局异常处理）而被直接击穿或绕过。
- **[零信任架构与职责完全解耦]**：现代量化系统遵循金融工程“零信任原则”。前置风控哨兵网关对策略代码的内部正确性持完全怀疑态度。网关层只核验合规物理契约（资金足额性、价格偏差度、标的合规性、持仓集中度、心跳存活性）。
- **[失控算法的坚固物理保险丝]**：即使策略模型因超参数过拟合、死循环或逻辑混乱成为发单失控算法（Rogue Algorithm），独立前置风控网关也能像坚固的工业级空气开关一样在毫秒级内硬性掐断数据流并向全市场撤单，保全机构全部净资产安全。
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
        """心跳检查"""
        if (current_timestamp - self.last_heartbeat_timestamp) > self.heartbeat_timeout_sec:
            return False, "HEARTBEAT_TIMEOUT_DISCONNECTED"
        return True, "HEARTBEAT_OK"

    def trigger_emergency_kill_switch(self) -> List[str]:
        """触发紧急自毁熔断 (Emergency Kill Switch)"""
        self.is_kill_switch_active = True
        cancelled_orders: List[str] = []

        for oid, ord_obj in self.active_orders.items():
            if ord_obj.state not in {OrderState.FILLED, OrderState.CANCELLED, OrderState.REJECTED}:
                OrderStateMachine.transition(ord_obj, OrderState.CANCELLED)
                cancelled_orders.append(oid)

        return cancelled_orders

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
