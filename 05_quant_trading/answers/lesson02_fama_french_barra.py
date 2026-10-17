r"""
================================================================================
模块 05：量化投资多因子与统计套利 · 第 2/5 课
第 2 课：经典 Fama-French 多因子资产定价模型与 Barra 结构化风险分解 (参考答案版)
================================================================================

【Q1 深度参考答案】
Fama-French 因子与无套利定价理论（APT）：在多因子模型中，为什么一个异象（Anomaly）被确认为“系统性风险因子”后，其超额收益本质是对持有该风险承担者的“风险补偿（Risk Premium）”而非纯免费午餐？为什么当套利资金大规模涌入后，传统价值因子（HML）与规模因子（SMB）往往会发生长期溢价衰减？
- **[风险补偿的第一性原理：不存在免费的午餐]**：在有效市场或无套利均衡下，若某个投资策略能够长期获得高于无风险利率的收益，其必然在某些极度痛苦的宏观时刻承受了系统性亏损。例如，小市值股票（SMB）在宏观流动性紧缩或信贷危机中面临严重的再融资断裂与流动性折价风险；高估值便宜的价值股（HML）往往是陷入重度负债、技术落后甚至濒临破产的困境企业（Financial Distress）。投资者持有这些股票所获得的超额收益，本质是资本对其承担“暴雷破产风险”所要求的必要风险溢价补偿。
- **[套利资金涌入（Factor Crowding）与拥挤度踩踏]**：随着 Fama-French 经典论文的公开发表，全球 Smart Beta ETF 与量化基金将万亿美元资本按照相同规则配置于小盘股与低估值价值股。大量资金的买入迅速推高了这些资产的价格，直接抹平了原本由定价无效率造成的超额价差。
- **[宏观经济结构的永久性变迁]**：2010 年代后，以高研发开支、轻资产、网络效应为主导的科技巨头（如苹果、微软、亚马逊）统治市场，传统的账面价值（Book Value）无法反映无形资产（Intangibles）与专利价值，导致传统 HML 因子出现长达十年的历史性回撤与失灵。

【Q2 深度参考答案】
Barra 结构化风险模型的核心降维数学物理意义：全市场有 5000 只股票，直接估计样本协方差矩阵需要估计约 1250 万个参数，存在严重的奇异性与采样噪声（Curse of Dimensionality）。Barra 如何通过 $\Sigma = X F X^T + \Delta$ 的因子分解，将自由度压缩至 $K(K+1)/2 + N$？
- **[维数灾难与样本协方差的病态奇异性]**：对于 $N = 5000$ 只股票，其全对称协方差矩阵包含 $N(N+1)/2 = 12,502,500$ 个独立待估参数。然而，在日常量化回测中，历史样本观测长度通常仅有数年（如 252 天或 500 天），样本数 $T$ 远远小于资产数 $N$（$T \ll N$）。此时直接计算的样本协方差矩阵 $\hat{\Sigma}$ 严重欠秩且高度奇异，包含海量随机采样噪声，将其代入马科维茨优化器求逆（$\Sigma^{-1}$）会导致最优权重发生灾难性荒谬震荡。
- **[Barra 多因子结构化降维代数]**：Barra 模型假设所有股票的收益率均由少数 $K$ 个公共系统性风险因子（通常 $K \approx 40 \sim 60$，包含行业因子与风格因子）以及股票特异残差线性驱动：$r = X f + u$。因此，庞大的股票间协方差被优雅转化为：
  $$\Sigma_{N \times N} = X_{N \times K} F_{K \times K} X^T_{K \times N} + \Delta_{N \times N}$$
- **[自由度的指数级缩减]**：此时需要估计的系统性因子协方差矩阵 $F$ 仅有 $K(K+1)/2 \approx 60 \times 61 / 2 = 1830$ 个参数，在长时序样本下能够极其稳健地精确估计；特异风险对角阵 $\Delta$ 仅需估计 $N = 5000$ 个对角方差。总参数量从 1250 万骤降至不到 7000 个（缩减了 99.94%），彻底消除了协方差矩阵的病态奇异性，保证了投资组合优化的数值稳定与全天候鲁棒性。

【Q3 深度参考答案】
纯 Alpha 基金的风格因子暴露敞口（Style Bias）风控惩罚：为什么顶级量化对冲基金（如 Two Sigma、Citadel）在组合优化器中对 Barra 风格因子（Size, Beta, Volatility, Momentum）设定了极窄的容差阈值（如暴露绝对值 $< 0.1\sigma$）？若基金经理号称有 20% 年化超额，但归因后 80% 收益来自小市值（SMB）敞口，投决会应如何定性其真实风险水平？
- **[对冲基金的商业契约：收取 2/20 管理费必须提供零 Beta 的纯 Alpha]**：机构投资者（LP，如大学捐赠基金、主权财富基金）向多策略量化对冲基金支付高昂管理费（2% 管理费 + 20% 业绩提成）的唯一目的，是获取与宏观大盘及主要市场风格不相关的绝对收益。如果 LP 想要做多小市值或价值风格，他们可以直接以 0.05% 的极低费率购买小盘指数 ETF，绝不需要向对冲基金支付 20% 的利润提成。
- **[风格因子的双刃剑特质与潜伏黑天鹅]**：风格因子在牛市顺周期时能产生巨大的动量加速度，但在去杠杆或风格切换时会发生惨烈的流动性踩踏（如 2024 年初中国 A 股小微盘股的极端流动性挤兑危机）。80% 收益来自小市值的基金，其实质是在进行“小市值看跌期权”的空头裸奔。
- **[投决会的定性结论与风控裁决]**：投决会必须将该业绩定性为“高脆弱性的伪 Alpha 风格对赌”。必须实施严格的组合优化硬约束（Style Exposure Bounds），强制将所有 Barra 风格因子敞口锁定在 $[-0.1, +0.1]$ 的标准差以内，倒逼投资经理通过截面特异选股能力（Idiosyncratic Alpha）产生真实超额，否则直接下调其风险资本额度（Risk Budget Allocation）。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：严控风格敞口，只为纯粹 Alpha 买单</div>
  <div class="callout-body">
    任何未被严格约束的风格暴露都是偷懒的下注。顶尖量化机构的护城河不在于敢不敢下注小盘股，而在于能否在所有已知系统性风格暴露完全中性化的苛刻条件下，依然稳定提取出统计显著的超额 Alpha。
  </div>
</div>
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
try:
    from scipy import stats
except ImportError:
    import math
    class _MockT:
        @staticmethod
        def cdf(x, df):
            arr = np.asarray(x, dtype=float)
            scale = np.sqrt(df / (df - 2.0)) if df > 2 else 1.0
            return 0.5 * (1.0 + np.vectorize(math.erf)(arr / (scale * math.sqrt(2.0))))
    class _MockStats:
        t = _MockT()
    stats = _MockStats()



def fama_french_multi_factor_regression(
    asset_returns: pd.Series,
    factor_returns: pd.DataFrame,
    risk_free_rate: float = 0.0,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    多元时间序列 OLS 回归与 Fama-French 因子收益剥离
    """
    # 对齐数据并剔除缺失值
    df = pd.concat([asset_returns.rename("y"), factor_returns], axis=1).dropna()
    y = (df["y"] - risk_free_rate).values
    factor_names = list(factor_returns.columns)
    F = df[factor_names].values
    n_samples, n_factors = F.shape

    # 构造设计矩阵 [1, F_1, F_2, ..., F_K]
    X = np.column_stack([np.ones(n_samples), F])

    # OLS 求解
    beta_hat, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    y_pred = X @ beta_hat
    residuals = y - y_pred

    # 自由度与方差估计
    dof = n_samples - X.shape[1]
    sse = float(np.sum(residuals**2))
    mse = sse / dof if dof > 0 else 0.0

    inv_XtX = np.linalg.inv(X.T @ X)
    se_beta = np.sqrt(np.maximum(0.0, mse * np.diag(inv_XtX)))
    t_stats = beta_hat / np.where(se_beta == 0, 1e-12, se_beta)
    p_values = 2.0 * (1.0 - stats.t.cdf(np.abs(t_stats), df=dof))

    sst = float(np.sum((y - np.mean(y))**2))
    r2 = float(1.0 - sse / sst) if sst > 1e-12 else 0.0
    adj_r2 = float(1.0 - (1.0 - r2) * (n_samples - 1) / dof) if dof > 0 else r2

    alpha = float(beta_hat[0])
    annualized_alpha = alpha * annual_periods
    alpha_t_stat = float(t_stats[0])
    alpha_p_value = float(p_values[0])

    betas = {f_name: float(beta_hat[i + 1]) for i, f_name in enumerate(factor_names)}
    beta_t_stats = {f_name: float(t_stats[i + 1]) for i, f_name in enumerate(factor_names)}

    specific_volatility = float(np.std(residuals, ddof=1) * np.sqrt(annual_periods))
    systematic_risk_ratio = float(r2)
    specific_risk_ratio = float(1.0 - r2)

    return {
        "alpha": alpha,
        "annualized_alpha": annualized_alpha,
        "alpha_t_stat": alpha_t_stat,
        "alpha_p_value": alpha_p_value,
        "betas": betas,
        "beta_t_stats": beta_t_stats,
        "r_squared": r2,
        "adj_r_squared": adj_r2,
        "residuals": pd.Series(residuals, index=df.index),
        "specific_volatility": specific_volatility,
        "systematic_risk_ratio": systematic_risk_ratio,
        "specific_risk_ratio": specific_risk_ratio,
    }


def barra_style_attribution(
    portfolio_weights: np.ndarray,
    factor_exposures: np.ndarray,
    factor_cov_matrix: np.ndarray,
    specific_vars: np.ndarray,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    Barra 结构化多因子风险归因
    """
    w = portfolio_weights.reshape(-1, 1)
    X = factor_exposures  # N x K

    # 组合因子暴露度向量 x_p = X^T * w (K x 1)
    x_p = (X.T @ w).flatten()

    # 组合单期因子方差 = x_p^T * Sigma_F * x_p
    factor_variance_daily = float(x_p.T @ factor_cov_matrix @ x_p)
    factor_variance_annual = factor_variance_daily * annual_periods

    # 组合单期特质方差 = sum(w_i^2 * delta_i)
    specific_variance_daily = float(np.sum((portfolio_weights**2) * specific_vars))
    specific_variance_annual = specific_variance_daily * annual_periods

    total_variance_annual = factor_variance_annual + specific_variance_annual
    total_volatility = float(np.sqrt(total_variance_annual))

    factor_risk_pct = float(factor_variance_annual / total_variance_annual) if total_variance_annual > 0 else 0.0
    specific_risk_pct = float(specific_variance_annual / total_variance_annual) if total_variance_annual > 0 else 0.0

    return {
        "portfolio_factor_exposures": x_p,
        "factor_variance": factor_variance_annual,
        "specific_variance": specific_variance_annual,
        "total_variance": total_variance_annual,
        "total_volatility": total_volatility,
        "factor_risk_pct": factor_risk_pct,
        "specific_risk_pct": specific_risk_pct,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 02: Fama-French 多因子与 Barra 归因单元测试 (参考答案版)")
    print("=" * 70)

    np.random.seed(42)
    n_samples = 504
    factor_names = ["MKT", "SMB", "HML", "RMW", "CMA"]
    n_factors = len(factor_names)

    f_returns = np.random.normal(loc=[0.0004, 0.0002, 0.0001, 0.0002, 0.0001], scale=0.01, size=(n_samples, n_factors))
    dates = pd.date_range("2023-01-01", periods=n_samples, freq="B")
    factor_df = pd.DataFrame(f_returns, index=dates, columns=factor_names)

    true_alpha_daily = 0.0003
    true_betas = np.array([1.05, 0.60, -0.25, 0.40, 0.15])
    noise = np.random.normal(loc=0.0, scale=0.006, size=n_samples)

    asset_ret_series = pd.Series(
        true_alpha_daily + np.dot(f_returns, true_betas) + noise,
        index=dates,
    )

    reg_res = fama_french_multi_factor_regression(asset_ret_series, factor_df, annual_periods=252)

    print(f"年化 Alpha: {reg_res['annualized_alpha']*100:.2f}% (t-stat: {reg_res['alpha_t_stat']:.3f}, p-val: {reg_res['alpha_p_value']:.4e})")
    print(f"拟合优度 R^2: {reg_res['r_squared']:.4f}, 调整后 R^2: {reg_res['adj_r_squared']:.4f}")
    print(f"年化特质波动率: {reg_res['specific_volatility']*100:.2f}%")
    print(f"系统性风险占比: {reg_res['systematic_risk_ratio']*100:.2f}%, 特质风险占比: {reg_res['specific_risk_ratio']*100:.2f}%")
    for f_name in factor_names:
        print(f"  因子 {f_name} 暴露 Beta: {reg_res['betas'][f_name]:.4f} (t-stat: {reg_res['beta_t_stats'][f_name]:.3f})")

    assert abs(reg_res["annualized_alpha"] - true_alpha_daily * 252) < 0.05, "Alpha 估算偏差过大"
    assert reg_res["alpha_t_stat"] > 1.0, "构造的正向 Alpha 应具备正 t 统计量"
    assert abs(reg_res["betas"]["MKT"] - 1.05) < 0.08, "MKT Beta 估计偏差过大"
    assert abs(reg_res["betas"]["SMB"] - 0.60) < 0.08, "SMB Beta 估计偏差过大"
    assert abs(reg_res["betas"]["HML"] - (-0.25)) < 0.08, "HML Beta 估计偏差过大"
    assert reg_res["r_squared"] > 0.70, "多因子回归解释度 R^2 应大于 70%"
    assert abs(reg_res["systematic_risk_ratio"] + reg_res["specific_risk_ratio"] - 1.0) < 1e-4, "方差分解之和应为 100%"

    n_assets = 10
    w = np.ones(n_assets) / n_assets
    np.random.seed(101)
    X = np.random.uniform(-1.0, 1.0, size=(n_assets, n_factors))
    cov_F = factor_df.cov().values
    spec_vars = np.random.uniform(0.0001, 0.0003, size=n_assets)

    barra_res = barra_style_attribution(w, X, cov_F, spec_vars, annual_periods=252)

    print(f"\nBarra 年化总波动率: {barra_res['total_volatility']*100:.2f}%")
    print(f"公因子风险占比: {barra_res['factor_risk_pct']*100:.2f}%")
    print(f"特质风险占比: {barra_res['specific_risk_pct']*100:.2f}%")

    assert barra_res["total_variance"] > 0.0, "总方差必须为正"
    assert abs(barra_res["factor_risk_pct"] + barra_res["specific_risk_pct"] - 1.0) < 1e-5, "Barra 风险占比之和必须为 100%"
    assert len(barra_res["portfolio_factor_exposures"]) == n_factors, "组合因子暴露维度必须与因子数一致"

    print("Lesson 02 参考答案全部通过 (Exit Code 0)！")
