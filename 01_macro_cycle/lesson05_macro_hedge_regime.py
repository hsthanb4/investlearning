r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 5/5 课
第 5 课：宏观体制切换与全天候对冲配置 (Macro Regime Switching & All-Weather Hedging)
================================================================================

::: {.callout-note}
### 投决会全天候公理：资产多样化与风险平价的前提是宏观因子风险的正交暴露
- **[桥水全天候哲学]**：任何金融资产的定价均取决于“经济增长（高于/低于预期）”与“通胀环境（高于/低于预期）”两个正交驱动因子。
- **[体制非线性切换]**：宏观市场不是单一连续高斯稳态，而是由“流动性扩张/收缩”与“波动率平静/恐慌”构成的多稳态非线性马尔可夫状态机。
- **[尾部相关性收敛]**：在流动性冻结与恐慌飙升的危机体制下，股债负相关关系可能彻底失效并收敛为 1.0，必须建立外生风险断路器。
:::

- **[自适应动态对冲数学模型]**：
  - 股票目标敞口判定函数由宏观流动性动量与隐含波动率联合驱动：

$$
\omega^{\text{Equity}}_t = f(\text{Liquidity Trend}_t, \text{VIX}_t) = \begin{cases}
0.20, & \text{VIX}_t > 30.0 \quad (\text{危机体制：触发硬断路器，强制现金防御}) \\
0.90, & \text{VIX}_t \le 30.0 \land \text{Liquidity Trend}_t > 0 \quad (\text{扩张体制：积极做多享受估值扩张}) \\
0.50, & \text{VIX}_t \le 30.0 \land \text{Liquidity Trend}_t \le 0 \quad (\text{中性体制：稳健防守平衡回撤})
\end{cases}
$$

- **[变量定义域与物理意义]**：
  - $\text{VIX}_t \in (0, 100)$：CBOE 市场波动率指数，度量标普500期权市场隐含的未来 30 天年化波动率。VIX > 30 对应历史极端危机（如 2008年、2020年3月）。
  - $\text{Liquidity Trend}_t \in \mathbb{R}$：央行净流动性一阶差分或环比趋势。

- **[组合动态追踪方程]**：
  - 严格消除前视偏差（Lookahead Bias），当期收益率由前一交易日收盘确定的权重实现：

$$
R^{\text{Portfolio}}_t = \omega^{\text{Equity}}_{t-1} \cdot R^{\text{Equity}}_t + (1 - \omega^{\text{Equity}}_{t-1}) \cdot R^{\text{Cash}}_t
$$

- **[引导句锚点 1]**：桥水全天候宏观四象限资产风险正交配置图如下所示：

```mermaid
flowchart TD
    RawData["宏观输入: 央行流动性脉冲 (Liquidity) + 市场波动率 (VIX)"] --> StateMachine["宏观体制自适应状态机 (Macro Regime Machine)"]
    StateMachine --> Regime1["1. 扩张期 (Expansion: 流动性宽松 + 低波动) ➔ 股票权益 90%, 适度杠杆"]
    StateMachine --> Regime2["2. 中性防御期 (Neutral: 流动性收紧 + 低波动) ➔ 股票 50%, 增配平价国债"]
    StateMachine --> Regime3["3. 危机风暴期 (Crisis: VIX > 30 恐慌) ➔ 触发风险断路器, 股票强制压缩至 20%, 现金与黄金防御"]
    Regime1 --> Portfolio["全天候自适应对冲组合: 动态回撤控制与夏普比率倍增"]
    Regime2 --> Portfolio
    Regime3 --> Portfolio
```

- **[架构要点拆解 1]**：
  - **[1. 四象限风险平分]**：增长与通胀的四种可能情景各分配 25% 风险预算。
  - **[2. 资产风险正交化]**：挑选在特定宏观环境下具备高确定性超额收益的底层资产进行对冲。
  - **[3. 长期复利抗通胀]**：组合穿越 50 年美联储加息与衰退周期，实现稳健向上的净值曲线。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[协方差矩阵崩溃]**：在极端黑天鹅时刻，资产间非线性杠杆清算会瞬间摧毁过去三年建立的相关性假设。
- **[外生宏观断路器优先]**：风控系统必须优先遵循外生硬规则（如 VIX 阈值、隔夜回购利率冻结），严禁完全依赖统计内生止损。
:::

【思考题】
Q1: 为什么基于宏观指标的择时与体制切换策略在超高频（如日度、分钟级）往往胜率较低甚至充斥伪信号，而在中长周期（季度至年度、6~18个月）却具有极高的稳健性与穿透力？请从宏观经济变量的发布滞后性、信号噪声比（SNR）与信贷周期传导惯性推导。
Q2: 经典风险平价（Risk Parity）全天候模型在面临 2022 年“高通胀 + 美联储暴力加息”引发的股债双杀时，为什么遭遇了重大净值回撤？怎样通过引入“宏观通胀/流动性体制先验过滤器”来修补这一缺陷？
Q3: 为什么现代量化宏观对冲基金在设计“危机防御哨兵”（Kill Switch / Crisis Protocol）时，绝不能仅依赖价格技术止损，而必须设置外生流动性硬门槛（如 interbank spread 跨越阈值、隔夜拆借冻结）？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现多体制股票敞口动态映射规则 (1.5分)；
  2. 实现全天候自适应宏观状态机类与多资产权重分配 (1.5分)；
  3. 实现动态对冲回测与回撤风险平抑评估 (1分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须深入剖析宏观因果链与微观清算机制；
- 通过线：8/10 分。一票否决：危机阶段未降仓、回测存在未来函数、删除断言。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def determine_equity_exposure(liquidity_trend: float, volatility_vix: float) -> float:
    """
    根据流动性与波动率决定股票权益目标敞口 (0.0 ~ 1.0):
    - VIX > 30 (高风险恐慌): 无论流动性如何，敞口降至 0.2
    - VIX <= 30 且 liquidity_trend > 0: 积极看多，敞口 0.9
    - VIX <= 30 且 liquidity_trend <= 0: 中性防御，敞口 0.5

    参数:
        liquidity_trend: 净流动性环比或一阶趋势加速度 (正数代表宽松，负数代表紧缩)
        volatility_vix: 市场恐慌波动率指数 VIX

    返回:
        float: 目标股票配置权重 [0.0, 1.0]
    """
    # TODO: 实现规则判定
    pass


class MacroRegimeStateMachine:
    """
    全天候宏观体制自适应状态机 (Macro Regime State Machine)
    将市场划分为四大离散状态:
    - 'Expansion' (扩张期: 宽松 + 低波): 股票高配 (60%), 国债 (20%), 商品 (10%), 现金 (10%)
    - 'Neutral' (中性防御: 紧缩 + 低波): 股票标配 (30%), 国债 (40%), 商品 (10%), 现金 (20%)
    - 'Inflationary' (通胀高波: 紧缩 + 中高波 VIX 在 22~30): 股票 (15%), 国债 (15%), 商品 (40%), 现金 (30%)
    - 'Crisis' (危机流动性休克: VIX > 30): 股票 (10%), 国债 (30%), 黄金商品 (10%), 现金 (50%)
    """

    def __init__(self):
        self.current_state = "Neutral"

    def update_state(self, liquidity_trend: float, vix: float) -> str:
        """
        根据当期输入转移状态机内部状态并返回状态名称
        """
        # TODO: 根据流动性趋势与 VIX 判定并更新状态
        pass

    def get_target_allocation(self) -> Dict[str, float]:
        """
        返回当前状态下的四资产目标配置权重
        """
        # TODO: 返回目标资产权重字典
        pass


def simulate_dynamic_hedge(
    equity_returns: pd.Series,
    liquidity_trends: pd.Series,
    vix_series: pd.Series,
    cash_return_per_period: float = 0.0002,
) -> Dict[str, float]:
    """
    回测宏观体制动态敞口调节对冲策略与买入持有基准表现对比:
    在每期 t，使用 t-1 期的宏观信号决定 t 期的权益敞口 (防止前视偏差):
        r_port_t = exposure_{t-1} * equity_returns_t + (1 - exposure_{t-1}) * cash_return

    返回绩效字典:
        {
            "benchmark_max_drawdown": 纯股票买入持有最大回撤 (%),
            "hedged_max_drawdown": 动态宏观对冲最大回撤 (%),
            "max_drawdown_reduction": 回撤降低幅度 (基准回撤 - 对冲回撤, %),
            "hedged_total_return": 对冲策略累计总回报 (%)
        }
    """
    # TODO: 逐期滚动回测，严格按上一期信号计算当期收益，输出风险平抑效果
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础敞口规则 ----------------
    assert determine_equity_exposure(0.5, 18.0) == 0.9
    assert determine_equity_exposure(-0.2, 22.0) == 0.5
    assert determine_equity_exposure(0.8, 35.0) == 0.2

    # ---------------- 基础测试 2: 全天候状态机多资产权重 ----------------
    sm = MacroRegimeStateMachine()
    s1 = sm.update_state(0.4, 16.0)
    assert s1 == "Expansion", f"预期 Expansion, 实际 {s1}"
    w1 = sm.get_target_allocation()
    assert abs(w1["Stocks"] - 0.60) < 1e-4
    assert abs(sum(w1.values()) - 1.0) < 1e-4

    s2 = sm.update_state(-0.3, 19.0)
    assert s2 == "Neutral", f"预期 Neutral, 实际 {s2}"
    w2 = sm.get_target_allocation()
    assert abs(w2["Stocks"] - 0.30) < 1e-4

    s3 = sm.update_state(-0.5, 38.0)
    assert s3 == "Crisis", f"预期 Crisis, 实际 {s3}"
    w3 = sm.get_target_allocation()
    assert abs(w3["Stocks"] - 0.10) < 1e-4
    assert abs(w3["Cash"] - 0.50) < 1e-4

    # ---------------- 基础测试 3: 动态对冲模拟与回撤控制 ----------------
    np.random.seed(42)
    periods = 60
    # 构造一段包含牛市平稳与突发暴跌危机的行情序列
    eq_rets = [0.02] * 20 + [-0.08] * 10 + [0.015] * 30
    liq_s = [0.5] * 20 + [-0.8] * 10 + [0.3] * 30
    vix_s = [16.0] * 20 + [38.0] * 10 + [18.0] * 30

    res = simulate_dynamic_hedge(pd.Series(eq_rets), pd.Series(liq_s), pd.Series(vix_s))
    assert res["benchmark_max_drawdown"] > 50.0, f"基准遭遇暴跌回撤应超过50%, 实际: {res['benchmark_max_drawdown']}"
    assert res["hedged_max_drawdown"] < 25.0, f"动态对冲后最大回撤应显著压缩至25%以下, 实际: {res['hedged_max_drawdown']}"
    assert res["max_drawdown_reduction"] > 30.0, f"回撤降低幅度应大于30%, 实际: {res['max_drawdown_reduction']}"

    print("Lesson 05 Exercise Passed!")
