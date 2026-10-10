"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 4/5 课
参考实现与标准问答解析
第 4 课：动量指标向量化推导、自适应波动率通道与无前视偏差信号生成
================================================================================
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


def calculate_wilder_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    向量化计算经典怀尔德 (Wilder) 平滑相对强弱指标 RSI (0 ~ 100)
    """
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)

    # 怀尔德平滑等价于 alpha = 1 / period 的指数移动平均 (adjust=False)
    alpha = 1.0 / period
    avg_gain = gain.ewm(alpha=alpha, adjust=False).mean()
    avg_loss = loss.ewm(alpha=alpha, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi = rsi.fillna(100.0)  # 若无任何损失，RSI 封顶 100.0

    return rsi


def calculate_adaptive_bollinger_bands(
    df: pd.DataFrame,
    period: int = 20,
    num_std: float = 2.0
) -> pd.DataFrame:
    """
    计算布林带 (Bollinger Bands) 轨道与自适应波动率特征指标
    """
    res = df.copy()

    middle = res["close"].rolling(window=period).mean()
    rolling_std = res["close"].rolling(window=period).std(ddof=0)

    upper = middle + num_std * rolling_std
    lower = middle - num_std * rolling_std
    bandwidth = (upper - lower) / middle
    pct_b = (res["close"] - lower) / (upper - lower).replace(0.0, np.nan)

    res["bb_middle"] = middle
    res["bb_upper"] = upper
    res["bb_lower"] = lower
    res["bb_bandwidth"] = bandwidth
    res["bb_pct_b"] = pct_b

    return res


def generate_signals_no_lookahead(
    df: pd.DataFrame,
    rsi_oversold: float = 30.0,
    rsi_overbought: float = 70.0
) -> pd.DataFrame:
    """
    构建均值回归交易信号，并实施严格的无前视偏差因果对齐 (Shift-1)
    """
    res = df.copy()
    raw_signal = pd.Series(0, index=res.index, dtype=int)

    # 均值回归触发条件
    buy_cond = (res["rsi"] < rsi_oversold) & (res["bb_pct_b"] < 0.0)
    sell_cond = (res["rsi"] > rsi_overbought) & (res["bb_pct_b"] > 1.0)

    raw_signal[buy_cond] = 1
    raw_signal[sell_cond] = -1

    res["raw_signal"] = raw_signal
    # 严格滞后一期撮合执行，彻底消除当日收盘前视偏差
    res["position"] = raw_signal.shift(1).fillna(0).astype(int)

    return res


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 04 参考实现与测试")
    print("=" * 60)

    # 1. 验证 RSI 计算
    sample_prices = pd.Series([
        100.0, 102.0, 101.5, 103.0, 105.0, 104.2, 106.5, 108.0, 107.5, 109.0,
        111.0, 110.5, 112.0, 114.0, 113.5, 115.0, 117.0, 116.5, 118.0, 120.0,
        119.0, 117.5, 115.0, 113.0, 111.5, 108.0, 105.0, 103.0, 101.0, 99.0
    ])

    rsi_series = calculate_wilder_rsi(sample_prices, period=14)
    print("前20期 RSI 计算样本:\n", rsi_series.tail(10))

    assert len(rsi_series) == len(sample_prices)
    assert rsi_series.iloc[19] > 60.0
    assert rsi_series.iloc[-1] < 40.0

    # 2. 验证布林带与自适应波动率计算
    df_sample = pd.DataFrame({"close": sample_prices})
    bb_df = calculate_adaptive_bollinger_bands(df_sample, period=10, num_std=2.0)
    print("布林带计算样本 (最后5行):\n", bb_df[["close", "bb_middle", "bb_upper", "bb_lower", "bb_bandwidth", "bb_pct_b"]].tail())

    assert "bb_middle" in bb_df.columns
    assert "bb_bandwidth" in bb_df.columns
    assert "bb_pct_b" in bb_df.columns
    valid_idx = bb_df["bb_middle"].dropna().index[-1]
    assert abs((bb_df.loc[valid_idx, "bb_upper"] - bb_df.loc[valid_idx, "bb_middle"]) -
               (bb_df.loc[valid_idx, "bb_middle"] - bb_df.loc[valid_idx, "bb_lower"])) < 1e-5

    # 3. 验证无前视偏差信号生成
    bb_df["rsi"] = rsi_series
    sig_df = generate_signals_no_lookahead(bb_df, rsi_oversold=35.0, rsi_overbought=65.0)
    print("信号生成结果 (末尾行):\n", sig_df[["close", "rsi", "bb_pct_b", "raw_signal", "position"]].tail())

    for t in range(1, len(sig_df)):
        assert sig_df.loc[t, "position"] == sig_df.loc[t - 1, "raw_signal"]

    print("Lesson 04 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：滤波相位滞后、无趋势震荡的摩擦损耗、体制过滤机制）：
1. 震荡市中均线失效的物理机制：
   - 移动平均线（MA）的本质是趋势跟踪，依赖资产价格具备显著的自相关性与动量延续性；
   - 当市场进入无趋势的均值回归震荡区间时，自相关系数归零或为负。此时价格围绕某一中枢来回穿梭；
   - 每次价格冲高，短期均线向上金叉长期均线，诱导多头在区间上沿高位追入；随后价格迅速反转向下，均线死叉触发止损割肉，如此往复数十次，策略净值遭受致命的“磨损千刀割”（Death by a Thousand Cuts）。
2. 量化基金的防御体制过滤器：
   - ADX（平均趋向指标）过滤：计算 ADX 值，当 ADX < 20 时，判定市场处于无趋势弱震荡状态，强制关闭所有均线突破策略，转入休眠或网格做市模式；
   - 波动率带宽过滤：当布林带宽度低于阈值时，禁止追随趋势性穿越信号。

Q2 标准解析（得分要点：波动率聚集与均值回归、波动率挤压后暴利突破、防假突破过滤）：
1. 波动率挤压（Squeeze）的金融学机理：
   - 曼德博指出市场呈现“低波动与高波动交替聚集”的幂律特征；
   - 当布林带宽度 BandWidth 缩减至历史极低分位（如 5% 分位数）时，说明多空双方在极窄的筹码区间内充分换手达到极度脆弱的微观平衡；
   - 这种蓄势意味着任何微小的外部增量资金或宏观催化剂都会打破平衡，引发单边单向爆发行情（弹簧被压到极致后的释放）。
2. 防假突破被洗出的执行纪律：
   - 绝不在挤压区间内部盲目猜方向左侧下单；
   - 等待带宽开始重新由最小拐点放大（BandWidth 扩张）且伴随成交量翻倍放大（Volume Expansion）；
   - 要求突破 K 线实体彻底完全收在布林外轨之外（%B > 1.0 或 %B < 0.0），并结合 ATR 追踪止损，若收回中轨则果断砍仓。

Q3 标准解析（得分要点：前视偏差/未来函数的致命性、向量化回测契约与因果性）：
1. Same-bar 收盘价撮合的实盘致命后果：
   - 算法逻辑：“如果今日收盘价 Close_t 跌破下轨且 RSI < 30，则以今日收盘价 Close_t 买入”；
   - 实盘灾难：在交易所实盘撮合中，当你知道 Close_t 的精确数字时，当天的交易窗口已经彻底关闭（15:00 集合竞价结束），你根本不可能穿越时空回到 15:00 前以 Close_t 挂单成交！
   - 如果回测引擎直接用 Close_t 撮合，回测收益曲线将异常平滑暴利（夏普比率可虚高至 4.0 以上），但一上线实盘就立即遭遇巨额滑点、买不进或卖不出，净值断崖崩塌。
2. 架构防范标准：
   - 在特征工程与信号生成后，必须强制执行 `position = raw_signal.shift(1)`；
   - 明确定义策略收益计算公式：`Strategy_Return[t] = Position[t] * Asset_Return[t]`，确保 t 时刻的持仓严格只由 t-1 时刻及以前的信息决定，恪守严格的时间因果律。
""")
