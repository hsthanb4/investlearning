r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 4/5 课
第 4 课：风险价值 (VaR)、条件风险价值 (CVaR) 与动态回撤熔断控制 (参考答案版)
================================================================================

【Q1 深度参考答案】
风险价值（VaR）的“黑天鹅盲区”与次可加性（Sub-additivity）公理失效：为什么阿茨纳（Artzner et al. 1999）将 VaR 斥为“非一致性风险度量指标”？请构造一个期权空头组合或极端肥尾组合，说明为什么在特定情况下两个低风险子组合合并后，整体组合的 VaR 竟然大于子组合 VaR 之和？为什么巴塞尔协议 III 强制采用 CVaR（Expected Shortfall）替代 VaR？
- **[一致性风险度量的次可加性（Sub-additivity）公理]**：在投资学第一性原理中，分散化投资（Diversification）绝不应该增加总风险：$\rho(X + Y) \le \rho(X) + \rho(Y)$。然而，VaR 仅仅是一个特定置信水平下的分位数切片（Quantile），不满足次可加性公理。
- **[期权空头反例推导]**：
  假设有两种独立的巨灾债券 A 和 B。每种债券有 96% 的概率正常兑付产生小额收益，有 4% 的独立概率发生毁灭性违约损失 1 亿元。
  1. 对于 95% 置信水平的 VaR（$\alpha = 5\%$）：由于违约概率仅为 4%（$< 5\%$），在 95% 的置信度下，单项债券 A 和单项债券 B 的最坏预期损失均在其正常兑付范围内，即 $\text{VaR}_{95\%}(A) = 0, \text{VaR}_{95\%}(B) = 0$；
  2. 现在将两者等权组合为 $A + B$。组合发生至少一次违约的概率为：$1 - (1 - 0.04)^2 = 1 - 0.9216 = 7.84\% > 5\%$；
  3. 此时组合违约概率跨过了 5% 的门槛，组合的 95% 风险价值跃升为：$\text{VaR}_{95\%}(A + B) = 5000 \text{ 万元}$；
  4. 结果出现了荒谬的悖论：$\text{VaR}(A + B) = 5000 \text{万} > \text{VaR}(A) + \text{VaR}(B) = 0$！分散化反而导致 VaR 暴增。
- **[CVaR 的数理优越性与巴塞尔 III 的全面强制]**：条件风险价值（CVaR / Expected Shortfall）计算的是“一旦损失击穿 VaR 阈值后，极端尾部损失的条件数学期望”。Rockafellar & Uryasev (2000) 证明 CVaR 满足凸性与次可加性，且能够无死角积分所有极端黑天鹅损失。巴塞尔协议 III 已经全面强制要求银行与对冲基金以 97.5% CVaR 取代 99% VaR 作为资本准备金计提标准。

【Q2 深度参考答案】
参数法正态 VaR 在 2008 / 2020 危机中的系统性穿仓：正态分布假设下，收益率偏离均值 6 个标准差（$6\sigma$）的发生概率为数亿年一次。但在真实金融危机中，为何连续多日出现所谓的 $6\sigma \sim 8\sigma$ 事件？肥尾柯西/帕累托分布如何彻底击穿参数法 VaR 的防线？
- **[高斯钟形曲线的指数级极速衰减（Thin Tails）]**：正态分布的概率密度函数以 $e^{-x^2 / 2\sigma^2}$ 的超指数速率极速衰减。偏离均值 4 个标准差（$4\sigma$）的日概率约为 $3.17 \times 10^{-5}$（约 125 年一次）；偏离 6 个标准差（$6\sigma$）的概率约为 $1 \times 10^{-9}$（约 400 万年一次）；而偏离 8 个标准差的事件在宇宙诞生至今的时间里都不可能发生。
- **[真实金融市场的幂律肥尾现实（Power-law Fat Tails）]**：曼德博（Mandelbrot）与塔勒布（Taleb）证实，金融资产收益率服从具有长厚尾特性的帕累托或 Student-t 分布（$P(|X| > x) \sim x^{-\alpha}$）。在幂律分布下，尾部概率以代数级多项式衰减，其极端暴跌的发生概率比正态分布高出数万倍至数百万倍。
- **[危机穿仓的因果悲剧]**：华尔街机构在 2008 年次贷危机前，使用参数法正态 VaR 计算次贷衍生品的风险，得出风险准备金极其充裕的虚假安全结论。而当流动性踩踏与信用挤兑爆发时，市场在数周内连续上演理论上“数万年一次”的 $6\sigma \sim 8\sigma$ 暴跌。盲信参数法正态 VaR 的顶级投行（如贝尔斯登、雷曼兄弟）在瞬时极端损失击穿准备金后，直接流动性休克破产。

【Q3 深度参考答案】
动态历史最高水位线（HWM）阶梯式风控哨兵的因果性契约：在量化私募实盘风控中，为什么要实施“回撤超 -5% 降半仓，回撤超 -10% 硬熔断全现金冷冻”的阶梯式断路器？在算法架构上，为什么该风控决策必须严格滞后 1 期（Shift-1）执行？
- **[负复利深渊与本金防守的阶梯缓冲]**：
  回撤对于投资组合的伤害是非线性的（-10% 回撤需盈利 11% 回本，-20% 需 25%，-50% 需 100%）。当策略自高水位回撤触及 -5% 时，往往表明当前市场环境与模型底层假设发生了短期失配（如量化多头遭遇流动性微盘挤兑）。此时主动将仓位砍半（$M = 0.5$），能够以物理手段瞬间将组合的波动率压降 50%，为净值修复争取宝贵的缓冲空间；若跌势不止击穿 -10%，则表明模型遭遇了重大体制突变，必须强制清零冷冻（$M = 0$），将最大可能亏损牢牢锁定在容忍上限之内。
- **[杜绝日内前视作弊（No Lookahead Execution）]**：在回测代码中，若在 $t$ 日盘中利用包含 $t$ 日自身收盘价的 $\text{HWM}_t$ 来判定当日仓位乘数 $M_t$，这在实盘中是绝对无法实现的（日内价格实时跳动，收盘价在 15:00 之前未定）。
- **[严格的因果时序契约（$T-1$ 决策 $T$ 日执行）]**：工业级量化风控哨兵必须强制实施滞后一期规则：在 $t-1$ 日收盘后，根据已确定固化的历史最高水位线 $\text{HWM}_{t-1}$ 计算出回撤率 $\text{DD}_{t-1}$，生成风控乘数 $M_t$；并在 $t$ 日开盘以集合竞价或开盘第一笔交易完成减仓。这一契约虽然在突发暴跌日多承担了 1 天的降仓时滞，但它百分之百保证了回测结果在实盘物理世界中的可复制性与严肃性。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：拒绝正态侥幸，信奉硬核熔断</div>
  <div class="callout-body">
    VaR 是平时的体温计，CVaR 是危机的救生索，而阶梯式动态回撤熔断哨兵是防穿仓的最后一道物理保险丝。在量化对冲的世界里，唯有将风控纪律编码为不可撤销的自动化断路器，资本才得以在极端杀跌中全身而退。
  </div>
</div>
"""

from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
from scipy import stats


def calculate_parametric_var_cvar(
    returns: np.ndarray,
    confidence: float = 0.95,
) -> Tuple[float, float]:
    """
    基于正态分布假定的参数法单期 VaR 与 CVaR (以正数表示损失率)：
        alpha = 1 - confidence
        VaR_param = z_alpha * sigma - mu
        CVaR_param = sigma * (phi(z_alpha) / alpha) - mu
    """
    alpha = 1.0 - confidence
    mu = float(np.mean(returns))
    sigma = float(np.std(returns, ddof=1)) if len(returns) > 1 else float(np.std(returns))
    
    z_alpha = stats.norm.ppf(1.0 - alpha)  # e.g., 1.64485 for 95%
    var_param = float(z_alpha * sigma - mu)
    
    phi_z = stats.norm.pdf(z_alpha)
    cvar_param = float(sigma * (phi_z / alpha) - mu)
    return var_param, cvar_param


def calculate_historical_var_cvar(
    returns: np.ndarray,
    confidence: float = 0.95,
) -> Tuple[float, float]:
    """
    基于经验分布的历史模拟法单期 VaR 与 CVaR (以正数表示损失率)：
        alpha = 1 - confidence
        cutoff = percentile(returns, alpha * 100)
        VaR_hist = -cutoff
        CVaR_hist = -mean(returns[returns <= cutoff])
    """
    alpha = 1.0 - confidence
    cutoff = np.percentile(returns, alpha * 100.0)
    var = float(-cutoff)
    tail_losses = -returns[returns <= cutoff]
    cvar = float(np.mean(tail_losses)) if len(tail_losses) > 0 else var
    return var, cvar


def simulate_dynamic_drawdown_sentinel(
    raw_returns: pd.Series,
    warning_dd: float = -0.05,
    cut_ratio: float = 0.50,
    circuit_breaker_dd: float = -0.10,
) -> Dict[str, Any]:
    """
    基于历史高水位线 (HWM) 的动态阶梯式回撤风控哨兵：
    逐日滚动跟踪策略累计财富 W_t 与历史最高水位线 HWM_t = max_{s <= t} W_s：
    回撤率: DD_t = (W_t - HWM_t) / HWM_t

    风控执行规则 (决策必须滞后 1 期执行以防止前视偏差):
    - 若上一日 DD > warning_dd: 仓位乘数 pos = 1.0 (正常)
    - 若上一日 circuit_breaker_dd < DD <= warning_dd: 仓位乘数 pos = cut_ratio (0.5 降仓预警)
    - 若上一日 DD <= circuit_breaker_dd: 仓位乘数 pos = 0.0 (硬熔断平仓冷冻)
    """
    n = len(raw_returns)
    controlled_rets = []
    
    # 跟踪受控财富与最高水位
    wealth = 1.0
    hwm = 1.0
    circuit_breaker_tripped = False
    
    # 滞后 1 期决策变量
    prev_dd = 0.0
    
    for t in range(n):
        # 根据上一日回撤决定当日仓位乘数
        if prev_dd > warning_dd:
            pos = 1.0
        elif prev_dd > circuit_breaker_dd:
            pos = cut_ratio
        else:
            pos = 0.0
            circuit_breaker_tripped = True
            
        r_t = raw_returns.iloc[t] * pos
        controlled_rets.append(r_t)
        
        # 更新受控财富与回撤
        wealth *= (1.0 + r_t)
        if wealth > hwm:
            hwm = wealth
        prev_dd = (wealth - hwm) / hwm

    controlled_series = pd.Series(controlled_rets, index=raw_returns.index)
    
    # 计算原始策略累计财富与最大回撤
    raw_wealth = (1.0 + raw_returns).cumprod()
    raw_hwm = raw_wealth.cummax()
    raw_dd = (raw_wealth - raw_hwm) / raw_hwm
    raw_max_dd = float(raw_dd.min())
    
    # 计算受控策略累计财富与最大回撤
    ctrl_wealth = (1.0 + controlled_series).cumprod()
    ctrl_hwm = ctrl_wealth.cummax()
    ctrl_dd = (ctrl_wealth - ctrl_hwm) / ctrl_hwm
    ctrl_max_dd = float(ctrl_dd.min())
    
    reduction_pct = float((ctrl_max_dd - raw_max_dd) / abs(raw_max_dd))
    
    return {
        "raw_max_drawdown": raw_max_dd,
        "controlled_max_drawdown": ctrl_max_dd,
        "controlled_returns": controlled_series,
        "drawdown_reduction_pct": reduction_pct,
        "circuit_breaker_tripped": circuit_breaker_tripped
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 04 参考实现与全量单元测试")
    print("=" * 70)

    # 1. 验证简单离散样本测试
    rets_simple = np.array([-0.10, -0.06, -0.05, -0.02, 0.01, 0.02, 0.03, 0.04, 0.05, 0.08])
    var90, cvar90 = calculate_historical_var_cvar(rets_simple, confidence=0.90)
    print(f"简单样本 90% 历史 VaR: {var90*100:.2f}%, 历史 CVaR: {cvar90*100:.2f}%")
    assert var90 > 0.0, "VaR 以正损失率表达"
    assert cvar90 >= var90, "根据定义, 极端条件期望 CVaR 必须大于等于 VaR"

    # 2. 对比厚尾分布 (Student-t, df=3) 下参数法与历史模拟法的巨大反差
    np.random.seed(42)
    t_rets = stats.t.rvs(df=3, loc=0.0005, scale=0.015, size=2000)

    p_var, p_cvar = calculate_parametric_var_cvar(t_rets, confidence=0.95)
    h_var, h_cvar = calculate_historical_var_cvar(t_rets, confidence=0.95)

    print(f"\n厚尾数据 95% 参数法 VaR: {p_var*100:.2f}%, 参数法 CVaR: {p_cvar*100:.2f}%")
    print(f"厚尾数据 95% 历史法 VaR: {h_var*100:.2f}%, 历史法 CVaR: {h_cvar*100:.2f}%")

    assert p_cvar >= p_var, "参数法 CVaR 必须大于等于参数法 VaR"
    assert h_cvar >= h_var, "历史模拟法 CVaR 必须大于等于历史法 VaR"
    assert h_cvar > p_cvar, f"厚尾极端损失预期应显著击穿正态假设: 历史 CVaR ({h_cvar}) > 参数 CVaR ({p_cvar})"

    # 3. 验证动态高水位回撤控制与阶梯式熔断器
    n_days = 252
    raw_rets_arr = np.random.normal(0.001, 0.015, n_days)
    raw_rets_arr[100:150] = np.random.normal(-0.008, 0.02, 50)
    raw_series = pd.Series(raw_rets_arr)

    sentinel_res = simulate_dynamic_drawdown_sentinel(
        raw_series,
        warning_dd=-0.05,
        cut_ratio=0.50,
        circuit_breaker_dd=-0.10,
    )

    print(f"\n未受控原始策略最大回撤: {sentinel_res['raw_max_drawdown']*100:.2f}%")
    print(f"受控策略最大回撤: {sentinel_res['controlled_max_drawdown']*100:.2f}%")
    print(f"回撤削减幅度: {sentinel_res['drawdown_reduction_pct']*100:.2f}%")
    print(f"是否触发硬熔断: {sentinel_res['circuit_breaker_tripped']}")

    assert sentinel_res["raw_max_drawdown"] < -0.30, "原始策略在暴跌注入期间应发生深幅回撤 (< -30%)"
    assert sentinel_res["controlled_max_drawdown"] > -0.15, f"受控策略最大回撤应受控在 -15% 以内"
    assert sentinel_res["drawdown_reduction_pct"] > 0.50, "回撤削减幅度应超过 50%"
    assert sentinel_res["circuit_breaker_tripped"] is True, "暴跌行情应成功触发二级硬熔断保护"

    print("Lesson 04 风险计量与动态回撤风控单元测试全部通过！")
