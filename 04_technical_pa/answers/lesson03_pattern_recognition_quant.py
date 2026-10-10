"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 3/5 课
参考实现与标准问答解析
第 3 课：经典几何形态量化：头肩底判定器与统计防伪
================================================================================
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List


def detect_inverse_head_and_shoulders(
    points: Dict[str, float],
    current_close: float,
    shoulder_tolerance: float = 0.05,
    neckline_tolerance: float = 0.08,
    min_head_prominence: float = 0.03,
    min_depth: float = 0.08
) -> Dict[str, Any]:
    """
    量化头肩底 (Inverse Head and Shoulders) 几何特征提取与判定器
    """
    ls = points["left_shoulder"]
    nl1 = points["neckline1"]
    head = points["head"]
    nl2 = points["neckline2"]
    rs = points["right_shoulder"]

    reasons: List[str] = []

    # 1. 头部深度与突出度检验
    if head >= ls or head >= rs:
        reasons.append("头部必须严格低于左右两肩波谷")
    prom_ls = (ls - head) / head
    prom_rs = (rs - head) / head
    if prom_ls < min_head_prominence or prom_rs < min_head_prominence:
        reasons.append(f"头部相对双肩不够深陷突出 (要求>={min_head_prominence*100:.1f}%)")

    # 2. 左右双肩对称性检验
    shoulder_diff = abs(ls - rs) / ls
    if shoulder_diff > shoulder_tolerance:
        reasons.append(f"左右双肩高度不对称 (|LS - RS|/LS = {shoulder_diff*100:.1f}% > {shoulder_tolerance*100:.1f}%)")

    # 3. 颈线倾斜度检验
    neckline_tilt = abs(nl1 - nl2) / nl1
    if neckline_tilt > neckline_tolerance:
        reasons.append(f"颈线倾斜度过大 ({neckline_tilt*100:.1f}% > {neckline_tolerance*100:.1f}%)")

    # 4. 颈线水平与形态高度
    neckline_price = (nl1 + nl2) / 2.0
    pattern_height = neckline_price - head
    if pattern_height / head < min_depth:
        reasons.append(f"形态垂直高度过浅 ({pattern_height/head*100:.1f}% < {min_depth*100:.1f}%)")

    is_valid_ihs = len(reasons) == 0
    breakout_confirmed = current_close > neckline_price
    target_price = neckline_price + pattern_height

    # 5. 盈亏比计算 (以右肩为基准止损位)
    stop_loss = rs
    risk = current_close - stop_loss
    reward = target_price - current_close
    if is_valid_ihs and breakout_confirmed and risk > 0:
        risk_reward_ratio = float(reward / risk)
    else:
        risk_reward_ratio = 0.0

    return {
        "is_valid_ihs": is_valid_ihs,
        "breakout_confirmed": breakout_confirmed,
        "neckline_price": float(neckline_price),
        "pattern_height": float(pattern_height),
        "target_price": float(target_price),
        "risk_reward_ratio": float(risk_reward_ratio),
        "reasons": reasons
    }


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 03 参考实现与测试")
    print("=" * 60)

    # 1. 有效头肩底测试
    valid_points = {
        "left_shoulder": 100.0,
        "neckline1": 110.0,
        "head": 92.0,
        "neckline2": 112.0,
        "right_shoulder": 102.0
    }
    res_valid = detect_inverse_head_and_shoulders(valid_points, current_close=113.0)
    print("有效头肩底判定结果:", res_valid)

    assert res_valid["is_valid_ihs"] is True
    assert res_valid["breakout_confirmed"] is True
    assert abs(res_valid["neckline_price"] - 111.0) < 1e-4
    assert abs(res_valid["pattern_height"] - 19.0) < 1e-4
    assert abs(res_valid["target_price"] - 130.0) < 1e-4
    assert abs(res_valid["risk_reward_ratio"] - (17.0 / 11.0)) < 1e-3

    # 2. 头部平坦畸变测试
    flat_head_points = {
        "left_shoulder": 100.0, "neckline1": 110.0,
        "head": 99.0,           "neckline2": 110.0,
        "right_shoulder": 100.0
    }
    res_flat = detect_inverse_head_and_shoulders(flat_head_points, current_close=112.0)
    assert res_flat["is_valid_ihs"] is False
    assert any("头部" in r for r in res_flat["reasons"])

    # 3. 双肩不对称畸变测试
    asym_points = {
        "left_shoulder": 100.0, "neckline1": 120.0,
        "head": 85.0,           "neckline2": 122.0,
        "right_shoulder": 115.0
    }
    res_asym = detect_inverse_head_and_shoulders(asym_points, current_close=125.0)
    assert res_asym["is_valid_ihs"] is False
    assert any("双肩" in r for r in res_asym["reasons"])

    print("Lesson 03 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：人类大脑的模式识别偏差、纯随机游走中的形态涌现、全样本胜率坍塌）：
1. 幻想性视错觉（Pareidolia）与幸存者偏差：
   人类进化中大脑被训练为过度识别模式（即使是一片随机噪音）。主观交易者在复盘时，只记住了那些随后走出翻倍大行情的“完美头肩底”，而选择性遗忘了无数个在盘整中夭折、或反向暴跌爆仓的失败形态。
2. 统计学与随机游走实证：
   在纯粹由几何布朗运动（Geometric Brownian Motion）或高斯随机游走生成的无规律合成价格序列中，运行几何形态识别算法，同样能够高频检测出标准的“头肩底”、“双重底”和“旗形”；
   在严谨的全样本、包含全部退市标的的量化回测中，裸头肩形态突破的实际胜率仅在 42%~45% 之间，其数学期望值本身为负（扣除交易摩擦）。形态必须配合大级别流动性背景（Liquidity Pool）与成交量异动，才能转化为正期望系统。

Q2 标准解析（得分要点：左侧猜顶底 vs 右侧确认、时间戳因果契约与防止偷价）：
1. 为什么不能在右肩提前入场：
   在右肩形成阶段，市场仅走完了形态的 70%，此时既可能向上突破颈线完成头肩底，也极可能演变为“顺势下破前低形成下降中继通道（Bearish Flag）”；
   提前在右肩左侧入场本质是“赌反转”，将承担未被证实的不对称下行风险。
2. 回测引擎中的因果性契约（Causality Contract）：
   - 信号产生时间戳（Signal Timestamp）：形态确认必须以“突破 K 线收盘价 Close > 颈线”为信号触发点（如 t 根 K 线收盘）；
   - 执行时间戳（Execution Timestamp）：真实的物理买单最早只能在 t+1 根 K 线的 Open 撮合；
   - 严禁在 t 根 K 线的内部以颈线价格直接成交（这属于典型的前视偏差/偷价）。区分候选扫描与突破成交，是保障量化系统实盘与回测一致性的铁律。

Q3 标准解析（得分要点：成交量配合倍数、假突破诱多陷阱、回踩确认机制）：
1. 突破时的成交量放大（Volume Surge）：
   - 有效突破通常伴随机构资金的真金白银市价扫盘，突破根 K 线的成交量应至少达到过去 20 根均量（MA20 Volume）的 1.5 ~ 2.0 倍以上；
   - 若价格虽越过颈线但缩量严重，说明主力资金并未进场，大概率是散户追涨形成的“流动性真空假突破”，诱多后随时反转。
2. 回踩测试（Pullback Confirmation）策略：
   - 激进型：突破收盘即以小仓位跟进；
   - 稳健型（买方推荐）：等待突破后的首次缩量回踩颈线（Pullback & Retest），观察原阻力线是否成功转化为强支撑（Resistance turns into Support）；
   - 一旦在回踩颈线处出现看涨吞没或长下影线拒跌 K 线，此时再满仓入场，既能彻底规避 80% 的假突破多头陷阱，又能将止损紧贴颈线下方，显著拔高盈亏比。
""")
