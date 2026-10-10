r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 3/5 课
第 3 课：凯利公式数学推导、破产概率与分数凯利 (Kelly Criterion & Risk of Ruin)
================================================================================

【课程定位与第一性原理】
在量化交易与博弈论的数学皇冠上，John L. Kelly Jr. (1956) 与 Edward O. Thorp (1969) 推导出的
**凯利公式（Kelly Criterion）**被誉为资本复利增长的唯一数学最优解。

1. 离散博弈下的凯利推导：
   - 设交易者在每次博弈中投入资金比例 $f \in [0, 1)$，胜率为 $p$，净盈亏比为 $b$（获利 $b \cdot f$，亏损 $f$）；
   - 目标：最大化财富长期对数几何增长率：
     $$\max_{f} \; \mathbb{E}[\ln W] = p \ln(1 + b f) + (1 - p) \ln(1 - f)$$
   - 一阶导数极值条件：
     $$\frac{d \mathbb{E}[\ln W]}{df} = \frac{p b}{1 + b f} - \frac{1 - p}{1 - f} = 0 \implies f^* = \frac{p b - (1 - p)}{b} = p - \frac{1 - p}{b}$$
   - 若期望为负（$p b - (1 - p) \le 0$），最优下注比例为 0（绝对不入场）。

2. 连续几何布朗运动（GBM）与多资产连续凯利公式：
   - 资产价格服从 $d S_t / S_t = \mu dt + \sigma dW_t$，无风险借贷利率为 $r_f$；
   - 财富演化：$\frac{d W_t}{W_t} = (r_f + f (\mu - r_f)) dt + f \sigma dW_t$；
   - 根据伊藤引理（Itô's Lemma）：
     $$d \ln W_t = \left[ r_f + f (\mu - r_f) - \frac{1}{2} f^2 \sigma^2 \right] dt + f \sigma dW_t$$
   - 对数增长率是关于杠杆 $f$ 的二次凸抛物线：
     $$g(f) = r_f + f (\mu - r_f) - \frac{1}{2} f^2 \sigma^2 \implies f^* = \frac{\mu - r_f}{\sigma^2}$$
   - 推广至 $N$ 维多资产连续协方差矩阵 $\Sigma$：
     $$f^* = \Sigma^{-1} (\mu - r_f \mathbf{1})$$

3. 波动率拖累（Volatility Drag）与过度下注的毁灭性（Over-betting Trap）：
   - 当 $f = f^*$ 时，获得理论最大几何增长速度 $g_{\max} = r_f + \frac{(\mu - r_f)^2}{2 \sigma^2}$；
   - 当 $f = 2 f^*$ 时，二次方差惩罚项完全抵消超额收益，$g(2 f^*) = r_f$；
   - 当 $f > 2 f^*$ 时，几何增长率甚至低于无风险利率，破产概率（Risk of Ruin）在数学上趋近于 100%！

4. 分数凯利（Fractional Kelly）的工程必要性：
   - 全凯利（Full Kelly）具有极度凶险的波动，且有高达 33.3% 的理论概率发生超过 50% 的灾难性回撤；
   - 半凯利（Half-Kelly, $0.5 \times f^*$）：仅放弃 25% 的最大增长速度，却将遭遇 50% 回撤的概率从 33% 暴跌至 1.5%！
     工业界对冲基金严格执行 0.3 ~ 0.5 分数凯利，为参数估计误差留出绝对冗余。

【核心流程与心智模型】
```mermaid
flowchart TD
    Edge["策略优势度量: 预期收益 mu, 波动率 sigma (或胜率 p, 盈亏比 b)"] --> KellySolve["连续多资产凯利求解: f* = Sigma^-1 * (mu - rf)"]
    KellySolve --> OverbetCheck{"杠杆倍数 f > 2 * f* ?"}
    OverbetCheck -- 是 --> RuinDoom["波动率拖累主导 (Volatility Drag) ➔ 长期几何破产概率 = 100%"]
    OverbetCheck -- 否 --> ScaleDown["工业级分数凯利安全缩放: f_safe = c * f* (c in [0.3, 0.5])"]
    ScaleDown --> MC_Sim["蒙特卡洛 1000 路径破产压力测试 (模拟 1 年期回撤与破产率)"]
    MC_Sim --> Verdict["风控落地: 破产率严格归零, 夏普比率最大化"]
```

【工业界实战场景与风控陷阱】
1. 参数过拟合与“把估计误差当优势”：
   若历史回测将年化超额高估了 1 倍，按历史数据执行全凯利，实盘中实际上是在以 $2 \times f^*$ 的破产速度运行！
2. 吸收壁（Absorbing Barrier）与强制平仓：
   现实交易中券商有追缴保证金（Margin Call）和强制平仓线，一旦净值跌破平仓线，博弈强行终止，复利公式立即失效。
3. 肥尾跳跃（Jump Diffusion）对连续假定的击穿：
   连续模型假设价格无跳空缺口；极端行情下一字跌停会导致实际损失远超正态分布预估，全凯利将直接爆仓。

【思考题】
Q1: 为什么胜率高达 80% 的策略，如果单次满仓或过度加杠杆下注，只要遇到一次小概率黑天鹅事件（如极端跳空暴跌），总财富就会彻底归零？请用几何平均数与对数效用函数推导说明。
Q2: 请推导连续几何布朗运动下的多资产凯利公式 $f^* = \Sigma^{-1}(\mu - r)$，并从二次函数顶点解释为什么过度杠杆（$f > 2 f^*$）必然导致几何财富增长率转负？
Q3: 为什么华尔街顶级量化机构（如 Renaissance Technologies, Citadel）在实盘中从不使用全凯利（Full Kelly），而是严格执行分数凯利（如 0.3~0.5 凯利）？请从参数估计误差与回撤效用损失两个维度进行量化论证。

【评分与通过规则】
- 代码 4 分：
  1. 准确实现离散凯利与多资产连续协方差凯利公式 (1.5分)；
  2. 准确构建基于几何布朗运动的蒙特卡洛破产概率对比模拟器 (1.5分)；
  3. 准确验证过度杠杆（2.5x f*）下的破产率激增与分数凯利的极低破产率 (1分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须从吸收壁不可逆性、二次抛物线推导与参数估计误差深入证明；
- 通过线：8/10 分。一票否决：公式推导错误、蒙特卡洛模拟出现负财富越界、删除断言校验。
"""

from typing import List, Dict, Any, Tuple
import numpy as np


def calculate_discrete_kelly(win_rate: float, win_loss_ratio: float) -> float:
    """
    计算经典离散二项博弈的凯利最优下注比例：
        f* = (p * b - (1 - p)) / b
    若预期收益为负 (p * b - (1 - p) <= 0)，返回 0.0。

    参数:
        win_rate: 交易胜率 p (0.0 ~ 1.0)
        win_loss_ratio: 净盈亏比 b (平均盈利金额 / 平均亏损金额)

    返回:
        float: 最优资金下注比例 f* (范围 [0.0, 1.0))
    """
    # TODO: 实现离散凯利公式
    pass


def calculate_continuous_multi_asset_kelly(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.02,
) -> np.ndarray:
    """
    计算连续时间多资产凯利最优杠杆向量：
        f* = Sigma^{-1} * (mu - rf * 1)

    参数:
        expected_returns: 各资产年化预期收益率向量 mu (N 维)
        cov_matrix: 各资产年化收益协方差矩阵 Sigma (N x N)
        risk_free_rate: 年化无风险利率 rf

    返回:
        np.ndarray: 各资产最优凯利杠杆向量 f* (N 维)
    """
    # TODO: 求解多资产连续凯利向量
    pass


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
    蒙特卡洛破产概率与财富复利模拟引擎：
    在连续几何布朗运动假定下，对比不同凯利乘数 (如 Half Kelly: 0.5, Full Kelly: 1.0, Over-leverage: 2.5) 的表现：
    1. 计算理论最优单资产连续凯利杠杆: f_opt = (mu - rf) / sigma^2
    2. 对每个乘数 m in kelly_multipliers，实际杠杆为 lev = m * f_opt：
       每日对数收益漂移项: drift = (rf + lev * (mu - rf) - 0.5 * lev^2 * sigma^2) * dt
       每日对数收益扩散项: diffusion = lev * sigma * sqrt(dt)
    3. 模拟 n_simulations 条长为 n_steps 交易日的财富演化路径 W_t (初始财富 W_0 = 1.0)；
    4. 若在模拟期间任意时刻 min(W_t) <= ruin_threshold (如净值跌破 20%)，判定为“破产触底”；
    5. 统计每种杠杆下的：
       - "ruin_probability": 破产概率 (破产路径数 / 总模拟数)
       - "median_final_wealth": 期末财富中位数 W_T

    返回字典包含:
        - "f_optimal": 理论全凯利杠杆值
        - "results": 字典 {multiplier: {"ruin_prob": float, "median_wealth": float}}
    """
    # TODO: 实现多路径几何布朗运动蒙特卡洛破产模拟
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 03: 凯利公式推导与破产概率单元测试")
    print("=" * 70)

    # 1. 验证离散凯利公式
    # 胜率 60%, 盈亏比 1.5 -> f* = (0.6 * 1.5 - 0.4) / 1.5 = 0.5 / 1.5 = 0.3333
    f_d1 = calculate_discrete_kelly(0.60, 1.5)
    assert abs(f_d1 - 0.333333) < 1e-4, f"离散凯利计算偏差: {f_d1}"

    # 胜率 40%, 盈亏比 1.0 -> 负期望 -> 返回 0.0
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

    # 4. 断言验证风控铁律
    # 半凯利 (0.5x) 和全凯利 (1.0x) 在 1 年期内的破产率极低 (< 1%)
    assert mc_res["results"][0.5]["ruin_prob"] < 0.01, "半凯利破产率应接近 0"
    assert mc_res["results"][1.0]["ruin_prob"] < 0.05, "全凯利 1 年破产率应受控"

    # 过度杠杆 (2.5x f* = 6.25 倍杠杆) 必然遭遇波动率毁灭，破产率显著高于 10%
    assert mc_res["results"][2.5]["ruin_prob"] > 0.10, "过度杠杆破产率应显著激增 (>10%)"
    # 过度杠杆的期末财富中位数由于波动率拖累，必然显著低于半凯利和全凯利
    assert mc_res["results"][2.5]["median_wealth"] < mc_res["results"][0.5]["median_wealth"], "过度杠杆财富中位数必然因波动率拖累劣于半凯利"

    print("Lesson 03 凯利公式与破产概率单元测试全部通过！")
