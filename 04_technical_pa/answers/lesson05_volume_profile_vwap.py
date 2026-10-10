"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 5/5 课
参考实现与标准问答解析
第 5 课：成交量分布 (Volume Profile)、POC/VAH/VAL 与锚定 VWAP 偏离策略
================================================================================
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple


def build_volume_profile(
    df: pd.DataFrame,
    num_bins: int = 10,
    value_area_pct: float = 0.70
) -> Dict[str, Any]:
    """
    构建价格成交量分布直方图 (Volume Profile) 并计算 POC, VAH, VAL
    """
    tp = (df["high"] + df["low"] + df["close"]) / 3.0
    min_p = float(df["low"].min())
    max_p = float(df["high"].max())

    if max_p <= min_p:
        raise ValueError("价格区间无效，最大价必须大于最小价")

    # 1. 价格等间距离散化切分
    bins = np.linspace(min_p, max_p, num_bins + 1)
    bin_mids = 0.5 * (bins[:-1] + bins[1:])
    bin_indices = np.clip(np.digitize(tp, bins) - 1, 0, num_bins - 1)

    # 2. 统计各分箱成交量
    bin_volumes = np.zeros(num_bins, dtype=float)
    for b_idx, vol in zip(bin_indices, df["volume"].values):
        bin_volumes[b_idx] += float(vol)

    # 3. 确定控制点 POC (成交量最大的价格节点)
    poc_idx = int(np.argmax(bin_volumes))
    poc_price = float(bin_mids[poc_idx])

    # 4. 计算 70% 价值区 (Value Area)
    total_volume = float(np.sum(bin_volumes))
    target_volume = total_volume * value_area_pct

    cur_volume = bin_volumes[poc_idx]
    up_idx = poc_idx + 1
    down_idx = poc_idx - 1

    while cur_volume < target_volume and (up_idx < num_bins or down_idx >= 0):
        if up_idx < num_bins and down_idx >= 0:
            if bin_volumes[up_idx] >= bin_volumes[down_idx]:
                cur_volume += bin_volumes[up_idx]
                up_idx += 1
            else:
                cur_volume += bin_volumes[down_idx]
                down_idx -= 1
        elif up_idx < num_bins:
            cur_volume += bin_volumes[up_idx]
            up_idx += 1
        elif down_idx >= 0:
            cur_volume += bin_volumes[down_idx]
            down_idx -= 1

    vah_price = float(bin_mids[min(up_idx - 1, num_bins - 1)])
    val_price = float(bin_mids[max(down_idx + 1, 0)])

    # 确保单调关系: VAH >= POC >= VAL
    vah_price = max(vah_price, poc_price)
    val_price = min(val_price, poc_price)

    profile_df = pd.DataFrame({
        "bin_lower": bins[:-1],
        "bin_mid": bin_mids,
        "bin_upper": bins[1:],
        "volume": bin_volumes
    })

    return {
        "poc_price": poc_price,
        "vah_price": vah_price,
        "val_price": val_price,
        "total_volume": total_volume,
        "binned_profile": profile_df
    }


def calculate_anchored_vwap_bands(
    df: pd.DataFrame,
    num_std: float = 2.0
) -> pd.DataFrame:
    """
    计算累积 VWAP 以及基于成交量加权方差的上下标准差偏离通道
    """
    res = df.copy()
    tp = (res["high"] + res["low"] + res["close"]) / 3.0
    v = res["volume"].astype(float)

    cum_pv = (tp * v).cumsum()
    cum_v = v.cumsum()
    vwap = cum_pv / cum_v

    # 向量化加权方差: E[X^2] - (E[X])^2
    cum_pv2 = (tp * tp * v).cumsum()
    variance = np.maximum((cum_pv2 / cum_v) - (vwap ** 2), 0.0)
    vwap_std = np.sqrt(variance)

    vwap_upper = vwap + num_std * vwap_std
    vwap_lower = vwap - num_std * vwap_std
    vwap_zscore = (tp - vwap) / vwap_std.replace(0.0, np.nan)

    res["typical_price"] = tp
    res["vwap"] = vwap
    res["vwap_upper"] = vwap_upper
    res["vwap_lower"] = vwap_lower
    res["vwap_zscore"] = vwap_zscore

    return res


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 05 参考实现与测试")
    print("=" * 60)

    # 1. 验证 Volume Profile 计算
    vp_df = pd.DataFrame({
        "high":   [ 92.0,  96.0,  99.0, 101.0, 102.0, 101.0, 100.0, 105.0, 109.0, 112.0],
        "low":    [ 89.0,  93.0,  97.0,  99.0,  99.0,  98.0,  97.0, 102.0, 106.0, 108.0],
        "close":  [ 90.0,  95.0,  98.0, 100.0, 101.0, 100.0,  99.0, 104.0, 108.0, 110.0],
        "volume": [  100,   200,   800,  1500,  2000,  1600,   900,   300,   150,   100]
    })

    profile_res = build_volume_profile(vp_df, num_bins=10, value_area_pct=0.70)
    print("Volume Profile 结果:")
    print("POC 价格:", profile_res["poc_price"])
    print("VAH (价值区高点):", profile_res["vah_price"])
    print("VAL (价值区低点):", profile_res["val_price"])

    assert 98.0 <= profile_res["poc_price"] <= 102.0
    assert profile_res["vah_price"] >= profile_res["poc_price"] >= profile_res["val_price"]
    assert profile_res["total_volume"] == sum(vp_df["volume"])

    # 2. 验证 VWAP 与加权标准差通道
    vwap_df = calculate_anchored_vwap_bands(vp_df, num_std=2.0)
    print("VWAP 计算结果 (尾部5行):\n", vwap_df[["typical_price", "vwap", "vwap_upper", "vwap_lower", "vwap_zscore"]].tail())

    assert "vwap" in vwap_df.columns
    assert "vwap_upper" in vwap_df.columns
    assert "vwap_lower" in vwap_df.columns
    assert "vwap_zscore" in vwap_df.columns

    for i in range(1, len(vwap_df)):
        assert vwap_df.loc[i, "vwap_upper"] >= vwap_df.loc[i, "vwap"] >= vwap_df.loc[i, "vwap_lower"]

    print("Lesson 05 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：拍卖理论微观供需平衡、正态经验规则、突破价值区的单边失衡）：
1. 价值区（70% 规则）的数理本质：
   - 拍卖市场理论（Auction Market Theory, AMT）假定在正常交易状态下，资产价格围绕公允价值波动，成交量分布近似服从高斯钟形曲线（Bell Curve）；
   - 在统计学中，均值正负 1 倍标准差（±1σ）涵盖了约 68.2% 的概率密度。AMT 取整为 70% 作为“高频撮合公允价值区（Value Area）”；
   - 处于价值区内部时，多空双方对当前定价高度认可，行情以“低买高卖”的高频震荡均值回归为主。
2. 突破 VAH/VAL 的趋势质变：
   - 当价格放量击穿 VAH（向上）或 VAL（向下）且无法在短期内拉回时，表明有强大外生力量（如机构建仓、重大利好利空催化）彻底打破了旧的微观平衡；
   - 此时在区间边缘挂单逆势做均值回归的逆势盘全部被击穿打爆，触发强平止损；
   - 价格进入“价格发现阶段（Price Discovery）”，快速奔向下一个更高或更低的流动性真空区，形成单边暴利趋势行情。

Q2 标准解析（得分要点：机构大单执行算法的考核基准、被动与主动流动性聚集）：
1. 机构交易员的 KPI 与 VWAP：
   - 主权基金、互募对冲基金在买入数亿金额标的时，受合规与投决会严格监督，其最核心的量化考核标准即为“执行价格与市场成交量加权均价（VWAP）的差值”（Implementation Shortfall / Slippage vs VWAP）；
   - 若执行均价低于当日 VWAP，则评价为“Alpha 执行”，可获得丰厚奖金；若高于 VWAP，则被判定为“劣质执行”。
2. 为何 VWAP 会形成天然强支撑/阻力：
   - 当价格回调跌至当日 VWAP 附近时，所有需要执行买入指令的量化执行算法（VWAP Execution Algos）会集中在此处挂单进场吃单（因为此时买入能够拉低整体持仓成本至 VWAP 以下）；
   - 海量机构被动买单的瞬间涌入，筑起了一道坚不可摧的“买方流动性长城”，使得价格触及 VWAP 时几乎必然产生强烈的支撑弹升效应。

Q3 标准解析（得分要点：事件驱动锚定、市场筹码持仓成本中枢、群体心理防线）：
1. 锚定 VWAP（Anchored VWAP, AVWAP）的博弈论优势：
   - 传统 VWAP 每天收盘清零、次日重置，仅反映日内超短期资金偏好；
   - 而将锚点设定在“年内大底反转日”、“公司重组/财报超预期爆发日”或“历史天量突破日”，该 AVWAP 真实记录了**“自该重大转折事件发生以来，市场上所有参与者真金白银买入筹码的加权平均持仓成本”**。
2. 心理与资本防线：
   - 只要当前市价保持在 AVWAP 之上，意味着自该事件以来入场的主流多头群体整体处于盈利状态（未兑现浮盈），持股心态稳定，抛压极轻；
   - 一旦价格深度回调重新回踩测试该 AVWAP，不仅早期获利盘会在此坚决护盘加仓，场外踏空资金也会视其为“与主力建仓成本持平的最佳二买点”，因而释放极其惊人的中长期反弹推力。
""")
