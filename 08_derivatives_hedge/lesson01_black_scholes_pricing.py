r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 1 课：BSM 连续期权定价与平价公式

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握 Black-Scholes-Merton (BSM) 欧式期权偏微分方程（PDE）的经济学假设与解析闭式解推导；
2. 深刻理解看涨看跌期权平价公式（Put-Call Parity）的无套利现金流复制结构；
3. 掌握期权杠杆比率（Gearing Ratio / Lambda）与深度虚值期权剧烈百分比涨幅的微观机制；
4. 编写代码实现 BSM 看涨与看跌期权定价算法、平价校验与转换/反转套利（Reversal & Conversion）价差识别。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，阐述美式期权提前行权边界与套利锁利机制。

---
## 核心心智模型与数理推导

### 1. BSM 连续时间定价公式 (Black-Scholes-Merton, 1973)

假设标的资产现货价格 $S_t$ 服从几何布朗运动（GBM）：
$$
\frac{dS_t}{S_t} = \mu dt + \sigma dW_t
$$
构建由 1 份衍生品头寸 $V(S, t)$ 与 $-\Delta$ 份标的资产组成的无套利复制组合 $\Pi = V - \Delta S$。
依据伊藤引理（Itô's Lemma）展开并在瞬时消除布朗运动扰动项 $dW_t$，得到 BSM 偏微分方程：
$$
\frac{\partial V}{\partial t} + r S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - r V = 0
$$
对于欧式期权，边界条件为：
- 看涨期权（Call）：$C(S, T) = \max(S - K, 0)$
- 看跌期权（Put）：$P(S, T) = \max(K - S, 0)$

闭式解析解（Closed-form Solution）：
$$
\begin{aligned}
d_1 &= \frac{\ln(S / K) + (r + \frac{1}{2}\sigma^2)T}{\sigma \sqrt{T}} \\
d_2 &= d_1 - \sigma \sqrt{T} \\
C(S, K, T, r, \sigma) &= S N(d_1) - K e^{-rT} N(d_2) \\
P(S, K, T, r, \sigma) &= K e^{-rT} N(-d_2) - S N(-d_1)
\end{aligned}
$$
其中 $N(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^x e^{-u^2/2} du = \frac{1}{2} [1 + \text{erf}(x / \sqrt{2})]$ 为标准正态分布累积概率分布函数。

### 2. 看涨看跌期权平价公式 (Put-Call Parity)

考虑两个投资组合：
- **组合 A**：买入 1 份欧式看涨期权 $C$ + 持有面值 $K$ 的无风险零息债券（现值 $K e^{-rT}$）
- **组合 B**：买入 1 份欧式看跌期权 $P$ + 持有 1 股标的股票 $S$

在到期时刻 $T$：
- 若 $S_T > K$：组合 A 价值 $(S_T - K) + K = S_T$；组合 B 价值 $0 + S_T = S_T$
- 若 $S_T \le K$：组合 A 价值 $0 + K = K$；组合 B 价值 $(K - S_T) + S_T = K$

在所有可能状态下，两组合在到期时刻终值严格恒等。根据一价定律（Law of One Price），两者在 $t=0$ 时刻现值必须严格相等：
$$
C + K e^{-rT} = P + S \implies C - P = S - K e^{-rT}
$$
"""

import math
from typing import Tuple, Dict, Any


def standard_normal_cdf(x: float) -> float:
    """标准正态分布累积分布函数 N(x)"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bsm_call_put_price(S: float, K: float, T: float, r: float, sigma: float) -> Tuple[float, float]:
    """
    计算 BSM 欧式看涨与看跌期权理论价格。
    
    :param S: 标的现货价格 (Spot Price)
    :param K: 期权行权价格 (Strike Price)
    :param T: 距到期日剩余年化时间 (Time to Maturity, 年)
    :param r: 无风险连续复利年化利率 (Risk-free Rate)
    :param sigma: 标的资产年化波动率 (Volatility)
    :return: (call_price, put_price) 四舍五入保留 4 位小数
    """
    # TODO: 实现 BSM 解析解公式计算 call 与 put，并注意边界条件 (T<=0 或 sigma<=0)
    pass


def verify_put_call_parity(S: float, K: float, T: float, r: float, call_price: float, put_price: float, tolerance: float = 1e-4) -> Tuple[bool, float]:
    """
    校验看涨看跌期权平价关系：
    左侧 LHS = C - P
    右侧 RHS = S - K * exp(-r * T)
    差值 diff = LHS - RHS
    若 abs(diff) < tolerance 则平价关系成立。
    """
    # TODO: 计算 LHS 与 RHS 并计算 diff，返回 (is_valid, round(diff, 6))
    pass


def detect_parity_arbitrage(S: float, K: float, T: float, r: float, market_call: float, market_put: float, fee: float = 0.01) -> Dict[str, Any]:
    """
    根据实际期权市价检测 Put-Call Parity 套利机会。
    - 若 market_call - market_put > S - K*exp(-r*T) + fee:
      看涨期权被高估 -> 执行转换套利 (Conversion): 卖出 Call, 买入 Put, 买入股票 S, 借入现金 K*exp(-r*T)
    - 若 market_call - market_put < S - K*exp(-r*T) - fee:
      看跌期权被高估 (Call 被低估) -> 执行反转套利 (Reversal): 买入 Call, 卖出 Put, 融券卖出股票 S, 贷出资金
    """
    # TODO: 计算价差 spread = (market_call - market_put) - (S - K * exp(-r * T))
    # 依据 spread 与手续费 fee 阈值判断套利方向与收益
    pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么当期权处于极度深度虚值（Deep OTM）时，其绝对价格对标的微小变动极其迟钝，但一旦标的资产发生跳空异动，其百分比收益率可达数十倍甚至上百倍？

**你的答案：**
[在此处写下你的分析：需对比绝对 Delta 与有效杠杆倍数 Omega = Delta * (S/C)，并阐述 Gamma 凸性加速度在暴击时的非线性爆炸机理]


### Q2：在实际做市商交易柜台（Market Making Desk）中，当出现 Put-Call Parity 价差偏离时，做市商如何通过“转换套利（Conversion）”与“反转套利（Reversal）”实现完全无风险的锁利？

**你的答案：**
[在此处写下你的分析：需构建两组现金流对冲组合，推导到期结算矩阵，证明其在任何行情下到期终值严格归零锁利]


### Q3：为什么对于不支付股息（Non-dividend Paying）的股票，美式看涨期权（American Call）永远不应该提前行权，而美式看跌期权（American Put）在深度实值时提前行权是最优选择？

**你的答案：**
[在此处写下你的分析：需从时间价值、资金成本利息放弃、下行保底保护三个维度论证 Call；并从深度实值 Put 的最大赔付额利息折现损失论证提前行权必要性]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] BSM Call and Put Pricing...")
    S0, K0, T0, r0, sigma0 = 100.0, 100.0, 1.0, 0.05, 0.20
    call_p, put_p = bsm_call_put_price(S0, K0, T0, r0, sigma0)

    assert abs(call_p - 10.4506) < 1e-3, f"Expected 10.4506, got {call_p}"
    assert abs(put_p - 5.5735) < 1e-3, f"Expected 5.5735, got {put_p}"

    print("[Testing] Put-Call Parity Verification...")
    is_parity, diff = verify_put_call_parity(S0, K0, T0, r0, call_p, put_p)
    assert is_parity, f"Put-Call parity violated! diff: {diff}"
    assert abs(diff) < 1e-3

    print("[Testing] Boundary Conditions (Zero Maturity & Zero Vol)...")
    c_exp, p_exp = bsm_call_put_price(S=110.0, K=100.0, T=0.0, r=0.05, sigma=0.20)
    assert c_exp == 10.0
    assert p_exp == 0.0

    c_novol, p_novol = bsm_call_put_price(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.0)
    assert abs(c_novol - 4.8771) < 1e-3
    assert p_novol == 0.0

    print("[Testing] Put-Call Parity Arbitrage Detection...")
    arb1 = detect_parity_arbitrage(S=100.0, K=100.0, T=1.0, r=0.05, market_call=12.00, market_put=5.5735, fee=0.01)
    assert arb1["signal"] == "CONVERSION_ARBITRAGE"
    assert arb1["arbitrage_profit"] > 1.50

    arb2 = detect_parity_arbitrage(S=100.0, K=100.0, T=1.0, r=0.05, market_call=8.00, market_put=5.5735, fee=0.01)
    assert arb2["signal"] == "REVERSAL_ARBITRAGE"
    assert arb2["arbitrage_profit"] > 2.0

    arb_none = detect_parity_arbitrage(S=100.0, K=100.0, T=1.0, r=0.05, market_call=10.4506, market_put=5.5735, fee=0.01)
    assert arb_none["signal"] == "NO_ARBITRAGE"

    print("All assertions passed! Module 08 Lesson 01 verification successful.")
