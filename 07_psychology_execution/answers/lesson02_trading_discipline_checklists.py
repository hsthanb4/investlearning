r"""
# 模块 07：行为金融学、交易心理与执行纪律 · 第 2 课：交易执行清单机制与自律状态机

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

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
    
    状态空间：
    - READY: 准备就绪，允许提交合规订单
    - IN_POSITION: 持仓监控中，严禁重复开仓
    - COOLDOWN: 处于连亏冷静期，冻结所有新开仓指令
    - HALTED: 触及日内硬熔断，当日彻底终止交易
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
        self.state = "READY"
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
        if not checklist.get("setup_valid", False):
            return False, "REJECTED: Trading setup is invalid"
        if checklist.get("reward_risk_ratio", 0.0) < 2.0:
            return False, "REJECTED: Reward-to-risk ratio is below 2.0"
        if checklist.get("emotional_temperature", 5) > 3:
            return False, "REJECTED: Emotional temperature is too high (>3)"
        return True, "CHECKLIST_PASSED"

    def request_order(self, order: Dict[str, Any], checklist: Dict[str, Any]) -> Tuple[bool, str]:
        """
        开仓请求审核：
        1. 状态必须为 READY
        2. 清单必须无条件通过
        3. 订单必须自带止损价，且单笔最大风险敞口不得超过账户资金的 max_loss_pct_per_trade
        """
        if self.state == "HALTED":
            return False, "BLOCKED: System is HALTED for the day"
        if self.state == "COOLDOWN":
            return False, f"BLOCKED: System in COOLDOWN, {self.cooldown_remaining} ticks remaining"
        if self.state == "IN_POSITION":
            return False, "BLOCKED: Already in position"

        valid, msg = self.validate_pre_flight_checklist(checklist)
        if not valid:
            return False, msg

        entry_price = order.get("entry_price", 0.0)
        stop_loss = order.get("stop_loss", 0.0)
        size = order.get("size", 0.0)
        side = order.get("side", "BUY")

        if stop_loss <= 0.0:
            return False, "REJECTED: Stop loss must be explicitly defined"
        if side == "BUY" and stop_loss >= entry_price:
            return False, "REJECTED: Long order stop loss must be below entry price"
        if side == "SELL" and stop_loss <= entry_price:
            return False, "REJECTED: Short order stop loss must be above entry price"

        risk_per_share = abs(entry_price - stop_loss)
        total_risk_amount = risk_per_share * size
        max_allowed_risk = self.current_capital * self.max_loss_pct_per_trade

        if total_risk_amount > max_allowed_risk + 1e-6:
            return False, f"REJECTED: Trade risk ${total_risk_amount:.2f} exceeds budget ${max_allowed_risk:.2f}"

        self.state = "IN_POSITION"
        self.active_position = {
            "symbol": order["symbol"],
            "side": side,
            "size": size,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": order.get("take_profit", 0.0)
        }
        return True, "ORDER_FILLED"

    def check_market_price_and_enforce_stops(self, current_price: float) -> Tuple[bool, Optional[str]]:
        """
        动态行情监控与硬止损强制执行：
        多头：current_price <= stop_loss 触发强平
        空头：current_price >= stop_loss 触发强平
        若触发止损，立刻以 stop_loss 价格强制平仓并推进状态机。
        """
        if self.state != "IN_POSITION" or not self.active_position:
            return False, None

        pos = self.active_position
        triggered = False
        if pos["side"] == "BUY" and current_price <= pos["stop_loss"]:
            triggered = True
        elif pos["side"] == "SELL" and current_price >= pos["stop_loss"]:
            triggered = True

        if triggered:
            _, new_state = self.close_position(exit_price=pos["stop_loss"], reason="HARD_STOP_LOSS")
            return True, f"STOP_TRIGGERED: State -> {new_state}"

        return False, None

    def close_position(self, exit_price: float, reason: str = "NORMAL") -> Tuple[float, str]:
        """
        平仓结算与状态跃迁：
        计算盈亏，更新资金池、连亏计数器与日内亏损池。
        判断是否触发日内硬熔断 (HALTED) 或连续亏损冷静期 (COOLDOWN)。
        """
        if self.state != "IN_POSITION" or not self.active_position:
            return 0.0, self.state

        pos = self.active_position
        if pos["side"] == "BUY":
            pnl = (exit_price - pos["entry_price"]) * pos["size"]
        else:
            pnl = (pos["entry_price"] - exit_price) * pos["size"]

        self.current_capital += pnl
        self.active_position = None

        if pnl < 0:
            self.consecutive_losses += 1
            self.daily_realized_loss += abs(pnl)
        else:
            self.consecutive_losses = 0

        if self.daily_realized_loss >= (self.initial_capital * self.daily_max_loss_pct - 1e-6):
            self.state = "HALTED"
            return round(pnl, 2), "HALTED"

        if self.consecutive_losses >= self.max_consecutive_losses:
            self.state = "COOLDOWN"
            self.cooldown_remaining = self.cooldown_ticks
            return round(pnl, 2), "COOLDOWN"

        self.state = "READY"
        return round(pnl, 2), "READY"

    def tick_cooldown(self) -> None:
        """
        推进冷静期时钟：
        倒计时归零时，自动复位连亏计数器，并将状态重新置为 READY。
        """
        if self.state == "COOLDOWN":
            self.cooldown_remaining -= 1
            if self.cooldown_remaining <= 0:
                self.cooldown_remaining = 0
                self.consecutive_losses = 0
                self.state = "READY"


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么在职业交易规范中，“止损位只能向盈利方向移动（追踪止损），绝不允许向亏损方向扩大（向下移动止损）”被奉为第一铁律？从破产概率（Risk of Ruin）角度推导其因果。

参考答案：
1. 期望破产概率的非线性爆炸：
   数学上，资本回撤与恢复所需的涨幅是非线性的（亏损 10% 需涨 11.1%，亏损 50% 需涨 100%，亏损 90% 需涨 900%）。
   一旦交易员允许“向下移动止损”，单笔亏损的期望损失就从一个“有界的固定小常数”（如本金的 1%~2%）退化为一个“无界且期望为负的肥尾随机变量”。
   多次放宽止损等价于在吸收壁（吸附破产态）附近进行无限制的负期望马尔可夫游走，破产概率（Risk of Ruin）将趋近于 100%。
2. 认知失谐与行为瘫痪：
   心理学层面，第一次挪动止损是因为“不想面对既定亏损”；当价格进一步下跌到达新止损位时，痛苦程度成倍增加，交易员大脑会产生更强烈的逃避动机，
   进而第二次、第三次挪动止损，直到爆仓或被迫斩仓在最低点。

### Q2：在交易状态机中，为何必须区分“连亏冷静期（COOLDOWN）”与“日内彻底熔断（HALTED）”两个不同层级的状态？

参考答案：
1. 风险源的属性差异（战术失灵 vs 战略崩溃）：
   - 连续亏损（例如连亏 2~3 笔）在统计学上是正期望交易系统的正常泊松波动（方差噪声），但它会对交易员的生理内分泌产生剧烈扰动（引发短期躁动或报复冲动）。
     设置 `COOLDOWN` 锁定数个周期（如 3 根 K 线或 30 分钟），核心目的是切断多巴胺与肾上腺素的短期情绪循环，让前额叶皮层重新夺回认知主导权，待情绪平复后继续捕获市场机会。
   - 日内硬熔断（如单日亏损触及本金 5%）通常意味着极端异常市场环境（如黑天鹅暴跌、流动性枯竭、流动性陷阱），或者交易员的模型彻底脱离了当前市场 Regime。
     此时继续交易面临致命风险，必须切入 `HALTED` 状态彻底关闭当日权限，强制进行收盘复盘与风险对账。

### Q3：为什么将“情绪温度打分（Emotional Temperature <= 3）”强制置于订单准入清单中？这种主观打分在实际量化与程序化执行中如何客观化？

参考答案：
1. 心理元认知（Metacognition）阻断：
   人类在情绪失控时往往“意识不到自己已经失控”。通过强制要求交易员在下单前在界面上点选情绪状态（1:极度冷静, 3:平稳, 5:暴怒/焦虑），
   这本身就是一个迫使前额叶皮层启动“元认知（思考自己的思考）”的心智刹车动作。一旦打分超过 3，系统判定为认知受损，坚决拒单。
2. 客观化工程落地：
   在纯程序化或量化交易系统中，可以将“情绪打分”转化为算法行为特征代理变量：
   - 下单频率突增倍数（Order Frequency Spike）；
   - 止损撤单尝试次数；
   - 仓位规模相对于历史均值的突增比例（Sizing Deviation）；
   - 敲击键盘或鼠标的异常点击速率与窗口切换频率。
   一旦这些代理指标异动，算法直接判定系统或操盘手处于“情绪倾侧状态”，自动上调风控拦截级别。
"""


# ==============================================================================
# 单元测试与断言校验
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
