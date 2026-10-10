r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 4/5 课
第 4 课：交易冲击成本、滑点与 Almgren-Chriss 最优拆单模型 (Market Impact & Almgren-Chriss Execution)
================================================================================

【课程定位与第一性原理】
在真实机构量化交易中，“回测是百万富翁，实盘是破产清算”的最核心原因往往在于
忽略了**交易执行冲击成本（Market Impact）与滑点（Slippage）**。

当管理资产规模（AUM）达到数千万至数十亿美元时，单次调仓涉及的母单（Parent Order）
占标的股票日均成交量（ADV）的 5%~20%。如果一次性打出市价单，将在纳秒级时间内吃穿数十档盘口，
导致实际成交均价大幅偏离无冲击基准价。
反之，如果拆成微型子单在数天内极慢执行，虽然冲击极小，但持仓暴漏在巨大的未平仓价格波动风险
（Timing Risk / Execution Variance）中，可能在执行完成前股票已暴跌。

【理论模型：市场冲击的物理分解】
根据微观结构经典理论，市场冲击可以被正交分解为：
1. 永久冲击（Permanent Price Impact）：
   由于母单交易向市场透露了知情交易者的私人信息，促使做市商与对手盘永久性上修对该资产的公允价值估计。
   该冲击是不可逆的：
       g(v_k) = \gamma \cdot v_k
2. 临时冲击（Temporary Price Impact）：
   由于单笔子单在微观瞬间消耗了限价订单簿的局部深度，在短时间内推高价格；随后随做市商回补挂单而回弹。
   该冲击仅影响当期子单的撮合成交价：
       h(v_k) = \eta \cdot v_k  （或平方根形式 \eta \cdot \text{sign}(v_k) \sqrt{|v_k|}）

【数学推导：Almgren-Chriss (2000) 最优拆单解析解】
设总交易量为 X，划分为 N 个时间步，步长为 \tau，总时长 T = N \tau。
令 x_k 表示第 k 步开始时的剩余未执行持仓（x_0 = X, x_N = 0），子单执行量 n_k = x_{k-1} - x_k。
- 期望执行冲击成本（Expected Implementation Shortfall）：
    \mathbb{E}[x] = \frac{1}{2} \gamma X^2 + \eta \sum_{k=1}^N \frac{n_k^2}{\tau}
- 持仓波动方差风险（Variance of Shortfall）：
    V[x] = \sigma^2 \sum_{k=1}^N \tau x_k^2
交易者目标是最小化拉格朗日效用函数：
    \min_{\{x_k\}} U(x) = \mathbb{E}[x] + \lambda V[x]
其中 \lambda \ge 0 为风险厌恶系数。
- 当 \lambda = 0（风险中性）：最优拆单退化为线性的 **TWAP**（Time-Weighted Average Price），每步执行等额股数，
  使临时冲击平方和达到最小；
- 当 \lambda > 0（风险厌恶）：最优持仓轨迹呈现双曲正弦函数解析解：
    x_j = \frac{\sinh(\kappa (T - t_j))}{\sinh(\kappa T)} \cdot X
  其中 \kappa \approx \sqrt{\frac{\lambda \sigma^2}{\eta}}。
  轨迹呈现明显的**“前置加速（Front-loaded）”**特征：前期快速大额卖出平抑波动，后期缓慢收尾。

【拆单路径架构对比图】
```mermaid
flowchart LR
    RiskNeutral["风险中性 (\lambda = 0) ➔ 线性均匀 TWAP (临时冲击最小)"]
    RiskAverse["风险厌恶 (\lambda > 0) ➔ 前置加速指数衰减 AC 轨迹 (规避持仓波动)"]
    VolumeSmile["日内成交量微笑 (U型) ➔ 按历史成交画像分配的 VWAP 算法"]
```

【思考题】
Q1: 为什么散户如果按市价单全仓买入小市值股票，瞬间产生的滑点可能直接吃掉全年的策略预期收益？
    请从微观订单簿深度有限性与平方根冲击法则（Square-Root Law: I \propto \sigma \sqrt{Q / V}）推导。
Q2: 区分 TWAP（时间加权均价）与 VWAP（成交量加权均价）算法在实际算法交易（Execution Algo）中的优缺点与适用场景。
    在开盘与收盘存在“日内 U 型成交量微笑曲线”（Intraday Volume Smile）时，盲目使用 TWAP 会遭受怎样的非线性滑点惩罚？
Q3: 什么是“隐形冰山单”（Iceberg Order）与“暗池嗅探器（Ping / Sniffer Algos）”？
    高频量化机构如何利用微小探测单（Sub-penny Pings）识别出市场中潜藏的巨额冰山母单并实施掠夺性交易（Predatory Trading）？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现 TWAP 均匀拆单与整数守恒 (1分)；
  2. 准确实现 VWAP 成交量权重拆单与余数配额分配 (1.5分)；
  3. 准确求解 Almgren-Chriss 双曲正弦前置执行轨迹与冲击成本估计 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：深入阐明微观冲击成因与前置执行权衡；
- 通过线：8/10 分。一票否决：拆单总股数不守恒、风险厌恶下拆单方向算反、删除断言。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np


def generate_twap_schedule(total_shares: int, num_slices: int) -> List[int]:
    """
    生成均匀 TWAP 拆单计划列表:
    将 total_shares 均匀拆分至 num_slices 个步长区间，总和必须完全等于 total_shares。
    处理整除余数，余数均摊在前面的分片上。
    """
    # TODO: 实现 TWAP 均匀拆单逻辑
    pass


def generate_vwap_schedule(total_shares: int, volume_profile: List[float]) -> List[int]:
    """
    生成基于日内成交量权重画像的 VWAP 拆单计划列表:
    volume_profile: 各时段历史成交量占比 (如 [0.3, 0.1, 0.1, 0.2, 0.3])
    使用最大余数法保证拆分后的整数股数之和精确等于 total_shares。
    """
    # TODO: 实现 VWAP 权重分配与整数守恒
    pass


def calculate_almgren_chriss_trajectory(
    total_shares: float,
    num_steps: int,
    sigma: float,
    eta: float,
    gamma: float,
    lam: float,
    tau: float = 1.0,
) -> np.ndarray:
    """
    求解 Almgren-Chriss 最优拆单剩余持仓轨迹 x_j (j = 0, 1, ..., N):
    参数:
        total_shares: 总待执行股数 X (x_0 = X)
        num_steps: 时间步数 N (x_N = 0)
        sigma: 资产日收益率波动率
        eta: 临时冲击敏感度参数
        gamma: 永久冲击参数
        lam: 交易者风险厌恶系数 (lambda >= 0)
        tau: 单步时间跨度 (默认 1.0)

    返回:
        np.ndarray: 长度为 num_steps + 1 的剩余持仓数组 [x_0, x_1, ..., x_N]
        若 lam == 0，返回线性 TWAP 轨迹;
        若 lam > 0，返回双曲正弦解析解:
            kappa = sqrt(lam * sigma^2 / eta)
            x_j = sinh(kappa * (T - t_j)) / sinh(kappa * T) * X
    """
    # TODO: 求解 Almgren-Chriss 解析持仓轨迹
    pass


def estimate_execution_shortfall(
    schedule: List[int],
    eta: float,
    gamma: float,
    sigma: float,
    tau: float = 1.0,
) -> Dict[str, float]:
    """
    估计给定拆单计划下的期望冲击成本与执行方差:
        n_k = schedule[k]
        x_k = 剩余未执行持仓 (累计倒算)
        E[Cost] = 0.5 * gamma * X^2 + eta * sum(n_k^2 / tau)
        V[Cost] = sigma^2 * tau * sum(x_k^2)
    """
    # TODO: 计算期望冲击成本与方差风险
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础 TWAP 拆单 ----------------
    plan = generate_twap_schedule(1005, 5)
    assert len(plan) == 5, f"Expected 5 slices, got {len(plan)}"
    assert sum(plan) == 1005, f"Sum must be 1005, got {sum(plan)}"
    assert plan[0] in [201, 202], f"First slice expected 201 or 202, got {plan[0]}"

    # 边界测试: 无法整除的余数分配
    plan_rem = generate_twap_schedule(1003, 5)
    assert sum(plan_rem) == 1003
    assert plan_rem == [201, 201, 201, 200, 200]

    # ---------------- 基础测试 2: VWAP 比例拆单 ----------------
    # 典型 U 型成交量画像: 开盘 35%, 盘中三段各 10%, 收盘 35%
    profile = [0.35, 0.10, 0.10, 0.10, 0.35]
    vwap_plan = generate_vwap_schedule(10000, profile)
    assert len(vwap_plan) == 5
    assert sum(vwap_plan) == 10000
    assert vwap_plan[0] == 3500
    assert vwap_plan[1] == 1000
    assert vwap_plan[4] == 3500

    # ---------------- 基础测试 3: Almgren-Chriss 轨迹求解 ----------------
    X = 100_000.0
    N = 10
    # 风险中性: lambda = 0 ➔ 纯线性 TWAP
    traj_neutral = calculate_almgren_chriss_trajectory(
        total_shares=X, num_steps=N, sigma=0.02, eta=2.5e-6, gamma=1.0e-6, lam=0.0,
    )
    assert abs(traj_neutral[0] - X) < 1e-4
    assert abs(traj_neutral[-1] - 0.0) < 1e-4
    assert abs(traj_neutral[5] - 50_000.0) < 1e-4, f"风险中性中点应为 50000, 实际为: {traj_neutral[5]}"

    # 风险厌恶: lambda = 1e-4 > 0 ➔ 前置加速卖出
    traj_averse = calculate_almgren_chriss_trajectory(
        total_shares=X, num_steps=N, sigma=0.02, eta=2.5e-6, gamma=1.0e-6, lam=1.0e-4,
    )
    assert abs(traj_averse[0] - X) < 1e-4
    assert abs(traj_averse[-1] - 0.0) < 1e-4
    # 前置卖出意味着在中点时刻，剩余持仓显著低于线性 TWAP (即提前抛售完毕)
    assert traj_averse[5] < traj_neutral[5], f"风险厌恶轨迹中点剩余持仓应低于中性轨迹: {traj_averse[5]} vs {traj_neutral[5]}"

    # ---------------- 基础测试 4: 冲击成本与方差评估 ----------------
    twap_int = [10000] * 10
    shortfall = estimate_execution_shortfall(
        schedule=twap_int, eta=2.5e-6, gamma=1.0e-6, sigma=0.02,
    )
    assert shortfall["expected_cost"] > 0
    assert shortfall["variance_risk"] > 0

    print("Lesson 04 Exercise Passed!")
