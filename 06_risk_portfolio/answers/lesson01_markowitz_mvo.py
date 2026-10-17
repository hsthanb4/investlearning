r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 1/5 课
第 1 课：马科维茨均值-方差理论 (MVO) 与有效前沿求解 (参考答案版)
================================================================================

【Q1 深度参考答案】
托宾两基金分离定理（Tobin's Separation Theorem）与资本市场线（CML）第一性原理：为什么在引入无风险利率 $R_f$ 后，所有理性投资者的最优风险资产配置都会收敛到唯一的“切点组合（Tangency Portfolio / Max Sharpe）”？不同风险偏好的投资者如何通过借贷无风险资产实现效用最大化？
- **[切线几何斜率的唯一全局最优性]**：在马科维茨风险-收益坐标系中，从无风险收益率点 $(0, R_f)$ 向有效前沿双曲线引一条射线，该射线的斜率即为夏普比率（Sharpe Ratio = $(E[R_p] - R_f)/\sigma_p$）。根据凸分析几何定理，当该射线与有效前沿刚好相切于切点组合（Tangency Portfolio）时，射线斜率达到全局极大值。此时该射线被称为资本市场线（Capital Market Line, CML）。
- **[风险资产与资金分配的完全两步解耦]**：托宾两基金分离定理指出，投资决策被完美切分为两个完全独立的阶段：
  1. **第一阶段（客观工程计算）**：所有投资者无论其主观风险偏好是极其保守还是极度激进，计算出的最优风险资产权重比例均严格一致——即全市场唯一的切点组合 $w^*$；
  2. **第二阶段（主观效用匹配）**：投资者仅需根据自身风险厌恶系数，在“无风险资产”与“切点组合 $w^*$”之间分配资本比例 $\alpha \in [0, +\infty)$。
- **[杠杆借贷与效用无差异曲线相切]**：极度保守者将 80% 资金存入无风险国债、20% 投资切点组合（位于 CML 左下方）；风险中性者 100% 配置切点组合；极度进取者以无风险利率借入杠杆资金配置 150% 切点组合（位于 CML 右上方延伸段）。由于 CML 线上任何一点的夏普比率均严格高于单纯风险资产前沿曲线，两基金分离方案实现了全市场所有风险偏好投资者的福利最大化。

【Q2 深度参考答案】
均值-方差优化“误差放大器（Error Maximizer）”假说：为什么理查德·米肖（Michaud）尖锐指出未加约束的 MVO 优化器实质是在“过度拟合收益率估计误差”？在协方差矩阵求逆 $\Sigma^{-1}$ 运算中，微小的输入预期收益率误差（如 $\Delta \mu = 0.5\%$）为何会导致最优权重发生高达 50% 以上的荒谬极端翻转？工程上如何通过收缩估计（Ledoit-Wolf Shrinkage）或黑石-利特曼（Black-Litterman）模型进行解耦？
- **[误差放大器的数学物理机制]**：无约束均值-方差最优权重解析解为 $w^* \propto \Sigma^{-1}(\mu - R_f \mathbf{1})$。协方差矩阵求逆本质是对其特征值进行倒数加权。在真实金融样本中，最小特征值通常由随机噪声（Estimation Noise）构成，求逆运算将其倒数放大数百倍。更致命的是，优化器具有极端功利性：如果某只股票由于历史采样偶然偏差导致样本均值 $\hat{\mu}$ 虚高 $0.5\%$，优化器会误将其视为天赐良机，调动海量杠杆疯狂给该资产满仓，同时做空与其高度相关的其他真实优质资产。
- **[病态翻转与极端权重集中度]**：输入端几乎无法察觉的微小估计残差，经过 $\Sigma^{-1}$ 矩阵相乘后，直接诱发输出权重发生 50% 以上的翻转，导致投资组合在 1~2 只特定资产上发生病态角点集中，实盘表现极度脆弱。
- **[工业级工程解决方案]**：
  1. **Ledoit-Wolf 协方差收缩（Covariance Shrinkage）**：将高噪样本协方差向结构化先验目标（如单因子市场模型或常相关矩阵）进行凸收缩：$\Sigma_{\text{shrunk}} = \delta F + (1-\delta) \hat{\Sigma}$，有效抬高最小特征值下界，消除病态求逆奇异性；
  2. **黑石-利特曼模型（Black-Litterman）**：放弃直接预测 $\mu$，而是反向从全市场资本总市值权重（Market Equilibrium）出发，通过反向优化提取“内生隐含均衡超额收益 $\Pi = \lambda \Sigma w_{\text{mkt}}$”，在此稳健基准上，再以贝叶斯框架融入投资经理的相对观点（Views），使最终优化权重平滑偏离基准，彻底消除了极端翻转。

【Q3 深度参考答案】
卖空约束（No-Shorting Constraint）的凸优化非线性影响：当允许无限制做空时，MVO 有析出封闭解析解；而当施加 $w_i \ge 0$ 的非负权重约束时，为什么必须借助 Karush-Kuhn-Tucker (KKT) 条件或二次规划（QP）数值求解？卖空限制是如何将有效前沿向右下方推移并降低理论最大夏普的？
- **[无约束解析解 vs 不等式约束的非光滑性]**：在允许做空（$w \in \mathbb{R}^N$）时，约束仅有单一方程 $\mathbf{1}^T w = 1$。拉格朗日乘子法可以直接求导并列出一阶线性方程组，求逆即可得出优雅的解析闭式解。然而，当加入卖空约束 $w_i \ge 0$ 时，约束条件变成了 $N$ 个不等式约束。每个不等式在边界处激活（$w_i = 0$）或未激活（$w_i > 0$），导致解的最优一阶条件必须满足互补松弛性（Complementary Slackness）：$\lambda_i \ge 0, w_i \ge 0, \lambda_i w_i = 0$。这不再是简单的线性代数问题，必须通过有效集法（Active Set）或内点法（Interior Point）进行二次规划（QP）迭代求解。
- **[可行解空间的几何压缩与前沿推移]**：从凸分析拓扑角度看，允许做空时的可行域是整个仿射超平面（Affine Hyperplane），而卖空限制将可行域严格限制在单纯形多胞体（Simplex）内部。更小的可行域意味着更苛刻的极值搜索空间，其全局最优解的目标函数值必然弱于或等于更大空间的最优解。
- **[夏普比率的被动折损与实盘现实折衷]**：卖空约束剥离了通过做空高估垃圾股来对冲系统性风险并提供资金杠杆的能力。因此，施加非负约束后的有效前沿曲线被硬生生向右下方推移（对于相同的收益，波动率更高；对于相同的波动率，收益更低），理论最大夏普比率不可避免地下跌 15%~30%。然而，这一理论折损换来的是实盘中免除了无限追缴保证金（Margin Call）的穿仓风险，是公募与大部分长期资管机构必不可少的物理合规约束。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：敬畏二次规划边界，拒绝纸面最优假象</div>
  <div class="callout-body">
    纯数学推导的无约束最优点往往落在实盘无法执行的荒谬做空角点上。在工业界，必须牢牢扎根于带有严格单票上限与卖空限制的非负二次规划，在约束空间内寻找真实可落地的最佳稳健解。
  </div>
</div>
"""

from typing import Tuple, Dict, Any, List
import numpy as np
try:
    from scipy.optimize import minimize
except ImportError:
    def _project_simplex(v, z=1.0):
        n = len(v)
        u = np.sort(v)[::-1]
        cssv = np.cumsum(u)
        rho = np.nonzero(u * np.arange(1, n + 1) > (cssv - z))[0][-1]
        theta = (cssv[rho] - z) / (rho + 1.0)
        return np.maximum(v - theta, 0.0)

    def minimize(fun, x0, method="SLSQP", bounds=None, constraints=None, tol=1e-8, options=None):
        x = np.copy(x0).astype(float)
        n = len(x)
        lr = 0.02
        for it in range(800):
            grad = np.zeros(n)
            f_val = fun(x)
            eps = 1e-6
            for i in range(n):
                xp = np.copy(x)
                xp[i] += eps
                grad[i] = (fun(xp) - f_val) / eps
            x_new = x - lr * grad
            x_proj = _project_simplex(x_new, 1.0)
            if constraints:
                cons_list = constraints if isinstance(constraints, (list, tuple)) else [constraints]
                for c in cons_list:
                    if c.get("type") == "eq":
                        val = c["fun"](x_proj)
                        if abs(val) > 1e-4:
                            grad_c = np.zeros(n)
                            for i in range(n):
                                xp = np.copy(x_proj)
                                xp[i] += eps
                                grad_c[i] = (c["fun"](xp) - val) / eps
                            x_proj = _project_simplex(x_proj - 0.4 * val * grad_c, 1.0)
            diff = np.max(np.abs(x_proj - x))
            x = x_proj
            if diff < 1e-7:
                break
        class Res:
            def __init__(self, x):
                self.x = x
                self.success = True
        return Res(x)



def calculate_portfolio_performance(
    weights: np.ndarray,
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
) -> Tuple[float, float]:
    """
    计算投资组合的年化预期收益率与年化波动率
    """
    ret = float(np.dot(weights, expected_returns))
    vol = float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))
    return ret, vol


def solve_global_minimum_variance(
    cov_matrix: np.ndarray,
) -> np.ndarray:
    """
    求解全球最小方差组合 (GMV Portfolio)
    """
    n = len(cov_matrix)
    # Check if unconstrained analytic solution w = Sigma^-1 1 / (1^T Sigma^-1 1) is non-negative
    try:
        inv_cov = np.linalg.pinv(cov_matrix)
        ones = np.ones(n)
        w_analytic = inv_cov @ ones / (ones.T @ inv_cov @ ones)
        if np.all(w_analytic >= -1e-5):
            w_opt = np.maximum(0.0, w_analytic)
            return w_opt / np.sum(w_opt)
    except Exception:
        pass

    w0 = np.ones(n) / float(n)
    bounds = [(0.0, 1.0)] * n
    cons = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0})

    def obj_variance(w):
        return np.dot(w.T, np.dot(cov_matrix, w))

    res = minimize(obj_variance, w0, method="SLSQP", bounds=bounds, constraints=cons)
    w_opt = np.maximum(0.0, res.x)
    return w_opt / np.sum(w_opt)


def solve_max_sharpe_portfolio(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.02,
) -> np.ndarray:
    """
    求解最大夏普比率组合 (Tangency / Maximum Sharpe Portfolio)
    """
    n = len(expected_returns)
    # Check if unconstrained analytic solution w = Sigma^-1 (mu - rf 1) is non-negative
    try:
        inv_cov = np.linalg.pinv(cov_matrix)
        excess_r = expected_returns - risk_free_rate * np.ones(n)
        w_analytic = inv_cov @ excess_r
        if np.sum(w_analytic) > 1e-12 and np.all(w_analytic >= -1e-5):
            w_opt = np.maximum(0.0, w_analytic)
            return w_opt / np.sum(w_opt)
    except Exception:
        pass

    w0 = np.ones(n) / float(n)
    bounds = [(0.0, 1.0)] * n
    cons = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0})

    def neg_sharpe(w):
        r = np.dot(w, expected_returns)
        v = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        return -(r - risk_free_rate) / (v + 1e-12)

    res = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds, constraints=cons)
    w_opt = np.maximum(0.0, res.x)
    return w_opt / np.sum(w_opt)


def solve_max_sharpe_portfolio(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.02,
) -> np.ndarray:
    """
    求解最大夏普比率组合 (Tangency / Maximum Sharpe Portfolio)
    """
    n = len(expected_returns)
    w0 = np.ones(n) / float(n)
    bounds = [(0.0, 1.0)] * n
    cons = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0})

    def neg_sharpe(w):
        r = np.dot(w, expected_returns)
        v = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        return -(r - risk_free_rate) / (v + 1e-12)

    res = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds, constraints=cons)
    w_opt = np.maximum(0.0, res.x)
    return w_opt / np.sum(w_opt)


def generate_efficient_frontier(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    num_points: int = 15,
) -> Dict[str, Any]:
    """
    生成马科维茨有效前沿 (Efficient Frontier) 离散曲线点集
    """
    w_gmv = solve_global_minimum_variance(cov_matrix)
    r_min, _ = calculate_portfolio_performance(w_gmv, expected_returns, cov_matrix)
    r_max = float(np.max(expected_returns))

    target_returns = np.linspace(r_min, r_max, num_points)
    n = len(expected_returns)
    bounds = [(0.0, 1.0)] * n

    frontier_vols = []
    frontier_weights = []

    def obj_var(w):
        return np.dot(w.T, np.dot(cov_matrix, w))

    for r_target in target_returns:
        cons = (
            {"type": "eq", "fun": lambda w: np.sum(w) - 1.0},
            {"type": "eq", "fun": lambda w, rt=r_target: np.dot(w, expected_returns) - rt},
        )
        res = minimize(obj_var, w_gmv, method="SLSQP", bounds=bounds, constraints=cons)
        w_pt = np.maximum(0.0, res.x)
        w_pt = w_pt / np.sum(w_pt)
        v_pt = float(np.sqrt(np.dot(w_pt.T, np.dot(cov_matrix, w_pt))))
        frontier_vols.append(v_pt)
        frontier_weights.append(w_pt)

    return {
        "target_returns": list(target_returns),
        "frontier_volatilities": frontier_vols,
        "frontier_weights": np.array(frontier_weights),
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 01: 马科维茨均值-方差模型单元测试 (参考答案版)")
    print("=" * 70)

    # 1. 基础性能计算验证 (2 资产基准)
    w_base = np.array([0.5, 0.5])
    mu_base = np.array([0.10, 0.20])
    cov_base = np.array([[0.04, 0.0], [0.0, 0.09]])
    p_ret, p_vol = calculate_portfolio_performance(w_base, mu_base, cov_base)
    assert abs(p_ret - 0.15) < 1e-4, f"组合预期收益应为 0.15, 实际: {p_ret}"
    assert abs(p_vol - 0.180277) < 1e-4, f"组合波动率应为 0.180277, 实际: {p_vol}"

    # 2. 四资产真实配置优化验证 [美股, 美债, 黄金, 大宗商品]
    mu_4 = np.array([0.10, 0.04, 0.07, 0.06])
    cov_4 = np.array([
        [0.040, 0.002, 0.005, 0.012],
        [0.002, 0.008, 0.001, 0.003],
        [0.005, 0.001, 0.025, 0.008],
        [0.012, 0.003, 0.008, 0.035],
    ])
    rf = 0.02

    # 求解全球最小方差组合 GMV
    w_gmv = solve_global_minimum_variance(cov_4)
    r_gmv, vol_gmv = calculate_portfolio_performance(w_gmv, mu_4, cov_4)
    print(f"GMV 权重: {np.round(w_gmv, 4)}, 收益: {r_gmv*100:.2f}%, 波动率: {vol_gmv*100:.2f}%")

    assert abs(np.sum(w_gmv) - 1.0) < 1e-4, "GMV 权重之和必须等于 1.0"
    assert np.all(w_gmv >= -1e-6), "GMV 权重不能存在负值做空"
    assert w_gmv[1] > 0.50, f"低波动债券在 GMV 中应占主要比重, 实际: {w_gmv[1]:.4f}"

    # 求解最大夏普比率组合 Tangency
    w_ms = solve_max_sharpe_portfolio(mu_4, cov_4, risk_free_rate=rf)
    r_ms, vol_ms = calculate_portfolio_performance(w_ms, mu_4, cov_4)
    sharpe_ms = (r_ms - rf) / vol_ms
    print(f"最大夏普权重: {np.round(w_ms, 4)}, 收益: {r_ms*100:.2f}%, 波动率: {vol_ms*100:.2f}%, 夏普: {sharpe_ms:.4f}")

    assert abs(np.sum(w_ms) - 1.0) < 1e-4, "最大夏普权重之和必须等于 1.0"
    assert np.all(w_ms >= -1e-6), "最大夏普权重不能存在负值做空"
    sharpe_gmv = (r_gmv - rf) / vol_gmv
    assert sharpe_ms >= sharpe_gmv, "切线组合的夏普比率必须高于 GMV 组合"

    # 生成有效前沿
    frontier = generate_efficient_frontier(mu_4, cov_4, num_points=10)
    print(f"有效前沿收益区间: {np.round(frontier['target_returns'], 4)}")
    print(f"有效前沿波动区间: {np.round(frontier['frontier_volatilities'], 4)}")

    assert len(frontier["target_returns"]) == 10, "前沿采样点数量不符"
    assert len(frontier["frontier_volatilities"]) == 10, "前沿波动率数量不符"
    vols = frontier["frontier_volatilities"]
    assert all(vols[i] <= vols[i + 1] + 1e-4 for i in range(len(vols) - 1)), "有效前沿上半支波动率应随收益递增"

    print("Lesson 01 参考答案测试全部通过 (Exit Code 0)！")
