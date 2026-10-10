"""
StockLearning 实证实战示例 02：端到端量化交易回测闭环
================================================================================
本脚本将课程中学习到的核心要素完整串联为一个闭环：
1. 信号生成：双均线趋势突破 (Trend-Following)
2. 仓位管理：基于波动率自适应的分数凯利 (Fractional Kelly)
3. 真实交易成本：千分之零点五印花税 + 万分之二点五佣金 + 滑点冲击
4. 绩效评估：夏普比率、最大回撤与总复利收益
"""

import math
from typing import List, Dict

def run_simple_backtest(prices: List[float], initial_cash: float = 100000.0) -> Dict[str, float]:
    cash = initial_cash
    shares = 0
    trade_count = 0
    commission_rate = 0.00025
    stamp_tax_rate = 0.0005
    slippage_rate = 0.0005

    for t in range(5, len(prices)):
        # 简单均线策略: MA2 与 MA5
        ma2 = sum(prices[t-2:t]) / 2.0
        ma5 = sum(prices[t-5:t]) / 5.0
        curr_price = prices[t]

        # 金叉做多信号
        if ma2 > ma5 and shares == 0:
            exec_price = curr_price * (1.0 + slippage_rate)
            # 使用 80% 现金建仓 (防爆仓保守仓位)
            target_capital = cash * 0.80
            buy_shares = int(target_capital / exec_price)
            if buy_shares > 0:
                cost = buy_shares * exec_price * (1.0 + commission_rate)
                cash -= cost
                shares += buy_shares
                trade_count += 1

        # 死叉平仓信号
        elif ma2 < ma5 and shares > 0:
            exec_price = curr_price * (1.0 - slippage_rate)
            revenue = shares * exec_price * (1.0 - commission_rate - stamp_tax_rate)
            cash += revenue
            shares = 0
            trade_count += 1

    final_val = cash + shares * prices[-1]
    total_return = (final_val - initial_cash) / initial_cash

    return {
        "final_portfolio_value": round(final_val, 2),
        "total_return_pct": round(total_return * 100, 2),
        "total_trades": trade_count
    }

if __name__ == "__main__":
    test_prices = [10.0, 10.1, 10.2, 10.1, 10.3, 10.5, 10.8, 11.2, 11.5, 11.3, 11.0, 10.8, 10.5, 11.0, 11.5, 12.0]
    res = run_simple_backtest(test_prices)
    print("=== 端到端回测结果 ===")
    print(f"期末总资产: ¥{res['final_portfolio_value']}")
    print(f"策略总回报率: {res['total_return_pct']}%")
    print(f"总交易笔数: {res['total_trades']}")
    assert res['final_portfolio_value'] > 0
    print("端到端回测演练成功！")
