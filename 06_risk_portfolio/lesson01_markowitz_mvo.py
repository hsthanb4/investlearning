r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 1/5 课
第 1 课：马科维茨均值-方差理论 (MVO) 与有效前沿求解 (Markowitz Efficient Frontier)
================================================================================

【课程定位与第一性原理】
哈里·马科维茨（Harry Markowitz 1952）现代投资组合理论（Modern Portfolio Theory, MPT）
是量化资产配置历史上的奠基之石。它首次以严格数学语言证明了：
投资组合的风险不等于各个单资产风险的简单线性加权，通过资产间的非完全相关性（$\rho < 1$），
分散化投资能够作为全金融市场中唯一的“免费午餐（Free Lunch）”，在不牺牲预期回报的前提下压缩总方差。

- **[两基金分离定理与切点组合]**：在引入无风险借贷利率 $R_f$ 后，所有理性投资者的有效前沿坍缩为一条唯一的资本市场线（CML），其与双曲线前沿的切点即为最大夏普比率组合。
- **[二次规划 (QP) 凸优化求解]**：在禁止做空（$w_i \ge 0$）与满仓预算（$\sum w_i = 1$）约束下，有效前沿是典型的严格凸二次规划问题，收敛于全局唯一最优解。
- **[误差放大器 (Error Maximizer) 现实缺陷]**：由于输入预期收益率 $\mu$ 极其难以准确估计，协方差矩阵求逆运算会放大估计噪音，必须引入权重上限或收缩估计治理。

【核心概念与就近图文排版】

1. 有效前沿双曲线与资本市场线 CML：
观察下图关于全局最小方差组合 (GMV)、有效前沿上支与无风险利率切点组合 (Max Sharpe) 拓扑几何：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.1.1：马科维茨有效前沿 (Efficient Frontier) 与资本市场线 (CML) 切点模型</span>
    <span class="diagram-tag">MARKOWITZ-MVO</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m06_l01_efficient_frontier_cml.svg -->
  </div>
</div>

- **[可行投资组合集 (Feasible Set)]**：所有权重合法组合构成的紧凑凸集，其最左侧外边缘构成投资组合双曲线前沿。
- **[全局最小方差组合 GMV]**：前沿最左端的顶点，代表在不考虑预期收益率约束下组合能达到的绝对最低波动率。
- **[有效前沿上支 (Efficient Frontier)]**：GMV 以上的凸边界曲线；对于相同的波动率，上支提供严格更高的预期收益率，下半支为劣解。

2. 二次规划求解等高椭圆与约束超平面：
下图展示了均值-方差凸优化在权重单纯形与协方差等高椭圆上的几何投影：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.1.2：二次规划 (QP) 求解几何拓扑：凸优化等高椭圆与单纯形约束面</span>
    <span class="diagram-tag">CONVEX-OPTIMIZATION</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m06_l01_quadratic_programming_geometry.svg -->
  </div>
</div>

- **[等方差椭圆轮廓线]**：目标函数 $\frac{1}{2} w^T \Sigma w$ 在权重空间中形成一组以原点或无约束极值点为中心的同心同轴椭球。
- **[线性单纯形约束超平面]**：$\sum w_i = 1$ 与 $w_i \ge 0$ 构成了多维多胞体可行域（Simplex）。
- **[KKT 切点条件收敛]**：优化解发生在等高线椭球与单纯形可行域边界相切的切点位置，保证解的全局唯一性。

3. 误差放大器效应与病态权重翻转：
下图展示了预期收益率产生微小 $0.5\%$ 估计扰动时，无约束优化权重发生的剧烈病态翻转：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.1.3：马科维茨“误差放大器”(Error Maximizer) 效应与病态权重翻转</span>
    <span class="diagram-tag">NUMERICAL-INSTABILITY</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m06_l01_error_maximization_instability.svg -->
  </div>
</div>

- **[协方差矩阵求逆敏感性]**：无约束解析解 $w^* \propto \Sigma^{-1} (\mu - r \mathbf{1})$。条件数（Condition Number）过高时对 $\mu$ 的扰动极度放大。
- **[极端权重荒谬配置]**：微调某个资产预期收益率，其配置权重可能从 50% 暴增至 92%，而另一个资产被动砍至 8%。
- **[工程治理约束网]**：必须施加单资产上限（如 $w_i \le 15\%$）或对协方差矩阵使用 Ledoit-Wolf 收缩估计。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：分散化是全金融市场唯一的免费午餐</div>
  <div class="callout-body">
    只要资产间相关系数 $\rho < 1$，资产组合方差就必然严格小于加权单项方差之和。通过将低相关甚至负相关的资产（股票、国债、黄金、CTA）有机组合，组合能在完全不牺牲收益的前提下将波动率削减 30%~50%。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁直接将未经正则化或未经收缩的原始历史收益率均值作为 $\mu$ 输入 MVO 优化器！对历史平均收益的盲信只会产生对过去赢家资产的过度杠杆集中配置，在风格反转时招致毁灭性打击。
  </div>
</div>

【数学与优化模型】
$$\min_{w} \frac{1}{2} w^T \Sigma w \quad \text{s.t.} \quad \mathbf{1}^T w = 1, \quad w_i \ge 0 \quad (\text{GMV 规划})$$
$$\max_{w} \frac{w^T \mu - R_f}{\sqrt{w^T \Sigma w}} \quad \text{s.t.} \quad \mathbf{1}^T w = 1, \quad w_i \ge 0 \quad (\text{Max Sharpe 规划})$$
$$\mu_p = w^T \mu, \quad \sigma_p = \sqrt{w^T \Sigma w}$$
定义域：$\Sigma \succ 0 \text{ (严格正定)}, \quad w \in [0, 1]^N, \quad R_f \ge 0$。

【思考题】
Q1: 托宾两基金分离定理（Tobin's Separation Theorem）与资本市场线（CML）第一性原理：为什么在引入无风险利率 $R_f$ 后，所有理性投资者的最优风险资产配置都会收敛到唯一的“切点组合（Tangency Portfolio / Max Sharpe）”？不同风险偏好的投资者如何通过借贷无风险资产实现效用最大化？
Q2: 均值-方差优化“误差放大器（Error Maximizer）”假说：为什么理查德·米肖（Michaud）尖锐指出未加约束的 MVO 优化器实质是在“过度拟合收益率估计误差”？在协方差矩阵求逆 $\Sigma^{-1}$ 运算中，微小的输入预期收益率误差（如 $\Delta \mu = 0.5\%$）为何会导致最优权重发生高达 50% 以上的荒谬极端翻转？工程上如何通过收缩估计（Ledoit-Wolf Shrinkage）或黑石-利特曼（Black-Litterman）模型进行解耦？
Q3: 卖空约束（No-Shorting Constraint）的凸优化非线性影响：当允许无限制做空时，MVO 有析出封闭解析解；而当施加 $w_i \ge 0$ 的非负权重约束时，为什么必须借助 Karush-Kuhn-Tucker (KKT) 条件或二次规划（QP）数值求解？卖空限制是如何将有效前沿向右下方推移并降低理论最大夏普的？

【评分与通过规则】
- 代码 4 分：全局最小方差组合 GMV 求解 (1分) + 最大夏普切线组合求解 (1.5分) + 有效前沿生成器 (1.5分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：从两基金分离、误差放大器求逆数值不稳定性及凸优化 KKT 条件展开
- 通过线：8/10 分。一票否决：权重之和不等于 1、有效前沿非单调
"""

from typing import Tuple, Dict, Any, List
import numpy as np
from scipy.optimize import minimize


def calculate_portfolio_performance(
    weights: np.ndarray,
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
) -> Tuple[float, float]:
    """
    计算投资组合的年化预期收益率与年化波动率：
        R_p = w^T * mu
        sigma_p = sqrt(w^T * Sigma * w)

    参数:
        weights: 资产配置权重向量 w (N 维, sum(w) = 1)
        expected_returns: 资产预期收益率向量 mu (N 维)
        cov_matrix: 资产收益协方差矩阵 Sigma (N x N)

    返回:
        Tuple[float, float]: (组合预期收益率, 组合波动率)
    """
    # TODO: 实现组合期望收益率与波动率计算
    pass


def solve_global_minimum_variance(
    cov_matrix: np.ndarray,
) -> np.ndarray:
    """
    求解全球最小方差组合 (GMV Portfolio)：
        min_w  w^T * Sigma * w
        s.t.   sum(w) = 1,  w_i >= 0

    参数:
        cov_matrix: 资产收益协方差矩阵 Sigma (N x N)

    返回:
        np.ndarray: GMV 最优权重向量 w_gmv (N 维)
    """
    # TODO: 实现 GMV 二次规划求解器
    pass


def solve_max_sharpe_portfolio(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.02,
) -> np.ndarray:
    """
    求解最大夏普比率组合 (Tangency / Maximum Sharpe Portfolio)：
        max_w  (w^T * mu - rf) / sqrt(w^T * Sigma * w)
        s.t.   sum(w) = 1,  w_i >= 0

    参数:
        expected_returns: 资产预期收益率向量 mu (N 维)
        cov_matrix: 资产收益协方差矩阵 Sigma (N x N)
        risk_free_rate: 年化无风险利率 rf

    返回:
        np.ndarray: 最大夏普最优权重向量 w_ms (N 维)
    """
    # TODO: 实现最大夏普比率优化求解器
    pass


def generate_efficient_frontier(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    num_points: int = 15,
) -> Dict[str, Any]:
    """
    生成马科维茨有效前沿 (Efficient Frontier) 离散曲线点集：
    1. 求解 GMV 组合，获得前沿最低收益边界 R_min 与对应最小方差 sigma_min；
    2. 找到单资产最高收益 R_max；
    3. 在 [R_min, R_max] 区间内均匀采样 num_points 个目标收益率 R_target；
    4. 对每个目标收益率求解带等式收益约束的方差最小化二次规划：
           min_w  w^T * Sigma * w
           s.t.   w^T * mu = R_target,  sum(w) = 1,  w_i >= 0

    返回字典包含:
        - "target_returns": 目标收益率列表
        - "frontier_volatilities": 对应的有效前沿最优最小波动率列表
        - "frontier_weights": 对应的各点资产权重矩阵 (num_points x N)
    """
    # TODO: 实现有效前沿离散采样与二次规划求解
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 01: 马科维茨均值-方差模型与有效前沿单元测试")
    print("=" * 70)

    # 1. 基础性能计算验证 (2 资产基准)
    w_base = np.array([0.5, 0.5])
    mu_base = np.array([0.10, 0.20])
    cov_base = np.array([[0.04, 0.0], [0.0, 0.09]])  # 独立资产
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
    # 低波动的债券资产应分配最高权重
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
    # 有效前沿上半支必须满足：随着目标收益率上升，最小波动率单调递增
    vols = frontier["frontier_volatilities"]
    assert all(vols[i] <= vols[i + 1] + 1e-4 for i in range(len(vols) - 1)), "有效前沿上半支波动率应随收益递增"

    print("Lesson 01 马科维茨均值-方差模型单元测试全部通过！")
