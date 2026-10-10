"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 2/5 课
第 2 课：供需区 (Order Blocks) 与流动性扫荡 (Liquidity Sweep) 检测
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 深度思考题回答完整、逻辑严谨（各 2 分）：共 6 分
- 合格线：8/10 分

【理论精讲】
1. 智能资金概念（Smart Money Concepts, SMC）与机构订单微观结构：
   大型对冲基金、主权财富基金与做市商无法像散户一样以市价单随意建仓，否则会造成极大的滑点（Slippage）冲击成本。
   机构建仓必须寻找海量“对手盘流动性”（Counterparty Liquidity）。

2. 订单块（Order Block, OB）的算法量化定义：
   - 看涨订单块（Bullish OB）：
     在价格发生强劲脉冲式向上暴涨（Displacement，实体巨大且产生突破）之前，机构为了诱空建仓而推动的**最后一根下跌阴线**（Close < Open）。
     该阴线的价格区间（Top = High 或 Body Top, Bottom = Low）构成了未来强有力的机构买入需求区（Demand Zone）。
   - 看跌订单块（Bearish OB）：
     在价格发生强劲脉冲式向下暴跌之前，机构为了诱多出货而推动的**最后一根上涨阳线**（Close > Open）。
     该阳线的价格区间（Top = High, Bottom = Low 或 Body Bottom）构成了未来的机构供给区（Supply Zone）。
   - 缓解状态（Mitigation）：
     当价格未来首次回踩进入该 OB 区间（Low <= Top 且 High >= Bottom）但未击穿底线时，机构在此追加或保护剩余订单，常引发剧烈弹升（First Touch Reaction）；若价格收盘彻底跌穿 Bottom，则该 Bullish OB 被击穿失效（Invalidated）。

3. 流动性扫荡（Liquidity Sweep / 假突破）：
   大众散户习惯将止损挂在明显的波峰高点之上（买方流动性池 BSL, Buy-Side Liquidity）或波谷低点之下（卖方流动性池 SSL, Sell-Side Liquidity）。
   - BSL 扫荡（诱多假突破）：
     K 线最高价瞬间刺破关键摆动高点（High > Swing_High），扫掉前期空头止损买单并诱骗追涨买单；但收盘价迅速被巨量卖单砸回高点下方（Close < Swing_High）。长上影线揭示机构主力已成功完成出货。
   - SSL 扫荡（诱空假跌破）：
     K 线最低价瞬间刺破关键摆动低点（Low < Swing_Low），扫掉多头止损卖单并诱骗追空卖单；但收盘价迅速被强劲买单拉回低点上方（Close > Swing_Low）。长下影线揭示机构主力完成低吸洗盘。

【三个思考题 (Q1~Q3)】
Q1: 对手盘流动性（Counterparty Liquidity）机制：为什么“假突破立即拉回”（Liquidity Sweep）往往是职业机构胜率极高的反向交易机会？请从市价单（Market Orders）、止损挂单（Stop Orders）以及做市商被动吸收的角度剖析资金博弈过程。
Q2: 公平价值缺口（Fair Value Gap, FVG / 价格失衡 Imbalance）：在经典三根 K 线模型中，FVG 的严格数学几何定义是什么？为什么机构订单块（Order Block）与未回补 FVG 区域重叠时，会形成统计胜率极高的“高概率订单块（High Probability OB）”？
Q3: 订单块缓解（Mitigation）与衰减时效：为什么首次回踩（First Touch）订单块的反应往往最剧烈，而经过价格多次反复回踩（2次及以上）的订单块防御有效性会急剧衰减？量化算法应如何维护“活动订单块队列”以防止过期死信号？
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional


def detect_liquidity_sweep(candle: Dict[str, float], key_level: float, sweep_type: str = "BSL") -> bool:
    """
    判断单根 K 线是否对关键结构水平实施了流动性扫荡 (假突破)
    
    参数:
    candle: dict 包含 'high', 'low', 'close', 'open'
    key_level: 关键参考水平 (如前高 Swing High 或前低 Swing Low)
    sweep_type: "BSL" (扫荡上方买方流动性/假突破) 或 "SSL" (扫荡下方卖方流动性/假跌破)
    
    返回:
    bool: 是否构成扫荡
    - BSL: candle['high'] > key_level 且 candle['close'] < key_level
    - SSL: candle['low'] < key_level 且 candle['close'] > key_level
    """
    # TODO: 请实现流动性扫荡判定逻辑
    pass


def identify_order_blocks(
    df: pd.DataFrame,
    displacement_ratio: float = 1.8
) -> List[Dict[str, Any]]:
    """
    自动识别历史行情中的未缓解看涨与看跌订单块 (Order Blocks)
    
    参数:
    df: 包含 'open', 'high', 'low', 'close' 的 DataFrame
    displacement_ratio: 脉冲 K 线实体大小与前一根 K 线实体大小的最小比例阈值
    
    算法规则:
    1. 寻找看涨 OB (Bullish OB):
       - t 根为下跌阴线 (close[t] < open[t])
       - t+1 根为强劲阳线 (close[t+1] > open[t+1])
       - 脉冲实体扩张: body[t+1] >= displacement_ratio * body[t] 且 close[t+1] > high[t]
       - 记录 OB 区间: top = high[t], bottom = low[t], index = t
    2. 寻找看跌 OB (Bearish OB):
       - t 根为上涨阳线 (close[t] > open[t])
       - t+1 根为强劲阴线 (close[t+1] < open[t+1])
       - 脉冲实体扩张: body[t+1] >= displacement_ratio * body[t] 且 close[t+1] < low[t]
       - 记录 OB 区间: top = high[t], bottom = low[t], index = t
    3. 跟踪后续缓解状态 (Mitigation):
       - 对每个已确认的 OB，遍历 t+2 以后的 K 线：
         * Bullish OB: 若后续某根 K 线 low <= top 且 low >= bottom，标记为已缓解 mitigated = True；
                       若 close < bottom，标记为失效 invalidated = True
         * Bearish OB: 若后续某根 K 线 high >= bottom 且 high <= top，标记为已缓解 mitigated = True；
                       若 close > top，标记为失效 invalidated = True
    """
    # TODO: 请实现订单块识别与缓解状态追踪算法
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 02: 订单块识别与流动性扫荡检测测试")
    print("=" * 60)

    # 1. 流动性扫荡判定测试
    # 阻力位 100.0
    c_sweep_bsl = {"open": 98.0, "high": 102.5, "low": 97.5, "close": 99.0}   # 假突破拉回
    c_break_bsl = {"open": 98.0, "high": 102.5, "low": 97.5, "close": 101.5}  # 实体站上
    c_none_bsl  = {"open": 96.0, "high": 99.2,  "low": 95.0, "close": 98.5}   # 未触及

    assert detect_liquidity_sweep(c_sweep_bsl, 100.0, "BSL") is True
    assert detect_liquidity_sweep(c_break_bsl, 100.0, "BSL") is False
    assert detect_liquidity_sweep(c_none_bsl,  100.0, "BSL") is False

    # 支撑位 90.0
    c_sweep_ssl = {"open": 92.0, "high": 93.0, "low": 87.5, "close": 91.0}   # 假跌破拉回
    c_break_ssl = {"open": 92.0, "high": 93.0, "low": 87.5, "close": 88.5}   # 实体跌穿
    assert detect_liquidity_sweep(c_sweep_ssl, 90.0, "SSL") is True
    assert detect_liquidity_sweep(c_break_ssl, 90.0, "SSL") is False

    # 2. 订单块识别与缓解状态测试
    # 构造 K 线数据:
    # t=0: 小阴线 (open 100, close 98, high 101, low 97, body=2)
    # t=1: 巨大暴涨阳线 (open 98, close 108, high 109, low 98, body=10 >= 1.8*2=3.6, close 108 > high 101) -> t=0 确认为 Bullish OB!
    # t=2: 冲高盘整 (open 108, close 110, high 112, low 107)
    # t=3: 回踩探入 OB 区间 (open 109, close 102, high 110, low 99) -> low=99 <= top=101 且 low >= bottom=97 -> 触发缓解!
    ob_df = pd.DataFrame({
        "open":  [100.0,  98.0, 108.0, 109.0, 102.0],
        "high":  [101.0, 109.0, 112.0, 110.0, 106.0],
        "low":   [ 97.0,  98.0, 107.0,  99.0, 101.0],
        "close": [ 98.0, 108.0, 110.0, 102.0, 105.0]
    })

    obs = identify_order_blocks(ob_df, displacement_ratio=1.8)
    print("识别到的订单块列表:", obs)

    assert len(obs) >= 1, "必须成功识别出至少一个订单块"
    bull_ob = [o for o in obs if o["type"] == "BULLISH_OB"][0]
    assert bull_ob["index"] == 0, "看涨订单块应位于 t=0"
    assert bull_ob["top"] == 101.0
    assert bull_ob["bottom"] == 97.0
    assert bull_ob["mitigated"] is True, "在 t=3 处价格回踩至 99.0，应被标记为已缓解"

    print("Lesson 02 练习题测试全部通过！")
