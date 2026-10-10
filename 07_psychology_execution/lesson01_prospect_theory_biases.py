"""
================================================================================
模块 07：行为金融学、交易心理与执行纪律 · 第 1/4 课
第 1 课：前景理论与处置效应 (Disposition Effect) 量化度量
================================================================================
【理论精讲】
Kahneman & Tversky (1979) 前景理论核心发现：
1. 损失厌恶（Loss Aversion）：亏损 1000 元带来的痛苦，约为获得 1000 元带来的快乐的 2~2.5 倍！
2. S 型价值函数：在盈利区厌恶风险（急于套现锁定利润），在亏损区追求风险（死扛甚至加仓摊平成本）。
Odean (1998) 处置效应量化指标：
- PGR (Proportion of Gains Realized) = 已实现盈利交易数 / (已实现盈利数 + 账面盈利未卖数)
- PLR (Proportion of Losses Realized) = 已实现亏损交易数 / (已实现亏损数 + 账面亏损未卖数)
散户典型特征：PGR 显著大于 PLR（“卖出牛股、抱紧烂股”）。

【思考题】
Q1: 为什么散户在买入股票被套 10% 时不愿止损，而在被套 50% 时反而彻底“躺平”不再看盘？请用心理账户与前景理论解释。
Q2: 沉没成本谬误（Sunk Cost Fallacy）如何诱导交易者在已经证明逻辑破产的交易中继续追加保证金？
Q3: 怎样利用程序化强制止损单（Stop-Loss Order）完全剥夺人类交易员在危急时刻的决策犹豫？
"""

def calculate_disposition_effect(pgr: float, plr: float) -> float:
    """
    计算处置效应偏离度:
    DE = PGR - PLR
    若 DE > 0，表明存在显著的“急于卖赢家、死抱输家”处置效应偏差
    """
    # TODO: 实现处置效应计算
    pass

if __name__ == "__main__":
    assert calculate_disposition_effect(0.65, 0.25) == 0.40
    print("Lesson 01 (Disposition Effect) Exercise Passed!")
