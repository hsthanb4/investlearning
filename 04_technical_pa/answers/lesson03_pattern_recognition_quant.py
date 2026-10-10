r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 3/5 课
第 3 课：经典价格形态量化识别与几何拓扑 (参考答案版)
================================================================================

【Q1 深度参考答案】
经典头肩形态的供需力量衰竭推导：从三次尝试突破的成交量逐级递减、左肩/头/右肩的微观换手率，推导为何颈线破位后常引发量度跌幅的非线性踩踏？
- **[多头攻击动能的递减法则]**：在头肩顶形态中，左肩是强趋势的主升浪，伴随天量成交；随后冲高回落；头部虽创出新高，但成交量明显萎缩（量价背离），说明增量买盘枯竭；右肩的反弹甚至无法触及头部高点，反映多头资金彻底丧失进攻意愿。
- **[颈线支撑的筹码沉淀]**：两次回调的低点连线（颈线）沉淀了大量在形态构筑期间左侧抄底的浮筹。所有右肩买入者与颈线附近的多头，其止损单均密集成交在颈线下方。
- **[非线性雪崩正反馈]**：一旦价格跌破颈线，触发三维共振卖盘：① 颈线多头集中斩仓卖盘；② 趋势突破算法的追空市价单；③ 意识到形态破位的长线机构撤出买单挂单（流动性真空）。三重合力形成做空正反馈，驱动价格快速打满垂直高度 H 的量度跌幅。

【Q2 深度参考答案】
威科夫弹簧效应（Wyckoff Spring）与次底假摔猎杀：为什么在双底（W-Bottom）结构中，第二个底部略微刺穿第一个底部最低点（Spring）反而比未刺穿的平底具有更高的反弹胜率？从流动性清算与浮筹吸收的角度论述。
- **[平底双底的浮筹残留缺陷]**：若第二个底未跌破前低，虽然形态美观，但前低下方积压的大量散户止损单并未被清洗，多头平均持仓成本偏高，后市拉升时极易遭遇获利盘和解套盘的连续砸盘压制。
- **[弹簧假摔的流动性核爆吸收]**：主力资金在次底故意下砸打破前低支撑线，引发条件触发的卖方止损盘（SSL）与破位追空盘狂暴涌出。主力利用这波瞬时的高流动性大口吞下廉价筹码，完成终极吸筹（Terminal Shakeout）。
- **[浮筹彻底出清的轻盈拉升]**：随着坚决杀跌盘被洗劫一空，盘口上方的抛压阻力被彻底排空。主力资金只需很小的买盘即可将价格光速拉回前低之上并暴击颈线，形成胜率与爆发力极佳的威科夫 Spring 结构。

【Q3 深度参考答案】
形态量化算法的“几何容差”陷阱：为什么在真实市场中机械要求左右肩绝对对称（0% 误差）会导致策略几乎无法触发，而容差过大（如 > 20%）又会陷入过拟合与高假阳性（False Positive）灾难？算法如何自适应动态平衡？
- **[机械零容差的样本稀疏（Underfitting）]**：金融市场充满微观噪声，左右肩在自然撮合下绝对等高的概率接近测度零。若设定对称误差低于 1%，全市场数年可能无法捕捉到任何有效样本，策略失去实际可交易性。
- **[过大容差的数据挖掘伪形态（Overfitting & False Positives）]**：若将容差放大至 15%~25%，算法会将普通的震荡无序锯齿波错误识别为头肩形态。此类“畸变伪形态”背后根本不存在多空动能衰竭的因果链，实盘交易胜率将骤降至 35% 以下，带来灾难性回撤。
- **[自适应动态平衡解法]**：工程架构上应当采用“双重约束网”：① 静态几何容差锚定在 5%~8%；② 引入微观动量或成交量确认因子（如头部成交量必须高于右肩成交量，右肩反弹动能 RSI 必须弱于左肩）。通过多维度交叉印证，在样本覆盖率与信号纯度之间达成纳什均衡。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：拒绝图形玄学，坚持严格量化</div>
  <div class="callout-body">
    形态的有效性来自市场多空预期的失衡，而非几何图形的美观。只有在严格拓扑容差、量价背离与盈亏比大于 1:1.5 的前提下，形态交易才具备统计套利的正期望。
  </div>
</div>
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
