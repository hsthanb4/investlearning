r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 5/5 课
第 5 课：横截面动量与时间序列趋势复合策略 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么纯粹的截面动量多空策略在熊市触底、市场强力暴力反弹时容易发生惨烈的“动量崩溃”（Momentum Crash）？请从输家资产的期权凸性（Option-like Convexity）与空头平仓踩踏剖析其深层机制：
- **输家资产的期权凸性（Option-like Convexity of Losers）**：
  根据 Daniel & Moskowitz (2016) 的经典实证研究，在深度熊市或流动性恐慌杀跌的末期，跌幅最大的“输家组合”（Losers）通常是由高财务杠杆、面临债务违约危机或陷入严重经营困境的股票组成。
  根据 Merton 结构化企业信用定价模型，濒临破产企业的股权本质上是**深度虚值的看涨期权（Deep Out-of-the-Money Call Option）**。
  一旦宏观流动性反转或政策强力救市（如 2009 年 3 月全球金融危机见底、2020 年 4 月全球流动性天量宽松），这些困境企业的破产概率急剧下降，其股权展现出极高的凸性，会在极短的几天内发生报复性暴涨（涨幅可达 100%~300%）。
- **赢家资产的防御性滞后与空头逼空踩踏（Short Squeeze）**：
  1. 在熊市中表现相对坚挺的“赢家组合”（Winners）往往是公用事业、高分红、必须消费等防守型资产。在市场风险偏好（Risk-On）极速爆发时，市场增量流动性迅速抽离防守板块以追逐高弹性困境资产，导致赢家股票涨幅极小甚至出现逆势补跌；
  2. 纯截面动量策略在空头端持有巨额的 Losers 空头头寸。当输家资产暴涨时，空头保证金迅速告急，策略被强制以市价止损买入平仓，引发连锁式“空头踩踏逼空（Short Squeeze）”；
  3. 多头端不涨甚至补跌，空头端遭遇数倍暴涨，多空组合净值在短短几周内即可遭遇 40%~60% 的灾难性回撤，彻底抹平过去数年积累的所有超额收益。

【Q2 深度参考答案】
为什么在经典动量因子构建中，学术界与业界普遍采用“12-1 动量”（即过去 12 个月收益率，但剔除最近 1 个月）而不是“近 12 个月完整动量”？最近 1 个月的价格行为存在什么微观市场结构效应？
- **短周期反转与中周期动量的周期分离**：
  大量实证资产定价文献（Jegadeesh 1990; Lehmann 1990）揭示：股票收益率在 1 周至 1 个月的时间尺度上呈现极强的**短期负自相关性（反转效应）**，而在 3~12 个月的中期时间尺度上才展现出持续的**正自相关性（动量效应）**。
- **微观流动性反冲与指令单失衡（Microstructure Noise & Bid-Ask Bounce）**：
  1. **流动性补偿机制**：当某只股票在最近几天遭遇机构集中增持或散户情绪性冲动买入时，由于短期限价订单薄（LOB）厚度有限，买单会迅速吃穿卖盘档位，导致成交价暂时被推升至公允价值上方（产生短线流动性溢价）；在随后数日内，做市商与套利资本回补挂单，价格必然向微观均衡点反冲回落（Bid-Ask Bounce）；
  2. **机构月末调仓效应（Rebalancing Pressure）**：大型公募基金与养老金在月末或季度末具有严格的行业与个股仓位上限约束。当某只股票当月暴涨时，机构必须在月末被动卖出部分持仓以维持风险平价或指数跟踪基准，给前期暴涨股票带来确定性的短期抛压。
- **因子纯度保障**：
  若在动量因子中包含最近 1 个月，强烈的短线反转效应将直接冲销掉中期动量的统计预测力，导致因子的 Rank IC 和 ICIR 发生显著衰减。因此，工业界必须剔除最近 1 个月（或日频因子剔除最近 5~10 天），提取纯净的中期趋势 Alpha。

【Q3 深度参考答案】
怎样利用大盘时间序列趋势（如基准指数 MA 均线）作为过滤器，构建双动量（Dual Momentum）复合轮动策略？该策略在牛市、熊市和震荡市中的行为特征分别是什么？
- **双动量（Dual Momentum, Gary Antonacci）复合架构机制**：
  1. **外层时间序列宏观过滤器（TSMOM Gate）**：跟踪基准宽基指数（如标普500、沪深300）。若指数价格高于其 20 日/60 日移动均线（或过去 60 日区间收益为正），系统判定宏观处于上升多头通道，激活股票仓位（仓位权重 = 1.0）；反之若跌破均线，判定为系统性风险释放期，强制总仓位降为 0.0（持有现金或隔夜无风险货币工具）；
  2. **内层截面相对强弱引擎（CSMOM Engine）**：在总开关开启时，在股票池中根据 $12 - 1$ 动量排序，等权或风险加权持有相对排名最强的 Top K 只领头羊。
- **不同市场周期下的系统行为特征**：
  1. **牛市（Bull Market）**：大盘指数稳步运行在均线上方，时序过滤器全程保持 100% 满仓状态。截面动量算法全力捕捉处于主升浪的领涨龙头，享受动量 Alpha 带来的高进攻弹性，净值大幅领跑基准；
  2. **单边大熊市（Bear Market）**：大盘破位后，时序过滤器在下跌初期（通常大盘回撤 3%~5% 处）立即果断空仓避险，完全规避后续深不见底的系统性阴跌与暴跌主跌浪（如 2008 年次贷危机、2015 年 A 股去杠杆下挫），策略净值走平防御，并彻底免疫了熊市底部的“动量崩溃”；
  3. **震荡市（Sideways Market）**：大盘在均线附近反复穿梭拉锯，时序过滤器容易遭遇“假突破”诱多和“跌破割肉”的洗盘磨损（Whipsaw Loss）；但由于截面选股依然能在局部结构性行情中提供 Alpha 缓冲，整体策略在全周期仍能实现更低的最大回撤与显著更高的夏普比率。
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
    Score_{i, t} = (Price_{i, t - skip_recent} / Price_{i, t - lookback}) - 1.0
    """
    p_num = prices_df.shift(skip_recent)
    p_den = prices_df.shift(lookback)
    return (p_num / p_den) - 1.0


def compute_market_trend_filter(
    benchmark_series: pd.Series,
    ma_window: int = 20,
) -> pd.Series:
    """
    计算大盘时间序列趋势过滤器 (TSMOM Filter)
    """
    ma = benchmark_series.rolling(window=ma_window).mean()
    return (benchmark_series >= ma).astype(float)


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
    双动量复合轮动策略 vs 纯截面动量策略回测对比引擎
    """
    dates = stock_prices.index
    n_days = len(dates)
    stock_cols = stock_prices.columns

    # 1. 动量得分矩阵与大盘趋势过滤器
    csmom_scores = calculate_csmom_scores(stock_prices, lookback=lookback, skip_recent=skip_recent)
    ts_filter = compute_market_trend_filter(benchmark_price, ma_window=ma_window)

    raw_pos = pd.DataFrame(0.0, index=dates, columns=stock_cols)
    comp_pos = pd.DataFrame(0.0, index=dates, columns=stock_cols)

    # 2. 生成每日调仓目标权重
    warmup = max(lookback, ma_window)
    for t in range(warmup, n_days):
        d = dates[t]
        scores = csmom_scores.loc[d].dropna()
        if len(scores) < top_k:
            continue

        top_stocks = scores.nlargest(top_k).index
        w_each = 1.0 / float(top_k)

        # 纯截面动量持仓
        raw_pos.loc[d, top_stocks] = w_each

        # 复合动量持仓 (受大盘趋势总开关调控)
        if ts_filter.loc[d] == 1.0:
            comp_pos.loc[d, top_stocks] = w_each

    # 3. 严格滞后 1 期执行以防止前视偏差
    raw_pos_exec = raw_pos.shift(1).fillna(0.0)
    comp_pos_exec = comp_pos.shift(1).fillna(0.0)

    # 4. 计算每日策略收益率
    stock_returns = stock_prices.pct_change().fillna(0.0)
    raw_daily_rets = (raw_pos_exec * stock_returns).sum(axis=1)
    comp_daily_rets = (comp_pos_exec * stock_returns).sum(axis=1)

    # 截取预热期之后的有效样本进行统计
    raw_eval_rets = raw_daily_rets.iloc[warmup:]
    comp_eval_rets = comp_daily_rets.iloc[warmup:]

    def _eval_metrics(r: pd.Series) -> Tuple[float, float, float, float]:
        cum = (1.0 + r).cumprod()
        total = float(cum.iloc[-1] - 1.0)
        ann_r = float(r.mean() * annual_periods)
        ann_v = float(r.std(ddof=1) * np.sqrt(annual_periods))
        sharpe = float(ann_r / ann_v) if ann_v > 1e-12 else 0.0
        roll_m = cum.cummax()
        dd = (cum - roll_m) / roll_m
        mdd = float(dd.min())
        return ann_r, ann_v, sharpe, mdd

    raw_ann, raw_vol, raw_sharpe, raw_mdd = _eval_metrics(raw_eval_rets)
    comp_ann, comp_vol, comp_sharpe, comp_mdd = _eval_metrics(comp_eval_rets)

    drawdown_reduction = float((comp_mdd - raw_mdd) / abs(raw_mdd)) if abs(raw_mdd) > 1e-12 else 0.0

    return {
        "raw_csmom_annual_return": raw_ann,
        "raw_csmom_sharpe": raw_sharpe,
        "raw_csmom_max_drawdown": raw_mdd,
        "composite_annual_return": comp_ann,
        "composite_sharpe": comp_sharpe,
        "composite_max_drawdown": comp_mdd,
        "drawdown_reduction_pct": drawdown_reduction,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 05: 横截面动量与时间序列趋势复合策略单元测试 (参考答案版)")
    print("=" * 70)

    np.random.seed(42)
    n_days = 400
    dates = pd.date_range("2023-01-01", periods=n_days, freq="B")

    bench_ret = np.zeros(n_days)
    bench_ret[:200] = np.random.normal(0.001, 0.01, 200)
    bench_ret[200:300] = np.random.normal(-0.003, 0.02, 100)
    bench_ret[300:] = np.random.normal(0.001, 0.01, 100)
    bench_price_series = pd.Series(100.0 * np.cumprod(1.0 + bench_ret), index=dates)

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

    assert perf["composite_annual_return"] > 0.15, "复合策略年化收益率应大于 15%"
    assert perf["composite_sharpe"] > perf["raw_csmom_sharpe"], "复合策略夏普比率应显著超越纯截面动量"
    assert perf["composite_max_drawdown"] > perf["raw_csmom_max_drawdown"], "复合策略最大回撤应显著小于纯动量"
    assert perf["drawdown_reduction_pct"] > 0.30, f"回撤收窄比例应大于 30%, 实际: {perf['drawdown_reduction_pct']*100:.2f}%"

    print("Lesson 05 参考答案单元测试全部通过 (Exit Code 0)！")
