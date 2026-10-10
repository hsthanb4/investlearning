r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 4/5 课
第 4 课：交易冲击成本、滑点与 Almgren-Chriss 最优拆单模型 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么散户如果按市价单全仓买入小市值股票，瞬间产生的滑点可能直接吃掉全年的策略预期收益？请从微观订单簿深度有限性与平方根冲击法则（Square-Root Law: I ∝ σ √(Q / V)）推导：
- **[平方根冲击法则与深度非线性损耗]**：
  - **[1. 平方根定律经验公理]**：学术界与工业界量化实证普遍证实，大单交易产生的总价格冲击与交易量占日均成交量（ADV）的比例满足普适的平方根法则：
    $$I = Y \cdot \sigma \cdot \sqrt{\frac{Q}{V}}$$
    其中 $Q$ 为本次订单规模，$V$ 为日均成交量 ADV，$\sigma$ 为股票日波动率，$Y$ 为常数（通常约在 0.5~0.7 之间）。
  - **[2. 小市值微观盘口的深度极度脆弱]**：小市值股票（如微盘股）日均成交额极低，订单簿每一档的可用流动性仅有数万元至十数万元。当交易者以市价单打入百万级资金时，$Q/V$ 比值极大；同时微盘股固有年化波动率 $\sigma$ 高达 50%~80%，平方根冲击放大倍数极为惊人。
  - **[3. 非线性穿仓抹杀 Alpha]**：市价单在纳秒时间内连续打穿五档甚至十档盘口，成交均价（VWAP）比下单前的即期价格高出 2%~5%。一个设计年化超额收益为 15% 的策略，单次建仓和未来调仓平仓各承受 3% 的双向非线性滑点损耗，全年的 Alpha 收益将直接被执行成本彻底吞噬。

【Q2 投决会深度解析】
区分 TWAP（时间加权均价）与 VWAP（成交量加权均价）算法在实际算法交易（Execution Algo）中的优缺点与适用场景。在开盘与收盘存在“日内 U 型成交量微笑曲线”（Intraday Volume Smile）时，盲目使用 TWAP 会遭受怎样的非线性滑点惩罚？
- **[算法执行边界与日内微笑曲面适配]**：
  - **[1. TWAP 算法特征与缺陷]**：TWAP 将母单等额切割并均匀分布在固定的时间切片上。其理论优势在于能使二次凸性的临时冲击平方和达到最小；但其致命缺陷在于完全脱离了市场的实际流动性节律。
  - **[2. 日内 U 型成交量微笑曲线]**：全市场股票在交易时间内呈现显著的“两头高、中间低”成交量分布（开盘 09:30~10:00 消化夜间隔夜信息，成交量占全天 25%~30%；午盘 13:00~14:00 极度清淡；尾盘 14:30~15:00 机构调仓再次放量）。
  - **[3. 盲目套用 TWAP 的非线性滑点惩罚]**：若在流动性清淡的午盘时段依然强行执行与开盘相同规模的固定子单，此时由于盘口挂单深度极为菲薄，子单将产生极大的瞬时穿透冲击；反之在开盘尾盘流动性极充裕时却未能充分放量撮合。VWAP 算法依据历史成交量画像严格按比例加权分配，使子单规模与即时市场承载深度动态拟合，平均执行滑点通常显著优于机械 TWAP。

【Q3 投决会深度解析】
什么是“隐形冰山单”（Iceberg Order）与“暗池嗅探器（Ping / Sniffer Algos）”？高频量化机构如何利用微小探测单（Sub-penny Pings）识别出市场中潜藏的巨额冰山母单并实施掠夺性交易（Predatory Trading）？
- **[冰山单微观解构与高频嗅探掠夺]**：
  - **[1. 冰山订单物理机制]**：机构为了隐蔽大单意图，使用冰山委托将 100,000 股母单设置为“每次仅显示 500 股可见（Display Size）”，前 500 股成交后，系统自动在原价格档位补充下一批 500 股，以此压低表面上的静态深度。
  - **[2. 高频探测算法（Ping Algos）的嗅探原理]**：掠夺性高频做市商在订单簿内部以 100 股的微小市价单或微小跳价（Sub-penny / 最小变动价位）向盘口快速打入“探测单（Ping）”。当发现某一特定买价档位被吃掉 500 股后，瞬间被系统以纳秒速度原位自动回补，且该过程重复数次，高频算法即可在统计上 99% 确诊该价位存在庞大的未成交冰山母单。
  - **[3. 掠夺性交易（Predatory Trading）的收割链]**：一旦确诊存在巨额买方冰山母单提供托底，高频机构立刻停止向市场提供卖单流动性，反手在买一档排在冰山单之前疯狂抢购该股票，推升价格上涨数个价位，随后在更高价位反向卖给该被动吃单的机构冰山单，实现“零风险倒买倒卖”，导致冰山单买方遭受严重的逆向选择推价成本。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np


def generate_twap_schedule(total_shares: int, num_slices: int) -> List[int]:
    """
    生成均匀 TWAP 拆单计划列表:
    将 total_shares 均匀拆分至 num_slices 个步长区间，总和必须完全等于 total_shares。
    """
    base = total_shares // num_slices
    rem = total_shares % num_slices
    return [base + (1 if i < rem else 0) for i in range(num_slices)]


def generate_vwap_schedule(total_shares: int, volume_profile: List[float]) -> List[int]:
    """
    生成基于日内成交量权重画像的 VWAP 拆单计划列表 (最大余数法保证整数守恒)
    """
    prof = np.array(volume_profile, dtype=float)
    weights = prof / np.sum(prof)

    raw_shares = weights * total_shares
    int_shares = np.floor(raw_shares).astype(int)
    rem_shares = total_shares - np.sum(int_shares)

    # 按小数部分由大到小排序分配余数
    fractional = raw_shares - int_shares
    order = np.argsort(-fractional)

    for i in range(rem_shares):
        idx = order[i % len(order)]
        int_shares[idx] += 1

    return int_shares.tolist()


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
    求解 Almgren-Chriss 最优拆单剩余持仓轨迹 x_j (j = 0, 1, ..., N)
    """
    T = num_steps * tau
    times = np.linspace(0, T, num_steps + 1)

    if lam <= 1e-12:
        # 风险中性: 线性 TWAP
        return total_shares * (1.0 - times / T)

    kappa = np.sqrt(lam * (sigma ** 2) / eta)
    denom = np.sinh(kappa * T)
    if denom == 0 or np.isinf(denom):
        traj = total_shares * np.exp(-kappa * times)
    else:
        traj = (np.sinh(kappa * (T - times)) / denom) * total_shares

    traj[0] = float(total_shares)
    traj[-1] = 0.0
    return traj


def estimate_execution_shortfall(
    schedule: List[int],
    eta: float,
    gamma: float,
    sigma: float,
    tau: float = 1.0,
) -> Dict[str, float]:
    """
    估计给定拆单计划下的期望冲击成本与执行方差
    """
    n_k = np.array(schedule, dtype=float)
    X = float(np.sum(n_k))
    x_k = X - np.cumsum(n_k)

    exp_cost = 0.5 * gamma * (X ** 2) + eta * float(np.sum((n_k ** 2) / tau))
    var_risk = (sigma ** 2) * tau * float(np.sum(x_k ** 2))

    return {
        "expected_cost": float(exp_cost),
        "variance_risk": float(var_risk),
    }


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础 TWAP 拆单 ----------------
    plan = generate_twap_schedule(1005, 5)
    assert len(plan) == 5, f"Expected 5 slices, got {len(plan)}"
    assert sum(plan) == 1005, f"Sum must be 1005, got {sum(plan)}"
    assert plan[0] in [201, 202], f"First slice expected 201 or 202, got {plan[0]}"

    plan_rem = generate_twap_schedule(1003, 5)
    assert sum(plan_rem) == 1003
    assert plan_rem == [201, 201, 201, 200, 200]

    # ---------------- 基础测试 2: VWAP 比例拆单 ----------------
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
    traj_neutral = calculate_almgren_chriss_trajectory(
        total_shares=X, num_steps=N, sigma=0.02, eta=2.5e-6, gamma=1.0e-6, lam=0.0,
    )
    assert abs(traj_neutral[0] - X) < 1e-4
    assert abs(traj_neutral[-1] - 0.0) < 1e-4
    assert abs(traj_neutral[5] - 50_000.0) < 1e-4, f"风险中性中点应为 50000, 实际为: {traj_neutral[5]}"

    traj_averse = calculate_almgren_chriss_trajectory(
        total_shares=X, num_steps=N, sigma=0.02, eta=2.5e-6, gamma=1.0e-6, lam=1.0e-4,
    )
    assert abs(traj_averse[0] - X) < 1e-4
    assert abs(traj_averse[-1] - 0.0) < 1e-4
    assert traj_averse[5] < traj_neutral[5], f"风险厌恶轨迹中点剩余持仓应低于中性轨迹: {traj_averse[5]} vs {traj_neutral[5]}"

    # ---------------- 基础测试 4: 冲击成本与方差评估 ----------------
    twap_int = [10000] * 10
    shortfall = estimate_execution_shortfall(
        schedule=twap_int, eta=2.5e-6, gamma=1.0e-6, sigma=0.02,
    )
    assert shortfall["expected_cost"] > 0
    assert shortfall["variance_risk"] > 0

    print("Lesson 04 Answer Verified!")
