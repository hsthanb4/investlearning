r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 3/5 课
第 3 课：订单流不平衡 (Order Flow Imbalance, OFI) 与高频价格预测 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么 OFI 相比于单纯的“主动买入成交量减主动卖出成交量”（净主动买入额 Net Taker Volume），
能够提供信噪比更高、更纯净的短期价格预测能力？
请从做市商被动撤单与盘口新挂单事件的信息含量角度推导：
- **全微观事件捕获与订单流信息完备性**：
  1. **成交量仅反映微观事件的冰山一角**：净主动买入量（Net Taker Volume）仅仅统计了以市价单形式激进成交的订单，
     完全遗漏了限价订单簿中占据 80% 以上流量的“限价单挂单（Passive Limit Adds）”与“限价单撤销（Cancellations）”。
  2. **撤单包含极度昂贵的逆向信息**：当拥有高速低延迟通道的做市商或知情交易者感知到利空时，
     他们首先做出的反应不是市价砸盘，而是立即撤销买一价上的所有被动挂单（Cancel Bids）。
     在净主动买入指标中，没有任何成交发生，该指标记录为 0；然而在 OFI 框架中，买一挂单的消失被精确计为
     $I_t^b = -q_{t-1}^b$（显著的负向冲击），提前预警盘口即将向下破位。
  3. **支撑阻力位的新增挂单承接**：若大资金在买一价持续增挂 10 万股被动限价单托盘（$I_t^b = +100000$），
     即使当前未发生任何撮合成交，买方深度的硬性垫单直接提高了卖方的下砸阻力，推升微观价格向上跳跃。
     因此，OFI 完整聚合了“挂、吃、撤”三大微观动力源，信息完备度压倒单纯的成交量。

【Q2 深度参考答案】
为什么在实盘高频量化交易中，单步 OFI 对价格变化的解释力在毫秒至秒级极强（R^2 常常达到 50%~70%），
但随着预测时间窗口拉长（如 5分钟、15分钟），其预测能力呈现指数级衰减？做市商如何利用 OFI 衰减半衰期设定库存管理风控？
- **微观流动性补充与半衰期衰减机制**：
  1. **盘口真空的超短期机械因果**：在 10 毫秒至 1 秒的极窄切片内，订单簿的厚度是有限的。
     一个正向的 OFI 脉冲代表买一档挂单暴增或卖一档被彻底吃穿，中间价在机械上必须向上跳跃 1 个 Tick。
     这种物理级撮合因果在微观瞬间呈现出确定性，因而 $R^2$ 极高。
  2. **做市商流动性回补与均值回归（Liquidity Replenishment）**：当卖一档被吃穿、价格上跳后，
     散布在全市场的其他算法做市商会在 100 毫秒至数秒内重新向新的卖一口挂入卖单（补充流动性赚取更厚利差）。
     随着时间窗口拉长至 5 分钟、15 分钟，宏观情绪、跨市场套利与基本面资金介入，原先由微观订单簿失衡引发的
     瞬时脉冲早已被多空再平衡抹平，OFI 呈现出极短的指数衰减半衰期（通常只有几百毫秒到数秒）。
  3. **做市商风控与持仓衰减（Inventory Decay）**：做市商利用 OFI 信号建立超短期头寸后，
     必须根据测算出的 OFI 衰减半衰期 $\tau_{1/2}$ 设定硬性平仓时钟。若在 $2 \times \tau_{1/2}$ 时间内
     价格未能继续突破，必须无条件主动平仓，严防瞬时流动性 Alpha 衰退为不可控的长期隔夜库存风险。

【Q3 深度参考答案】
在跨多档盘口（Level 1 至 Level 10）拓展 Multi-Level OFI 时，为什么越深的档位（如买五、买十）
需要赋予越大的权重衰减（如指数衰减 exp(-alpha * k)）？深档挂单中存在大量“虚假挂单（Ghost Orders / Spoofing）”
会对未加权的多档 OFI 造成怎样的污染？
- **档位距离衰减与虚假信号隔离**：
  1. **价格距离与即时成交概率（Execution Probability）的几何衰减**：排在买一（L1）的订单随时面临被成交，
     其承担的被动成交风险最高，因而其反映的真实交易意图最为纯粹；
     而排在买十（L10）的挂单距离当前市价有 10 个 Tick 的安全垫，在被成交前有充分的逃逸撤单时间，即时成交概率接近于零。
  2. **深档是幌骗（Spoofing）的高发重灾区**：投机庄家极喜欢在买八、买九、买十挂出数千万股的“幽灵大单（Ghost Orders）”，
     制造该标的拥有极强流动性托底的虚假繁荣。如果对所有档位等权重相加，深档的巨额虚假挂单将产生巨大的伪正向 OFI 信号，
     诱导多头量化模型追高买入，随后庄家在成交前瞬间撤销深档大单，多头模型直接落入陷阱。
  3. **指数衰减权重 $w_k = e^{-\alpha k}$ 的滤波降噪价值**：通过引入衰减因子 $\alpha > 0$，使 L1 占据 60% 以上核心权重，
     L5 以后权重衰减至极小值，既能吸收浅层深度的边际挂单弹性，又能物理隔离深层虚假挂单对信号的投毒污染。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def calculate_ofi(
    b_price_prev: float,
    b_size_prev: int,
    b_price_curr: float,
    b_size_curr: int,
    a_price_prev: float,
    a_size_prev: int,
    a_price_curr: float,
    a_size_curr: int,
) -> float:
    """
    计算单个 Tick 步长的 Level 1 订单流不平衡 (OFI):
        OFI = I_Bid - I_Ask
    """
    if b_price_curr > b_price_prev:
        i_bid = b_size_curr
    elif b_price_curr == b_price_prev:
        i_bid = b_size_curr - b_size_prev
    else:
        i_bid = -b_size_prev

    if a_price_curr < a_price_prev:
        i_ask = a_size_curr
    elif a_price_curr == a_price_prev:
        i_ask = a_size_curr - a_size_prev
    else:
        i_ask = -a_size_prev

    return float(i_bid - i_ask)


def calculate_tick_ofi_series(tick_df: pd.DataFrame) -> pd.Series:
    """
    从连续的 Tick 快照数据集中批量计算单步 OFI 序列
    """
    n = len(tick_df)
    ofi_vals = [0.0]

    for t in range(1, n):
        row_prev = tick_df.iloc[t - 1]
        row_curr = tick_df.iloc[t]
        val = calculate_ofi(
            row_prev["b_price"], int(row_prev["b_size"]),
            row_curr["b_price"], int(row_curr["b_size"]),
            row_prev["a_price"], int(row_prev["a_size"]),
            row_curr["a_price"], int(row_curr["a_size"]),
        )
        ofi_vals.append(val)

    return pd.Series(ofi_vals, index=tick_df.index)


def calculate_multi_level_ofi(
    b_prices_prev: List[float],
    b_sizes_prev: List[int],
    b_prices_curr: List[float],
    b_sizes_curr: List[int],
    a_prices_prev: List[float],
    a_sizes_prev: List[int],
    a_prices_curr: List[float],
    a_sizes_curr: List[int],
    decay: float = 0.5,
) -> float:
    """
    计算跨多档深度 (Multi-Level) 加权订单流不平衡
    """
    n_levels = min(len(b_prices_prev), len(b_prices_curr), len(a_prices_prev), len(a_prices_curr))
    total_ofi = 0.0

    for k in range(n_levels):
        w_k = np.exp(-decay * k)
        ofi_k = calculate_ofi(
            b_prices_prev[k], b_sizes_prev[k],
            b_prices_curr[k], b_sizes_curr[k],
            a_prices_prev[k], a_sizes_prev[k],
            a_prices_curr[k], a_sizes_curr[k],
        )
        total_ofi += w_k * ofi_k

    return float(total_ofi)


def estimate_ofi_price_impact(ofi_series: pd.Series, mid_price_series: pd.Series) -> Dict[str, float]:
    """
    估计 OFI 对中间价变化的一阶价格冲击系数与预测拟合度
    """
    d_mid = mid_price_series.diff()
    df = pd.DataFrame({"ofi": ofi_series, "d_mid": d_mid}).dropna()

    corr = float(df["ofi"].corr(df["d_mid"]))
    var_ofi = float(np.var(df["ofi"].values, ddof=1))
    if var_ofi > 1e-12:
        cov = float(np.cov(df["ofi"].values, df["d_mid"].values)[0, 1])
        beta = cov / var_ofi
    else:
        beta = 0.0

    r_squared = float(corr ** 2)

    return {
        "correlation": float(corr),
        "beta": float(beta),
        "r_squared": float(r_squared),
    }


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础单步 OFI 计算 ----------------
    ofi = calculate_ofi(10.0, 80, 10.1, 100, 10.2, 50, 10.2, 40)
    assert abs(ofi - 110.0) < 1e-4, f"Expected 110.0, got {ofi}"

    ofi2 = calculate_ofi(10.1, 100, 10.0, 70, 10.2, 50, 10.15, 60)
    assert abs(ofi2 - (-160.0)) < 1e-4, f"Expected -160.0, got {ofi2}"

    # ---------------- 基础测试 2: 多档 Multi-Level OFI ----------------
    bp_prev = [10.0, 9.9]
    bs_prev = [100, 200]
    bp_curr = [10.0, 9.9]
    bs_curr = [150, 200]

    ap_prev = [10.1, 10.2]
    as_prev = [80, 150]
    ap_curr = [10.1, 10.2]
    as_curr = [60, 150]

    multi_ofi = calculate_multi_level_ofi(
        bp_prev, bs_prev, bp_curr, bs_curr,
        ap_prev, as_prev, ap_curr, as_curr,
        decay=0.5,
    )
    assert abs(multi_ofi - 70.0) < 1e-4, f"Expected 70.0, got {multi_ofi}"

    # ---------------- 基础测试 3: OFI 时序与价格冲击回归 ----------------
    np.random.seed(42)
    n_ticks = 100
    synth_ofi = np.random.normal(0.0, 50.0, n_ticks)
    synth_d_mid = 0.002 * synth_ofi + np.random.normal(0.0, 0.02, n_ticks)
    synth_mid = 100.0 + np.cumsum(synth_d_mid)

    s_ofi = pd.Series(synth_ofi)
    s_mid = pd.Series(synth_mid)

    impact = estimate_ofi_price_impact(s_ofi, s_mid)
    assert impact["correlation"] > 0.85, f"OFI 与价格变化应高度正相关, 实际: {impact['correlation']}"
    assert 0.0015 <= impact["beta"] <= 0.0025, f"Beta 冲击系数应接近 0.002, 实际: {impact['beta']}"
    assert impact["r_squared"] > 0.70, f"R^2 应高于 0.70, 实际: {impact['r_squared']}"

    print("Lesson 03 Answer Verified!")
