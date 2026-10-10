r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 3/5 课
第 3 课：经典价格形态量化识别与几何拓扑 (头肩底、双底与威科夫弹簧)
================================================================================

【课程定位与第一性原理】
传统技术分析常因主观“看图说话”而沦为伪科学。本课立足量化工程第一性原理，
将经典价格形态解构为严格的极值点拓扑空间（Topological Extremum Space）与几何约束网，
穿透形态背后多空力量衰竭、浮筹清洗与威科夫弹簧效应（Wyckoff Spring）的博弈本质。

- **[头肩底的供需耗尽本质]**：头肩底并非神秘的东方玄学，而是空头三次向下冲击时动能逐级衰竭的物理映射——左肩恐慌抛售，头部最后宣泄，右肩无力创新低，颈线突破宣告供求平衡被彻底打翻。
- **[威科夫弹簧的流动性假摔]**：在双底结构中，次底故意刺破前低（Spring）随后光速收复，是主力资金在低位触发散户破位止损单以快速吸筹的极致体现。
- **[几何容差与数学可证伪性]**：形态量化识别器必须以参数化容差（双肩对称比、颈线斜率、头部深陷度）取代肉眼主观臆断，实现 100% 确定性的计算机代码回测。

【核心概念与就近图文排版】

1. 头肩底几何拓扑与颈线断裂：
观察下图关于头肩形态各几何节点（左肩、头部、右肩、颈线）的严格量化特征：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.1：经典头肩顶形态 (Head & Shoulders) 几何拓扑与颈线断裂确认</span>
    <span class="diagram-tag">HEAD-SHOULDERS-TOPOLOGY</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l03_head_and_shoulders_anatomy.svg -->
  </div>
</div>

- **[头部突出性约束]**：头部最低点必须显著深陷于左右双肩之下，相对双肩均价至少突出 $\ge 3\%$。
- **[双肩对称性容差]**：左肩低点与右肩低点的高度差异必须受控在动态容差 $\epsilon_{\text{shoulder}} \le 5\%$ 之内。
- **[颈线突破与量度目标]**：收盘价站上颈线价格 $P_{\text{neck}}$ 确认突破，理论最小量度目标位为 $P_{\text{target}} = P_{\text{neck}} + H$，其中 $H = P_{\text{neck}} - P_{\text{head}}$。

2. 双底形态与威科夫弹簧效应 (Spring)：
下图展示了双底形态中次底假摔猎杀止损并迅速收复的威科夫弹簧结构：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.2：双底形态 (W-Bottom) 与威科夫弹簧效应 (Spring) 诱空反转结构</span>
    <span class="diagram-tag">WYCKOFF-SPRING</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l03_double_bottom_spring.svg -->
  </div>
</div>

- **[初次探底阻击]**：底 1 发生后迎来超跌反弹，确立中枢颈线高点。
- **[弹簧刺破假跌破]**：底 2 跌破底 1 最低点引发破位追空盘，但随即被大单承接并收出长下影线。
- **[突破确认入场]**：价格放量收复颈线确立双底反转，盈亏比往往超过 1:3。

3. 形态量化算法特征抽取流水线：
下图展示了量化系统自动从离散价格时序中提纯形态的 4 步状态过滤网：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.3：形态量化识别算法：局部极值点拓扑抽取与容差约束网</span>
    <span class="diagram-tag">ALGO-EXTRACTION</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l03_quant_feature_extraction.svg -->
  </div>
</div>

- **[极值点序列提纯]**：通过双向滑动窗口提取 5 拐点序列 $E = [e_1, e_2, e_3, e_4, e_5]$。
- **[几何拓扑逻辑校验]**：验证 $e_3 < \min(e_1, e_5)$ 且 $e_2, e_4 > \max(e_1, e_5)$。
- **[动态容差网过滤]**：剔除双肩畸变、颈线倾角过大（$|\theta| > 15^\circ$）的非标准伪形态。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：形态是供需博弈的几何残差</div>
  <div class="callout-body">
    形态本身没有任何预测未来的魔法。优秀的量化交易员只将形态视为“盈亏比极度非对称的风险收益契约”，在颈线突破时入场，止损设在右肩下方，追求至少 1:2 的数学期望。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁在形态未完成颈线收盘突破前“抢跑买入”。在右肩形成过程中提前下注，极易掉入下降中继三角形或双底破位下杀的深渊。
  </div>
</div>

【数学与几何判决模型】
$$\text{Sym}_{\text{shoulder}} = \frac{|P_{\text{LS}} - P_{\text{RS}}|}{P_{\text{LS}}} \le \epsilon_{\text{shoulder}} \quad (\epsilon \le 0.05)$$
$$\text{Prom}_{\text{head}} = \min\left(\frac{P_{\text{LS}} - P_{\text{Head}}}{P_{\text{Head}}}, \frac{P_{\text{RS}} - P_{\text{Head}}}{P_{\text{Head}}}\right) \ge \delta_{\text{prom}} \quad (\delta \ge 0.03)$$
$$\text{RRR} = \frac{P_{\text{target}} - P_{\text{entry}}}{P_{\text{entry}} - P_{\text{stop}}} = \frac{(P_{\text{neck}} + H) - C_t}{C_t - P_{\text{RS}}}$$
定义域：$P_{\text{Head}} < \min(P_{\text{LS}}, P_{\text{RS}}), \quad P_{\text{neck}} > P_{\text{LS}}, \quad C_t \ge P_{\text{neck}}$。

【思考题】
Q1: 经典头肩形态的供需力量衰竭推导：从三次尝试突破的成交量逐级递减、左肩/头/右肩的微观换手率，推导为何颈线破位后常引发量度跌幅的非线性踩踏？
Q2: 威科夫弹簧效应（Wyckoff Spring）与次底假摔猎杀：为什么在双底（W-Bottom）结构中，第二个底部略微刺穿第一个底部最低点（Spring）反而比未刺穿的平底具有更高的反弹胜率？从流动性清算与浮筹吸收的角度论述。
Q3: 形态量化算法的“几何容差”陷阱：为什么在真实市场中机械要求左右肩绝对对称（0% 误差）会导致策略几乎无法触发，而容差过大（如 > 20%）又会陷入过拟合与高假阳性（False Positive）灾难？算法如何自适应动态平衡？

【评分与通过规则】
- 代码 4 分：头肩底几何拓扑校验与颈线突破判定 (2.5分) + 目标价与盈亏比计算 (1.5分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：以拓扑几何与订单流衰竭为核心展开论述
- 通过线：8/10 分。一票否决：未突破即判定有效、盈亏比计算错误
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
    
    参数:
    points 字典必须包含 5 个关键拐点价格:
    - 'left_shoulder': 左肩低点 (float)
    - 'neckline1': 第一次反弹颈线高点 (float)
    - 'head': 头部深坑低点 (float)
    - 'neckline2': 第二次反弹颈线高点 (float)
    - 'right_shoulder': 右肩低点 (float)
    current_close: 当前候选突破 K 线收盘价 (float)
    shoulder_tolerance: 左右肩对称容差 (默认 5%)
    neckline_tolerance: 颈线倾斜容差 (默认 8%)
    min_head_prominence: 头部相对双肩的最低深陷突出度 (默认 3%)
    min_depth: 形态总高度占头部价格的最低比例 (默认 8%)
    
    返回字典:
    - 'is_valid_ihs': bool, 是否符合头肩底几何形态全部约束
    - 'breakout_confirmed': bool, 是否完成收盘价突破颈线
    - 'neckline_price': float, 颈线基准价格
    - 'pattern_height': float, 形态垂直高度
    - 'target_price': float, 理论量度目标位
    - 'risk_reward_ratio': float, 突破入场盈亏比 (若未突破或止损异常返回 0.0)
    - 'reasons': List[str], 校验未通过的具体原因描述列表
    """
    # TODO: 请实现严格的头肩底拓扑几何判定逻辑
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 03: 头肩底几何特征提取与判定器测试")
    print("=" * 60)

    # 1. 标准完美的有效头肩底样本
    # 左肩 100, 颈线1 110, 头部 92 (明显低于双肩), 颈线2 112, 右肩 102
    # 头部深陷: (100 - 92)/92 = 8.7% > 3%, (102 - 92)/92 = 10.8% > 3%
    # 双肩对称: |100 - 102| / 100 = 2% < 5%
    # 颈线倾斜: |110 - 112| / 110 = 1.8% < 8%
    # 颈线均价: 111.0, 形态高度 = 111 - 92 = 19.0 (高度占比 19/92 = 20.6% > 8%)
    # 目标位 = 111 + 19 = 130.0
    valid_points = {
        "left_shoulder": 100.0,
        "neckline1": 110.0,
        "head": 92.0,
        "neckline2": 112.0,
        "right_shoulder": 102.0
    }
    
    # 突破确认 (当前收盘价 113 > 颈线 111)
    res_valid = detect_inverse_head_and_shoulders(valid_points, current_close=113.0)
    print("有效头肩底判定结果:", res_valid)

    assert res_valid is not None, "结果不能为 None"
    assert res_valid["is_valid_ihs"] is True, "必须判定为有效头肩底"
    assert res_valid["breakout_confirmed"] is True, "必须确认完成颈线突破"
    assert abs(res_valid["neckline_price"] - 111.0) < 1e-4
    assert abs(res_valid["pattern_height"] - 19.0) < 1e-4
    assert abs(res_valid["target_price"] - 130.0) < 1e-4
    # 止损 102, 突破买入 113 -> 风险 = 113 - 102 = 11.0; 潜在收益 = 130 - 113 = 17.0
    # R/R = 17.0 / 11.0 ≈ 1.545
    assert abs(res_valid["risk_reward_ratio"] - (17.0 / 11.0)) < 1e-3

    # 2. 畸变形态测试 A: 头部不够突出 (头部 99，与双肩 100 几乎持平 -> 类似三重底而非头肩底)
    flat_head_points = {
        "left_shoulder": 100.0, "neckline1": 110.0,
        "head": 99.0,           "neckline2": 110.0,
        "right_shoulder": 100.0
    }
    res_flat = detect_inverse_head_and_shoulders(flat_head_points, current_close=112.0)
    print("头部平坦形态判定:", res_flat["is_valid_ihs"], res_flat["reasons"])
    assert res_flat["is_valid_ihs"] is False
    assert any("头部" in r for r in res_flat["reasons"])

    # 3. 畸变形态测试 B: 左右肩极其不对称 (|100 - 115| / 100 = 15% > 5%)
    asym_points = {
        "left_shoulder": 100.0, "neckline1": 120.0,
        "head": 85.0,           "neckline2": 122.0,
        "right_shoulder": 115.0
    }
    res_asym = detect_inverse_head_and_shoulders(asym_points, current_close=125.0)
    print("双肩不对称形态判定:", res_asym["is_valid_ihs"], res_asym["reasons"])
    assert res_asym["is_valid_ihs"] is False
    assert any("双肩" in r for r in res_asym["reasons"])

    print("Lesson 03 练习题测试全部通过！")
