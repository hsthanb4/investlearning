"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 2/5 课
参考实现与标准问答解析
第 2 课：供需区 (Order Blocks) 与流动性扫荡 (Liquidity Sweep) 检测
================================================================================
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional


def detect_liquidity_sweep(candle: Dict[str, float], key_level: float, sweep_type: str = "BSL") -> bool:
    """
    判断单根 K 线是否对关键结构水平实施了流动性扫荡 (假突破)
    """
    if sweep_type == "BSL":
        return (candle["high"] > key_level) and (candle["close"] < key_level)
    elif sweep_type == "SSL":
        return (candle["low"] < key_level) and (candle["close"] > key_level)
    return False


def identify_order_blocks(
    df: pd.DataFrame,
    displacement_ratio: float = 1.8
) -> List[Dict[str, Any]]:
    """
    自动识别历史行情中的看涨与看跌订单块 (Order Blocks) 并跟踪其缓解状态
    """
    n = len(df)
    obs: List[Dict[str, Any]] = []

    for t in range(n - 1):
        open_t = df.loc[t, "open"]
        close_t = df.loc[t, "close"]
        high_t = df.loc[t, "high"]
        low_t = df.loc[t, "low"]
        body_t = max(abs(close_t - open_t), 1e-6)

        open_next = df.loc[t + 1, "open"]
        close_next = df.loc[t + 1, "close"]
        high_next = df.loc[t + 1, "high"]
        low_next = df.loc[t + 1, "low"]
        body_next = abs(close_next - open_next)

        # 1. 判定看涨订单块 Bullish OB
        if close_t < open_t and close_next > open_next:
            if (body_next >= displacement_ratio * body_t) and (close_next > high_t):
                top = float(high_t)
                bottom = float(low_t)

                mitigated = False
                invalidated = False

                for j in range(t + 2, n):
                    cur_low = df.loc[j, "low"]
                    cur_high = df.loc[j, "high"]
                    cur_close = df.loc[j, "close"]

                    # 若价格回踩入 OB 区域 [bottom, top]
                    if (cur_low <= top) and (cur_high >= bottom):
                        mitigated = True
                    # 若收盘价彻底跌破 OB 下沿，失效
                    if cur_close < bottom:
                        invalidated = True
                        break

                obs.append({
                    "index": t,
                    "type": "BULLISH_OB",
                    "top": top,
                    "bottom": bottom,
                    "mitigated": mitigated,
                    "invalidated": invalidated
                })

        # 2. 判定看跌订单块 Bearish OB
        elif close_t > open_t and close_next < open_next:
            if (body_next >= displacement_ratio * body_t) and (close_next < low_t):
                top = float(high_t)
                bottom = float(low_t)

                mitigated = False
                invalidated = False

                for j in range(t + 2, n):
                    cur_low = df.loc[j, "low"]
                    cur_high = df.loc[j, "high"]
                    cur_close = df.loc[j, "close"]

                    if (cur_high >= bottom) and (cur_low <= top):
                        mitigated = True
                    if cur_close > top:
                        invalidated = True
                        break

                obs.append({
                    "index": t,
                    "type": "BEARISH_OB",
                    "top": top,
                    "bottom": bottom,
                    "mitigated": mitigated,
                    "invalidated": invalidated
                })

    return obs


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 02 参考实现与测试")
    print("=" * 60)

    # 1. 流动性扫荡判定测试
    c_sweep_bsl = {"open": 98.0, "high": 102.5, "low": 97.5, "close": 99.0}
    c_break_bsl = {"open": 98.0, "high": 102.5, "low": 97.5, "close": 101.5}
    c_none_bsl  = {"open": 96.0, "high": 99.2,  "low": 95.0, "close": 98.5}

    assert detect_liquidity_sweep(c_sweep_bsl, 100.0, "BSL") is True
    assert detect_liquidity_sweep(c_break_bsl, 100.0, "BSL") is False
    assert detect_liquidity_sweep(c_none_bsl,  100.0, "BSL") is False

    c_sweep_ssl = {"open": 92.0, "high": 93.0, "low": 87.5, "close": 91.0}
    c_break_ssl = {"open": 92.0, "high": 93.0, "low": 87.5, "close": 88.5}
    assert detect_liquidity_sweep(c_sweep_ssl, 90.0, "SSL") is True
    assert detect_liquidity_sweep(c_break_ssl, 90.0, "SSL") is False

    # 2. 订单块识别与缓解状态测试
    ob_df = pd.DataFrame({
        "open":  [100.0,  98.0, 108.0, 109.0, 102.0],
        "high":  [101.0, 109.0, 112.0, 110.0, 106.0],
        "low":   [ 97.0,  98.0, 107.0,  99.0, 101.0],
        "close": [ 98.0, 108.0, 110.0, 102.0, 105.0]
    })

    obs = identify_order_blocks(ob_df, displacement_ratio=1.8)
    print("识别到的订单块列表:", obs)

    assert len(obs) >= 1
    bull_ob = [o for o in obs if o["type"] == "BULLISH_OB"][0]
    assert bull_ob["index"] == 0
    assert bull_ob["top"] == 101.0
    assert bull_ob["bottom"] == 97.0
    assert bull_ob["mitigated"] is True

    print("Lesson 02 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：流动性猎杀微观机制、对手盘充足性、反向交易高期望值）：
1. 为什么假突破是绝佳反向买卖点：
   - 机构资金由于头寸庞大，建仓最大的制约是流动性不足。直接市价吃单会引发剧烈不利滑点；
   - 当价格向上刺破前期阻力位时，会瞬间触发两批庞大的市价买单流动性：
     a. 前期持有空头仓位者的保护性止损买单（Stop-Loss Buy Orders）；
     b. 突破型趋势交易者（Breakout Traders）的追涨入场买单；
   - 机构主力恰好利用这股瞬间涌现的天量买方流动性，全部倾泻自己的大额空头限价卖单（完成高位派发）；
   - 一旦买方流动性被吸收殆尽，市场上不再有后续买盘支撑，价格如自由落体般暴跌，造成追高者踩踏止损，推动价格加速崩跌。因此，跟随机构识别出 Sweep 后立即反手开仓，胜率和赔率极高。

Q2 标准解析（得分要点：FVG 的三根 K 线几何拓扑、供需真空与订单块重叠共振）：
1. 公平价值缺口（FVG）的严格定义：
   在连续 3 根 K 线（1, 2, 3）构成的形态中：
   - 看涨 FVG（Bullish FVG）：K 线 2 发生极其迅猛的单边上涨大阳线，使得 K 线 1 的最高价（High_1）与 K 线 3 的最低价（Low_3）之间出现价格空白断层（Gap = Low_3 - High_1 > 0）；
   - 这段空白区间意味着买卖双方在该价格带未进行充分撮合（Inefficient Price Action），属于纯粹的多头单边扫荡。
2. 与 Order Block 的共振效应：
   - 只有伴随 FVG 产生的 Order Block 才是真正由机构主动激进性买盘驱动的“高质量有效 OB”；
   - 未来价格回踩该区域时，既是在“回补 FVG 价格失衡”，又是在“重测机构 Order Block 底仓”，双重供需引力叠加，使得该点位的反弹确定性与盈亏比达到顶峰。

Q3 标准解析（得分要点：订单消耗衰减定律、动态活跃队列维护与失效过滤）：
1. 为什么首次回踩（First Touch）最有效：
   - 当机构在 OB 处建仓时，部分未成交的限价挂单仍留在撮合引擎账本中；
   - 价格首次回踩（First Touch）时，这些沉淀的机构防御挂单被瞬间触发，释放强大推力；
   - 但若价格多次回踩（2次、3次及以上），说明每次反弹幅度越来越小，多头买盘逐步被空头蚕食消化，OB 内部的未成交机构订单被全部吸收耗尽（Mitigated），阻力/支撑防线变薄，极易被直接放量击穿。
2. 量化算法的活动队列（Active OB Pool）维护架构：
   - 数据结构：采用优先级队列或滑动字典维护处于活动状态的 `active_obs`；
   - 状态转移判定：
     * 首次触及（`cur_low <= top and cur_high >= bottom`）：标记 `touch_count += 1`，发出高置信度一级信号；
     * 若 `touch_count >= 2` 或超过固定时间窗口（如 50 根 K 线未回踩），将其降权并移入次级观察池；
     * 彻底失效（`cur_close < bottom`）：立即将该 OB 从活动队列中 `pop` 物理移除，防止过期死信号污染后续交易引擎。
""")
