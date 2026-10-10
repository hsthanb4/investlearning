r"""
================================================================================
模块 07：行为金融学、交易心理与执行纪律 · 第 2/4 课
第 2 课：交易执行清单机制与风控守门员有限状态机 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：意志力假象与有限状态机刚性防线
在神经生理学层面，高压市场波动会激发人体交感神经系统剧烈分泌肾上腺素与皮质醇，导致负责理性概率推演的大脑前额叶皮层机能被杏仁核完全劫持（即‘倾侧（Tilt）’现象）。资深投资机构绝不相信任何交易员的个人意志力，而是将交易权限降维移交给不可篡改的‘飞行前清单（Pre-Flight Checklist）’与‘风控有限状态机（Finite State Machine, FSM）’。
:::

- **[认知资源损耗与决策疲劳]**：日内高频盯盘导致神经递质过度消耗，使人类在经历回撤后产生不可遏制的‘报复性交易（Revenge Trading）’冲动，通过违规加仓企图光速翻本。
- **[清单革命的工程化阻断]**：严格借鉴航空航天与重症医学清单规范，强制将交易入场拆解为信号逻辑、盈亏比（RR Ratio ≥ 2.0）、生理情绪温度（Emotional Temp ≤ 3）等刚性门槛，未达标者直接物理拒单。
- **[状态机的刚性锁闭逻辑]**：通过定义明确的状态跃迁规则（READY ➔ IN_POSITION ➔ COOLDOWN ➔ HALTED），系统在连续亏损或触及日内硬熔断时强制收回交易席位权限。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了交易风控守门员有限状态机的单向跃迁因果拓扑与冷却熔断机制。

```mermaid
flowchart TD
    READY["READY (准备就绪 / 允许开仓)"]
    IN_POS["IN_POSITION (持仓监控中 / 严禁重复开仓)"]
    COOLDOWN["COOLDOWN (连亏冷静期 / 冻结新单)"]
    HALTED["HALTED (日内硬熔断 / 彻底终止)"]

    READY -->|清单验证通过 & 风险额度达标| IN_POS
    READY -.->|清单违规或超风险预算| READY
    IN_POS -->|盈利平仓或单次止损| READY
    IN_POS -->|连续亏损达到上限 (如2次)| COOLDOWN
    COOLDOWN -->|冷静期时钟倒计时归零| READY
    IN_POS -->|日内累计亏损达到硬熔断线 (如5%)| HALTED
    COOLDOWN -->|持仓残差触及日内硬熔断线| HALTED
```

- **[要点 1：状态互斥与单向流转]**：处于 IN_POSITION 时绝对禁止加仓摊平成本；处于 COOLDOWN 时完全冻结新订单入口，彻底隔绝由于情绪亢奋导致的二次冲动。
- **[要点 2：冷却时钟 tick 的自愈机制]**：COOLDOWN 状态通过外部离散时间步递减（Tick Cooldown），迫使交易员离开终端至少 30 分钟以上，等待神经激素代谢回归基线。
- **[要点 3：不可逆日内熔断终态]**：HALTED 状态为当日交易日的吸收态（Absorbing State），一旦触及，日内无论行情出现何等所谓‘天赐良机’，交易权限均被物理锁死直至次日清算。

锚点指引：下图揭示了账户净值从动态回撤到阶梯式熔断阈值的风控触发逻辑。

```mermaid
flowchart LR
    A["账户实时净值变化"] --> B{"回撤阶梯审查"}
    B -->|单笔回撤 > 2%| C["单笔硬止损触发 (强制市价强平)"]
    B -->|连亏次数 >= 2| D["切入 COOLDOWN (锁定 3 周期冷静)"]
    B -->|日内净亏损 >= 5%| E["切入 HALTED (当日不可逆关机)"]
```

- **[要点 1：单笔损失有界性保障]**：单笔最大损失限制为总资本的 2%，使得任何单次不可抗力黑天鹅都不会对整体资产负债表构成不可逆创伤。
- **[要点 2：避免连续泊松亏损踩踏]**：连续两次亏损意味着当前策略风格与日内行情 Regime 极度不适配，强行继续交易的边际期望收益为负。
- **[要点 3：吸收壁破产防御]**：日内 5% 熔断底线守护了资本底座，确保留存 95% 以上的有生力量参与后续正期望周期的复利博弈。

【数学与估值模型】
风控状态转移矩阵与单笔风险预算硬约束：
$$
\text{Risk}_{\text{order}} = |\text{Price}_{\text{entry}} - \text{Price}_{\text{stop}}| \times \text{Size} \le \text{Capital}_t \times \gamma_{\text{trade}}
$$
变量定义域与参数约束：
- $\text{Price}_{\text{entry}}, \text{Price}_{\text{stop}} > 0$：入场价与止损价，多头必须满足 $\text{Price}_{\text{stop}} < \text{Price}_{\text{entry}}$，空头反之。
- $\text{Size} \in \mathbb{N}^+$：报单持仓股数或合约数。
- $\text{Capital}_t > 0$：账户当前时刻可用有效权益资本（USD 或 RMB）。
- $\gamma_{\text{trade}} \in (0, 0.05]$：单笔交易最大风险敞口系数，投决会标准通常设定为 $1\% \sim 2\%$。

日内累计亏损硬熔断约束：
$$
\text{Loss}_{\text{daily}} = \sum_{i \in \text{Trades Today}} \max(0, -\text{PnL}_i) \ge \text{Capital}_0 \times \gamma_{\text{daily}} \implies \text{State} \leftarrow \text{HALTED}
$$
变量定义域：$\text{Capital}_0$ 为当日初始开盘净资产，$\gamma_{\text{daily}} \in [0.03, 0.08]$，基准设定为 $5\%$。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **下移止损位的毁灭性谬误**：严禁在入场后向下移动止损价（Loosening Stop-Loss）。这在数学上等价于将有界风险突变为无界肥尾风险，是导致交易员破产的头号死因。
2. **报复性翻倍下注（马丁格尔陷阱）**：在遭遇亏损后加倍下单以求‘一把回本’，违反鞅过程收益守恒，在真实有限资本约束下必然在吸附壁归零。
3. **主观豁免检查清单**：任何声称‘盘感极佳因此无需填报清单’的主观逾矩行为，均被投决会视为最高级别合规违规，一票否决。
:::

【思考题】
Q1: 为什么在职业交易规范中，“止损位只能向盈利方向移动（追踪止损），绝不允许向亏损方向扩大（向下移动止损）”被奉为第一铁律？从破产概率（Risk of Ruin）角度推导其因果。
Q2: 在交易状态机中，为何必须区分“连亏冷静期（COOLDOWN）”与“日内彻底熔断（HALTED）”两个不同层级的状态？
Q3: 为什么将“情绪温度打分（Emotional Temperature <= 3）”强制置于订单准入清单中？这种主观打分在实际量化与程序化执行中如何客观化？

【Q1 深度参考答案】
- **[期望破产概率的非线性爆炸]**：数学上资本回撤与恢复所需涨幅呈非线性暴增（亏 50% 需涨 100%，亏 90% 需涨 900%）。挪动止损把有界损失常数变成无界负期望随机变量，使破产概率（Risk of Ruin）逼近 100%。
- **[认知失谐与逃避升级]**：挪动止损本质是逃避现实痛苦，随着价格进一步下跌痛苦成倍放大，促使交易员二次、三次挪动，陷入不可逆爆仓。
- **[吸收壁不可逆性]**：本金清零属于马尔可夫吸收态，向下挪止损实质是主动加速向吸收壁滑落。

【Q2 深度参考答案】
- **[战术噪声 vs 战略失灵的本质差异]**：连亏 2 次通常是正期望系统的正常方差波动，但会激活生理内分泌冲动；`COOLDOWN` 核心是阻断多巴胺与肾上腺素的短期情绪循环，让前额叶皮层重新夺回认知主导权。
- **[日内硬熔断的极端机制防范]**：单日亏损触及 5% 通常意味着市场进入 Regime 突变或流动性挤兑，当前模型完全失效；`HALTED` 强制物理断开交易席位，避免单日穿仓。
- **[状态分级的阶梯纵深防御]**：分级控制构建了双重缓冲，既避免对正常回撤过度反应，又在发生系统性危机时提供绝对硬约束。

【Q3 深度参考答案】
- **[心理元认知的前额叶心智刹车]**：情绪失控时人类常无法意识到失控；强制打分强迫大脑启动元认知反思，打分超过 3 时坚决物理拒单。
- **[量化系统中的客观代理变量转化]**：在程序化系统中可将情绪打分转化为：下单频率突增倍数（Order Frequency Spike）、止损撤单尝试次数、仓位偏离度（Sizing Deviation）、键盘鼠标异常交互速率。
- **[异常行为驱动的自适应风控]**：一旦客观代理变量异动，系统自动判定交易员或模型处于 Tilt 状态，直接触发网关拦截与席位冻结。
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
