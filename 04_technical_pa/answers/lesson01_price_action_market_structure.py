r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 1/5 课
第 1 课：价格行为学与市场结构识别状态机 (参考答案版)
================================================================================

【Q1 深度参考答案】
滞后均线 vs 实时价格行为（Price Action）：为什么基于移动平均线（如 MA5/MA20）的金叉死叉信号在震荡市中会导致灾难性的连续假信号与回撤，而基于微观市场结构（Swing Points & BOS）突破能够第一时间识别机构买卖盘意图？
- **[移动平均线的低通滤波相位时滞]**：均线本质是价格时域信号的 FIR/IIR 线性平滑滤波器。平滑必然带来固有的时间延迟（Phase Lag）；窗口期越长，滞后越严重。当金叉形成时，价格往往已行至波段反弹的极限位，盈亏比极低。
- **[震荡市的负期望磨损]**：在无趋势箱体中，均线反复缠绕，均线金叉往往买在波段顶部、死叉割在波段底部，导致连续高频“左右挨打”并产生高额交易换手佣金磨损。
- **[微观摆动点的流动性锚定]**：Swing High 和 Swing Low 是市场供需天平达到极限的物理转折点，凝结了做市商库存成本与散户止损盘。BOS 突破反映的是真实挂单深度的击穿与吸收，代表机构主动买单的即时事实，不含任何平滑过滤滞后。

【Q2 深度参考答案】
实体收盘突破（Candle Body Close Break） vs 影线假突破扫荡（Wick Sweep）：在判定 BOS 和 CHoCH 时，为什么机构级交易算法严格要求“K线收盘价有效突破前高/前低”，而将“最高价刺破但收盘跌回”判定为流动性扫荡（Liquidity Sweep）而非有效突破？
- **[收盘价的公允均衡权重]**：日内极值（High/Low）往往由偶发的薄流动性脉冲成交或算法刺透触发；而蜡烛实体的收盘价（Close）反映了一根 K 线博弈结束时机构资金愿意接受的公允均衡价。
- **[流动性掠夺的微观猎杀]**：当价格仅以影线刺穿前高阻力位后迅速回落，反映机构主力在利用前高上方的散户追涨买单（Buy Stop）与空头止损买单作为流动性对手盘，趁机倾泻其庞大空头头寸完成高位派发。
- **[算法防伪与胜率保障]**：只有实体收盘价站上前高之上，才证明多头资金完成了对该价格带上方全部未成交卖单的实质性消化；将其作为入场前置条件能过滤掉 70% 以上的诱多屠杀。

【Q3 深度参考答案】
多时间周期嵌套（Multi-Timeframe Structure）：假设日线处于明确的空头结构（连续 LH + LL），而 15 分钟级别由于突发利好出现 CHoCH 向上反弹。作为职业交易员，你应如何利用多时间周期共振设计“大级别顺势挂单，小级别抓反转确认”的交易计划？
- **[大周期定战略偏向（Directional Bias）]**：日线级别的 LH + LL 确立了宏观主趋势为绝对空头（Higher Timeframe Bias = Short Only）。严禁在小级别反弹中重仓做多，逆大势交易期望收益为负。
- **[小级别定狙击战术（Precision Entry）]**：将 15 分钟的反弹 CHoCH 判定为日线空头趋势中的高价值回调（Pullback）。监控反弹动能触及日线级关键供需区（Order Block）或 0.618 斐波那契折返位。
- **[微观反转触发执行（Secondary Confirmation）]**：当反弹触及关键阻力带后，等待 15 分钟级别重新出现看跌 CHoCH（跌破局部抬高低点），随即顺势建立空头头寸。该结构将止损严格控制在 15 分钟局部高点，而止盈目标直指日线级前低 LL，获得 1:4 以上的优异盈亏比。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：顺大势、逆小势、抓共振</div>
  <div class="callout-body">
    任何单一时间维度的价格行为都是片面的。高水平机构交易员通过将高时间周期的结构边界与低时间周期的流动性触发点相互锚定，实现确定性与盈亏比的双重最大化。
  </div>
</div>
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple


def detect_swing_points(df: pd.DataFrame, window: int = 2) -> pd.DataFrame:
    """
    自动化识别价格序列中的摆动高点 (Swing High) 与摆动低点 (Swing Low)
    """
    res = df.copy()
    n = len(res)

    is_sh = [False] * n
    is_sl = [False] * n
    sh_price = [np.nan] * n
    sl_price = [np.nan] * n

    highs = res["high"].values
    lows = res["low"].values

    for i in range(window, n - window):
        # 检验是否为局部波峰 Swing High
        current_h = highs[i]
        is_peak = True
        for offset in range(1, window + 1):
            if current_h <= highs[i - offset] or current_h <= highs[i + offset]:
                is_peak = False
                break
        if is_peak:
            is_sh[i] = True
            sh_price[i] = current_h

        # 检验是否为局部波谷 Swing Low
        current_l = lows[i]
        is_valley = True
        for offset in range(1, window + 1):
            if current_l >= lows[i - offset] or current_l >= lows[i + offset]:
                is_valley = False
                break
        if is_valley:
            is_sl[i] = True
            sl_price[i] = current_l

    res["is_swing_high"] = is_sh
    res["is_swing_low"] = is_sl
    res["swing_high_price"] = sh_price
    res["swing_low_price"] = sl_price

    return res


def analyze_market_structure(df: pd.DataFrame, window: int = 2) -> Dict[str, Any]:
    """
    基于识别的摆动点，按时间推进构建市场结构演变状态机，识别 BOS 与 CHoCH 事件
    """
    swings_df = detect_swing_points(df, window=window)
    n = len(swings_df)

    current_trend = "UNDEFINED"
    last_sh: float = None
    last_sl: float = None
    events: List[Dict[str, Any]] = []

    for i in range(n):
        c = swings_df.loc[i, "close"]

        # 1. 检查是否有突破产生
        if last_sh is not None and c > last_sh:
            if current_trend == "BULLISH":
                events.append({
                    "index": i,
                    "type": "BOS_BULL",
                    "price": float(c),
                    "break_level": float(last_sh)
                })
            else:
                events.append({
                    "index": i,
                    "type": "CHoCH_BULL",
                    "price": float(c),
                    "break_level": float(last_sh)
                })
                current_trend = "BULLISH"
            last_sh = None

        elif last_sl is not None and c < last_sl:
            if current_trend == "BEARISH":
                events.append({
                    "index": i,
                    "type": "BOS_BEAR",
                    "price": float(c),
                    "break_level": float(last_sl)
                })
            else:
                events.append({
                    "index": i,
                    "type": "CHoCH_BEAR",
                    "price": float(c),
                    "break_level": float(last_sl)
                })
                current_trend = "BEARISH"
            last_sl = None

        # 2. 如果当前 K 线是确认的摆动点，更新基准水平
        if swings_df.loc[i, "is_swing_high"]:
            last_sh = swings_df.loc[i, "swing_high_price"]
            if current_trend == "UNDEFINED" and last_sl is not None:
                current_trend = "BULLISH" if c > last_sl else "BEARISH"

        if swings_df.loc[i, "is_swing_low"]:
            last_sl = swings_df.loc[i, "swing_low_price"]
            if current_trend == "UNDEFINED" and last_sh is not None:
                current_trend = "BEARISH" if c < last_sh else "BULLISH"

    return {
        "events": events,
        "current_trend": current_trend,
        "last_swing_high": last_sh,
        "last_swing_low": last_sl
    }


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 01 参考实现与测试")
    print("=" * 60)

    synthetic_ohlc = pd.DataFrame({
        "open":  [100, 98, 96,  98, 104, 102,  99, 106, 114, 110, 104,  97,  94,  92,  93],
        "high":  [103, 100, 98, 101, 106, 103, 101, 108, 116, 112, 106, 100,  96,  95,  94],
        "low":   [ 98,  96, 94,  96, 101,  99,  97, 104, 110, 105,  95,  92,  90,  89,  90],
        "close": [ 99,  97, 95, 100, 105, 100, 100, 107, 115, 106,  96,  93,  91,  92,  93]
    })

    swings_df = detect_swing_points(synthetic_ohlc, window=2)
    print("摆动点识别结果:\n", swings_df[["high", "low", "is_swing_high", "is_swing_low"]])

    assert swings_df.loc[2, "is_swing_low"] == True
    assert swings_df.loc[4, "is_swing_high"] == True
    assert swings_df.loc[6, "is_swing_low"] == True
    assert swings_df.loc[8, "is_swing_high"] == True

    structure_res = analyze_market_structure(synthetic_ohlc, window=2)
    print("市场结构分析结果:")
    print("当前趋势:", structure_res["current_trend"])
    print("检测到的事件:", structure_res["events"])

    event_types = [e["type"] for e in structure_res["events"]]
    assert "BOS_BULL" in event_types
    assert "CHoCH_BEAR" in event_types

    print("Lesson 01 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：均线的滞后性本质、微观摆动点的供需流动性映射）：
1. 均线滞后性的数学根源：
   - 移动平均线（MA）本质是对历史价格的时域低通滤波（Low-pass Filter），无论简单移动平均（SMA）还是指数移动平均（EMA），其相位延迟（Phase Lag）不可避免；
   - 在震荡市或趋势初转期，均线反应迟缓，当金叉出现时价格往往已行至波段反弹的末端；此时买入不仅没有盈亏比优势，反而极易直接追在短期波峰，随后震荡回落触发死叉止损，导致高频左右挨打、净值大幅回撤。
2. 市场结构（Swing Points）的第一性原理：
   - Swing High 和 Swing Low 是市场买卖双方在特定时间窗口内达到力量极限的物理锚点，其背后往往凝聚着大量的散户止损盘与做市商流动性挂单；
   - 当价格放量突破关键摆动点（BOS）时，意味着某一方的吸收（Absorption）与防御被彻底击溃，供需天平瞬间失衡，这是机构大单进场留下的直接脚印，不含任何平滑过滤滞后。

Q2 标准解析（得分要点：收盘价意图度量、假突破/流动性扫荡的微观机制）：
1. 收盘价（Close）的博弈权重：
   - 在专业交易与量化体系中，日内极值（High/Low）往往由偶发的薄流动性扫单或散户追单撮合而成；而蜡烛实体的收盘价（Close）反映了一根 K 线博弈结束时机构资金愿意接受的公允均衡价。
   - 只有收盘价站上前高之上（Close > Swing High），才代表多头资金完成了对该价格带上方全部挂单阻力的实质性消化（Breakout Confirmation）。
2. 影线刺破（Wick Sweep）的流动性猎杀本质：
   - 若价格最高点冲破 Swing High，但随后在数分钟内被猛烈砸回，收盘价依然被压制在阻力位下方，形成一根长长的上影线；
   - 这在价格行为学中被严格定义为“流动性扫荡”（Liquidity Sweep）或“假突破（Fakeout）”；
   - 其微观机制是机构主力利用突破追涨盘（Breakout Buyers）的买入市价单以及前期空头的止损买单（Buy Stop Orders）作为流动性对手盘，趁机倾泻其海量空头头寸进行派发，随后推动价格剧烈下杀。因此将其误判为 BOS 将直接掉入机构的屠宰场。

Q3 标准解析（得分要点：多周期时间框架对齐、大顺小逆策略架构）：
1. 顶层大级别决定主战场方向（日线 Bearish）：
   - 日线级别的 Lower Highs 和 Lower Lows 构成了核心阻力带与大趋势偏向（Higher Timeframe Bias = Short Only）；
   - 在大级别空头背景下，绝不轻易在小级别反弹中重仓做多，因为逆大势交易胜率和盈亏比均极低。
2. 小级别微观结构决定精准狙击点（15分钟 CHoCH）：
   - 当 15 分钟级别出现向上 CHoCH 时，交易员不应盲目追涨，而应将其视为“日线空头趋势中的高价值回调（Pullback）”；
   - 监控 15 分钟的反弹走势逐步触及日线级别的关键供需区（Order Block）或 0.618 斐波那契折返位；
   - 当反弹动能耗尽、15 分钟级别重新向下出现 Bearish CHoCH 确认反转时，果断进场建立空头仓位；
   - 这种操作将止损精确压缩在 15 分钟小结构的局部高点，而止盈目标直指日线级别的下一个前低（LL），从而获得 1:3 甚至 1:5 以上的极佳盈亏比。
""")
