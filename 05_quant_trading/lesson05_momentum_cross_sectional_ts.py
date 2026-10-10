r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 5/5 课
第 5 课：横截面动量与时间序列趋势复合策略 (Dual Momentum Composite Strategy)
================================================================================

【课程定位与第一性原理】
动量效应（Momentum Effect）是现代量化金融中最为普遍且持久的经典异象之一。
动量策略在学术与工业界演化为两大核心分支：

1. 横截面动量（Cross-Sectional Momentum, CSMOM, Jegadeesh & Titman 1993）：
   - 相对强弱博弈：在股票资产池内部，按照过去收益率排序，买入表现最好的前 $K$ 只“赢家组合（Winners）”，
     卖出/剔除表现最差的“输家组合（Losers）”；
   - 行为金融学成因：分析师对企业基本面渐进消息的“反应不足（Under-reaction）”以及后续散户追涨杀跌的“过度反应（Over-reaction）”；
   - 经典“12-1 动量”准则：计算过去 12 个月收益率时，必须剔除最近 1 个月（或周频剔除最近 1 周），
     因为最近 1 个月存在强烈的短线流动性反冲与指令单失衡引起的“短期反转效应（Short-term Reversal）”。

2. 时间序列动量（Time-Series Momentum / Trend Following, TSMOM, Moskowitz, Ooi & Pedersen 2012）：
   - 绝对趋势跟踪：仅关注资产自身过去一段时间的绝对走势方向（如收盘价是否站在移动均线上方、或者过去 60 日收益率是否为正）；
   - 顺势而为：趋势向上时开多，趋势向下时平仓空仓或做空，提供下行保护与“危机 Alpha（Crisis Alpha）”。

3. 动量崩溃（Momentum Crash, Daniel & Moskowitz 2016）与双动量（Dual Momentum）复合破局：
   - 纯截面动量存在致命阿喀琉斯之踵：在极端熊市或恐慌杀跌触底后的 V 型报复性反弹中，输家资产（高财务杠杆、高 Beta、濒临违约资产）
     具有极强的“深虚值看涨期权凸性（Option-like Convexity）”，往往在几天内暴涨 50%~100%；而赢家资产（低波防御股）反弹滞后，
     导致纯截面动量发生惨烈的“动量崩溃（回撤常达 40%~60%）”；
   - 双动量复合策略：以大盘时间序列趋势（TSMOM）作为全组合的“宏观总开关”——
     大盘处于上升通道时，全力在股票池中选拔横截面领头羊（满仓 CSMOM 获取高 Alpha）；
     大盘跌破生命线均线时，果断空仓避险，彻底切断系统性大跌与动量崩溃风险。

【核心流程与心智模型】
```mermaid
flowchart TD
    Bench["基准大盘指数时序 (如沪深300 / 标普500)"] --> MA["计算时序均线: MA(P, window)"]
    Bench --> TrendCheck{"时序趋势判断: Index >= MA ?"}
    
    TrendCheck -- "否 (下行熊市/破位)" --> CashMode["宏观防御模式: 组合总仓位降为 0% (持有现金/国债)"]
    
    TrendCheck -- "是 (上升通道/多头)" --> StockPool["激活股票池截面选拔引擎"]
    StockPool --> CSMOM["计算 12-1 剔除近期反转的截面动量得分"]
    CSMOM --> TopK["排序选拔相对强弱排名前 Top K 领头羊"]
    TopK --> Alloc["满仓等权/风险平价配置 Top K 赢家资产"]
    
    Alloc --> NextPeriod["T+1 日严格执行换仓 (杜绝前视偏差)"]
    CashMode --> NextPeriod
```

【工业界实战场景与风控陷阱】
1. 震荡市中的假突破与洗盘摩擦（Whipsaw Loss）：
   在无趋势的窄幅震荡市中，大盘指数在均线上下频繁穿梭，时序过滤器容易频繁触发追涨买入与割肉空仓，
   产生摩擦损耗。工业界通常加入 ATR 波动率通道或 3%~5% 缓冲带以过滤高频假信号。
2. 股票停牌与流动性黑洞：
   动量股往往是热点题材，突发停牌会导致组合无法执行换手，必须建立替代标的与风险限额机制。
3. 因子拥挤（Factor Crowding）：
   当市场上大量量化产品集中在相同形成期的动量股时，一旦趋势逆转，多头止损踩踏将导致闪崩。

【思考题】
Q1: 为什么纯粹的截面动量多空策略在熊市触底、市场强力暴力反弹时容易发生惨烈的“动量崩溃”（Momentum Crash）？请从输家资产的期权凸性（Option-like Convexity）与空头平仓踩踏剖析其深层机制。
Q2: 为什么在经典动量因子构建中，学术界与业界普遍采用“12-1 动量”（即过去 12 个月收益率，但剔除最近 1 个月）而不是“近 12 个月完整动量”？最近 1 个月的价格行为存在什么微观市场结构效应？
Q3: 怎样利用大盘时间序列趋势（如基准指数 MA 均线）作为过滤器，构建双动量（Dual Momentum）复合轮动策略？该策略在牛市、熊市和震荡市中的行为特征分别是什么？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现带跳过期的截面动量得分计算矩阵 (1分)；
  2. 准确实现大盘时间序列趋势过滤器 (1分)；
  3. 准确实现双动量复合策略回测引擎并验证相对于纯动量的风控提升 (2分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须从期权凸性、流动性微观结构与周期环境行为特征展开；
- 通过线：8/10 分。一票否决：回测信号未滞后 1 期引入未来函数、删除断言校验。
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd


def calculate_csmom_scores(
    prices_df: pd.DataFrame,
    lookback: int = 40,
    skip_recent: int = 5,
) -> pd.DataFrame:
    """
    计算截面动量 (CSMOM) 得分矩阵：
    为消除近期流动性反转效应，计算从 t - lookback 期至 t - skip_recent 期的区间收益率：
        Score_{i, t} = (Price_{i, t - skip_recent} / Price_{i, t - lookback}) - 1.0

    参数:
        prices_df: 股票价格历史矩阵 (index: 日期, columns: 股票代码)
        lookback: 动量回看窗口长度
        skip_recent: 剔除的近期窗口长度 (如 5 天对应约 1 周短线反转过滤)

    返回:
        pd.DataFrame: 截面动量得分矩阵 (前 lookback 期为 NaN)
    """
    # TODO: 实现截面动量得分矩阵计算
    pass


def compute_market_trend_filter(
    benchmark_series: pd.Series,
    ma_window: int = 20,
) -> pd.Series:
    """
    计算大盘时间序列趋势过滤器 (TSMOM Filter)：
    - 计算基准指数的移动平均线: MA_t = rolling_mean(benchmark, ma_window)
    - 若 benchmark_t >= MA_t，市场处于多头趋势，输出 1.0；
    - 若 benchmark_t < MA_t，市场处于破位或熊市，输出 0.0。

    参数:
        benchmark_series: 基准大盘指数价格序列
        ma_window: 均线平滑窗口 (如 20 日均线)

    返回:
        pd.Series: 0.0 或 1.0 的仓位乘数序列
    """
    # TODO: 实现大盘移动平均趋势过滤器
    pass


def backtest_composite_momentum_strategy(
    stock_prices: pd.DataFrame,
    benchmark_price: pd.Series,
    top_k: int = 3,
    lookback: int = 40,
    skip_recent: int = 5,
    ma_window: int = 20,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    双动量复合轮动策略 vs 纯截面动量策略回测对比引擎：
    1. 计算截面动量得分矩阵 calculate_csmom_scores；
    2. 计算大盘时序趋势过滤器 compute_market_trend_filter；
    3. 构建持仓矩阵 (所有调仓决策必须滞后 1 期执行以防止前视未来偏差):
       - 纯截面动量 (Raw CSMOM): 每日对动量得分排名前 top_k 的股票等权配置 1/top_k；
       - 双动量复合策略 (Composite): 仅当大盘趋势为 1.0 时配置前 top_k 股票，大盘趋势为 0.0 时全仓现金 (仓位为 0)；
    4. 计算两者的收益率曲线、年化收益、年化波动、夏普比率与最大回撤。

    返回字典包含:
        - "raw_csmom_annual_return": 纯截面动量年化收益率
        - "raw_csmom_sharpe": 纯截面动量夏普比率
        - "raw_csmom_max_drawdown": 纯截面动量最大回撤 (负值)
        - "composite_annual_return": 双动量复合策略年化收益率
        - "composite_sharpe": 双动量复合策略夏普比率
        - "composite_max_drawdown": 双动量复合策略最大回撤 (负值)
        - "drawdown_reduction_pct": 复合策略相对于纯动量回撤收窄比例 ((raw_dd - comp_dd) / abs(raw_dd))
    """
    # TODO: 实现完整的策略生成、执行滞后与绩效对比引擎
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 05: 横截面动量与时间序列趋势复合策略单元测试")
    print("=" * 70)

    # 1. 构造具有“牛市 ➔ 暴跌 ➔ 修复”完整周期的仿真市场数据
    np.random.seed(42)
    n_days = 400
    dates = pd.date_range("2023-01-01", periods=n_days, freq="B")

    # 构造大盘指数：前 200 天牛市，中间 100 天深幅暴跌熊市，后 100 天底部震荡修复
    bench_ret = np.zeros(n_days)
    bench_ret[:200] = np.random.normal(0.001, 0.01, 200)
    bench_ret[200:300] = np.random.normal(-0.003, 0.02, 100)
    bench_ret[300:] = np.random.normal(0.001, 0.01, 100)
    bench_price_series = pd.Series(100.0 * np.cumprod(1.0 + bench_ret), index=dates)

    # 构造 10 只具有不同相对强弱与特质波动的个股价格面板
    n_stocks = 10
    stock_cols = [f"Stock_{i:02d}" for i in range(n_stocks)]
    stock_rets = np.zeros((n_days, n_stocks))
    for i in range(n_stocks):
        stock_rets[:, i] = bench_ret + (i - 4.5) * 0.0003 + np.random.normal(0, 0.015, n_days)
    stock_prices_df = pd.DataFrame(
        100.0 * np.cumprod(1.0 + stock_rets, axis=0),
        index=dates,
        columns=stock_cols,
    )

    # 2. 执行回测对比
    perf = backtest_composite_momentum_strategy(
        stock_prices_df,
        bench_price_series,
        top_k=3,
        lookback=40,
        skip_recent=5,
        ma_window=20,
        annual_periods=252,
    )

    print(f"纯截面动量 (Raw CSMOM)  - 年化收益: {perf['raw_csmom_annual_return']*100:.2f}%, 夏普: {perf['raw_csmom_sharpe']:.2f}, 最大回撤: {perf['raw_csmom_max_drawdown']*100:.2f}%")
    print(f"双动量复合 (Composite)  - 年化收益: {perf['composite_annual_return']*100:.2f}%, 夏普: {perf['composite_sharpe']:.2f}, 最大回撤: {perf['composite_max_drawdown']*100:.2f}%")
    print(f"最大回撤收窄比例: {perf['drawdown_reduction_pct']*100:.2f}%")

    # 3. 断言验证复合策略的风控优势
    assert perf["composite_annual_return"] > 0.15, "复合策略年化收益率应大于 15%"
    assert perf["composite_sharpe"] > perf["raw_csmom_sharpe"], "复合策略夏普比率应显著超越纯截面动量"
    assert perf["composite_max_drawdown"] > perf["raw_csmom_max_drawdown"], "复合策略最大回撤应显著小于纯动量"
    # 回撤收窄幅度应超过 30%
    assert perf["drawdown_reduction_pct"] > 0.30, f"回撤收窄比例应大于 30%, 实际: {perf['drawdown_reduction_pct']*100:.2f}%"

    print("Lesson 05 单元测试全部通过！")
