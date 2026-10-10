r"""
# 模块 07：行为金融学、交易心理与执行纪律 · 第 2 课：交易执行清单机制与自律状态机

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握阿图·葛文德《清单革命》在交易室执行中的工程化落地（Pre-Flight Checklist）；
2. 深刻理解“止损不可变原则（Inviolable Stop-Loss Rule）”与报复性交易（Revenge Trading）的破坏力；
3. 设计并实现交易风控守门员（Risk Guardian）有限状态机（FSM），对连续亏损进行冷静期强制锁定（Cooldown Lockout）；
4. 运用面向对象与状态模式，实现单笔硬止损强平、最大日内亏损熔断（Daily Loss Circuit Breaker）等铁律约束。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，阐述神经生物学层面的“情绪倾侧（Tilt）”与状态机防御逻辑。

---
## 核心心智模型与状态机拓扑

### 1. 为什么“意志力”是不可靠的？

在极端市场行情下，人类大脑会分泌大量的去甲肾上腺素与皮质醇：
- **倾侧现象（Tilt）**：连续遭遇亏损或意外被止损后，交易者大脑的前额叶皮层（负责理性规划、概率权衡）被杏仁核（负责恐惧、战斗或逃跑）劫持。
- **报复性交易（Revenge Trading）**：此时交易者产生强烈的“不甘心”，企图通过加大仓位、撤销止损、甚至立刻反手开仓来“立刻回本”，导致亏损在数小时内呈指数级放大。
- **清单革命与状态机防线**：职业对冲基金绝不依赖交易员的意志力，而是将交易决策抽象为一个带有刚性约束的状态机（State Machine）。任何订单必须通过清单验证，一旦触及风控红线，系统强制收回交易权限。

### 2. 操盘手自律风控状态机架构 (Finite State Machine)

```
             ┌─────────────────────────┐
             │       系统初始化        │
             └────────────┬────────────┘
                          │
                          ▼
                  ┌───────────────┐
      ┌───────────┤     READY     │◄────────────┐
      │           │ (允许合规开仓) │             │
      │           └───────┬───────┘             │
      │清单违规/超风险     │通过清单 & 风险检查    │ 冷静期倒计时归零
      │(直接拒绝开仓)     ▼                     │ (自动解除锁定)
      │           ┌───────────────┐             │
      └──────────►│  IN_POSITION  │             │
                  │ (持有并监控)  │             │
                  └───────┬───────┘             │
                          │平仓或触及止损       │
                          ▼                     │
                 [ 检查风控触发条件 ]           │
                 /                \             │
  连续亏损 >= 阈值                 日内累计亏损 >= 熔断阈值
       /                            \
      ▼                              ▼
┌───────────────┐              ┌───────────────┐
│   COOLDOWN    │              │    HALTED     │
│ (强制冷静锁定)│              │ (日内彻底熔断)│
└───────┬───────┘              └───────────────┘
        │
        └──────每单位时间 tick_cooldown() 减 1 ──┘
```
"""

from typing import Dict, Any, Tuple, Optional


class TradingStateGuardian:
    """
    操盘手交易自律风控守门员状态机。
    """

    def __init__(
        self,
        initial_capital: float = 100000.0,
        max_consecutive_losses: int = 2,
        cooldown_ticks: int = 3,
        max_loss_pct_per_trade: float = 0.02,
        daily_max_loss_pct: float = 0.05
    ):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.state = "READY"  # READY, IN_POSITION, COOLDOWN, HALTED
        self.consecutive_losses = 0
        self.max_consecutive_losses = max_consecutive_losses
        self.cooldown_ticks = cooldown_ticks
        self.cooldown_remaining = 0
        self.max_loss_pct_per_trade = max_loss_pct_per_trade
        self.daily_max_loss_pct = daily_max_loss_pct
        self.daily_realized_loss = 0.0
        self.active_position: Optional[Dict[str, Any]] = None

    def validate_pre_flight_checklist(self, checklist: Dict[str, Any]) -> Tuple[bool, str]:
        """
        飞行前执行清单严格检验：
        1. setup_valid == True (交易逻辑与信号确认)
        2. reward_risk_ratio >= 2.0 (盈亏比不低于 2:1)
        3. emotional_temperature <= 3 (情绪打分 1~5，超过 3 严禁开仓)
        """
        # TODO: 校验以上三项规则，全部通过返回 (True, "CHECKLIST_PASSED")，否则返回 (False, "REJECTED: ...")
        pass

    def request_order(self, order: Dict[str, Any], checklist: Dict[str, Any]) -> Tuple[bool, str]:
        """
        开仓请求审核：
        1. 状态必须为 READY
        2. 清单必须无条件通过
        3. 订单必须自带止损价，且单笔最大风险敞口不得超过账户资金的 max_loss_pct_per_trade
        """
        # TODO:
        # - 校验当前状态（HALTED/COOLDOWN/IN_POSITION 均应拒绝开仓）
        # - 校验清单
        # - 校验止损价与方向合法性 (多头止损需低于入场价，空头止损需高于入场价)
        # - 校验总风险金额 = abs(entry_price - stop_loss) * size <= current_capital * max_loss_pct_per_trade
        # - 审核通过后，更新 state 为 "IN_POSITION"，记录 self.active_position，返回 (True, "ORDER_FILLED")
        pass

    def check_market_price_and_enforce_stops(self, current_price: float) -> Tuple[bool, Optional[str]]:
        """
        动态行情监控与硬止损强制执行：
        多头：current_price <= stop_loss 触发强平
        空头：current_price >= stop_loss 触发强平
        若触发止损，立刻以 stop_loss 价格强制平仓并推进状态机。
        """
        # TODO:
        # - 检查 active_position 是否存在且处于 IN_POSITION
        # - 判断是否跌破/突破 stop_loss
        # - 若触发，调用 self.close_position(exit_price=pos["stop_loss"], reason="HARD_STOP_LOSS")
        # - 返回 (True, f"STOP_TRIGGERED: State -> {new_state}") 或 (False, None)
        pass

    def close_position(self, exit_price: float, reason: str = "NORMAL") -> Tuple[float, str]:
        """
        平仓结算与状态跃迁：
        计算盈亏，更新资金池、连亏计数器与日内亏损池。
        判断是否触发日内硬熔断 (HALTED) 或连续亏损冷静期 (COOLDOWN)。
        """
        # TODO:
        # - 计算 pnl 并累加到 self.current_capital
        # - 清空 self.active_position
        # - 若 pnl < 0，consecutive_losses += 1，累加 daily_realized_loss；若 pnl >= 0，consecutive_losses 归零
        # - 状态跃迁判断优先级 1：daily_realized_loss >= initial_capital * daily_max_loss_pct -> state = "HALTED"
        # - 状态跃迁判断优先级 2：consecutive_losses >= max_consecutive_losses -> state = "COOLDOWN", cooldown_remaining = cooldown_ticks
        # - 否则 state = "READY"
        # - 返回 (round(pnl, 2), self.state)
        pass

    def tick_cooldown(self) -> None:
        """
        推进冷静期时钟：
        倒计时归零时，自动复位连亏计数器，并将状态重新置为 READY。
        """
        # TODO:
        # - 若处于 COOLDOWN，cooldown_remaining 减 1
        # - 若 cooldown_remaining <= 0，重置 consecutive_losses = 0，state = "READY"
        pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么在职业交易规范中，“止损位只能向盈利方向移动（追踪止损），绝不允许向亏损方向扩大（向下移动止损）”被奉为第一铁律？从破产概率（Risk of Ruin）角度推导其因果。

**你的答案：**
[在此处写下你的分析：需阐述期望破产概率的非线性爆炸、亏损分布肥尾化，以及挪动止损背后的认知失谐机制]


### Q2：在交易状态机中，为何必须区分“连亏冷静期（COOLDOWN）”与“日内彻底熔断（HALTED）”两个不同层级的状态？

**你的答案：**
[在此处写下你的分析：需对比战术波动（方差噪声引发的情绪冲动）与战略崩溃（市场结构突变/模型失效）的本质差异]


### Q3：为什么将“情绪温度打分（Emotional Temperature <= 3）”强制置于订单准入清单中？这种主观打分在实际量化与程序化执行中如何客观化？

**你的答案：**
[在此处写下你的分析：需从元认知制动机制出发，并给出量化系统中的客观代理指标（如点击频率、仓位离散度、撤单率等）]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] TradingStateGuardian Initialization...")
    guardian = TradingStateGuardian(
        initial_capital=100000.0,
        max_consecutive_losses=2,
        cooldown_ticks=2,
        max_loss_pct_per_trade=0.02, # 单笔风险上限 2% ($2,000)
        daily_max_loss_pct=0.05      # 日内硬熔断 5% ($5,000)
    )
    assert guardian.state == "READY"
    assert guardian.current_capital == 100000.0

    print("[Testing] Pre-flight Checklist Validation...")
    bad_checklist_emotion = {
        "setup_valid": True,
        "reward_risk_ratio": 2.5,
        "emotional_temperature": 4
    }
    passed, msg = guardian.validate_pre_flight_checklist(bad_checklist_emotion)
    assert not passed and "Emotional temperature" in msg

    bad_checklist_rr = {
        "setup_valid": True,
        "reward_risk_ratio": 1.5,
        "emotional_temperature": 2
    }
    passed, msg = guardian.validate_pre_flight_checklist(bad_checklist_rr)
    assert not passed and "Reward-to-risk" in msg

    good_checklist = {
        "setup_valid": True,
        "reward_risk_ratio": 3.0,
        "emotional_temperature": 2
    }
    passed, msg = guardian.validate_pre_flight_checklist(good_checklist)
    assert passed and msg == "CHECKLIST_PASSED"

    print("[Testing] Order Risk Budget Enforcement...")
    excessive_risk_order = {
        "symbol": "AAPL",
        "side": "BUY",
        "entry_price": 100.0,
        "stop_loss": 90.0,
        "size": 500
    }
    accepted, msg = guardian.request_order(excessive_risk_order, good_checklist)
    assert not accepted and "exceeds budget" in msg

    print("[Testing] Valid Order Entry & Position Tracking...")
    valid_order = {
        "symbol": "AAPL",
        "side": "BUY",
        "entry_price": 100.0,
        "stop_loss": 90.0,
        "take_profit": 130.0,
        "size": 100
    }
    accepted, msg = guardian.request_order(valid_order, good_checklist)
    assert accepted and msg == "ORDER_FILLED"
    assert guardian.state == "IN_POSITION"

    repeat_order, rep_msg = guardian.request_order(valid_order, good_checklist)
    assert not repeat_order and "Already in position" in rep_msg

    print("[Testing] Hard Stop-Loss Trigger...")
    stop_hit, _ = guardian.check_market_price_and_enforce_stops(92.0)
    assert not stop_hit
    assert guardian.state == "IN_POSITION"

    stop_hit, stop_msg = guardian.check_market_price_and_enforce_stops(89.0)
    assert stop_hit
    assert guardian.state == "READY"
    assert guardian.current_capital == 99000.0
    assert guardian.consecutive_losses == 1
    assert guardian.daily_realized_loss == 1000.0

    print("[Testing] Consecutive Losses & Cooldown Lockout...")
    accepted, _ = guardian.request_order(valid_order, good_checklist)
    assert accepted
    pnl, state = guardian.close_position(exit_price=90.0, reason="MANUAL_STOP")
    assert pnl == -1000.0
    assert state == "COOLDOWN"
    assert guardian.state == "COOLDOWN"
    assert guardian.cooldown_remaining == 2
    assert guardian.consecutive_losses == 2

    cooldown_blocked, cd_msg = guardian.request_order(valid_order, good_checklist)
    assert not cooldown_blocked and "COOLDOWN" in cd_msg

    guardian.tick_cooldown()
    assert guardian.cooldown_remaining == 1
    assert guardian.state == "COOLDOWN"

    guardian.tick_cooldown()
    assert guardian.cooldown_remaining == 0
    assert guardian.consecutive_losses == 0
    assert guardian.state == "READY"

    print("[Testing] Daily Max Loss Circuit Breaker (HALTED)...")
    order3 = {"symbol": "AAPL", "side": "BUY", "entry_price": 100.0, "stop_loss": 85.0, "size": 100}
    guardian.request_order(order3, good_checklist)
    guardian.close_position(exit_price=85.0)

    guardian.tick_cooldown()
    guardian.tick_cooldown()
    assert guardian.state == "READY"

    order4 = {"symbol": "AAPL", "side": "BUY", "entry_price": 100.0, "stop_loss": 85.0, "size": 100}
    guardian.request_order(order4, good_checklist)
    pnl4, state4 = guardian.close_position(exit_price=85.0)
    assert guardian.daily_realized_loss >= 5000.0
    assert state4 == "HALTED"
    assert guardian.state == "HALTED"

    blocked_halt, halt_msg = guardian.request_order(order4, good_checklist)
    assert not blocked_halt and "HALTED" in halt_msg

    print("All assertions passed! Module 07 Lesson 02 verification successful.")
