r"""
# 模块 08：期权衍生品、希腊字母与波动率对冲 · 第 4 课：隐含波动率曲面、微笑偏度与 VIX 交易

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

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
    lower = low_vol
    upper = high_vol

    for _ in range(max_iter):
        mid = (lower + upper) / 2.0
        price = bsm_call_price(S, K, T, r, mid)
        diff = price - target_price

        if abs(diff) < tol:
            return round(mid, 4)

        if price < target_price:
            lower = mid
        else:
            upper = mid

    return round((lower + upper) / 2.0, 4)


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
    # 无套利区间校验
    lower_bound = max(0.0, S - K * math.exp(-r * T))
    if target_price <= lower_bound or target_price >= S:
        return 0.0

    vol = initial_vol
    for _ in range(max_iter):
        price = bsm_call_price(S, K, T, r, vol)
        diff = price - target_price

        if abs(diff) < tol:
            return round(vol, 4)

        vega = bsm_vega(S, K, T, r, vol)
        if vega < 1e-7:
            # 偏导太小，牛顿法失效，转用二分法保证鲁棒性
            return solve_iv_bisection(target_price, S, K, T, r)

        vol = vol - diff / vega

        # 越界保护
        if vol <= 0.001 or vol > 5.0:
            return solve_iv_bisection(target_price, S, K, T, r)

    return round(vol, 4)


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
    F = S * math.exp(r * T)

    # 寻找 K0: 小于或等于 F 的最高行权价
    strikes_below_f = [opt["strike"] for opt in option_chain if opt["strike"] <= F]
    if not strikes_below_f:
        K0 = option_chain[0]["strike"]
    else:
        K0 = max(strikes_below_f)

    total_variance_sum = 0.0
    n = len(option_chain)

    for i in range(n):
        K = option_chain[i]["strike"]

        # 计算 Delta K_i (行权价跨度)
        if i == 0:
            dK = option_chain[1]["strike"] - option_chain[0]["strike"]
        elif i == n - 1:
            dK = option_chain[-1]["strike"] - option_chain[-2]["strike"]
        else:
            dK = (option_chain[i + 1]["strike"] - option_chain[i - 1]["strike"]) / 2.0

        # 获取虚值期权市价 Q(K)
        if K < K0:
            Q = option_chain[i]["put_price"]
        elif K > K0:
            Q = option_chain[i]["call_price"]
        else:
            Q = (option_chain[i]["call_price"] + option_chain[i]["put_price"]) / 2.0

        total_variance_sum += (dK / (K * K)) * Q

    # 方差互换公式
    term1 = (2.0 * math.exp(r * T) / T) * total_variance_sum
    term2 = (1.0 / T) * math.pow((F / K0 - 1.0), 2)
    sigma_sq = term1 - term2

    vix = 100.0 * math.sqrt(max(0.0, sigma_sq))
    return round(vix, 2)


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么股票指数期权的隐含波动率曲面通常呈现明显的“左高右低”负偏斜（Negative Skewness / Volatility Smirk）？1987 年“黑色星期一”股灾前后该曲面发生了何种范式转变？

参考答案：
1. 崩盘恐惧与保险溢价（Crash-o-Phobia）：
   - 在股票市场中，资产价格的下行往往伴随着杠杆破裂、强平抛售以及极度流动性挤兑，呈现肥尾厚下行（Heavy Left Tail）特征。
   - 机构投资者为了对冲现货多头组合遭遇系统性暴跌的灭顶之灾，愿意支付显著高于纯正态分布理论价值的昂贵溢价去抢购深度虚值看跌期权（OTM Put）。
   - 相反，市场对极端暴涨的虚值看涨期权（OTM Call）需求平淡，甚至有大量基金通过 Covered Call 持续抛售 Call 压低其价格。
   - 供需力量的严重失衡直接导致了低行权价的 IV 显著高于高行权价的 IV，形成了“左高右低”的偏斜曲面（Volatility Skew）。
2. 1987 年“黑色星期一”的历史断层：
   - 在 1987 年 10 月之前，美股期权隐含波动率曲面相对平坦，基本符合 BSM 假定的几何布朗运动与对数正态分布。
   - 黑色星期一当天道指单日狂泻 22.6%，这一在正态分布下“数十亿年才出现一次”的事件彻底粉碎了经典假设。
   - 自此，衍生品市场永久性地为深度虚值 Put 嵌入了极高的肥尾恐慌溢价，波动率偏斜成为全球权益期权市场的永久印记。

### Q2：如何利用 VIX 期货的期限结构（Term Structure）状态（Contango 升水 vs Backwardation 贴水）识别市场由平静常态向流动性危机切换的临界点？

参考答案：
1. 常态下的升水结构（Contango）：
   - 在绝大多数平稳温和市场中，VIX 期限结构呈向上倾斜（Contango，即远月价格 > 近月价格）。
   - 经济学含义：未来的不确定性天然大于当下，远期波动率包含时间风险溢价（Time Premium）。做空近月波动率、做多远月对冲是机构常态策略。
2. 危机爆发时的深度贴水（Backwardation 倒挂）：
   - 一旦突发黑天鹅暴跌（如 2008 雷曼倒闭、2020 疫情熔断），恐慌盘在现货与近月期权市场集中不计成本踩踏抢购避险。
   - 现货 VIX 指数与近月期货瞬间从 15 垂直飙升至 50~80，而远月期货涨幅相对温和（远期预期均值回归）。
   - 期限结构瞬间发生剧烈倒挂（Backwardation，即近月价格远高于远月价格）。
   - **临界点预警机制**：当 VIX 近月/次月比价（VIX1/VIX2 Ratio）突破 1.0 并持续上行时，表明系统进入无序去杠杆与流动性危机，量化宏观基金应全面降低风险敞口。

### Q3：为什么普通散户长期持有做多 VIX 的杠杆/反向 ETF（如 UVXY / VXX）会导致本金几乎 100% 归零？这一结构性损耗如何被波动率套利基金反向利用？

参考答案：
1. 负展期收益（Negative Roll Yield）的慢性毒药：
   - VXX / UVXY 这类做多波动率的 ETF 并不直接持有不可交易的现货 VIX，而是通过每日滚动持有前两个月的 VIX 期货合约来模拟敞口。
   - 由于 VIX 期货在 80% 以上的时间里处于深度 Contango（远月比近月贵，例如近月 15，远月 16.5）；
   - ETF 基金经理为了维持固定的久期，必须每天机械化地“卖出即将到期的便宜近月合约，买入昂贵的溢价远月合约”（高买低卖）；
   - 这种固定的展期损耗（Roll Decay）每月可蚕食 5%~10% 的净值，一年复合损耗高达 50%~80%，即便偶有黑天鹅脉冲暴涨，长期来看净值曲线也是不可逆地趋近于零。
2. 波动率做空基金的收割逻辑：
   - 机构对冲基金（如做空波动率策略）通过动态对冲做空 VXX 或卖出虚值看涨期权，长期稳定收割这一由结构性 Contango 产生的“波动率风险溢价（VRP）”，
   - 但前提是必须配置严格的极值硬止损与尾部看跌期权保护，以防止单次黑天鹅脉冲直接打爆账户。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Implied Volatility Solvers (Newton vs Bisection)...")
    S0, K0, T0, r0, true_sigma = 100.0, 100.0, 1.0, 0.05, 0.20
    # 理论价格约为 10.4506
    target_p = bsm_call_price(S0, K0, T0, r0, true_sigma)
    assert abs(target_p - 10.4506) < 1e-3

    # 二分法反解
    iv_bisection = solve_iv_bisection(target_p, S0, K0, T0, r0)
    assert abs(iv_bisection - 0.2000) < 1e-3, f"Bisection IV error: {iv_bisection}"

    # 牛顿迭代反解
    iv_newton = solve_iv_newton_raphson(target_p, S0, K0, T0, r0, initial_vol=0.35)
    assert abs(iv_newton - 0.2000) < 1e-3, f"Newton IV error: {iv_newton}"

    print("[Testing] IV Boundary Conditions...")
    # 尝试求解低于内在价值的非法市价 -> 返回 0.0
    invalid_iv = solve_iv_newton_raphson(target_price=2.0, S=100.0, K=90.0, T=1.0, r=0.05)
    assert invalid_iv == 0.0

    print("[Testing] CBOE Simplified VIX Index Construction...")
    # 构建一个跨全截面行权价 (50 ~ 150) 的期权链，基准真实波动率设为 20% (0.20)
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
    # 由于生成期权链时的年化波动率固定为 20%，构建出的无模型 VIX 指数应当高度贴合 20.0 (误差 < 0.5)
    assert abs(vix_index - 20.0) < 0.5, f"VIX calculation deviated too much from 20.0: {vix_index}"

    print("All assertions passed! Module 08 Lesson 04 verification successful.")
