r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 2/5 课
第 2 课：风险平价策略 (Risk Parity) 与边际风险贡献 (Marginal Risk Contribution)
================================================================================

【课程定位与第一性原理】
在传统的资产配置实践中（如经典的 60/40 股债组合），存在一个极其隐蔽却致命的“名义资本配置错觉”：
- 投资者名义上将 60% 资金分配给股票，40% 分配给债券；
- 但由于股票的年化波动率（约 16%~20%）是优质国债（约 4%~5%）的 3~4 倍；
- 根据资产方差展开：股票端承担了整个投资组合超过 85%~92% 的总方差风险！
- 一旦发生系统性股灾（如 2008 年次贷危机），所谓的“股债平衡”组合将毫无防守能力，净值直接遭受重创。

桥水基金（Bridgewater Associates）创始人 Ray Dalio 提出**风险平价（Risk Parity / 全天候 All Weather）**核心哲学：
1. 风险预算大于资本预算（Risk Budgeting > Capital Budgeting）：
   决定投资组合命运的是每一类资产对组合总波动率的“实际风险贡献（Risk Contribution）”，而非名义账面资金占比；
2. 边际风险贡献（Marginal Risk Contribution, MRC）：
   组合波动率 $\sigma_p(w) = \sqrt{w^T \Sigma w}$ 关于资产权重 $w_i$ 的一阶偏导数：
   $$\text{MRC}_i = \frac{\partial \sigma_p}{\partial w_i} = \frac{(\Sigma w)_i}{\sqrt{w^T \Sigma w}} = \frac{(\Sigma w)_i}{\sigma_p}$$
3. 绝对风险贡献（Risk Contribution, RC）与欧拉齐次定理（Euler's Theorem）：
   $$\text{RC}_i = w_i \times \text{MRC}_i = \frac{w_i (\Sigma w)_i}{\sigma_p}$$
   根据一阶齐次函数欧拉展开，所有资产的绝对风险贡献总和严格等于组合总波动率：
   $$\sum_{i=1}^N \text{RC}_i = \sum_{i=1}^N \frac{w_i (\Sigma w)_i}{\sigma_p} = \frac{w^T \Sigma w}{\sigma_p} = \sigma_p$$
4. 百分比风险贡献（Percentage Risk Contribution, PRC）与等风险贡献（ERC）：
   $$\text{PRC}_i = \frac{\text{RC}_i}{\sigma_p} = \frac{w_i (\Sigma w)_i}{w^T \Sigma w}, \quad \sum_{i=1}^N \text{PRC}_i = 1.0$$
   风险平价要求所有资产对组合总风险的贡献完全相等：
   $$\text{RC}_1 = \text{RC}_2 = \dots = \text{RC}_N = \frac{\sigma_p}{N} \iff \text{PRC}_i = \frac{1}{N}$$

【核心流程与心智模型】
```mermaid
flowchart TD
    AssetCov["大类资产历史协方差矩阵 Sigma"] --> WeightInit["初始权重猜测: 波动率倒数权重 w_0 ~ 1/sigma_i"]
    WeightInit --> MRC_Calc["计算组合当前边际风险贡献 MRC = Sigma * w / sigma_p"]
    MRC_Calc --> RC_Calc["计算各资产绝对风险贡献 RC_i = w_i * MRC_i 与占比 PRC_i = RC_i / sigma_p"]
    RC_Calc --> ObjLoss["计算风险均衡偏离度损失: sum (PRC_i - 1/N)^2"]
    ObjLoss --> CheckConv{"偏离度 < 1e-8 或收敛 ?"}
    CheckConv -- 否 --> SLSQP["SLSQP 优化迭代更新资产权重向量 w"]
    SLSQP --> MRC_Calc
    CheckConv -- 是 --> RiskParityPortfolio["输出等风险贡献 (ERC) 风险平价最优资产配置权重"]
```

【工业界实战场景与风控陷阱】
1. 低波资产加杠杆的流动性反噬（The Leverage Dilemma）：
   由于债券波动率极低，风险平价通常需要配置 60%~70% 的债券仓位。若不加杠杆，组合总年化收益仅有 4%~5%；
   为了达到股票级别的期望收益，机构通常对债券端施加 2~3 倍杠杆。然而在流动性紧缩或利率快速飙升时（如 2022 年），
   杠杆融资成本暴增且债券价格重挫，风险平价将遭受沉重打击。
2. 股债“负相关性”在通胀周期的失效（Regime Break）：
   全天候策略的根基建立在“经济衰退时股票大跌但国债大涨”的负相关避险逻辑。
   但一旦遭遇供给侧驱动的恶性通胀（如 2022 年全球通胀加息周期），央行被迫加息，引发“股债双杀”，
   传统风险平价会发生深度回撤，必须足额引入抗通胀大宗商品与黄金。

【思考题】
Q1: 为什么风险平价策略必须对低波动率的债券端施加杠杆（Leverage）才能达到机构投资人满意的年化回报？如果去杠杆运行，风险平价组合会面临什么现实困境？
Q2: 2022 年全球央行激进加息期间，传统 60/40 与风险平价（全天候）策略双双遭遇了历史级别的大幅回撤。请从“股债负相关性被通胀击穿”与“无风险折现率飙升”的金融工程机制剖析原因。
Q3: 怎样利用目标优化函数（如 Spinu 对数障碍函数或残差平方和）通过 SLSQP 优化器高效求解非对角相关协方差矩阵下的风险平价精确解？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现边际风险贡献 (MRC)、绝对风险贡献 (RC) 与百分比风险贡献 (PRC) 的数学解耦 (1.5分)；
  2. 准确构建等风险贡献 (ERC) 目标损失函数并使用 SLSQP 求解 (1.5分)；
  3. 准确验证在非对角相关协方差矩阵下，各资产 PRC 严格达到 1/N (1分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须从杠杆复利边界、宏观通胀体制与非线性凸优化深入剖析；
- 通过线：8/10 分。一票否决：误把资本等权当做风险平价、优化器未收敛、删除断言校验。
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
from scipy.optimize import minimize


def calculate_risk_contributions(
    weights: np.ndarray,
    cov_matrix: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """
    计算投资组合各项资产的边际风险贡献 (MRC)、绝对风险贡献 (RC) 与百分比风险贡献 (PRC)：
    1. 组合总波动率: sigma_p = sqrt(w^T * Sigma * w)
    2. 边际风险贡献 (MRC): MRC = (Sigma * w) / sigma_p
    3. 绝对风险贡献 (RC): RC_i = w_i * MRC_i
    4. 百分比风险贡献 (PRC): PRC_i = RC_i / sigma_p = (w_i * (Sigma * w)_i) / (w^T * Sigma * w)

    参数:
        weights: 资产配置权重向量 w (N 维, sum(w) = 1)
        cov_matrix: 资产协方差矩阵 Sigma (N x N)

    返回:
        Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
            (mrc, rc, prc, total_volatility)
    """
    # TODO: 实现 MRC, RC, PRC 及总波动率计算
    pass


def solve_risk_parity_weights(
    cov_matrix: np.ndarray,
    target_risk_budget: Optional[np.ndarray] = None,
    tol: float = 1e-10,
) -> np.ndarray:
    """
    基于非线性二次/残差最小化求解风险平价 (Equal Risk Contribution, ERC) 最优资产权重：
    优化目标:
        min_w  sum_{i=1}^N ( PRC_i(w) - b_i )^2
        s.t.   sum(w) = 1,  w_i >= 0
    若 target_risk_budget (b) 为 None，默认采用等风险平价 b_i = 1/N。

    参数:
        cov_matrix: 资产收益协方差矩阵 Sigma (N x N)
        target_risk_budget: 目标风险预算向量 b (N 维, 默认全等 1/N, sum(b) = 1)
        tol: SLSQP 优化收敛容差

    返回:
        np.ndarray: 风险平价最优权重向量 w_rp (N 维, sum(w) = 1)
    """
    # TODO: 实现风险平价非线性优化求解器
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 02: 风险平价策略与边际风险贡献单元测试")
    print("=" * 70)

    # 1. 检验传统 60/40 股债组合的“风险分配严重失衡”现象
    vols_2 = np.array([0.18, 0.05])  # 股票波动 18%, 债券波动 5%
    corr_2 = np.array([[1.0, -0.1], [-0.1, 1.0]])
    cov_2 = np.diag(vols_2) @ corr_2 @ np.diag(vols_2)

    w_6040 = np.array([0.60, 0.40])
    mrc_6040, rc_6040, prc_6040, vol_6040 = calculate_risk_contributions(w_6040, cov_2)
    print(f"传统 60/40 组合总波动率: {vol_6040*100:.2f}%")
    print(f"传统 60/40 股票风险贡献占比: {prc_6040[0]*100:.2f}%, 债券风险贡献占比: {prc_6040[1]*100:.2f}%")

    # 股票承担了超过 85% 的绝对风险
    assert prc_6040[0] > 0.85, f"传统 60/40 组合中股票风险占比应超过 85%, 实际: {prc_6040[0]*100:.2f}%"
    assert abs(np.sum(rc_6040) - vol_6040) < 1e-6, "欧拉展开: 绝对风险贡献之和必须严格等于组合总波动率"
    assert abs(np.sum(prc_6040) - 1.0) < 1e-6, "百分比风险贡献之和必须等于 1.0"

    # 2. 求解四类大类资产 [股票, 债券, 黄金, 大宗商品] 的等风险平价权重
    vols_4 = np.array([0.18, 0.05, 0.15, 0.22])
    corr_4 = np.array([
        [1.0, -0.2, 0.1, 0.3],
        [-0.2, 1.0, 0.2, -0.1],
        [0.1, 0.2, 1.0, 0.25],
        [0.3, -0.1, 0.25, 1.0],
    ])
    cov_4 = np.diag(vols_4) @ corr_4 @ np.diag(vols_4)

    w_rp = solve_risk_parity_weights(cov_4)
    mrc_rp, rc_rp, prc_rp, vol_rp = calculate_risk_contributions(w_rp, cov_4)

    print(f"\n风险平价资产配置权重: {np.round(w_rp, 4)}")
    print(f"风险平价组合年化波动率: {vol_rp*100:.2f}%")
    print(f"各项资产百分比风险贡献 PRC: {np.round(prc_rp, 4)}")

    # 3. 断言验证等风险贡献条件
    assert abs(np.sum(w_rp) - 1.0) < 1e-4, "权重之和必须等于 1.0"
    assert np.all(w_rp > 0.0), "风险平价权重必须全为严格正值"
    # 低波动的债券必须分配最大资本权重以平抑风险贡献
    assert w_rp[1] > 0.50, f"低波动债券权重应占主导 (>50%), 实际: {w_rp[1]:.4f}"
    # 每一类资产对总风险的贡献必须严格相等 (各占 25%)
    assert np.all(np.abs(prc_rp - 0.25) < 1e-3), f"所有资产的风险贡献必须严格均等为 25%, 实际: {prc_rp}"

    print("Lesson 02 风险平价单元测试全部通过！")
