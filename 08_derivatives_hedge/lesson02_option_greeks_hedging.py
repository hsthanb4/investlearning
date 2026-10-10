r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 2 课：期权希腊字母矩阵与动态 Delta 对冲

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握期权一阶与二阶希腊字母（Delta, Gamma, Vega, Theta, Rho）的偏导数推导与几何物理内涵；
2. 深刻理解做市商“买入低估波动率、做空高估波动率”并通过动态 Delta 中性剥离方向风险的机制；
3. 掌握离散对冲误差（Discrete Hedging Error）的数学成因：Gamma 与已实现波动率（Realized Vol）的交互作用；
4. 编写代码实现五大希腊字母全套解析计算，并构建做空看涨期权与标的现货的动态 Delta 中性对冲仿真引擎。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，阐述 Gamma 挤压（Gamma Squeeze）与 Short Gamma 尾部暴仓机制。

---
## 核心心智模型与数理推导

### 1. 泰勒展开与希腊字母全息矩阵

对于任意期权组合价值 $\Pi(S, \sigma, t, r)$，其在时间微元 $\Delta t$ 内的损益变化可通过多元泰勒展开表示为：
$$
\Delta \Pi \approx \underbrace{\frac{\partial \Pi}{\partial S} \Delta S}_{\text{Delta 收益}} + \underbrace{\frac{1}{2} \frac{\partial^2 \Pi}{\partial S^2} (\Delta S)^2}_{\text{Gamma 凸性收益}} + \underbrace{\frac{\partial \Pi}{\partial \sigma} \Delta \sigma}_{\text{Vega 波动率收益}} + \underbrace{\frac{\partial \Pi}{\partial t} \Delta t}_{\text{Theta 时间流逝}} + \underbrace{\frac{\partial \Pi}{\partial r} \Delta r}_{\text{Rho 利率收益}}
$$

| 希腊字母 | 数学定义 | 经济学物理含义 | Call / Put 正负性 |
|---|---|---|---|
| **Delta ($\Delta$)** | $\frac{\partial V}{\partial S}$ | 标的价格每变动 1 单位，期权价值变动量（对冲比率） | Call: $(0, 1)$；Put: $(-1, 0)$ |
| **Gamma ($\Gamma$)** | $\frac{\partial^2 V}{\partial S^2} = \frac{\partial \Delta}{\partial S}$ | 标的价格变动对 Delta 的敏感度（期权的加速度 / 凸性） | 买方恒为正 ($\Gamma > 0$)；卖方恒为负 |
| **Vega ($\nu$)** | $\frac{\partial V}{\partial \sigma}$ | 隐含波动率每上升 1 个百分点，期权价值的变动量 | 买方恒为正 ($\nu > 0$)；卖方恒为负 |
| **Theta ($\Theta$)** | $\frac{\partial V}{\partial t} = -\frac{\partial V}{\partial \tau}$ | 时间流逝一单位，期权时间价值的衰减损耗速度 | 买方通常为负 ($\Theta < 0$)；卖方为正 |
| **Rho ($\rho$)** | $\frac{\partial V}{\partial r}$ | 无风险利率每变动 1 个基点/百分点，期权价值变动量 | Call 为正；Put 为负 |

解析公式推导（标准正态 PDF 为 $\phi(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$）：
$$
\begin{aligned}
d_1 &= \frac{\ln(S / K) + (r + \frac{1}{2}\sigma^2)T}{\sigma \sqrt{T}}, \quad d_2 = d_1 - \sigma \sqrt{T} \\
\Delta_{\text{call}} &= N(d_1), \quad \Delta_{\text{put}} = N(d_1) - 1 \\
\Gamma &= \frac{\phi(d_1)}{S \sigma \sqrt{T}} \quad (\text{Call 与 Put 完全相同}) \\
\nu &= S \phi(d_1) \sqrt{T} \quad (\text{Call 与 Put 完全相同}) \\
\Theta_{\text{call}} &= -\frac{S \phi(d_1) \sigma}{2 \sqrt{T}} - r K e^{-rT} N(d_2) \\
\Theta_{\text{put}} &= -\frac{S \phi(d_1) \sigma}{2 \sqrt{T}} + r K e^{-rT} N(-d_2) \\
\rho_{\text{call}} &= K T e^{-rT} N(d_2), \quad \rho_{\text{put}} = -K T e^{-rT} N(-d_2)
\end{aligned}
$$

### 2. 动态 Delta 中性对冲仿真 (Dynamic Delta Hedging)

当做市商卖出 1 份看涨期权（获取权利金 $C_0$），其头寸面临正的股价上行风险（$\Delta_{\text{short}} = -\Delta_{\text{call}} < 0$）。
为了达到 Delta 中性（组合总 Delta = 0），做市商在现货市场买入 $\Delta_{\text{call}}$ 股股票。
随着标的资产价格波动与时间推移，在离散时间步 $t_1, t_2, \dots, t_N$：
- Delta 不断漂移变化；
- 做市商按新 Delta 动态调仓：$\Delta \text{shares} = \Delta_{t} - \Delta_{t-1}$；
- 股票调仓资金从现金借贷账户中划拨并按无风险利率计息；
- 理论上，在连续对冲极限下，最终组合总盈亏恒等于 0（完全复制）。
"""

import math
from typing import Dict, List, Tuple


def standard_normal_pdf(x: float) -> float:
    """标准正态分布概率密度函数 phi(x)"""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)


def standard_normal_cdf(x: float) -> float:
    """标准正态分布累积分布函数 N(x)"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def calculate_bsm_greeks(S: float, K: float, T: float, r: float, sigma: float) -> Dict[str, float]:
    """
    计算 BSM 欧式期权全部一阶与二阶希腊字母。
    """
    # TODO: 实现五大希腊字母 (call_delta, put_delta, gamma, vega, call_theta, put_theta, call_rho, put_rho)
    # 结果均四舍五入保留 4 位小数
    pass


def simulate_dynamic_delta_hedging(
    price_path: List[float],
    K: float,
    T: float,
    r: float,
    sigma: float
) -> Dict[str, float]:
    """
    做空 1 份欧式看涨期权，并使用标的股票进行离散动态 Delta 中性对冲仿真。
    
    :param price_path: 模拟的价格时间序列 [S_0, S_1, ..., S_N]
    :param K: 行权价
    :param T: 总到期年限
    :param r: 无风险利率
    :param sigma: 定价与对冲使用的波动率
    :return: 包含对冲终值、各步骤开销与对冲误差的字典
    """
    # TODO:
    # 1. 计算期初 Call 理论价格 c0，买入 delta_0 股票，现金账户为 c0 - delta_0 * S0
    # 2. 遍历 price_path 每个时间步，现金按连续复利增长 cash = cash * exp(r * dt)
    # 3. 计算新 Delta 并调仓股票，现金扣减 (new_delta - shares) * Si
    # 4. 到期清算：现金计息 + 股票抛售 - 期权赔付 max(SN - K, 0)
    # 5. 返回各阶段关键数据字典
    pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么期权卖方（Short Gamma / Short Vega）在平稳温和市场中每天稳收 Theta 时间价值，但在突发黑天鹅暴跌时可能瞬间爆仓破产？

**你的答案：**
[在此处写下你的分析：需从 BSM 偏微分方程关于 Theta 与 Gamma 的替代关系出发，推导极端行情下二阶凸性亏损爆炸与 Vega 暴涨的双重夹击机制]


### Q2：什么是“伽马挤压（Gamma Squeeze）”？2021 年美股 GameStop (GME) 散户轧空事件中，做市商的动态 Delta 对冲如何沦为火上浇油的暴涨推手？

**你的答案：**
[在此处写下你的分析：需阐述散户买入深度虚值 Call 迫使做市商持有负 Gamma，以及股价微涨时做市商被迫市价抢购现货对冲的正反馈循环]


### Q3：离散对冲频率（如每日对冲 vs 每小时对冲）与交易摩擦成本之间存在怎样的权衡？为什么“完美无误差对冲”在物理世界中不存在？

**你的答案：**
[在此处写下你的分析：需分析对冲残差方差随调仓频率的变化，并结合 Leland 定理说明频繁调仓导致的无限累积佣金冲突]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Analytical BSM Greeks Calculation...")
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.20
    greeks = calculate_bsm_greeks(S, K, T, r, sigma)

    assert abs(greeks["call_delta"] - 0.6368) < 1e-3, f"Call Delta error: {greeks['call_delta']}"
    assert abs(greeks["put_delta"] - (-0.3632)) < 1e-3, f"Put Delta error: {greeks['put_delta']}"
    assert abs((greeks["call_delta"] - greeks["put_delta"]) - 1.0) < 1e-4
    assert abs(greeks["gamma"] - 0.0188) < 1e-3, f"Gamma error: {greeks['gamma']}"
    assert abs(greeks["vega"] - 37.5240) < 1e-1, f"Vega error: {greeks['vega']}"
    assert abs(greeks["call_theta"] - (-6.4140)) < 1e-1, f"Call Theta error: {greeks['call_theta']}"
    assert abs(greeks["put_theta"] - (-1.6579)) < 1e-1, f"Put Theta error: {greeks['put_theta']}"
    assert abs(greeks["call_rho"] - 53.2325) < 1e-1, f"Call Rho error: {greeks['call_rho']}"
    assert abs(greeks["put_rho"] - (-41.8905)) < 1e-1, f"Put Rho error: {greeks['put_rho']}"

    print("[Testing] Greeks Boundary Conditions (Zero Maturity)...")
    expired_greeks = calculate_bsm_greeks(S=105.0, K=100.0, T=0.0, r=0.05, sigma=0.20)
    assert expired_greeks["call_delta"] == 1.0
    assert expired_greeks["put_delta"] == 0.0
    assert expired_greeks["gamma"] == 0.0

    print("[Testing] Dynamic Delta Neutral Hedging Simulation...")
    import numpy as np
    np.random.seed(42)
    N_steps = 100
    dt_step = T / N_steps
    simulated_path = [S]
    for _ in range(N_steps):
        z = np.random.normal(0, 1)
        st = simulated_path[-1] * math.exp((r - 0.5 * sigma * sigma) * dt_step + sigma * math.sqrt(dt_step) * z)
        simulated_path.append(st)

    hedge_res = simulate_dynamic_delta_hedging(simulated_path, K=100.0, T=1.0, r=0.05, sigma=0.20)
    assert abs(hedge_res["initial_call_premium"] - 10.4506) < 1e-3
    assert abs(hedge_res["initial_delta"] - 0.6368) < 1e-3
    print(f"Final Hedging PnL: {hedge_res['final_portfolio_pnl']}")
    assert abs(hedge_res["final_portfolio_pnl"]) < 1.0, f"Hedging tracking error too large: {hedge_res['final_portfolio_pnl']}"

    print("All assertions passed! Module 08 Lesson 02 verification successful.")
