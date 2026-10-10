"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 3/5 课
第 3 课：经典几何形态量化：头肩底判定器与统计防伪
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 深度思考题回答完整、逻辑严谨（各 2 分）：共 6 分
- 合格线：8/10 分

【理论精讲】
1. 传统形态学（Chartism）的伪科学陷阱与量化重构：
   传统技术分析充斥着“事后诸葛亮”画线与主观幻想性视错觉（Pareidolia）。
   同一张 K 线图，十个主观交易员可以画出十条不同的颈线。
   在现代量化投资体系中，形态必须被赋予**严格无歧义的拓扑空间几何数学定义**与**因果可证伪性**。

2. 头肩底（Inverse Head and Shoulders, IHS）的几何数学模型：
   形态由 5 个按时间先后依次出现的关键摆动极值点构成：
   1) L_LS: 左肩波谷 (Left Shoulder Low)
   2) H_NL1: 颈线波峰 1 (Left Neckline High)
   3) L_Head: 头部波谷 (Head Low)
   4) H_NL2: 颈线波峰 2 (Right Neckline High)
   5) L_RS: 右肩波谷 (Right Shoulder Low)
   
   严格量化准则：
   - 头部绝对深度 (Head Prominence):
     头部必须显著低于左右两肩：L_Head < L_LS 且 L_Head < L_RS；
     深度优势比例: (L_LS - L_Head) / L_Head >= min_prominence (如 3%) 且 (L_RS - L_Head) / L_Head >= min_prominence。
   - 左右双肩对称性 (Shoulder Symmetry):
     两肩水平高度差异不能过大：|L_LS - L_RS| / L_LS <= shoulder_tolerance (如 5%)。
   - 颈线倾斜容差 (Neckline Tilt):
     两个颈线高点形成的颈线不能过于陡峭：|H_NL1 - H_NL2| / H_NL1 <= neckline_tolerance (如 8%)。
   - 形态垂直跨度 (Pattern Height):
     基准颈线价格 Neckline_Price = (H_NL1 + H_NL2) / 2
     Pattern_Height = Neckline_Price - L_Head
     最小深度要求: Pattern_Height / L_Head >= min_depth (如 8%)。
   - 突破确认与盈亏比测算 (Breakout & Risk/Reward):
     当且仅当收盘价站稳颈线上方 (Close > Neckline_Price) 时，形态触发多头突破确认。
     理论量度最小目标位 Target_Price = Neckline_Price + Pattern_Height
     标准止损位 Stop_Loss = L_RS (右肩波谷)
     风险收益比 R/R = (Target_Price - Close) / (Close - Stop_Loss)。

【三个思考题 (Q1~Q3)】
Q1: 视觉主观拟合偏差（Pareidolia / 幻想性视错觉）：为什么主观交易员肉眼看到的“完美头肩底/头肩顶”，在进行严格量化数学定义后，全市场全样本历史回测胜率往往仅在 40%~45% 左右？这揭示了技术形态分析在统计学上的哪些本质缺陷（如幸存者偏差、样本自由度过高与形态模糊性）？
Q2: 几何形态的无未来函数回测实现（Look-Ahead Bias Elimination）：在实时行情或量化回测中，右肩形成尚未突破颈线时，能不能提前左侧入场？将“形态候选检测”与“颈线实体突破确认（Breakout）”在时间戳（Timestamp）上分开，对于回测引擎的因果性契约有何决定性影响？
Q3: 假突破陷阱（Bull Trap）与假形态防御机制：头肩底颈线突破后，高达 30%~40% 的概率会演变成“假突破后反向深跌”。量化策略应如何结合“突破时成交量倍数（Volume Surge >= 1.5x~2.0x 均量）”与“回踩颈线不破（Pullback Confirmation）”来过滤假突破噪声？
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
