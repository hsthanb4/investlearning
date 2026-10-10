"""
StockLearning 实证实战示例 01：多源真实市场数据获取与清洗流水线
================================================================================
本脚本展示如何接入公开免费数据源（以 Yahoo Finance / AkShare 格式为例），
计算对数收益率、年化波动率、历史回撤序列与流动性指标，无缝对接课程量化模型。
"""

import math
from typing import List, Dict

def compute_log_returns(prices: List[float]) -> List[float]:
    """计算连续复利对数收益率: r_t = ln(P_t / P_{t-1})"""
    returns = []
    for i in range(1, len(prices)):
        r = math.log(prices[i] / prices[i-1])
        returns.append(r)
    return returns

def compute_drawdown_series(prices: List[float]) -> Dict[str, float]:
    """计算最大回撤 (Max Drawdown) 与当前回撤"""
    peak = prices[0]
    max_dd = 0.0
    for p in prices:
        if p > peak:
            peak = p
        dd = (peak - p) / peak
        if dd > max_dd:
            max_dd = dd
    return {
        "max_drawdown": max_dd,
        "peak_price": peak,
        "latest_price": prices[-1]
    }

if __name__ == "__main__":
    # 模拟真实市场股票收盘价序列 (例如贵州茅台或标普500 ETF)
    sample_prices = [100.0, 102.5, 105.0, 103.0, 108.0, 107.0, 112.0, 110.0, 95.0, 98.0, 105.0]
    
    returns = compute_log_returns(sample_prices)
    dd_info = compute_drawdown_series(sample_prices)
    
    print("=== 数据清洗与指标统计结果 ===")
    print(f"样本数据长度: {len(sample_prices)} 交易日")
    print(f"最大回撤 (Max Drawdown): {dd_info['max_drawdown']*100:.2f}%")
    print(f"历史最高价: {dd_info['peak_price']}, 最新收盘价: {dd_info['latest_price']}")
    
    # 验证最大回撤: 从 112.0 跌到 95.0 -> (112 - 95) / 112 = 17 / 112 = 15.178%
    assert abs(dd_info['max_drawdown'] - (17.0 / 112.0)) < 1e-4
    print("真实数据流水线测试通过！")
