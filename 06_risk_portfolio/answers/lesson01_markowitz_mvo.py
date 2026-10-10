r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 1/5 课
第 1 课：马科维茨均值-方差模型、有效前沿与最大夏普组合 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么实践中对历史协方差矩阵直接求逆（Markowitz 纯数学优化）会导致“极端畸变权重”（Error Maximizer）？如何用 Ledoit-Wolf 收缩估计进行修正？
- **“错误放大器”（Michaud, 1989）的数理机制**：
  在均值-方差优化（MVO）中，最优权重数学解形式为 $w^* \propto \Sigma^{-1} (\mu - r_f)$。
  1. **参数敏感性极其非对称**：Chopra & Ziemba (1993) 证明，预期收益率 $\mu$ 的估计误差对权重配置破坏的危害程度是方差估计误差的 10 倍以上；
  2. **逆向放大错误**：优化器在数学上本质是一个“极端值放大器”。若某些资产在历史样本期内因为纯粹的随机游走偶然表现出色（历史均值偏高 $\hat{\mu}_i > \mu$），或者某些资产样本波动率碰巧被低估（$\hat{\sigma}_i < \sigma$），优化器会极其“贪婪”地将资金数倍重仓在该资产上；反之，若某优质资产在样本期遭遇偶发下挫，会被直接清零甚至大幅做空。这种在样本内看似“完美”的最优组合，在样本外真实市场中往往发生毁灭性崩塌。
- **协方差矩阵求逆的病态条件数（Condition Number）**：
  当资产数量 $N$ 较大而样本历史期数 $T$ 有限时（例如 $N=50, T=100$），样本协方差矩阵 $\hat{\Sigma}$ 的最小特征值非常接近于 0。在矩阵求逆 $\hat{\Sigma}^{-1}$ 时，小特征值的倒数会将历史采样噪声放大数十倍，导致权重对输入的微小扰动产生剧烈抖动。
- **Ledoit-Wolf 收缩估计（Shrinkage Estimation）修正**：
  Olivier Ledoit 与 Michael Wolf (2004) 提出结构化收缩框架：
  1. 样本协方差矩阵 $S$ 具有无偏但高估计方差的特征；
  2. 高度结构化的目标矩阵 $F$（如单因子市场模型或常相关矩阵 $\bar{\rho}$）具有低估计方差但有偏的特征；
  3. 通过在 Frobenius 范数下求解渐近最优收缩强度 $\alpha^* \in [0, 1]$：
     $$\Sigma_{\text{LW}} = \alpha^* F + (1 - \alpha^*) S$$
     有效拉升了接近于零的微小特征值，极大降低了矩阵条件数，彻底消除了极端权重分配，使样本外夏普比率提升 30%~50%。

【Q2 深度参考答案】
什么是夏普比率（Sharpe Ratio）与索提诺比率（Sortino Ratio）的区别？为什么下行波动率（Downside Volatility）比总波动率更符合机构投资者的真实效用偏好？
- **公式定义与惩罚项差异**：
  1. **夏普比率（Sharpe Ratio）**：
     $$\text{Sharpe} = \frac{\mathbb{E}[R_p] - R_f}{\sigma_p}, \quad \text{其中 } \sigma_p = \sqrt{\frac{1}{T-1} \sum_{t=1}^T (R_{p,t} - \bar{R}_p)^2}$$
     将高于均值的向上暴涨波动与低于均值的向下暴跌波动完全同等视作“方差风险”进行无差别惩罚；
  2. **索提诺比率（Sortino Ratio）**：
     $$\text{Sortino} = \frac{\mathbb{E}[R_p] - R_{\text{target}}}{\sigma_{\text{downside}}}, \quad \text{其中 } \sigma_{\text{downside}} = \sqrt{\frac{1}{T} \sum_{t=1}^T \min(0, R_{p,t} - R_{\text{target}})^2}$$
     仅将低于目标基准（如无风险利率或 0）的下行损失视为真正风险。
- **投资者真实效用偏好不对称性（Loss Aversion）**：
  1. 根据 Kahneman & Tversky 前景理论（Prospect Theory），人类对亏损的心理痛苦感受是对等收益快感的 2~2.5 倍；
  2. 向上大幅波动的资产（如深度虚值看涨期权、成长突变股、右偏正凸性策略）是投资人梦寐以求的收益来源，绝非风险；夏普比率会对其做出严重负向低估惩罚；
  3. 索提诺比率能够精确识别具有“有限下行回撤、无限上行凸性”的优秀策略，更加符合顶级对冲基金配置专户的考核准则。

【Q3 深度参考答案】
为什么负相关的两项资产组合（$\rho < 0$）可以实现在预期收益不降的前提下大幅压低总方差？请从方差展开式推导证明“完全负相关下构建零方差组合”的数学条件：
- **两资产方差代数展开**：
  设两资产权重分别为 $w_1, w_2$（满足 $w_1 + w_2 = 1, w_1, w_2 > 0$），单资产波动率为 $\sigma_1, \sigma_2$，相关系数为 $\rho \in [-1, 1]$。
  投资组合方差公式为：
  $$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho \sigma_1 \sigma_2$$
- **负相关性降低风险机制**：
  组合预期收益 $\mathbb{E}[R_p] = w_1 \mu_1 + w_2 \mu_2$ 是线性的，不受相关系数 $\rho$ 影响。
  而当 $\rho < 0$ 时，交叉项 $2 w_1 w_2 \rho \sigma_1 \sigma_2 < 0$ 成为一个**天然的负风险对冲项**，强制将组合总方差压减至远低于单资产加权方差的水平。
- **完全负相关（$\rho = -1$）下零方差组合的严格数学证明**：
  当 $\rho = -1$ 时，交叉项变为完全平方形式：
  $$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 - 2 w_1 w_2 \sigma_1 \sigma_2 = (w_1 \sigma_1 - w_2 \sigma_2)^2$$
  若要使得投资组合总方差严格为零（$\sigma_p = 0$）：
  $$(w_1 \sigma_1 - w_2 \sigma_2)^2 = 0 \implies w_1 \sigma_1 = w_2 \sigma_2$$
  代入全仓约束条件 $w_2 = 1 - w_1$：
  $$w_1 \sigma_1 = (1 - w_1) \sigma_2 \implies w_1 (\sigma_1 + \sigma_2) = \sigma_2$$
  求解得到解析最优权重：
  $$w_1^* = \frac{\sigma_2}{\sigma_1 + \sigma_2}, \quad w_2^* = \frac{\sigma_1}{\sigma_1 + \sigma_2}$$
  此时组合方差严格等于 0，而组合预期收益率为：
  $$R_p = \frac{\sigma_2 \mu_1 + \sigma_1 \mu_2}{\sigma_1 + \sigma_2} > 0$$
  通过两项自身充满价格波动的风险资产，完美合成了零风险、正收益的确定性资产。这是马科维茨分散化理论最经典的数学证明。
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
