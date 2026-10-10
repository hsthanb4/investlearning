r"""
================================================================================
模块 08：期权衍生品与波动率对冲 · 第 4/4 课
第 4 课：隐含波动率曲面、微笑偏度与 CBOE VIX 指数无模型复制 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：波动率不是静态常数，而是不可被正态分布规训的随机过程
Black-Scholes-Merton 模型的最大原罪在于假设资产价格扩散服从单一固定波动率（$\sigma = \text{const}$）的几何布朗运动。然而 1987 年“黑色星期一”股灾证明，金融市场的实际收益分布具有严重的肥尾厚下行（Fat Tail）与偏度。市场交易员在期权盘口自发报出的隐含波动率（Implied Volatility, IV）沿行权价呈现“左高右低”的偏斜曲面（Volatility Skew / Smirk）。CBOE VIX 恐慌指数彻底淘汰了 BSM 反解模型，改用跨全截面虚值期权链的无模型方差互换（Model-Free Variance Swap）静态复制框架，为全市场提供了纯粹的未来 30 天期望方差物理定价。
:::

- **[超越方程与数值求根必然性]**：隐含波动率 $\sigma$ 同时出现在高斯积分上下限 $d_1, d_2$ 与指数分母中，不存在闭式解析反函数，必须使用牛顿-拉夫逊（Newton-Raphson）二阶迭代或二分法数值逼近。
- **[偏度背后反映的崩盘恐慌溢价（Crash-o-Phobia）]**：机构投资者常年抢购深度虚值看跌期权（OTM Put）以对冲现货多头的灭顶之灾，供需失衡导致低行权价期权的 IV 包含了极高的肥尾恐慌溢价。
- **[无模型方差复制的第一性原理]**：根据 Carr & Madan (1998) 展开定理，对数合同 $\ln(S_T / F)$ 的二阶展开可通过行权价反比平方 $1/K^2$ 加权的跨式期权链完全静态复制，彻底脱离任何特定随机游走假设。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了外汇对称波动率微笑（Smile）与美股指数左偏斜（Crash Skew）的几何形态对比。

```mermaid
flowchart TD
    subgraph 衍生品市场微观结构
        FX["外汇市场 (Forex) ➔ 双向跳跃对称 ➔ 经典波动率微笑 (Smile)"]
        EQ["权益市场 (S&P 500) ➔ 杠杆崩盘非对称 ➔ 左高右低负偏斜 (Skew)"]
    end
    subgraph 隐含波动率曲面特征
        FX --> S_Curve["虚值 Put 与虚值 Call 拥有大致相等的凸性溢价"]
        EQ --> K_Curve["深度虚值 Put (OTM Put) 价格奇贵 / 虚值 Call 价格低廉"]
    end
```

- **[要点 1：黑色星期一前后的范式巨震]**：1987 年以前美股期权曲面相对平坦；股灾当天道指狂泻 22.6% 彻底击碎正态假设，从此虚值 Put 溢价永久固化。
- **[要点 2：杠杆效应与流动性挤兑反馈]**：股票下跌伴随着公司财务杠杆上升与融资平仓踩踏，负偏斜曲面真实映射了资产下行与波动率飙升的高度负相关。
- **[要点 3：局部波动率与随机波动率模型]**：为拟合这一微笑偏斜，现代工业界全面演进为 Dupire 局部波动率（Local Vol）与 Heston 随机波动率模型。

锚点指引：下图揭示了 CBOE VIX 指数利用 $1/K^2$ 权重对全截面虚值期权进行方差互换静态积分的数学架构。

```mermaid
flowchart LR
    A["截面期权链 (Strikes K_1 ... K_N)"] --> B["行权价反比平方加权: w(K) = ΔK / K²"]
    B --> C["获取全截面虚值市价 Q(K):<br/>K < K0 采用 Put / K > K0 采用 Call"]
    C --> D["贴现求和: (2·e^rT / T) · Σ w(K)·Q(K) - (1/T)·(F/K0 - 1)²"]
    D --> E["年化标准差换算: VIX = 100 × √σ² (30天年化波动率)"]
```

- **[要点 1：行权价越低权重越高]**：$1/K^2$ 的权重衰减保证了虚值 Put 在极端下行时拥有最高的敏感度，契合方差互换对数收益的泰勒展开余项。
- **[要点 2：虚值期权流动性遴选规则]**：仅选取连续双边报价非零的流动性合约，在平价 $K_0$ 附近平滑拼接 Call 与 Put，完全消除了单个模型的假设偏误。
- **[要点 3：VIX 期限结构的升贴水密码]**：常态下远月高于近月（Contango），做多 VIX 的 ETF（如 UVXY）每月承担 5%~10% 的结构性展期损耗，长期几乎必然归零。

【数学与估值模型】
隐含波动率牛顿-拉夫逊数值反解迭代式：
$$
\sigma_{k+1} = \sigma_k - \frac{C_{\text{BSM}}(S, K, T, r, \sigma_k) - C_{\text{market}}}{\nu_{\text{BSM}}(S, K, T, r, \sigma_k)}
$$
变量定义域与参数约束：
- $\sigma \in (0.001, 5.0]$：初始试探点通常取 $\sigma_0 \in [0.20, 0.40]$。
- 临界收敛判据：$|C_{\text{BSM}}(\sigma_k) - C_{\text{market}}| < 10^{-5}$。
- 若 $\nu < 10^{-7}$（Vega 极小导致导数失效），系统自动平滑降级为二分法（Bisection）。

CBOE 无模型 30 天期望方差互换复制方程：
$$
\sigma_{\text{VIX}}^2 = \frac{2 e^{r T}}{T} \sum_{i=1}^n \frac{\Delta K_i}{K_i^2} Q(K_i) - \frac{1}{T} \left( \frac{F}{K_0} - 1 \right)^2
$$
$$
\text{VIX} = 100 \times \sqrt{\max(0, \sigma_{\text{VIX}}^2)}
$$
变量定义域：$F = S e^{rT}$，$K_0 \le F$ 为最高行权价，$\Delta K_i = \frac{K_{i+1} - K_{i-1}}{2}$，$Q(K_i)$ 为虚值期权报价。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **持有 UVXY / VXX 长期做多波动率的归零陷阱**：VIX 处于 80% 时间段的 Contango 结构，基金每日卖近月买远月产生巨大展期负收益（Roll Decay），一年复合损耗高达 60% 以上。
2. **Volmageddon（波动率末日）踩踏风险**：2018 年 2 月做空 VIX 的反向产品（如 XIV）在单日内暴跌 95% 触发清盘，证明了 Short Vol 必须具备严格的动态止损与尾部看跌防灾底线。
3. **二分法与牛顿法边界失效**：当输入的市场市价低于期权内在折现价值（违背无套利下界）时，任何数值算法都无法反解出实数波动率，必须预先进行数据纯净度过滤。
:::

【思考题】
Q1: 为什么股票指数期权的隐含波动率曲面通常呈现明显的“左高右低”负偏斜（Negative Skewness / Volatility Smirk）？1987 年“黑色星期一”股灾前后该曲面发生了何种范式转变？
Q2: 如何利用 VIX 期货的期限结构（Term Structure）状态（Contango 升水 vs Backwardation 贴水）识别市场由平静常态向流动性危机切换的临界点？
Q3: 为什么普通散户长期持有做多 VIX 的杠杆/反向 ETF（如 UVXY / VXX）会导致本金几乎 100% 归零？这一结构性损耗如何被波动率套利基金反向利用？

【Q1 深度参考答案】
- **[崩盘恐惧与保险溢价（Crash-o-Phobia）]**：在股票市场中，资产价格的下行往往伴随着杠杆破裂、强平抛售以及极度流动性挤兑，呈现肥尾厚下行（Heavy Left Tail）特征。机构投资者为了对冲现货多头组合遭遇系统性暴跌的灭顶之灾，愿意支付显著高于纯正态分布理论价值的昂贵溢价去抢购深度虚值看跌期权（OTM Put）。
- **[供需失衡驱动偏斜曲面固化]**：市场对极端暴涨的虚值看涨期权（OTM Call）需求平淡，甚至有大量基金通过 Covered Call 持续抛售 Call 压低其价格。供需力量的严重失衡直接导致了低行权价的 IV 显著高于高行权价的 IV，形成了“左高右低”的偏斜曲面（Volatility Skew）。
- **[1987 年黑色星期一的历史断层]**：在 1987 年 10 月之前，美股期权隐含波动率曲面相对平坦，基本符合 BSM 假定的几何布朗运动。黑色星期一当天道指单日狂泻 22.6%，这一在正态分布下“数十亿年才出现一次”的事件彻底粉碎了经典假设。自此，衍生品市场永久性地为深度虚值 Put 嵌入了极高的肥尾恐慌溢价。

【Q2 深度参考答案】
- **[常态下的升水结构（Contango）特征]**：在绝大多数平稳温和市场中，VIX 期限结构呈向上倾斜（Contango，即远月价格 > 近月价格）。未来的不确定性天然大于当下，远期波动率包含时间风险溢价（Time Premium）。做空近月波动率、做多远月对冲是机构常态策略。
- **[危机爆发时的深度贴水（Backwardation 倒挂）]**：一旦突发黑天鹅暴跌（如 2008 雷曼倒闭、2020 疫情熔断），恐慌盘在现货与近月期权市场集中不计成本踩踏抢购避险。现货 VIX 指数与近月期货瞬间从 15 垂直飙升至 50~80，而远月期货涨幅相对温和（远期预期均值回归），期限结构瞬间发生剧烈倒挂（Backwardation）。
- **[临界点预警机制与风险切断]**：当 VIX 近月/次月比价（VIX1/VIX2 Ratio）突破 1.0 并持续上行时，表明系统进入无序去杠杆与流动性危机，量化宏观基金应全面降低风险敞口并启动硬减仓策略。

【Q3 深度参考答案】
- **[负展期收益（Negative Roll Yield）的慢性毒药]**：VXX / UVXY 这类做多波动率的 ETF 并不直接持有不可交易的现货 VIX，而是通过每日滚动持有前两个月的 VIX 期货合约来模拟敞口。由于 VIX 期货在 80% 以上的时间里处于深度 Contango（远月比近月贵，例如近月 15，远月 16.5）；ETF 基金经理为了维持固定的久期，必须每天机械化地“卖出即将到期的便宜近月合约，买入昂贵的溢价远月合约”（高买低卖）。
- **[复利衰减的不可逆性]**：这种固定的展期损耗（Roll Decay）每月可蚕食 5%~10% 的净值，一年复合损耗高达 50%~80%，即便偶有黑天鹅脉冲暴涨，长期来看净值曲线也是不可逆地趋近于零。
- **[波动率做空基金的收割逻辑]**：机构对冲基金（如做空波动率策略）通过动态对冲做空 VXX 或卖出虚值看涨期权，长期稳定收割这一由结构性 Contango 产生的“波动率风险溢价（VRP）”，但前提是必须配置严格的极值硬止损与尾部看跌期权保护，以防止单次黑天鹅脉冲直接打爆账户。
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
    """二分法数值反解欧式看涨期权隐含波动率"""
    lower_bound = max(0.0, S - K * math.exp(-r * T))
    if target_price <= lower_bound:
        return 0.0

    low = low_vol
    high = high_vol

    for _ in range(max_iter):
        mid = (low + high) / 2.0
        p = bsm_call_price(S, K, T, r, mid)
        diff = p - target_price

        if abs(diff) < tol:
            return round(mid, 4)

        if diff > 0:
            high = mid
        else:
            low = mid

    return round((low + high) / 2.0, 4)


def solve_iv_newton_raphson(
    target_price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    initial_vol: float = 0.25,
    tol: float = 1e-5,
    max_iter: int = 50
) -> float:
    """牛顿-拉夫逊 (Newton-Raphson) 迭代法反解隐含波动率"""
    lower_bound = max(0.0, S - K * math.exp(-r * T))
    if target_price <= lower_bound:
        return 0.0

    vol = initial_vol
    for _ in range(max_iter):
        p = bsm_call_price(S, K, T, r, vol)
        diff = p - target_price

        if abs(diff) < tol:
            return round(vol, 4)

        vega = bsm_vega(S, K, T, r, vol)
        if vega < 1e-7:
            return solve_iv_bisection(target_price, S, K, T, r)

        vol = vol - diff / vega

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
    """
    F = S * math.exp(r * T)

    strikes_below_f = [opt["strike"] for opt in option_chain if opt["strike"] <= F]
    if not strikes_below_f:
        K0 = option_chain[0]["strike"]
    else:
        K0 = max(strikes_below_f)

    total_variance_sum = 0.0
    n = len(option_chain)

    for i in range(n):
        K = option_chain[i]["strike"]

        if i == 0:
            dK = option_chain[1]["strike"] - option_chain[0]["strike"]
        elif i == n - 1:
            dK = option_chain[-1]["strike"] - option_chain[-2]["strike"]
        else:
            dK = (option_chain[i + 1]["strike"] - option_chain[i - 1]["strike"]) / 2.0

        if K < K0:
            Q = option_chain[i]["put_price"]
        elif K > K0:
            Q = option_chain[i]["call_price"]
        else:
            Q = (option_chain[i]["call_price"] + option_chain[i]["put_price"]) / 2.0

        total_variance_sum += (dK / (K * K)) * Q

    term1 = (2.0 * math.exp(r * T) / T) * total_variance_sum
    term2 = (1.0 / T) * math.pow((F / K0 - 1.0), 2)
    sigma_sq = term1 - term2

    vix = 100.0 * math.sqrt(max(0.0, sigma_sq))
    return round(vix, 2)


# ==============================================================================
# 单元测试与断言校验
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
