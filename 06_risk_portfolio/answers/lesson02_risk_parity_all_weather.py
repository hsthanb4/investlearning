r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 2/5 课
第 2 课：风险平价策略 (Risk Parity) 与边际风险贡献 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么风险平价策略必须对低波动率的债券端施加杠杆（Leverage）才能达到机构投资人满意的年化回报？如果去杠杆运行，风险平价组合会面临什么现实困境？
- **低波资产的收益天花板与去杠杆困境**：
  在等风险贡献（ERC）优化下，由于优质主权债券（如 10Y 美债）的年化波动率（约 4%~5%）远低于权益股票（约 16%~20%），为了平衡二者的绝对风险贡献，风险平价模型通常必须将 60%~75% 的极高资本权重分配给低波债券，而股票仅能分配 15%~20%。
  若完全去杠杆运行（总仓位限制在 100%），假设股票长期年化回报为 9%，债券长期年化回报为 3.5%，大宗商品为 5%：
  组合无杠杆预期年化收益率仅为：$0.15 \times 9\% + 0.70 \times 3.5\% + 0.15 \times 5\% \approx 4.55\%$，组合年化波动率仅约 5.5%。
- **机构投资者负债端的现实约束**：
  大型机构投资者（如大学捐赠基金、养老金金控池）面临着每年 7%~8% 的刚性现金流支出要求与精算折现负债（Liability Matching）。
  无杠杆的风险平价策略虽然夏普比率极高（夏普达 0.8~1.0，远超传统股票的 0.4），但绝对名义收益过低，根本无法覆盖养老金的支出刚兑。
- **杠杆升维解法（桥水与 AQR 经典范式）**：
  桥水全天候基金与 AQR 风险平价基金的成熟解法是：利用回购协议（Repo）或国债期货对低波债券端施加 1.5~2.5 倍低成本杠杆，将整个组合的总波动率从 5.5% 主动放大至与股票同级别的 10%~12%。
  在保持原有优秀夏普比率的前提下，将年化回报推升至 9%~12%，从而在防御性与收益性之间达成完美统一。

【Q2 深度参考答案】
2022 年全球央行激进加息期间，传统 60/40 与风险平价（全天候）策略双双遭遇了历史级别的大幅回撤。请从“股债负相关性被通胀击穿”与“无风险折现率飙升”的金融工程机制剖析原因：
- **宏观主导因子的根本性切换：从增长周期到通胀周期**：
  在过去 20 年（2000~2020 年）的“大缓和时代”，全球处于低通胀甚至通缩中枢，主导经济周期的核心变量是“经济增长预期”。
  当经济遭遇衰退或股市大跌时，通胀处于低位，央行具备充裕空间通过大幅降息进行对冲，驱动长期国债价格暴涨。股债相关系数 $\rho < 0$，债券对冲股票呈现出极强的负相关避险红利。
  但在 2022 年，俄乌冲突引发全球能源大宗商品危机，叠加欧美超发货币引发 40 年未见之恶性供给侧通胀。
- **无风险折现率飙升引发股债双杀**：
  为了遏制通胀恶魔，美联储被迫放弃经济软着陆预期，连续加息 500 个基点。
  1. **折现率飙升杀股票**：全市场权益估值倍数（PE）遭遇断崖式压缩，标普500单年重挫超 19%；
  2. **基准利率飙升杀债券**：10 年期美债收益率从 1.5% 飙升至 4% 以上，彭博美债综合指数 2022 年暴跌超 13%，创下百年最差表现；
  3. **相关性由负转正**：股债相关系数由历史常态的 $-0.3$ 瞬间逆转跳升至 $+0.6$ 以上，互为对冲的假设彻底崩溃，演变为同向加速暴跌；
- **高杠杆债券持仓的致命反噬**：
  风险平价策略名义上重仓 60% 以上的债券底仓并使用了杠杆。在 2022 年，不仅债券现券价格雪崩，其回购融资借贷利息更从 0.25% 飙升至 5%，双重夹击导致风险平价组合遭遇成立以来最惨烈的年度回撤。

【Q3 深度参考答案】
怎样利用目标优化函数（如 Spinu 对数障碍函数或残差平方和）通过 SLSQP 优化器高效求解非对角相关协方差矩阵下的风险平价精确解？
- **残差平方和惩罚优化法（Maillard, Roncalli & Teiletche, 2010）**：
  1. 定义各项资产的百分比风险贡献：
     $$\text{PRC}_i(w) = \frac{w_i (\Sigma w)_i}{w^T \Sigma w}$$
  2. 构建以目标风险预算 $b_i = 1/N$ 为基准的二次残差目标函数：
     $$\min_w \sum_{i=1}^N \left( \text{PRC}_i(w) - \frac{1}{N} \right)^2 \quad \text{s.t.} \quad \sum_{i=1}^N w_i = 1, \; w_i \ge 0$$
  3. 采用 SLSQP 优化器迭代，其梯度平滑、直观且容易加入现实中的单资产持仓上下限（如 $w_i \le 0.40$）。
- **Spinu 对数障碍凸优化严格解（Spinu, 2013）**：
  Florin Spinu 证明，风险平价问题可以转化为如下无等式约束的对数凸优化问题：
  $$\min_x \frac{1}{2} x^T \Sigma x - \sum_{i=1}^N b_i \ln(x_i) \quad \text{s.t.} \quad x_i > 0$$
  1. 求关于 $x_i$ 的一阶偏导数（KKT 一阶最优条件）：
     $$\frac{\partial}{\partial x_i} = (\Sigma x)_i - \frac{b_i}{x_i} = 0 \iff x_i (\Sigma x)_i = b_i$$
  2. 这意味着任意两项资产的绝对风险贡献严格满足 $x_i (\Sigma x)_i = x_j (\Sigma x)_j = 1/N$；
  3. 由于对数障碍函数使得目标函数为严格凸函数（Strictly Convex），不存在局部极值点；
  4. 求解出最优向量 $x^*$ 后，直接进行尺度归一化：$w^* = \frac{x^*}{\sum_{i=1}^N x_i^*}$，即可获得无偏的等风险贡献精确最优权重。
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
