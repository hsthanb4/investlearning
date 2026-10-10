r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 3/5 课
第 3 课：凯利公式数学推导、破产风险与动态杠杆约束 (参考答案版)
================================================================================

【Q1 深度参考答案】
算术平均收益（Arithmetic Return） vs 几何平均收益（Geometric Return）：为什么一个胜率 50%、盈利 60%、亏损 40% 的高期望抛硬币博弈（单次算术期望收益率高达 $+10\%$），若交易者每次满仓下注全部本金，其长期财富必然 100% 破产归零？请推导伯努利对数效用下的复合几何增长率公式。
- **[单期算术平均期望与多期复利的本质背离]**：
  单次博弈的算术期望收益率为：
  $$\mathbb{E}[R] = 0.5 \times (+60\%) + 0.5 \times (-40\%) = +30\% - 20\% = +10\%$$
  表面上看，这是一个极具吸引力、年化期望极高的“暴利策略”。然而，若每次将全部本金满仓下注（$f = 1.0$），经历一次盈利与一次亏损后，账户总资金的复合乘数为：
  $$W_2 / W_0 = (1 + 0.60) \times (1 - 0.40) = 1.60 \times 0.60 = 0.96$$
  历经两轮对称博弈后，投资者本金净亏损了 $4\%$！
- **[长期大数定律下的几何平均衰减公式]**：
  在经历 $2N$ 次博弈后（其中盈利 $N$ 次，亏损 $N$ 次），投资者的财富累积为：
  $$W_{2N} = W_0 \times (0.96)^N \xrightarrow{N \to \infty} 0$$
  复合几何单期增长率严格等于：
  $$g = \sqrt{(1 + 0.6)(1 - 0.4)} - 1 = \sqrt{0.96} - 1 \approx -2.02\%$$
- **[破产因果结论]**：算术平均完全忽略了“亏损百分比对本金的非对称杀伤（跌 50% 需涨 100% 回本）”。在乘法复利世界中，几何平均增长率才是决定长期生死存亡的唯一物理量。任何试图满仓下注的投资者，无论单期算术期望多高，在大数定律的时间长河中必然 100% 破产归零。

【Q2 深度参考答案】
全凯利（Full Kelly）的心理折磨与半凯利（Half Kelly）的工程黄金法则：全凯利仓位虽然在数学上渐近最大化长期财富增长率，但其回撤幅度往往超过 80%（有 1/3 的概率发生本金缩水 50% 以上）。为什么华尔街顶级对冲基金（如文艺复兴 Renaissance Technologies）在实盘中普遍将仓位硬性压缩至“半凯利（$0.5 f^*$）甚至 0.3 凯利”？
- **[全凯利回撤深度的数学宿命]**：全凯利公式 $f^*$ 最大化的是无限时间下的财富期望对数增长率 $\mathbb{E}[\ln W]$。但极值定理决定了：在全凯利峰值点附近，曲线极其陡峭，且伴随着极其恐怖的波动率。理论概率推导表明：采用全凯利下注的投资者，在财富翻倍之前遭遇本金回撤超过 $50\%$ 的概率恰好等于整整 $\frac{1}{3} \approx 33.3\%$！极少有量化对冲基金的投资人（LP）或基金经理的神经系统能够承受高达 80% 的净值回撤而不发生恐慌赎回或心理崩溃。
- **[半凯利（Half Kelly）的非对称工程红利]**：
  考察几何增长率的二阶泰勒展开：$g(f) \approx f \mu - \frac{1}{2} f^2 \sigma^2$。
  1. 当我们选择半凯利 $f = 0.5 f^*$ 时：
     $$g(0.5 f^*) = 0.5 f^* \mu - \frac{1}{2} (0.25 {f^*}^2) \sigma^2 = \frac{3}{4} g(f^*) = 75\% \times g(f^*)$$
  2. 而波动率与下注方差：$\text{Var}(0.5 f^*) = 0.25 \times \text{Var}(f^*)$，方差直接削减了整整 $75\%$！
  3. 这意味着：仅放弃 $25\%$ 的理论增长速度，就能换取风险方差暴跌 $75\%$、回撤幅度收窄一半以上的巨大安全边际。
- **[参数估计误差（Parameter Uncertainty）的安全气囊]**：真实市场的胜率 $p$ 和盈亏比 $b$ 从来不是固定常数。量化研究员由于回测过拟合，几乎 100% 会高估自己的真实胜率。若根据高估参数使用全凯利，实际下注仓位会直接越过峰值落入 $f > 2f^*$ 的自杀破产区。使用 0.3x ~ 0.5x 半凯利下注，提供了强大的安全容错缓冲区，确保策略即便在参数高估 50% 的极端恶劣情况下，仍然稳稳停留在正复合增长的安全半球。

【Q3 深度参考答案】
连续时间多资产凯利向量 $f^* = \Sigma^{-1}(\mu - r)$ 的协方差敏感性：在多资产连续时间几何布朗运动假设下，多资产凯利公式在数学形式上为何等价于风险厌恶系数 $\lambda=1$ 的马科维茨均值-方差优化？当估计的协方差矩阵存在相关性高估或低估时，连续凯利杠杆如何导致灾难性的多资产交叉爆仓？
- **[连续时间凯利与对数效用 MVO 的数学同构]**：假定 $N$ 项资产服从伊藤多维几何布朗运动：$dP / P = \mu dt + \sigma dW$。投资者分配杠杆向量 $\mathbf{f}$。根据伊藤引理（Itô's Lemma），投资组合财富的对数动态服从：
  $$d(\ln W) = \left( r + \mathbf{f}^T (\mu - r \mathbf{1}) - \frac{1}{2} \mathbf{f}^T \Sigma \mathbf{f} \right) dt + \mathbf{f}^T \sigma dW$$
  最大化对数漂移率 $\mathbb{E}[d(\ln W)/dt]$，对 $\mathbf{f}$ 求一阶偏导：
  $$\frac{\partial g}{\partial \mathbf{f}} = (\mu - r \mathbf{1}) - \Sigma \mathbf{f} = 0 \implies \mathbf{f}^* = \Sigma^{-1} (\mu - r \mathbf{1})$$
  这在数学形式上与马科维茨均值-方差优化器中设定绝对风险厌恶系数 $\lambda = 1$ 的效用函数完全恒等。
- **[协方差矩阵求逆的交叉杠杆放大灾难]**：当资产数量增加时，非对角线的资产相关系数估计极易失真。若低估了资产之间的尾部相关性（如误以为美股与欧洲股市相关性仅有 0.3，而在危机中飙升至 0.95），$\Sigma^{-1}$ 运算会误判两项资产具备巨大的双向对冲能力，进而输出极高的多空对冲总杠杆（例如多头配置 400%、空头配置 300%）。
- **[流动性挤兑引发的交叉穿仓]**：一旦危机来临，资产相关性瞬间收敛为 1（All correlations go to 1 in a crisis），原本假定的对冲保护荡然无存。此时高达数倍的组合总杠杆会在毫秒级内触发券商强制平仓线，引发多资产连锁交叉踩踏与永久性爆仓清盘。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：拒绝满仓狂妄，践行半凯利哲学</div>
  <div class="callout-body">
    凯利公式是度量贪婪边界的标尺，而非放飞杠杆的通行证。资深对冲基金投资经理的最大美德是克制——在胜率最高的优势博弈中，永远只下注半凯利，将生存权牢牢握在自己手中。
  </div>
</div>
"""

from typing import List, Dict, Any, Tuple
import numpy as np


def calculate_discrete_kelly(win_rate: float, win_loss_ratio: float) -> float:
    """
    计算经典离散二项博弈的凯利最优下注比例
    """
    if win_loss_ratio <= 1e-12:
        return 0.0
    val = (win_rate * win_loss_ratio - (1.0 - win_rate)) / win_loss_ratio
    return max(0.0, float(val))


def calculate_continuous_multi_asset_kelly(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.02,
) -> np.ndarray:
    """
    计算连续时间多资产凯利最优杠杆向量
    """
    inv_cov = np.linalg.inv(cov_matrix)
    excess_returns = expected_returns - risk_free_rate
    f_star = inv_cov @ excess_returns
    return f_star


def simulate_kelly_risk_of_ruin(
    mu: float,
    sigma: float,
    risk_free_rate: float = 0.02,
    kelly_multipliers: List[float] = [0.5, 1.0, 2.5],
    ruin_threshold: float = 0.20,
    n_simulations: int = 1000,
    n_steps: int = 252,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """
    蒙特卡洛破产概率与财富复利模拟引擎
    """
    f_opt = (mu - risk_free_rate) / (sigma ** 2)
    dt = 1.0 / float(n_steps)
    rng = np.random.default_rng(random_seed)
    results = {}

    for m in kelly_multipliers:
        lev = m * f_opt
        drift = (risk_free_rate + lev * (mu - risk_free_rate) - 0.5 * (lev ** 2) * (sigma ** 2)) * dt
        diffusion = lev * sigma * np.sqrt(dt)

        shocks = rng.normal(0.0, 1.0, size=(n_simulations, n_steps))
        log_rets = drift + diffusion * shocks
        log_wealth = np.zeros((n_simulations, n_steps + 1))
        log_wealth[:, 1:] = np.cumsum(log_rets, axis=1)
        wealth = np.exp(log_wealth)

        min_w = np.min(wealth, axis=1)
        ruin_count = np.sum(min_w <= ruin_threshold)
        ruin_prob = float(ruin_count / n_simulations)
        median_wealth = float(np.median(wealth[:, -1]))

        results[m] = {
            "ruin_prob": ruin_prob,
            "median_wealth": median_wealth,
        }

    return {
        "f_optimal": float(f_opt),
        "results": results,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 03: 凯利公式推导与破产概率单元测试 (参考答案版)")
    print("=" * 70)

    # 1. 验证离散凯利公式
    f_d1 = calculate_discrete_kelly(0.60, 1.5)
    assert abs(f_d1 - 0.333333) < 1e-4, f"离散凯利计算偏差: {f_d1}"

    f_d2 = calculate_discrete_kelly(0.40, 1.0)
    assert f_d2 == 0.0, "负期望博弈最优凯利仓位必须为 0.0"

    # 2. 验证多资产连续凯利矩阵求解
    mu_assets = np.array([0.10, 0.05])
    cov_assets = np.array([[0.04, 0.005], [0.005, 0.01]])
    rf = 0.02

    f_vec = calculate_continuous_multi_asset_kelly(mu_assets, cov_assets, risk_free_rate=rf)
    print(f"多资产连续最优凯利杠杆向量: {np.round(f_vec, 4)}")
    assert len(f_vec) == 2, "杠杆向量维度不符"
    assert abs(f_vec[0] - 1.7333) < 1e-2, f"资产 1 最优杠杆应约为 1.73, 实际: {f_vec[0]:.4f}"
    assert abs(f_vec[1] - 2.1333) < 1e-2, f"资产 2 最优杠杆应约为 2.13, 实际: {f_vec[1]:.4f}"

    # 3. 验证蒙特卡洛破产概率与复利模拟
    mc_res = simulate_kelly_risk_of_ruin(
        mu=0.12,
        sigma=0.20,
        risk_free_rate=0.02,
        kelly_multipliers=[0.5, 1.0, 2.5],
        ruin_threshold=0.20,
        n_simulations=1000,
        n_steps=252,
        random_seed=42,
    )

    f_opt = mc_res["f_optimal"]
    print(f"\n单资产理论全凯利杠杆 f*: {f_opt:.2f}")
    assert abs(f_opt - 2.50) < 1e-4, f"全凯利杠杆应为 (0.12 - 0.02) / 0.04 = 2.50, 实际: {f_opt}"

    for mult, stats_dict in mc_res["results"].items():
        print(f"乘数 {mult:3.1f}x (杠杆: {mult*f_opt:4.2f}) ➔ 破产率: {stats_dict['ruin_prob']*100:5.2f}%, 期末财富中位数: {stats_dict['median_wealth']:.4f}")

    assert mc_res["results"][0.5]["ruin_prob"] < 0.01, "半凯利破产率应接近 0"
    assert mc_res["results"][1.0]["ruin_prob"] < 0.05, "全凯利 1 年破产率应受控"
    assert mc_res["results"][2.5]["ruin_prob"] > 0.10, "过度杠杆破产率应显著激增 (>10%)"
    assert mc_res["results"][2.5]["median_wealth"] < mc_res["results"][0.5]["median_wealth"], "过度杠杆财富中位数必然因波动率拖累劣于半凯利"

    print("Lesson 03 参考答案测试全部通过 (Exit Code 0)！")
