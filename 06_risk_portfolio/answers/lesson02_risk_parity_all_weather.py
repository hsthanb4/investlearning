r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 2/5 课
第 2 课：风险平价 (Risk Parity) 模型与全天候资产配置 (参考答案版)
================================================================================

【Q1 深度参考答案】
传统 60/40 股债配置的“名义分散化假象”：为什么表面上配置了 40% 债券资金的经典组合，其组合方差风险的 90% 以上仍然被股票风险独占？请从边际风险贡献（MRC）与欧拉方差分解定理进行严密数学推导。
- **[欧拉齐次函数定理与方差完全展开]**：组合总方差 $\sigma_p^2 = w^T \Sigma w$ 是关于权重向量 $w$ 的二阶齐次函数；总波动率 $\sigma_p(w) = \sqrt{w^T \Sigma w}$ 是一阶齐次函数。根据欧拉齐次函数定理：
  $$\sigma_p(w) = \sum_{i=1}^N w_i \frac{\partial \sigma_p}{\partial w_i} = \sum_{i=1}^N w_i \cdot \text{MRC}_i = \sum_{i=1}^N \text{TRC}_i$$
  其中，资产 $i$ 的边际风险贡献定义为 $\text{MRC}_i = \frac{(\Sigma w)_i}{\sigma_p}$，总风险贡献为 $\text{TRC}_i = w_i \cdot \text{MRC}_i$。
- **[60/40 组合参数带入代数推导]**：假定股票年化波动率 $\sigma_s = 18\%$，长期国债年化波动率 $\sigma_b = 4\%$，股债相关系数 $\rho = 0$。名义权重 $w_s = 0.60, w_b = 0.40$。
  1. 组合总方差：$\sigma_p^2 = (0.6)^2 \times (0.18)^2 + (0.4)^2 \times (0.04)^2 = 0.011664 + 0.000256 = 0.01192$；
  2. 组合总波动率：$\sigma_p = \sqrt{0.01192} \approx 10.92\%$；
  3. 股票的方差贡献比例：$\frac{w_s^2 \sigma_s^2}{\sigma_p^2} = \frac{0.011664}{0.01192} \approx 97.85\%$；
  4. 债券的方差贡献比例：$\frac{w_b^2 \sigma_b^2}{\sigma_p^2} = \frac{0.000256}{0.01192} \approx 2.15\%$。
- **[结论与投委会定性]**：数学推导无可辩驳地证明：表面上配置了 40% 现金给债券的 60/40 组合，其底层有接近 98% 的风险被股票绝对垄断。债券所谓的对冲分散效果在数量级上微不足道，所谓 60/40 组合实质就是一个被动下注股市单边牛市的高风险股票基金。

【Q2 深度参考答案】
风险平价（Risk Parity）对高杠杆（Leverage）的依赖与潜在致命死穴：为了让低波动资产（如长期国债）贡献与高波动股票相等的风险预算，风险平价策略必须对债券端进行 2~3 倍的杠杆放大。在 2022 年全球央行激进加息引发“股债双杀（Stock-Bond Positive Correlation Shock）”时，该机制为何遭遇历史性惨烈回撤？
- **[为了平价被迫加杠杆的内生矛盾]**：风险平价的核心要求是：股票与债券的风险贡献必须相等（$\text{TRC}_s = \text{TRC}_b$）。若股票波动率是债券的 4 倍，由 $w_s \sigma_s \approx w_b \sigma_b$ 可得，名义资本权重必须满足 $w_b \approx 4 w_s$。未加杠杆的纯现金风险平价只能配置 20% 股票 + 80% 债券，其组合预期收益率极低（仅有 4%~5%）。为了达到机构投资者 8%~10% 的目标收益率，策略必须借入廉价短期资金，将低波动债券端放大 2~3 倍杠杆（整体总组合杠杆率达到 200%~300%）。
- **[股债负相关性假说的基石动摇]**：过去 30 年（1990~2020）风险平价之所以所向披靡，关键依赖于一个外生宏观假定：在温和通胀与降息周期中，股债呈现天然的负相关性（$\rho < 0$，美股暴跌时资金涌入美债避险推高债价）。
- **[2022 年滞胀冲击下的双杀惨剧]**：2022 年美联储遭遇 40 年未遇的高通胀，被迫以 75 bps 的惊人节奏连续暴烈加息。由于通胀直接摧毁了固收资产的真实购买力，美国 30 年期国债全年暴跌超 30%，同时高估值科技股崩塌，股债相关性瞬间逆转为强正相关（$\rho \approx +0.6$）。风险平价策略重仓并加了 2.5 倍杠杆的债券端发生雪崩，不仅未能提供防守，反而成为亏损的最大放大器，导致全市场风险平价基金在 2022 年录得超 -25% 的历史最惨回撤。

【Q3 深度参考答案】
达利欧（Ray Dalio）全天候（All Weather）框架的宏观四象限哲学：请阐述全天候模型如何依据“经济增长（超预期/低于预期）”与“通胀（超预期/低于预期）”划分四大象限，并说明为什么黄金、大宗商品、通胀保值国债（TIPS）是传统股债组合抵御“滞胀（Stagflation）”不可或缺的对冲基石？
- **[宏观环境定价的二维预期差结构]**：达利欧认为，驱动所有资产价格波动的唯二核心宏观变量是“实际经济增长”与“通货膨胀”；并且资产价格变动不取决于变量的绝对水平，而取决于它们“相对于市场前期隐含预期（Expectations）的偏离差”：
  1. **经济增长超预期（Rising Growth）**：企业盈利繁荣，配置股票、信用债、商品；
  2. **经济增长低于预期（Falling Growth）**：经济下行衰退，央行降息救市，配置长期国债；
  3. **通胀低于预期（Falling Inflation）**：物价平稳利率下行，配置股票、成长型资产与长久期名义债券；
  4. **通胀超预期（Rising Inflation）**：物价飞涨利率飙升，名义债券遭受折现率打击，传统股票遭遇利润率挤压，必须配置大宗商品、黄金与 TIPS。
- **[传统股债组合在“滞胀象限”的致命防守真空]**：传统 60/40 组合只覆盖了“经济增长超预期”与“通胀低于预期”两个顺风象限，它在“经济增长低于预期 + 通胀超预期”的【滞胀象限】完全是裸奔的。在滞胀时期，分子端经济下行打击股票，分母端通胀推高贴现率打击债券，名义股债双双暴跌。
- **[实物资产与通胀保值券的物理防线]**：
  1. **大宗商品（Commodities）**：原材料与原油往往正是引发通胀的源头，价格随供需缺口暴涨，产生极高的抗通胀现金流；
  2. **TIPS（通胀保值国债）**：本金随 CPI 挂钩上调，直接对冲通胀风险，消除期限贴现侵蚀；
  3. **黄金（Gold）**：作为终极法币信用对冲物，在实际利率转负与地缘通胀失控时展现出无可替代的避险凸性。全天候通过在四大象限各平衡 25% 的风险预算，彻底消除了宏观盲区。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：用风险计价资产，用象限平衡周期</div>
  <div class="callout-body">
    资本的计价币种会贬值，但真实的风险贡献守恒不变。全天候模型的伟大之处在于承认人类对未来的不可预测性，通过在多维宏观风险源之间达成严格的风险平价，构建起真正穿透周期的反脆弱诺亚方舟。
  </div>
</div>
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
from scipy.optimize import minimize


def calculate_risk_contributions(
    weights: np.ndarray,
    cov_matrix: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """
    计算投资组合各项资产的边际风险贡献 (MRC)、绝对风险贡献 (RC) 与百分比风险贡献 (PRC)
    """
    w = np.array(weights).flatten()
    vol_p = float(np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))))
    if vol_p < 1e-12:
        n = len(w)
        return np.zeros(n), np.zeros(n), np.ones(n) / n, 0.0

    # 边际风险贡献 MRC = (Sigma * w) / vol_p
    mrc = (cov_matrix @ w) / vol_p

    # 绝对风险贡献 RC_i = w_i * MRC_i
    rc = w * mrc

    # 百分比风险贡献 PRC_i = RC_i / vol_p
    prc = rc / vol_p

    return mrc, rc, prc, vol_p


def solve_risk_parity_weights(
    cov_matrix: np.ndarray,
    target_risk_budget: Optional[np.ndarray] = None,
    tol: float = 1e-10,
) -> np.ndarray:
    """
    基于非线性残差最小化求解风险平价 (Equal Risk Contribution, ERC) 最优资产权重
    """
    n = len(cov_matrix)
    if target_risk_budget is None:
        b = np.ones(n) / float(n)
    else:
        b = np.array(target_risk_budget) / float(np.sum(target_risk_budget))

    # 初始猜测：反波动率加权
    vols = np.sqrt(np.diag(cov_matrix))
    inv_vols = 1.0 / np.maximum(vols, 1e-6)
    w0 = inv_vols / np.sum(inv_vols)

    bounds = [(1e-6, 1.0)] * n
    cons = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0})

    def obj_erc(w):
        w_norm = w / np.sum(w)
        vol_p = np.sqrt(w_norm.T @ cov_matrix @ w_norm)
        if vol_p < 1e-12:
            return 1.0
        mrc = (cov_matrix @ w_norm) / vol_p
        rc = w_norm * mrc
        prc = rc / vol_p
        return np.sum((prc - b) ** 2)

    res = minimize(
        obj_erc,
        w0,
        method="SLSQP",
        bounds=bounds,
        constraints=cons,
        tol=tol,
        options={"maxiter": 500},
    )

    w_opt = np.maximum(0.0, res.x)
    return w_opt / np.sum(w_opt)


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 02: 风险平价策略与边际风险贡献单元测试 (参考答案版)")
    print("=" * 70)

    # 1. 检验传统 60/40 股债组合的“风险分配严重失衡”现象
    vols_2 = np.array([0.18, 0.05])
    corr_2 = np.array([[1.0, -0.1], [-0.1, 1.0]])
    cov_2 = np.diag(vols_2) @ corr_2 @ np.diag(vols_2)

    w_6040 = np.array([0.60, 0.40])
    mrc_6040, rc_6040, prc_6040, vol_6040 = calculate_risk_contributions(w_6040, cov_2)
    print(f"传统 60/40 组合总波动率: {vol_6040*100:.2f}%")
    print(f"传统 60/40 股票风险贡献占比: {prc_6040[0]*100:.2f}%, 债券风险贡献占比: {prc_6040[1]*100:.2f}%")

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
    assert w_rp[1] > 0.50, f"低波动债券权重应占主导 (>50%), 实际: {w_rp[1]:.4f}"
    assert np.all(np.abs(prc_rp - 0.25) < 1e-3), f"所有资产的风险贡献必须严格均等为 25%, 实际: {prc_rp}"

    print("Lesson 02 参考答案测试全部通过 (Exit Code 0)！")
