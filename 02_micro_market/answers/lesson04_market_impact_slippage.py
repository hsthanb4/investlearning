r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 4/5 课
第 4 课：交易冲击成本、滑点与 Almgren-Chriss 最优拆单模型 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么散户如果按市价单全仓买入小市值股票，瞬间产生的滑点可能直接吃掉全年的策略预期收益？
请从微观订单簿深度有限性与平方根冲击法则（Square-Root Law: I \propto \sigma \sqrt{Q / V}）推导：
- **微观流动性黑洞与非线性滑点惩罚**：
  1. **小市值股票订单簿挂单厚度极端单薄**：小市值股票（日均成交额不足数千万元）的盘口各档位挂单往往仅有几十手到几百手。
     买一与卖一之间的自然点差（Spread）本身就较宽（如 0.5%~1%）。
  2. **平方根冲击法则（Square-Root Law）的物理普适性**：全球海量实证表明，订单对价格的相对冲击
     与委托量占日均成交量的比例平方根成正比：
     $$I = Y \cdot \sigma \cdot \sqrt{\frac{Q}{V}}$$
     其中 $Q$ 为委托股数，$V$ 为全天总成交量，$\sigma$ 为日波动率。
  3. **市价单无底线扫穿买卖盘**：若散户账户以市价单瞬间买入 50 万元小市值股票（可能占当时 5 分钟成交量的 50% 以上），
     市价单将连续击穿卖一、卖二至卖十档位，最高买入价可能瞬间拉升 3%~5%。
     交易完成后，由于做市商并未跟进，价格迅速回落至原中间价附近。该交易者在买入完成的瞬间，
     账面直接产生 3%~5% 的瞬时滑点亏损，直接抹杀了一整年的 Alpha 预期收益。

【Q2 深度参考答案】
区分 TWAP（时间加权均价）与 VWAP（成交量加权均价）算法在实际算法交易（Execution Algo）中的优缺点与适用场景。
在开盘与收盘存在“日内 U 型成交量微笑曲线”（Intraday Volume Smile）时，盲目使用 TWAP 会遭受怎样的非线性滑点惩罚？
- **算法架构对比与 U 型微笑曲线冲击**：
  1. **TWAP vs VWAP 核心设计对比**：
     - **TWAP（时间加权）**：将总时间切分为均匀区间，在每个时间段内以固定速率均匀发送子单。
       优点是代码实现简单、逻辑透明、不依赖对未来成交量的预测；缺点是完全忽略了市场流动性随时间的非均匀分布。
     - **VWAP（成交量加权）**：根据历史统计的日内成交量曲线（Volume Profile），在市场成交活跃时段加大拆单量，
       在冷清时段减少拆单量，使自己的执行均价紧密跟随市场全天加权均价。
  2. **U 型成交量微笑曲线（Volume Smile）的物理现实**：在全球所有主要交易所，交易量高度集中在
     开盘后前 30 分钟（消化隔夜信息）与收盘前半小时（被动指数基金与 ETF 调仓），呈现明显的两头高、中间凹陷的“U 型”分布。
     午间或盘中时段（10:30 - 14:00）全市场成交量仅占全天的 20%~30%。
  3. **盲目使用 TWAP 的非线性滑点惩罚**：若使用 TWAP 在盘中流动性最干涸的午间强行执行与开盘相同数量的大单，
     该子单在盘中占该时段市场真实交易量的比例（Participation Rate）将暴增 3~5 倍。
     根据冲击成本的二次方/超线性增长特性（$\text{Impact} \propto v^2$），盘中微薄的挂单簿深度被严重击穿，
     产生极高执行滑点；而在尾盘流动性极充裕时，TWAP 的拆单量又过小，白白浪费了吸收大单的流动性黄金窗口。

【Q3 深度参考答案】
什么是“隐形冰山单”（Iceberg Order）与“暗池嗅探器（Ping / Sniffer Algos）”？
高频量化机构如何利用微小探测单（Sub-penny Pings）识别出市场中潜藏的巨额冰山母单并实施掠夺性交易（Predatory Trading）？
- **微观对抗与掠夺性高频博弈**：
  1. **冰山订单（Iceberg Order）机制**：机构为隐藏真实意图，向交易所提交一种特殊限价单：
     设定总数量 100 万股，但仅在公开盘口展示 5000 股（Display Quantity）。当这 5000 股被成交后，
     交易主机底层自动从隐藏池补充新的 5000 股至盘口排队。
  2. **高频嗅探算法（Ping / Probe Orders）探测**：
     - 高频交易公司（HFT）开发出专门的嗅探算法，在买一或卖一口频繁发送极小份额的试探性市价单（如 100 股或美股的 1 股）；
     - 若每次吃掉 100 股后，发现该价格档位在纳秒时间内立即被原样补齐，且重复发生数十次，
       嗅探算法判定该处潜伏着一个巨额冰山买入母单。
  3. **掠夺性交易（Predatory Trading / Front-Running）闭环**：
     - 一旦确认冰山买单存在，HFT 算法立即以极速撤销自己的卖单，并抢先在冰山买单价格上方 1 个 Tick 处买入（搭便车，因为冰山大买单构成了天然无风险跌停托底）；
     - 随着价格被推高，HFT 再将筹码反手以高价倒手卖给被迫上调买价继续追单的冰山母单，
     - 最终使大机构母单承受严重的被动滑点放大（Adverse Selection by Pinging）。
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
