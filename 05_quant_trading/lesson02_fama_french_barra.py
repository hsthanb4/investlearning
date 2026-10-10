r"""
================================================================================
模块 05：量化投资多因子与统计套利 · 第 2/5 课
第 2 课：经典 Fama-French 多因子资产定价模型与 Barra 结构化风险分解 (FF5 & Barra Structural Model)
================================================================================

【课程定位与第一性原理】
在现代资产定价与对冲基金投资组合风险预算中，Fama-French 模型与 Barra 结构化风险体系
代表了从学术界资产定价到华尔街量化实盘风控的演进巅峰。
投资委员会在审视投资经理的投资业绩时，首要任务是通过多因子正交回归剥离其风格暴露（Beta），
严格甄别业绩究竟是源于承担系统性因子的风险溢价补偿，还是源于真正不可替代的纯选股阿尔法（Idiosyncratic Alpha）。

- **[APT 套利定价理论与因子正交化]**：股票收益率可严格正交分解为市场基准、规模、价值、盈利质量、投资风格五大多空对冲因子暴露与特异残差。
- **[Barra 结构化风险模型的维数缩减]**：5000 维股票样本协方差矩阵存在致命的病态奇异性；Barra 通过因子暴露矩阵 $X$ 将协方差压缩为 $\Sigma = X F X^T + \Delta$，彻底化解维数灾难。
- **[特异风险与系统性风险的方差归因]**：组合总方差必须精准切分为因子驱动的系统性方差与股票特异性方差；充分分散的量化组合应将特异方差降至 15% 以下。

【核心概念与就近图文排版】

1. Fama-French 五因子资产定价模型正交分解：
观察下图关于五因子多空基准组合构建与 Alpha 剥离的经典架构：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.2.1：Fama-French 五因子资产定价模型正交分解与 Alpha 剥离</span>
    <span class="diagram-tag">FAMA-FRENCH-5F</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l02_fama_french_factor_zoo.svg -->
  </div>
</div>

- **[MKT 市场风险溢价]**：基准全市场超额收益 $R_m - R_f$，度量宏观系统性市场贝塔。
- **[SMB 规模溢价]**：小市值组合减大市值组合收益（Small Minus Big），反映流动性风险补偿。
- **[HML 价值溢价]**：高账面市值比组合减低账面市值比收益（High Minus Low），反映困境反转估值补偿。
- **[RMW 盈利质量溢价]**：高 ROE/ROIC 健壮组合减低盈利弱势组合收益（Robust Minus Weak）。
- **[CMA 投资风格溢价]**：保守低资本开支组合减激进高资本扩张组合收益（Conservative Minus Aggressive）。

2. Barra 结构化风险模型矩阵分解拓扑：
下图展示了 Barra 风险模型将高维股票协方差降维投影至风格与行业因子的代数拓扑：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.2.2：Barra 多因子结构化风险模型矩阵：风格因子与行业暴露拓扑</span>
    <span class="diagram-tag">BARRA-RISK-MATRIX</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l02_barra_risk_model_matrix.svg -->
  </div>
</div>

- **[因子暴露矩阵 $X$]**：$N \times K$ 阶矩阵，包含行业虚拟变量与风格因子（Beta, Size, Momentum, Volatility）标准化暴露。
- **[因子协方差矩阵 $F$]**：$K \times K$ 阶紧凑正定矩阵，通过指数半衰期时序加权与 Newey-West 滞后自相关调整估计。
- **[特异风险对角阵 $\Delta$]**：$N \times N$ 阶纯对角阵，假定股票间残差特异风险相互正交，极大降低自由度。

3. 投资组合系统性与特异风险方差分解：
下图对比了集中持仓与全市场分散化量化组合在风险方差归因上的悬殊差异：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.2.3：投资组合总风险方差分解：风格系统性风险 vs 股票特异风险</span>
    <span class="diagram-tag">RISK-ATTRIBUTION</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l02_specific_risk_decomposition.svg -->
  </div>
</div>

- **[集中持仓的特异风险裸露]**：仅持股 10 只的组合特异风险占比 $> 65\%$，业绩高度取决于个股黑天鹅，无法享受大数定律保护。
- **[量化分散组合的系统性纯度]**：持股数百只的量化多因子组合特异风险 $< 15\%$，组合收益完全由因子的选股 Alpha 与风格暴露解释。
- **[组合总方差等式]**：$\sigma_p^2 = w^T X F X^T w + w^T \Delta w$。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：资本资产定价模型到多因子风险预算的跃迁</div>
  <div class="callout-body">
    单因子 CAPM 假定市场只有一个单一 Beta。而真实世界的风险是多维的——行业周期、市值规模、价值风格都是独立的宏观风险源。多因子风险模型的价值在于：让你清楚知道组合赚的每一分钱究竟是在承担哪种具体的风险。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    若某主动权益基金长期年化收益 25%，但 Barra 归因分析显示其超额收益的 90% 来自被动暴露小市值因子（SMB）与高贝塔因子，投决会应将其管理费标准下调为被动指数基金水平，并警惕流动性退潮时的清仓踩踏。
  </div>
</div>

【数学与回归模型】
$$R_{i, t} - R_{f, t} = \alpha_i + \beta_{i, \text{MKT}} \text{MKT}_t + \beta_{i, \text{SMB}} \text{SMB}_t + \beta_{i, \text{HML}} \text{HML}_t + \epsilon_{i, t}$$
$$\Sigma_{\text{Barra}} = X_{N \times K} F_{K \times K} X^T_{K \times N} + \Delta_{N \times N}$$
$$\text{Factor\_Risk\_Pct} = \frac{w^T X F X^T w}{\sigma_p^2} \times 100\%, \quad \text{Specific\_Risk\_Pct} = \frac{w^T \Delta w}{\sigma_p^2} \times 100\%$$
定义域：$N \gg K \ge 5, \quad \sigma_p^2 > 0, \quad \text{Factor\_Risk\_Pct} + \text{Specific\_Risk\_Pct} \equiv 100\%$。

【思考题】
Q1: Fama-French 因子与无套利定价理论（APT）：在多因子模型中，为什么一个异象（Anomaly）被确认为“系统性风险因子”后，其超额收益本质是对持有该风险承担者的“风险补偿（Risk Premium）”而非纯免费午餐？为什么当套利资金大规模涌入后，传统价值因子（HML）与规模因子（SMB）往往会发生长期溢价衰减？
Q2: Barra 结构化风险模型的核心降维数学物理意义：全市场有 5000 只股票，直接估计样本协方差矩阵需要估计约 1250 万个参数，存在严重的奇异性与采样噪声（Curse of Dimensionality）。Barra 如何通过 $\Sigma = X F X^T + \Delta$ 的因子分解，将自由度压缩至 $K(K+1)/2 + N$？
Q3: 纯 Alpha 基金的风格因子暴露敞口（Style Bias）风控惩罚：为什么顶级量化对冲基金（如 Two Sigma、Citadel）在组合优化器中对 Barra 风格因子（Size, Beta, Volatility, Momentum）设定了极窄的容差阈值（如暴露绝对值 $< 0.1\sigma$）？若基金经理号称有 20% 年化超额，但归因后 80% 收益来自小市值（SMB）敞口，投决会应如何定性其真实风险水平？

【评分与通过规则】
- 代码 4 分：Fama-French 多因子 OLS 正交回归与风险分解 (2分) + Barra 结构化协方差矩阵与组合风格归因 (2分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：从 APT 无套利定价、高维统计协方差降维及真实风格敞口展开
- 通过线：8/10 分。一票否决：方差分解不守恒、Beta 计算符号颠倒
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy import stats


def fama_french_multi_factor_regression(
    asset_returns: pd.Series,
    factor_returns: pd.DataFrame,
    risk_free_rate: float = 0.0,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    多元时间序列 OLS 回归与 Fama-French 因子收益剥离：
        (R_i - R_f) = alpha + beta_1 * F_1 + beta_2 * F_2 + ... + beta_K * F_K + epsilon

    参数:
        asset_returns: 资产/组合收益率时间序列 Series
        factor_returns: 各因子收益率 DataFrame (每列为一个公因子，如 MKT, SMB, HML 等)
        risk_free_rate: 无风险利率 (与收益率频度对齐，若为日频通常设为 0.0)
        annual_periods: 年化系数 (日频 252)

    返回字典包含:
        - "alpha": 单期 Alpha 截距
        - "annualized_alpha": 年化 Alpha = alpha * annual_periods
        - "alpha_t_stat": Alpha 的 t 统计量
        - "alpha_p_value": Alpha 的双尾 p 值
        - "betas": 字典 {factor_name: beta_value}
        - "beta_t_stats": 字典 {factor_name: t_stat}
        - "r_squared": 决定系数 R^2
        - "adj_r_squared": 调整后 R^2
        - "residuals": 特质残差收益率 Series
        - "specific_volatility": 年化特质波动率 (std(epsilon) * sqrt(annual_periods))
        - "systematic_risk_ratio": 系统性风险贡献占比 (R^2)
        - "specific_risk_ratio": 特质风险贡献占比 (1 - R^2)
    """
    # TODO: 实现多因子 OLS 回归与统计量估计
    pass


def barra_style_attribution(
    portfolio_weights: np.ndarray,
    factor_exposures: np.ndarray,
    factor_cov_matrix: np.ndarray,
    specific_vars: np.ndarray,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    Barra 结构化多因子风险归因：
        总协方差矩阵 V = X * Sigma_F * X^T + Delta
        组合方差 sigma_p^2 = (w^T * X) * Sigma_F * (X^T * w) + w^T * Delta * w

    参数:
        portfolio_weights: 组合资产权重向量 w (N 维, sum(w) = 1)
        factor_exposures: 资产因子暴露度矩阵 X (N x K)
        factor_cov_matrix: 因子收益协方差矩阵 Sigma_F (K x K, 单期)
        specific_vars: 个股特质方差向量 delta (N 维, 对角线元素, 单期)
        annual_periods: 年化系数 (默认 252)

    返回字典包含:
        - "portfolio_factor_exposures": 组合层面的因子暴露向量 x_p = X^T * w (K 维)
        - "factor_variance": 组合因子方差 (年化)
        - "specific_variance": 组合特质方差 (年化)
        - "total_variance": 组合总方差 (年化)
        - "total_volatility": 组合年化总波动率 (sqrt(total_variance))
        - "factor_risk_pct": 公因子系统性风险占比 (factor_variance / total_variance)
        - "specific_risk_pct": 特质风险占比 (specific_variance / total_variance)
    """
    # TODO: 实现 Barra 风险矩阵归因求解
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 02: Fama-French 多因子与 Barra 归因单元测试")
    print("=" * 70)

    # 1. 构造多因子时间序列仿真数据
    np.random.seed(42)
    n_samples = 504  # 两年日频交易数据
    factor_names = ["MKT", "SMB", "HML", "RMW", "CMA"]
    n_factors = len(factor_names)

    # 模拟真实市场因子日收益率
    f_returns = np.random.normal(loc=[0.0004, 0.0002, 0.0001, 0.0002, 0.0001], scale=0.01, size=(n_samples, n_factors))
    dates = pd.date_range("2023-01-01", periods=n_samples, freq="B")
    factor_df = pd.DataFrame(f_returns, index=dates, columns=factor_names)

    # 设定真实底层资产参数
    true_alpha_daily = 0.0003  # 真实日频 Alpha (年化约 7.5%)
    true_betas = np.array([1.05, 0.60, -0.25, 0.40, 0.15])
    noise = np.random.normal(loc=0.0, scale=0.006, size=n_samples)

    asset_ret_series = pd.Series(
        true_alpha_daily + np.dot(f_returns, true_betas) + noise,
        index=dates,
    )

    # 执行 Fama-French 多元回归归因
    reg_res = fama_french_multi_factor_regression(asset_ret_series, factor_df, annual_periods=252)

    print(f"年化 Alpha: {reg_res['annualized_alpha']*100:.2f}% (t-stat: {reg_res['alpha_t_stat']:.3f}, p-val: {reg_res['alpha_p_value']:.4e})")
    print(f"拟合优度 R^2: {reg_res['r_squared']:.4f}, 调整后 R^2: {reg_res['adj_r_squared']:.4f}")
    print(f"年化特质波动率: {reg_res['specific_volatility']*100:.2f}%")
    print(f"系统性风险占比: {reg_res['systematic_risk_ratio']*100:.2f}%, 特质风险占比: {reg_res['specific_risk_ratio']*100:.2f}%")
    for f_name in factor_names:
        print(f"  因子 {f_name} 暴露 Beta: {reg_res['betas'][f_name]:.4f} (t-stat: {reg_res['beta_t_stats'][f_name]:.3f})")

    # 断言回归参数还原度与显著性
    assert abs(reg_res["annualized_alpha"] - true_alpha_daily * 252) < 0.05, "Alpha 估算偏差过大"
    assert reg_res["alpha_t_stat"] > 1.0, "构造的正向 Alpha 应具备正 t 统计量"
    assert abs(reg_res["betas"]["MKT"] - 1.05) < 0.08, "MKT Beta 估计偏差过大"
    assert abs(reg_res["betas"]["SMB"] - 0.60) < 0.08, "SMB Beta 估计偏差过大"
    assert abs(reg_res["betas"]["HML"] - (-0.25)) < 0.08, "HML Beta 估计偏差过大"
    assert reg_res["r_squared"] > 0.70, "多因子回归解释度 R^2 应大于 70%"
    assert abs(reg_res["systematic_risk_ratio"] + reg_res["specific_risk_ratio"] - 1.0) < 1e-4, "方差分解之和应为 100%"

    # 2. 检验 Barra 风格风险归因矩阵计算
    n_assets = 10
    w = np.ones(n_assets) / n_assets  # 等权组合
    # 模拟资产因子暴露 X (10 x 5)
    np.random.seed(101)
    X = np.random.uniform(-1.0, 1.0, size=(n_assets, n_factors))
    # 因子收益单期协方差矩阵 (5 x 5)
    cov_F = factor_df.cov().values
    # 特质单期方差
    spec_vars = np.random.uniform(0.0001, 0.0003, size=n_assets)

    barra_res = barra_style_attribution(w, X, cov_F, spec_vars, annual_periods=252)

    print(f"\nBarra 年化总波动率: {barra_res['total_volatility']*100:.2f}%")
    print(f"公因子风险占比: {barra_res['factor_risk_pct']*100:.2f}%")
    print(f"特质风险占比: {barra_res['specific_risk_pct']*100:.2f}%")

    assert barra_res["total_variance"] > 0.0, "总方差必须为正"
    assert abs(barra_res["factor_risk_pct"] + barra_res["specific_risk_pct"] - 1.0) < 1e-5, "Barra 风险占比之和必须为 100%"
    assert len(barra_res["portfolio_factor_exposures"]) == n_factors, "组合因子暴露维度必须与因子数一致"

    print("Lesson 02 单元测试全部通过！")
