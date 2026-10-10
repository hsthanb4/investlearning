r"""
================================================================================
模块 05：量化投资多因子与统计套利 · 第 5/5 课
第 5 课：截面动量 (CSMOM) 与时间序列动量 (TSMOM)：崩盘机制与波动率过滤 (参考答案版)
================================================================================

【Q1 深度参考答案】
截面动量（CSMOM）与时间序列动量（TSMOM）的源泉与构造差异：请从投资组合净敞口（Dollar Exposure）、Alpha 来源（相对排名溢价 vs 宏观趋势危机 Alpha）对比两种动量范式。为什么 TSMOM 在历次宏观金融危机中能展现强大的非线性正向对冲收益？
- **[敞口结构与约束维度的根本差异]**：截面动量（CSMOM，Jegadeesh & Titman）强制要求在每一时间切片上，多头头寸与空头头寸金额完全相等（Net Dollar Neutral = 0）。它剥离了全市场的宏观 Beta，仅押注“相对优胜劣汰”。而时间序列动量（TSMOM，Moskowitz et al.）完全打破了截面约束，对每只资产仅依据其自身的历史时间序列（如过去 12 个月累计回报）独立下注：上涨则做多，下跌则做空。因此 TSMOM 的组合净敞口（Net Beta）是随市场宏观趋势自由浮动的。
- **[危机 Alpha（Crisis Alpha）的非线性看跌期权保护]**：在宏观暴跌与系统性熊市中（如 2008 年次贷危机、2000 年互联网泡沫破裂），全市场所有资产都在单边下挫。CSMOM 此时由于必须强制持有 100% 相对抗跌的多头仓位，多头腿依然会遭受惨重亏损；而 TSMOM 凭借严格的时序绝对趋势规则，在熊市初期就会全面将所有大类资产翻空（净做空股票、做多国债与黄金）。在漫长的主跌浪中，空头头寸产生巨额正现金流，使得 TSMOM 呈现出类似“免费长期实值看跌期权”的非对称收益。
- **[投资组合层面的全天候互补性]**：CSMOM 在慢牛和宽幅震荡的常态市场中选股超额显著，而 TSMOM 在极端单边牛市与极端单边熊市中提供强大的长波趋势跟踪与危机对冲。量化资产管理机构通常将两者等风险权重混合配置。

【Q2 深度参考答案】
动量崩盘（Momentum Crash）的期权特征与物理机制：Barroso & Santa-Clara (2015) 发现动量策略呈现显著的负偏度（Negative Skewness）与极端左尾崩盘风险。为什么在熊市触底、市场狂暴反弹阶段，做多前期赢家、做空前期输家的纯动量头寸会遭遇高达 50%~70% 的毁灭性单边回撤？从做空低价垃圾股的隐含空头看涨期权（Short Call Option）结构推导。
- **[做空低价困境股的隐含空头看涨期权（Short Call）物理剖析]**：在经历过漫长深幅熊市后，前期跌幅最惨烈的败者组合（Losers）通常股价极低（如变成几美元的仙股）、资产负债率爆表、濒临破产边缘。根据默顿（Merton 1974）结构化信用风险模型，高负债困境企业的股权本质是企业总资产价值上的欧式看涨期权（Call Option），行权价为债务面值。在熊市底部，该期权处于深度虚值（Deep OTM），其期权 Delta 极小，但其隐含 Gamma 极其惊人。
- **[反转时刻的 Gamma 凸性核爆]**：当宏观经济见底、央行启动天量降息与流动性救市时，极度折价的垃圾股破产概率骤降，深度虚值看涨期权瞬间被拉入平值甚至实值。其股价会发生不可思议的脉冲式暴涨（经常在数周内暴涨 200%~500%）。此时做空该组合的动量基金，其空头头寸承担着无上限的负 Gamma 亏损，面临毁灭性的轧空（Short Squeeze）。
- **[多头赢家组的弹性钝化与崩盘兑现]**：与此同时，前期表现最好的赢家组合（Winners）在熊市期间通常是业绩稳定、估值偏高的防御性抱团资产（如公用事业、高分红必选消费）。当市场风险偏好全面逆转为 Risk-On 时，资金疯狂撤离防御股、涌入弹性垃圾股，赢家组合严重滞涨甚至遭遇获利抛售。多头微幅盈利（+15%）完全无法阻挡空头翻倍暴亏（-200%），导致纯动量策略发生历史上惨绝人寰的动量崩盘（如 1932 年两个月内暴跌 91%，2009 年三至五月暴跌 74%）。

【Q3 深度参考答案】
目标波动率自适应缩放（Volatility Targeting）：为什么在动量策略中强制引入基于已实现波动率的动态仓位倒数加权 $w_t \propto 1/\hat{\sigma}_t$，不仅没有降低长期年化复合收益率，反而将历史最大回撤削减了 40% 以上并大幅提升了收益的右偏度？
- **[波动率风险溢价与动量风险的非对称脱节]**：动量策略的超额收益本质来自于资产相对价格强弱的记忆惯性，而非来自于承担无谓的高波动率。实证研究证明，动量策略的夏普比率在低波动率与中等波动率体制下最高，而在极端高波动率市场环境下（如 VIX > 30），市场噪声完全主导了趋势，动量策略的期望夏普直接转为负值。
- **[波动率聚集（Volatility Clustering）提供的提前避险时间窗口]**：动量崩盘并非发生在毫无征兆的晴朗天空下，而是 100% 发生在市场波动率已经持续飙升数周之后。通过使用短期滚动窗口（如 20 日已实现波动率 $\hat{\sigma}_t$）动态监控，当市场进入风暴区时，分母中的波动率急剧膨胀，算法自动将杠杆 $w_t$ 快速从 1.0 压缩至 0.2 甚至 0.1。
- **[几何平均复利的数学胜利]**：虽然在危机期间缩减杠杆使策略在反弹初期少赚了少许头寸收益，但它完全规避掉了单笔损失高达 60% 的灾难性本金腰斩。根据几何复合收益率公式 $g \approx \mu - \frac{1}{2}\sigma^2$，将下行方差 $\sigma^2$ 压减一半所带来的几何复利增益，远远超越了放弃部分微小收益的代价。策略不仅将历史最大回撤由 -50% 牢牢锁死在 -20% 以内，而且将夏普比率提升逾 50%，实现了量化工程上完美的风险收益非对称优化。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：驾驭动量之剑，严守波动率之盾</div>
  <div class="callout-body">
    动量崩盘是所有不加风控约束的动量模型的宿命。只有将大盘宏观体制滤网与目标波动率倒数缩放作为底层强制执行的物理熔断器，动量策略才能真正从学术纸面模型蜕变为长期穿透牛熊的机构级旗舰资产。
  </div>
</div>
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
