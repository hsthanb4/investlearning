r"""
================================================================================
模块 08：期权衍生品与波动率对冲 · 第 1/4 课
第 1 课：BSM 连续时间期权定价与平价公式无套利校验 (Black-Scholes-Merton & Put-Call Parity)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：衍生品定价的第一性原理不是预测，而是无套利复制
在量化金融历史上，Black-Scholes-Merton (1973) 模型的划时代意义并非提供了一个‘预测未来股价的占卜算式’，而是证明了：在连续时间无摩擦假设下，通过持有衍生品头寸并以动态 Delta 比例做空标的股票，可构造出一个完全消除几何布朗运动随机微元 $dW_t$ 的瞬时确定性组合。根据无套利一价定律（Law of One Price），该组合的瞬时资本回报率必须精确恒等于无风险利率 $r$。
:::

- **[风险中性测度的商业本质]**：期权公允估值与投资者对标的股票的主观预期收益率 $\mu$ 毫无数学关联。期权价值完全由无风险贴现折现率 $r$、到期期限 $T$ 以及价格扩散方差 $\sigma^2$ 共同锁定。
- **[平价天平的刚性约束]**：欧式看涨与看跌期权通过标的资产和零息国债贴现紧密锚定（$C - P = S - K e^{-rT}$）。做市商无需主观预测方向，任何打破平价的微小脱节都会被程序化转换/反转套利（Conversion / Reversal）光速推平。
- **[凸性溢价与非线性杠杆]**：期权赋予了持有者‘收益上行敞开、损失下行有界’的非对称凸性回报。这种非线性权利在金融物理学中必须通过支付时间价值（Theta 损耗）作为对价。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了 BSM 偏微分方程（PDE）构建无套利自融资组合消除随机扰动的微观机制。

```mermaid
flowchart TD
    Port["构建复制组合 Π = V(S,t) - Δ·S"] --> Ito["多元伊藤引理 (Itô's Lemma) 展开"]
    Ito --> Diff["dΠ = [∂V/∂t + μS ∂V/∂S + ½σ²S² ∂²V/∂S² - μS Δ] dt + [∂V/∂S - Δ] σS dW"]
    Diff --> Cancel{"令 Δ = ∂V/∂S (Delta 中性)"}
    Cancel --> Clean["布朗扰动项 [∂V/∂S - Δ] σS dW ≡ 0 (随机项彻底蒸发!)"]
    Clean --> NoArb["根据无套利原则: dΠ 必须精确等于 r·Π dt"]
    NoArb --> PDE["推导出 BSM 偏微分方程: ∂V/∂t + rS ∂V/∂S + ½σ²S² ∂²V/∂S² = rV"]
```

- **[要点 1：布朗噪声的纳秒级剥离]**：通过严格令 $\Delta = \frac{\partial V}{\partial S}$，组合在瞬时时间步 $dt$ 内完全摆脱了价格随机波动的牵制，变成绝对确定性资产。
- **[要点 2：资本成本 WACC 的无风险锚定]**：因为组合不存在任何特质方差或市场系统性风险，其预期收益率必须等于无风险短期国债收益率 $r$。
- **[要点 3：偏微分方程与边界条件闭式解]**：结合到期清算收益边界 $\max(S_T - K, 0)$，通过热传导方程变量替换即可解析求解出著名的 BSM 闭式公式。

锚点指引：下图展示了看涨看跌平价公式（Put-Call Parity）的无套利天平结构与套利边界。

```mermaid
flowchart LR
    subgraph 资产组合 A
        C["买入 Call (C)"]
        Bond["持有无风险零息债券 (K·e^-rT)"]
    end
    subgraph 资产组合 B
        P["买入 Put (P)"]
        Stock["买入标的股票 (S)"]
    end
    C & Bond --> PayoffA["到期现金流: max(S_T, K)"]
    P & Stock --> PayoffB["到期现金流: max(S_T, K)"]
    PayoffA -.严格恒等.- PayoffB
```

- **[要点 1：到期现金流状态全集复制]**：无论到期时刻标的股价暴涨至天际还是暴跌至归零，组合 A 与组合 B 的终值在所有可能状态下精确恒等。
- **[要点 2：转换套利无风险锁利]**：当市场 Call 价格过高打破平衡时，做市商做空 Call、做多 Put、做多股票并借入贴现现金，实现无风险确定性套利。
- **[要点 3：反转套利抹平贴水]**：当市场 Put 价格过高时，做市商反向操作融券做空股票并买入 Call，迫使二级市场定价迅速回归均衡中枢。

【数学与估值模型】
Black-Scholes-Merton 欧式期权闭式解析解：
$$
C(S, K, T, r, \sigma) = S N(d_1) - K e^{-rT} N(d_2)
$$
$$
P(S, K, T, r, \sigma) = K e^{-rT} N(-d_2) - S N(-d_1)
$$
$$
d_1 = \frac{\ln(S / K) + (r + \frac{1}{2}\sigma^2)T}{\sigma \sqrt{T}}, \quad d_2 = d_1 - \sigma \sqrt{T}
$$
变量定义域与参数约束：
- $S, K > 0$：标的现货价格与期权执行价格（USD 或 RMB）。
- $T > 0$：距到期日剩余年化时间（年，$T = \text{Days} / 365$）。若 $T = 0$，期权退化为内在价值 $C = \max(S-K, 0), P = \max(K-S, 0)$。
- $r \ge 0$：无风险连续复利年化利率。
- $\sigma > 0$：标的资产年化隐含波动率。若 $\sigma = 0$，期权价值由内在折现值完全确定。
- $N(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^x e^{-u^2/2} du$ 为标准正态累积分布函数。

Put-Call Parity 平价无套利约束方程：
$$
C - P = S - K e^{-rT} \iff \text{Spread} = (C - P) - (S - K e^{-rT}) \equiv 0
$$
套利触发阈值：$|\text{Spread}| > \text{Fee}_{\text{roundtrip}}$。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **模型假设与肥尾断裂风险**：BSM 假设标的对数收益率严格服从正态分布且波动率恒定，实盘中跳空跳跃与黑天鹅暴跌将导致深虚期权理论值严重低估真实崩盘概率。
2. **美式期权提前行权陷阱**：对于不分红股票，美式 Call 永远不应提前行权；但对于深度实值美式 Put，提前行权以落袋现金赚取利息是严格最优策略。
3. **交易摩擦与转换套利容量**：平价套利必须扣除双边融券利息成本、冲击滑点与借券不可得（Hard-to-Borrow）风险，严禁无视微观摩擦进行理论套利。
:::

【思考题】
Q1: 为什么当期权处于极度深度虚值（Deep OTM）时，其绝对价格对标的微小变动极其迟钝，但一旦标的资产发生跳空异动，其百分比收益率可达数十倍甚至上百倍？
Q2: 在实际做市商交易柜台（Market Making Desk）中，当出现 Put-Call Parity 价差偏离时，做市商如何通过“转换套利（Conversion）”与“反转套利（Reversal）”实现完全无风险的锁利？
Q3: 为什么对于不支付股息（Non-dividend Paying）的股票，美式看涨期权（American Call）永远不应该提前行权，而美式看跌期权（American Put）在深度实值时提前行权是最优选择？

【考核与通过规则】
- 代码填空并通过所有自动化单元测试断言：4 分
- Q1~Q3 问答题深入推导并符合投决会专业标准：各 2 分（共 6 分）
- 综合通过线：8/10 分
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
    """
    # TODO: 检测转换套利与反转套利
    pass


if __name__ == "__main__":
    print("Lesson 01 (BSM Option Pricing) Stub Initialized.")
