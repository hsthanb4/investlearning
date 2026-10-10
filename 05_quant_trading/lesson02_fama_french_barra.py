r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 2/5 课
第 2 课：Fama-French 多因子模型与 Barra 风格风险归因 (Factor Attribution)
================================================================================

【课程定位与第一性原理】
在现代资产定价与量化投资实践中，资本资产定价模型（CAPM）的单一市场 Beta 已无法解释横截面收益的复杂异象。
Eugene Fama 与 Kenneth French 先后提出三因子（1993）与五因子（2015）模型，开创了现代因子投资的基石：
    $$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,\text{MKT}} \text{MKT}_t + \beta_{i,\text{SMB}} \text{SMB}_t + \beta_{i,\text{HML}} \text{HML}_t + \beta_{i,\text{RMW}} \text{RMW}_t + \beta_{i,\text{CMA}} \text{CMA}_t + \epsilon_{i,t}$$
- $\text{MKT}$: 市场超额收益（Market Equity Premium）
- $\text{SMB}$ (Small Minus Big): 市值规模因子（小市值溢价）
- $\text{HML}$ (High Minus Low): 估值因子（高账面市值比 B/M 价值股溢价）
- $\text{RMW}$ (Robust Minus Weak): 盈利能力因子（高营业利润率企业溢价）
- $\text{CMA}$ (Conservative Minus Aggressive): 投资模式因子（保守投资、低资产扩张率企业溢价）

Barra 结构化风险多因子体系（MSCI Barra USE4 / CNE5）进一步将该理论工程化落地：
通过正交化与结构化协方差矩阵，将任意投资组合的收益率与风险方差彻底解耦为：
    $$\sigma_p^2 = w^T V w = \underbrace{(w^T X) \Sigma_F (X^T w)}_{\text{公因子系统性风险 (Factor Risk)}} + \underbrace{w^T \Delta w}_{\text{特质特有风险 (Specific Risk)}}$$
其中 $X$ 为资产因子暴露矩阵，$\Sigma_F$ 为因子协方差矩阵，$\Delta$ 为特质方差对角矩阵。
真正的 Alpha，是在剔除全部已知系统性风险暴露后，残差截距 $\alpha_i$ 依然在统计学上具备极高的 t 统计量显著性（$t > 2.0$）。

【核心流程与心智模型】
```mermaid
flowchart TD
    Ret["投资组合 / 个股收益率序列 $R_p$"] --> FactorMatrix["五大风格公因子时序 [MKT, SMB, HML, RMW, CMA]"]
    FactorMatrix --> OLS["多元时间序列普通最小二乘回归 (OLS)"]
    OLS --> Betas["因子暴露度: $\beta_{MKT}, \beta_{SMB}, \beta_{HML}, \beta_{RMW}, \beta_{CMA}$"]
    OLS --> Alpha["纯净特质超额收益: $\alpha_p$ 与显著性 t-stat"]
    OLS --> Residuals["特质残差时序: $\epsilon_t$ 与特质波动率 $\sigma_{\epsilon}$"]
    Betas --> BarraRisk["Barra 协方差风险归因矩阵: $X_p^T \Sigma_F X_p + w^T \Delta w$"]
    Residuals --> BarraRisk
    BarraRisk --> Report["风险归因报告: 系统性风险占比 vs 特质风险占比 (Alpha 纯度)"]
```

【工业界实战场景与风控陷阱】
1. 伪 Alpha 陷阱与“微盘股贝塔搬运工”：
   许多量化私募或公募基金宣称年化 Alpha 高达 20%，但在 Fama-French 五因子归因下，其 $\beta_{\text{SMB}}$ 高达 1.5 以上，
   实际收益 90% 来源于下沉微盘股获取的小市值流动性溢价。一旦发生微盘股流动性踩踏，该类策略将遭遇毁灭性净值回撤。
2. 多重共线性（Multicollinearity）与方差膨胀系数（VIF）：
   不同因子之间往往存在自相关（例如高账面市值比与低毛利率、或者低波动与大市值）。回归前必须检查因子相关性或进行正交化处理，
   防止 OLS 回归系数方差爆炸失真。
3. 动态时变 Beta（Regime-dependent Beta）：
   资产对因子的敏感度并非恒定常数。在市场极端下跌时，高流动性大盘股的 $\beta_{\text{MKT}}$ 可能会跳升。

【思考题】
Q1: 为什么过去十几年全球股票市场中 HML（传统价值因子）长期跑输成长与动量，而在 2021~2022 年全球通胀加息周期中又大幅均值回归？请从无风险折现率与股票久期（Duration of Equity）的金融经济学第一性原理剖析。
Q2: Barra 风险模型与 Fama-French 时间序列回归模型在工业界落地时有何本质哲学差异？（横截面 WLS 回归估算因子收益率 vs 时间序列 OLS 回归估算因子暴露 Beta）。
Q3: 怎样理解“很多声称有稳定 Alpha 的量化或公募基金经理，实质上只是长期单向暴露在小市值（SMB）与高贝塔风险敞口上的‘贝塔搬运工’”？在多因子归因体系下如何用 t 统计量剥离出真正的特质 Alpha？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现多因子多元 OLS 回归与 t 统计量、拟合优度计算 (1.5分)；
  2. 准确提取特质残差收益并计算特质波动率与方差分解 (1.5分)；
  3. 准确实现 Barra 组合风格风险与特质风险协方差矩阵归因 (1分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须从宏观折现率、横截面与时序计量经济学及风险溢价本质展开；
- 通过线：8/10 分。一票否决：矩阵维度颠倒、删除断言校验、直接返回虚假固定常数。
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
