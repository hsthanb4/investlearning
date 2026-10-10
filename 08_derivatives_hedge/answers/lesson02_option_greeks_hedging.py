r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 2 课：期权希腊字母矩阵与动态 Delta 对冲

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

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
    if T <= 0.0 or sigma <= 0.0:
        call_delta = 1.0 if S > K else 0.0
        put_delta = call_delta - 1.0
        return {
            "call_delta": round(call_delta, 4),
            "put_delta": round(put_delta, 4),
            "gamma": 0.0,
            "vega": 0.0,
            "call_theta": 0.0,
            "put_theta": 0.0,
            "call_rho": 0.0,
            "put_rho": 0.0
        }

    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    pdf_d1 = standard_normal_pdf(d1)
    cdf_d1 = standard_normal_cdf(d1)
    cdf_d2 = standard_normal_cdf(d2)

    call_delta = cdf_d1
    put_delta = cdf_d1 - 1.0
    gamma = pdf_d1 / (S * sigma * math.sqrt(T))
    vega = S * pdf_d1 * math.sqrt(T)

    term1 = - (S * pdf_d1 * sigma) / (2.0 * math.sqrt(T))
    call_theta = term1 - r * K * math.exp(-r * T) * cdf_d2
    put_theta = term1 + r * K * math.exp(-r * T) * standard_normal_cdf(-d2)

    call_rho = K * T * math.exp(-r * T) * cdf_d2
    put_rho = -K * T * math.exp(-r * T) * standard_normal_cdf(-d2)

    return {
        "call_delta": round(call_delta, 4),
        "put_delta": round(put_delta, 4),
        "gamma": round(gamma, 4),
        "vega": round(vega, 4),
        "call_theta": round(call_theta, 4),
        "put_theta": round(put_theta, 4),
        "call_rho": round(call_rho, 4),
        "put_rho": round(put_rho, 4)
    }


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
    N = len(price_path) - 1
    dt = T / N
    S0 = price_path[0]

    # 计算期初 Call 理论价格并收取权利金
    d1_0 = (math.log(S0 / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2_0 = d1_0 - sigma * math.sqrt(T)
    c0 = S0 * standard_normal_cdf(d1_0) - K * math.exp(-r * T) * standard_normal_cdf(d2_0)

    # 期初对冲：买入 delta_0 股股票
    delta_0 = standard_normal_cdf(d1_0)
    cash = c0 - delta_0 * S0
    shares = delta_0

    # 沿价格路径进行动态离散再平衡
    for i in range(1, N):
        tau = T - i * dt
        Si = price_path[i]

        # 现金账户按无风险利率计息
        cash = cash * math.exp(r * dt)

        # 计算当前时点的新 Delta
        d1_i = (math.log(Si / K) + (r + 0.5 * sigma * sigma) * tau) / (sigma * math.sqrt(tau))
        new_delta = standard_normal_cdf(d1_i)

        # 调仓买入/卖出股票以维持 Delta 中性
        trade_shares = new_delta - shares
        cash -= trade_shares * Si
        shares = new_delta

    # 到期结算时点 N
    SN = price_path[-1]
    cash = cash * math.exp(r * dt)

    # 期权履约现金流（卖出方支出赔付）
    option_payoff = max(0.0, SN - K)

    # 抛售持仓股票清算为现金
    stock_liquidation = shares * SN

    final_hedged_portfolio_value = cash + stock_liquidation - option_payoff

    return {
        "initial_call_premium": round(c0, 4),
        "initial_delta": round(delta_0, 4),
        "final_stock_price": round(SN, 4),
        "option_payoff": round(option_payoff, 4),
        "final_portfolio_pnl": round(final_hedged_portfolio_value, 4)
    }


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么期权卖方（Short Gamma / Short Vega）在平稳温和市场中每天稳收 Theta 时间价值，但在突发黑天鹅暴跌时可能瞬间爆仓破产？

参考答案：
1. Theta 与 Gamma 的永恒权衡（No-Free-Lunch PDE 约束）：
   根据 BSM 偏微分方程：$\Theta + r S \Delta + \frac{1}{2} \sigma^2 S^2 \Gamma = r V$。
   在 Delta 中性状态下，$\Theta \approx -\frac{1}{2} \sigma^2 S^2 \Gamma$。
   - 做空期权赚取正 Theta（$\Theta > 0$ 时间流逝赚钱），其数学代价是必须承担负 Gamma（$\Gamma < 0$）。
   - 在平静市场中，标的资产微小波动（$(\Delta S)^2 \approx 0$），负 Gamma 损耗很小，每日正 Theta 稳稳落袋，给人以“稳健高胜率理财”的幻觉。
2. 极端暴跌下的双重暴击（Gamma 倒戈与 Vega 膨胀）：
   - 当黑天鹅突发暴跌时，$(\Delta S)^2$ 剧烈放大，由 $\frac{1}{2} \Gamma (\Delta S)^2$ 带来的非线性亏损呈二次方爆炸；
   - 伴随市场恐慌，隐含波动率 $\sigma$ 暴涨（例如从 15% 飙升至 80%），卖方承担的负 Vega（$-\nu \Delta \sigma$）产生天文数字般的亏损；
   - 这种“平时赚小钱，一次亏到底”的非对称收益分布，正是长期资本管理公司（LTCM）等期权空头基金覆灭的数学本质。

### Q2：什么是“伽马挤压（Gamma Squeeze）”？2021 年美股 GameStop (GME) 散户轧空事件中，做市商的动态 Delta 对冲如何沦为火上浇油的暴涨推手？

参考答案：
1. 做市商被动成为期权净空头（Short Call）：
   散户在 Robinhood 等券商平台上集中疯狂买入 GME 的短期极度深度虚值看涨期权（OTM Call）。
   做市商（Market Makers）为了赚取买卖价差与流动性溢价，作为对手方被动卖出了海量 Call，从而持有巨额的负 Delta 和负 Gamma。
2. 动态 Delta 追高正反馈死循环：
   - 初始时虚值期权 Delta 极小（如 0.05），做市商只需买入少量现货股票对冲；
   - 当散户合力将股价推高哪怕一点点时，由于做市商持有负 Gamma，其 Delta 绝对值迅速激增（从 0.05 跃升至 0.30、0.70）；
   - 为了维持 Delta 中性以避免暴露巨大的裸空风险，做市商必须在现货市场上以市价强行买入数以百万计的 GME 现货股票进行机械性对冲；
   - 做市商的巨额买单进一步推高了股票现货价格，导致期权 Delta 更加接近 1.0，迫使做市商买入更多股票！这种机械化对冲引发的正反馈闭环直接导致股价出现垂直火箭式暴涨。

### Q3：离散对冲频率（如每日对冲 vs 每小时对冲）与交易摩擦成本之间存在怎样的权衡？为什么“完美无误差对冲”在物理世界中不存在？

参考答案：
1. 离散误差与跟踪方差（Discrete Tracking Error）：
   连续时间 BSM 模型假设对冲频率 $dt \to 0$。但在现实中，离散调仓间隔 $\Delta t$ 使得做市商在两次调仓之间必然暴露于未对冲的凸性风险中。
   每一步的对冲残差均值约为 0，但其方差与持仓 Gamma 及跳跃方差成正比：$\text{Var}(\text{Hedging Error}) \propto \frac{1}{N} \int_0^T S_t^4 \Gamma_t^2 dt$。
   要想降低对冲误差，就必须提高对冲频率 $N$。
2. 交易摩擦成本（Transaction Costs & Bid-Ask Spread）：
   每一次调仓都需要支付买卖价差、交易所规费以及对市场造成的冲击成本（Market Impact）。
   Leland (1985) 定理证明：在存在固定买卖佣金比例 $k$ 的市场中，若连续对冲，累计交易成本将趋于无穷大！
   因此，实际衍生品交易台必须使用带宽对冲（Band Hedging / Whalley-Wilmott 算法）：仅当标的价格波动超出某个容忍阈值区间时才触发调仓，在对冲误差方差与摩擦佣金之间寻求最优平衡。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Analytical BSM Greeks Calculation...")
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.20
    greeks = calculate_bsm_greeks(S, K, T, r, sigma)

    # 验证平值期权基准希腊字母
    # Call Delta ~ 0.6368, Put Delta ~ -0.3632
    assert abs(greeks["call_delta"] - 0.6368) < 1e-3, f"Call Delta error: {greeks['call_delta']}"
    assert abs(greeks["put_delta"] - (-0.3632)) < 1e-3, f"Put Delta error: {greeks['put_delta']}"
    assert abs((greeks["call_delta"] - greeks["put_delta"]) - 1.0) < 1e-4

    # Gamma ~ 0.0188
    assert abs(greeks["gamma"] - 0.0188) < 1e-3, f"Gamma error: {greeks['gamma']}"

    # Vega ~ 37.5240
    assert abs(greeks["vega"] - 37.5240) < 1e-1, f"Vega error: {greeks['vega']}"

    # Theta: Call ~ -6.4140, Put ~ -1.6579
    assert abs(greeks["call_theta"] - (-6.4140)) < 1e-1, f"Call Theta error: {greeks['call_theta']}"
    assert abs(greeks["put_theta"] - (-1.6579)) < 1e-1, f"Put Theta error: {greeks['put_theta']}"

    # Rho: Call ~ 53.2325, Put ~ -41.8905
    assert abs(greeks["call_rho"] - 53.2325) < 1e-1, f"Call Rho error: {greeks['call_rho']}"
    assert abs(greeks["put_rho"] - (-41.8905)) < 1e-1, f"Put Rho error: {greeks['put_rho']}"

    print("[Testing] Greeks Boundary Conditions (Zero Maturity)...")
    expired_greeks = calculate_bsm_greeks(S=105.0, K=100.0, T=0.0, r=0.05, sigma=0.20)
    assert expired_greeks["call_delta"] == 1.0
    assert expired_greeks["put_delta"] == 0.0
    assert expired_greeks["gamma"] == 0.0

    print("[Testing] Dynamic Delta Neutral Hedging Simulation...")
    # 构造一条可控的合成离散标的价格路径 (N=100 步)
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
    # 验证期初权利金约 10.4506, Delta 约 0.6368
    assert abs(hedge_res["initial_call_premium"] - 10.4506) < 1e-3
    assert abs(hedge_res["initial_delta"] - 0.6368) < 1e-3

    # 在离散 100 步动态对冲下，跟踪残差应非常微小 (|PnL| < 1.0)
    print(f"Final Hedging PnL: {hedge_res['final_portfolio_pnl']}")
    assert abs(hedge_res["final_portfolio_pnl"]) < 1.0, f"Hedging tracking error too large: {hedge_res['final_portfolio_pnl']}"

    print("All assertions passed! Module 08 Lesson 02 verification successful.")
