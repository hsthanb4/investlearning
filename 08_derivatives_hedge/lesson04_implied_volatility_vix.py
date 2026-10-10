r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 4 课：隐含波动率曲面、微笑偏度与 VIX 交易

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握隐含波动率（Implied Volatility, IV）的经济学内涵及其无法求出解析反函数的数理成因；
2. 熟练运用牛顿-拉夫逊（Newton-Raphson）迭代法与二分法数值反解欧式期权隐含波动率；
3. 深刻理解波动率微笑（Volatility Smile）与偏斜（Volatility Skew）背后反映的市场肥尾崩盘预期；
4. 掌握 CBOE VIX 恐慌指数的无模型（Model-Free）方差互换复制算法原理与简易指数构建。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，剖析 VIX 期限结构（Contango/Backwardation）及做多波动率产品的展期损耗陷阱。

---
## 核心心智模型与数理推导

### 1. 为什么隐含波动率无法直接解析求解？

在 BSM 模型中，欧式看涨期权价格是波动率 $\sigma$ 的单调增函数：
$$
\frac{\partial C}{\partial \sigma} = \text{Vega} = S \sqrt{T} \phi(d_1) > 0
$$
由于 $d_1$ 和 $d_2$ 中包含对数项与平方项，$\sigma$ 同时出现在高斯积分限与指数分母中，属于典型的非线性超越方程，不存在闭式解析反解 $\sigma = f^{-1}(C_{\text{market}})$。
必须使用数值方法逼近求解：
- **牛顿-拉夫逊迭代法（Newton-Raphson）**：
  二阶收敛速度极快：
  $$
  \sigma_{k+1} = \sigma_k - \frac{C(\sigma_k) - C_{\text{market}}}{\text{Vega}(\sigma_k)}
  $$
- **二分法（Bisection）**：
  只要 $C_{\text{market}}$ 处于无套利区间 $\max(0, S - K e^{-rT}) < C_{\text{market}} < S$，在区间 $[\sigma_{\min}, \sigma_{\max}]$ 内二分必定收敛。

### 2. CBOE VIX 指数的无模型方差复制原理 (Model-Free Implied Volatility)

CBOE 在 2003 年彻底淘汰了基于平值 BSM 反解的旧版 VIX，改用基于连续执行价格期权积分的无模型方差互换（Variance Swap）复制框架。
其核心原理来源于 Carr & Madan (1998) 展开定理：
标的资产对数收益的二阶方差，可以通过跨全截面行权价的看涨与看跌期权组合完全无模型静态复制：
$$
\sigma_{\text{VIX}}^2 = \frac{2 e^{r T}}{T} \sum_i \frac{\Delta K_i}{K_i^2} Q(K_i) - \frac{1}{T} \left( \frac{F}{K_0} - 1 \right)^2
$$
其中：
- $F = S e^{r T}$ 为远期平价指数价格；
- $K_0$ 为小于或等于 $F$ 的最高期权行权价；
- $Q(K_i)$ 为行权价 $K_i$ 对应的虚值期权市价（$K_i < K_0$ 时为 Put，$K_i > K_0$ 时为 Call，$K_0$ 时为 Call 与 Put 的均值）；
- $\Delta K_i = \frac{K_{i+1} - K_{i-1}}{2}$ 为行权价间距；
- 最终年化波动率指数：$\text{VIX} = 100 \times \sqrt{\sigma_{\text{VIX}}^2}$。
"""

import math
from typing import List, Dict, Any, Tuple


def standard_normal_pdf(x: float) -> float:
    """标准正态分布概率密度函数 phi(x)"""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)


def standard_normal_cdf(x: float) -> float:
    """标准正态分布累积分布函数 N(x)"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bsm_call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """BSM 欧式看涨期权理论定价"""
    if T <= 0.0:
        return max(0.0, S - K)
    if sigma <= 1e-6:
        return max(0.0, S - K * math.exp(-r * T))

    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * standard_normal_cdf(d1) - K * math.exp(-r * T) * standard_normal_cdf(d2)


def bsm_vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """期权 Vega"""
    if T <= 0.0 or sigma <= 1e-6:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    return S * standard_normal_pdf(d1) * math.sqrt(T)


def solve_iv_bisection(
    target_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    low_vol: float = 0.001,
    high_vol: float = 4.0,
    tol: float = 1e-5,
    max_iter: int = 100
) -> float:
    """
    使用二分法求解隐含波动率 (IV)。
    """
    # TODO: 实现二分法搜索，每次取区间中点计算理论价格，并收缩上下界
    pass


def solve_iv_newton_raphson(
    target_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    initial_vol: float = 0.25,
    tol: float = 1e-6,
    max_iter: int = 50
) -> float:
    """
    使用牛顿-拉夫逊法 (Newton-Raphson) 二阶快速迭代求解隐含波动率 (IV)。
    若 Vega 接近 0 或跳出边界，自动平滑退化为二分法。
    """
    # TODO: 实现牛顿迭代 vol = vol - (price - target_price) / vega，注意防止除以零或越界
    pass


def calculate_simplified_vix(
    S: float,
    r: float,
    T: float,
    option_chain: List[Dict[str, float]]
) -> float:
    """
    依据 CBOE 官方无模型方差互换复制框架计算简易 VIX 指数。
    
    :param S: 标的指数现价
    :param r: 无风险利率
    :param T: 期限 (例如 30/365 年)
    :param option_chain: 升序排列的期权截面链表，每项为:
           {"strike": K, "call_price": C, "put_price": P}
    :return: 年化 VIX 指数点位 (如 20.20 代表 20.20%)
    """
    # TODO:
    # 1. 计算远期价格 F = S * exp(r * T)
    # 2. 找到 K0 (小于等于 F 的最高行权价)
    # 3. 遍历 option_chain，根据行权价跨度 dK 与虚值价格 Q(K) 累加方差贡献: (dK / K^2) * Q(K)
    # 4. 根据方差互换公式求 sigma^2，开根号并乘以 100 输出 VIX 指数
    pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么股票指数期权的隐含波动率曲面通常呈现明显的“左高右低”负偏斜（Negative Skewness / Volatility Smirk）？1987 年“黑色星期一”股灾前后该曲面发生了何种范式转变？

**你的答案：**
[在此处写下你的分析：需阐述机构抢购虚值 Put 避险引发的崩盘恐慌溢价，以及 1987 年股灾对 BSM 对数正态分布假设的颠覆性重构]


### Q2：如何利用 VIX 期货的期限结构（Term Structure）状态（Contango 升水 vs Backwardation 贴水）识别市场由平静常态向流动性危机切换的临界点？

**你的答案：**
[在此处写下你的分析：需对比平静期远期时间溢价向上倾斜特征，与危机爆发时近月现货踩踏飙升引发的倒挂结构]


### Q3：为什么普通散户长期持有做多 VIX 的杠杆/反向 ETF（如 UVXY / VXX）会导致本金几乎 100% 归零？这一结构性损耗如何被波动率套利基金反向利用？

**你的答案：**
[在此处写下你的分析：需推导期货深度 Contango 结构下每日高买低卖的负展期损耗（Roll Decay），并分析做空波动率基金收割 VRP 的交易逻辑]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Implied Volatility Solvers (Newton vs Bisection)...")
    S0, K0, T0, r0, true_sigma = 100.0, 100.0, 1.0, 0.05, 0.20
    target_p = bsm_call_price(S0, K0, T0, r0, true_sigma)
    assert abs(target_p - 10.4506) < 1e-3

    iv_bisection = solve_iv_bisection(target_p, S0, K0, T0, r0)
    assert abs(iv_bisection - 0.2000) < 1e-3, f"Bisection IV error: {iv_bisection}"

    iv_newton = solve_iv_newton_raphson(target_p, S0, K0, T0, r0, initial_vol=0.35)
    assert abs(iv_newton - 0.2000) < 1e-3, f"Newton IV error: {iv_newton}"

    print("[Testing] IV Boundary Conditions...")
    invalid_iv = solve_iv_newton_raphson(target_price=2.0, S=100.0, K=90.0, T=1.0, r=0.05)
    assert invalid_iv == 0.0

    print("[Testing] CBOE Simplified VIX Index Construction...")
    test_chain = []
    T_vix = 30.0 / 365.0
    for strike_int in range(50, 152, 2):
        K_val = float(strike_int)
        d1 = (math.log(S0 / K_val) + (r0 + 0.5 * true_sigma * true_sigma) * T_vix) / (true_sigma * math.sqrt(T_vix))
        d2 = d1 - true_sigma * math.sqrt(T_vix)
        call_val = S0 * standard_normal_cdf(d1) - K_val * math.exp(-r0 * T_vix) * standard_normal_cdf(d2)
        put_val = K_val * math.exp(-r0 * T_vix) * standard_normal_cdf(-d2) - S0 * standard_normal_cdf(-d1)
        test_chain.append({"strike": K_val, "call_price": call_val, "put_price": put_val})

    vix_index = calculate_simplified_vix(S=S0, r=r0, T=T_vix, option_chain=test_chain)
    print(f"Calculated Simplified VIX Index: {vix_index}")
    assert abs(vix_index - 20.0) < 0.5, f"VIX calculation deviated too much from 20.0: {vix_index}"

    print("All assertions passed! Module 08 Lesson 04 verification successful.")
