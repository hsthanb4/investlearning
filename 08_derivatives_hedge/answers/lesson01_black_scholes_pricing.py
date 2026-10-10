r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 1 课：BSM 连续期权定价与平价公式

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

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
    if T <= 0.0:
        call = max(0.0, S - K)
        put = max(0.0, K - S)
        return round(call, 4), round(put, 4)

    if sigma <= 0.0:
        disc_k = K * math.exp(-r * T)
        call = max(0.0, S - disc_k)
        put = max(0.0, disc_k - S)
        return round(call, 4), round(put, 4)

    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call = S * standard_normal_cdf(d1) - K * math.exp(-r * T) * standard_normal_cdf(d2)
    put = K * math.exp(-r * T) * standard_normal_cdf(-d2) - S * standard_normal_cdf(-d1)

    return round(call, 4), round(put, 4)


def verify_put_call_parity(S: float, K: float, T: float, r: float, call_price: float, put_price: float, tolerance: float = 1e-4) -> Tuple[bool, float]:
    """
    校验看涨看跌期权平价关系：
    左侧 LHS = C - P
    右侧 RHS = S - K * exp(-r * T)
    差值 diff = LHS - RHS
    若 abs(diff) < tolerance 则平价关系成立。
    """
    lhs = call_price - put_price
    rhs = S - K * math.exp(-r * T)
    diff = lhs - rhs
    is_valid = abs(diff) < tolerance
    return is_valid, round(diff, 6)


def detect_parity_arbitrage(S: float, K: float, T: float, r: float, market_call: float, market_put: float, fee: float = 0.01) -> Dict[str, Any]:
    """
    根据实际期权市价检测 Put-Call Parity 套利机会。
    - 若 market_call - market_put > S - K*exp(-r*T) + fee:
      看涨期权被高估 -> 执行转换套利 (Conversion): 卖出 Call, 买入 Put, 买入股票 S, 借入现金 K*exp(-r*T)
    - 若 market_call - market_put < S - K*exp(-r*T) - fee:
      看跌期权被高估 (Call 被低估) -> 执行反转套利 (Reversal): 买入 Call, 卖出 Put, 融券卖出股票 S, 贷出资金
    """
    lhs = market_call - market_put
    rhs = S - K * math.exp(-r * T)
    spread = lhs - rhs

    if spread > fee:
        profit = spread - fee
        return {
            "signal": "CONVERSION_ARBITRAGE",
            "spread": round(spread, 4),
            "arbitrage_profit": round(profit, 4),
            "action": "Sell Call + Buy Put + Buy Stock + Borrow Cash"
        }
    elif spread < -fee:
        profit = -spread - fee
        return {
            "signal": "REVERSAL_ARBITRAGE",
            "spread": round(spread, 4),
            "arbitrage_profit": round(profit, 4),
            "action": "Buy Call + Sell Put + Short Stock + Lend Cash"
        }
    else:
        return {
            "signal": "NO_ARBITRAGE",
            "spread": round(spread, 4),
            "arbitrage_profit": 0.0,
            "action": "Hold"
        }


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么当期权处于极度深度虚值（Deep OTM）时，其绝对价格对标的微小变动极其迟钝，但一旦标的资产发生跳空异动，其百分比收益率可达数十倍甚至上百倍？

参考答案：
1. Delta 绝对敏感度 vs 有效杠杆倍数（Omega / Gearing）：
   - 欧式期权 Delta $\Delta = \frac{\partial C}{\partial S} = N(d_1)$。对于深度虚值看涨期权（如 $S=100, K=150$），$d_1 \ll 0$，此时 $\Delta \to 0$（例如 $\Delta = 0.02$）。标的股票变动 1 美元，期权绝对价格仅上涨 0.02 美元，绝对价格看似极其迟钝。
   - 然而，衡量衍生品收益弹性的指标是有效杠杆比率 $\Omega = \frac{\% \Delta C}{\% \Delta S} = \Delta \times \frac{S}{C}$。
     因为深度虚值期权自身价值极小（如 $C = 0.05$ 美元），其有效杠杆 $\Omega = 0.02 \times \frac{100}{0.05} = 40$ 倍。
2. Gamma 凸性与加速度爆发（Convexity Explosion）：
   当标的资产发生大幅同向暴涨时，二阶导数 Gamma 迅速将微小的 Delta 放大为 0.2、0.5 乃至接近 1.0。
   伴随隐含波动率在暴涨中的非线性飙升（Vega 溢价），期权价格从 0.05 快速暴涨至 5.00，实现 100 倍（10,000%）的非线性收益。

### Q2：在实际做市商交易柜台（Market Making Desk）中，当出现 Put-Call Parity 价差偏离时，做市商如何通过“转换套利（Conversion）”与“反转套利（Reversal）”实现完全无风险的锁利？

参考答案：
1. 转换套利（Conversion Arbitrage）：
   - 触发条件：看涨期权市价过高，即 $C - P > S - K e^{-rT}$。
   - 执行操作：卖出高估的看涨期权 $C$（收取权利金），买入低估的看跌期权 $P$（支付权利金），同时在现货市场以 $S$ 买入标的股票，并按无风险利率 $r$ 借入资金 $K e^{-rT}$。
   - 到期现金流结算：
     若到期 $S_T \ge K$：看涨期权被行权，以 $K$ 卖出手中股票；
     若到期 $S_T < K$：行使看跌期权，同样以 $K$ 卖出手中股票。
     在任意情况下，到期收回现金 $K$，刚好偿还借款本息 $K$。
     开仓时刻锁定的无风险净现金流：$(C - P) - (S - K e^{-rT}) > 0$，无惧未来任何市场风浪。
2. 反转套利（Reversal Arbitrage）：
   - 触发条件相反（看跌期权过高或看涨过低），通过反向构造：买入 Call、卖出 Put、融券卖出股票并出借现金，锁定瞬时套利利差。

### Q3：为什么对于不支付股息（Non-dividend Paying）的股票，美式看涨期权（American Call）永远不应该提前行权，而美式看跌期权（American Put）在深度实值时提前行权是最优选择？

参考答案：
1. 美式看涨期权永远不应提前行权：
   - 期权总价值 = 内在价值（Intrinsic Value） + 时间价值（Time Value）。
   - 若提前行权，持有者仅能获得内在价值 $\max(S - K, 0)$，意味着无偿放弃了所有正的时间价值（Time Premium $> 0$）；
   - 此外，提前行权需要立刻支付行权价现金 $K$，丧失了将现金存入银行获取无风险利息 $r$ 的货币时间价值；
   - 维持期权持仓还拥有下行有限损失保护（Downside Protection）。若交易者急需平仓，在二级市场直接卖出期权所得现金必定大于提前行权的内在价值。
2. 美式看跌期权在深度实值时提前行权最优：
   - 看跌期权的内在价值为 $K - S$。当标的资产暴跌接近 0（如破产重组 $S \to 0$）时，内在价值逼近理论最大值 $K$。
   - 此时若等到到期日再行权，投资者相当于把应得的现金 $K$ 延期到期末才收取，白白损失了高达 $K(1 - e^{-rT})$ 的无风险利息！
   - 当资金的时间价值损失超过期权剩余的极微小保护价值时，提前行权将现金 $K$ 兑现存入银行，净收益更高。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] BSM Call and Put Pricing...")
    S0, K0, T0, r0, sigma0 = 100.0, 100.0, 1.0, 0.05, 0.20
    call_p, put_p = bsm_call_put_price(S0, K0, T0, r0, sigma0)

    # 理论价格校验 (Call ~ 10.4506, Put ~ 5.5735)
    assert abs(call_p - 10.4506) < 1e-3, f"Expected 10.4506, got {call_p}"
    assert abs(put_p - 5.5735) < 1e-3, f"Expected 5.5735, got {put_p}"

    print("[Testing] Put-Call Parity Verification...")
    is_parity, diff = verify_put_call_parity(S0, K0, T0, r0, call_p, put_p)
    assert is_parity, f"Put-Call parity violated! diff: {diff}"
    assert abs(diff) < 1e-3

    print("[Testing] Boundary Conditions (Zero Maturity & Zero Vol)...")
    # 到期日 T = 0
    c_exp, p_exp = bsm_call_put_price(S=110.0, K=100.0, T=0.0, r=0.05, sigma=0.20)
    assert c_exp == 10.0
    assert p_exp == 0.0

    # 波动率 sigma = 0
    c_novol, p_novol = bsm_call_put_price(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.0)
    # K * exp(-r*T) = 100 * exp(-0.05) = 95.1229 -> call = 100 - 95.1229 = 4.8771
    assert abs(c_novol - 4.8771) < 1e-3
    assert p_novol == 0.0

    print("[Testing] Put-Call Parity Arbitrage Detection...")
    # 模拟 Call 被显著高估 (市场价 12.00, 理论价 10.45) -> 转换套利
    arb1 = detect_parity_arbitrage(S=100.0, K=100.0, T=1.0, r=0.05, market_call=12.00, market_put=5.5735, fee=0.01)
    assert arb1["signal"] == "CONVERSION_ARBITRAGE"
    assert arb1["arbitrage_profit"] > 1.50

    # 模拟 Call 被显著低估 (市场价 8.00) -> 反转套利
    arb2 = detect_parity_arbitrage(S=100.0, K=100.0, T=1.0, r=0.05, market_call=8.00, market_put=5.5735, fee=0.01)
    assert arb2["signal"] == "REVERSAL_ARBITRAGE"
    assert arb2["arbitrage_profit"] > 2.0

    # 无套利区间
    arb_none = detect_parity_arbitrage(S=100.0, K=100.0, T=1.0, r=0.05, market_call=10.4506, market_put=5.5735, fee=0.01)
    assert arb_none["signal"] == "NO_ARBITRAGE"

    print("All assertions passed! Module 08 Lesson 01 verification successful.")
