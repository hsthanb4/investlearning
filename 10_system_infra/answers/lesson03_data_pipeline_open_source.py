"""
================================================================================
模块 10：量化回测引擎避坑指南与实盘系统工程 · 第 3/4 课
第 3 课：现代量化数据管道：复权算法与 Point-in-Time 时序对齐校验【参考实现】
================================================================================
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd


# ==============================================================================
# 算法 1：工业级累计前复权因子算法 (Backward Adjustment)
# ==============================================================================

def compute_backward_adjusted_prices(
    raw_market_df: pd.DataFrame,
    dividend_df: pd.DataFrame
) -> pd.DataFrame:
    """
    计算日线行情的精准累计前复权价格 (保持最新一天价格不变，历史价格向下折算)
    """
    df = raw_market_df.sort_values("date").copy().reset_index(drop=True)
    df = pd.merge(
        df,
        dividend_df[["date", "symbol", "cash_dividend", "split_ratio"]],
        on=["date", "symbol"],
        how="left"
    )
    df["cash_dividend"] = df["cash_dividend"].fillna(0.0)
    df["split_ratio"] = df["split_ratio"].fillna(0.0)

    n = len(df)
    factors = [1.0] * n
    for i in range(1, n):
        div = df.loc[i, "cash_dividend"]
        split = df.loc[i, "split_ratio"]
        if div > 0.0 or split > 0.0:
            prev_close = df.loc[i - 1, "close"]
            ex_price = (prev_close - div) / (1.0 + split)
            factors[i] = ex_price / prev_close
        else:
            factors[i] = 1.0

    # 累计倒推相乘: adj_factor_t = product_{k=t+1}^{N-1} f_k
    cum_backward = [1.0] * n
    running_prod = 1.0
    for i in range(n - 1, -1, -1):
        cum_backward[i] = running_prod
        running_prod *= factors[i]

    df["adj_factor"] = cum_backward
    df["open_adj"] = df["open"] * df["adj_factor"]
    df["high_adj"] = df["high"] * df["adj_factor"]
    df["low_adj"] = df["low"] * df["adj_factor"]
    df["close_adj"] = df["close"] * df["adj_factor"]

    return df


# ==============================================================================
# 算法 2：Point-in-Time (PIT) 财报时序对齐管道
# ==============================================================================

def align_point_in_time_data(
    market_df: pd.DataFrame,
    fundamental_pit_df: pd.DataFrame
) -> pd.DataFrame:
    """
    将日线市场行情与 Point-in-Time 基本面财务数据严格对齐，杜绝因财报披露滞后导致的前视偏差
    """
    m = market_df.sort_values("date").copy()
    p = fundamental_pit_df.sort_values("publish_date").copy()

    aligned = pd.merge_asof(
        m,
        p,
        left_on="date",
        right_on="publish_date",
        by="symbol",
        direction="backward"
    )
    return aligned


# ==============================================================================
# 算法 3：时序数据管道完整性与时间戳防篡改校验器
# ==============================================================================

def validate_pipeline_integrity(df: pd.DataFrame) -> List[str]:
    """
    静态校验清洗对齐后的量化数据集，排查 3 类致命时序数据污染
    """
    issues = []

    # 1. 未来披露泄露
    if "publish_date" in df.columns and "date" in df.columns:
        valid_pub = df.dropna(subset=["publish_date", "date"])
        if (valid_pub["publish_date"] > valid_pub["date"]).any():
            issues.append("LEAK_FUTURE_PUBLISH_DATE")

    # 2. 时间戳乱序
    if "date" in df.columns:
        for symbol, grp in df.groupby("symbol"):
            if not grp["date"].is_monotonic_increasing:
                issues.append("OUT_OF_ORDER_TIMESTAMP")
                break

    # 3. 负值异常
    for col in ["open", "high", "low", "close", "volume", "adj_factor"]:
        if col in df.columns:
            if (df[col] < 0).any():
                issues.append("INVALID_NEGATIVE_DATA")
                break

    return issues


# ==============================================================================
# 自动化测试与参考答案解析
# ==============================================================================

if __name__ == "__main__":
    print("正在运行 10_system_infra / Lesson 03 参考实现断言验证...")

    # 测试 1: 累计前复权因子法与价格连续性校验
    dates = pd.date_range("2024-01-01", periods=5, freq="D")
    market_raw = pd.DataFrame({
        "date": dates,
        "symbol": "600000.SH",
        "open": [10.0, 10.2, 5.2, 5.3, 5.5],
        "high": [10.5, 10.6, 5.5, 5.6, 5.8],
        "low": [9.8, 10.0, 5.0, 5.1, 5.3],
        "close": [10.2, 10.4, 5.3, 5.4, 5.6],
        "volume": [1000, 1200, 2400, 2200, 2500]
    })

    div_records = pd.DataFrame({
        "date": [pd.Timestamp("2024-01-03")],
        "symbol": ["600000.SH"],
        "cash_dividend": [0.40],
        "split_ratio": [1.0]
    })

    adj_df = compute_backward_adjusted_prices(market_raw, div_records)
    assert adj_df is not None and len(adj_df) == 5
    assert abs(adj_df.iloc[-1]["close_adj"] - 5.6) < 1e-4
    assert abs(adj_df.iloc[-1]["adj_factor"] - 1.0) < 1e-4
    assert abs(adj_df.iloc[1]["close_adj"] - 5.00) < 1e-4
    adj_ret = adj_df.iloc[2]["close_adj"] / adj_df.iloc[1]["close_adj"] - 1.0
    assert abs(adj_ret - 0.06) < 1e-4

    # 测试 2: PIT 财报对齐
    m_dates = pd.date_range("2024-03-25", periods=8, freq="D")
    market_sample = pd.DataFrame({
        "date": m_dates,
        "symbol": "600000.SH",
        "close": [10.0 + i * 0.1 for i in range(8)]
    })

    pit_sample = pd.DataFrame({
        "symbol": ["600000.SH"],
        "report_date": [pd.Timestamp("2023-12-31")],
        "publish_date": [pd.Timestamp("2024-03-29")],
        "eps": [1.25],
        "net_profit_cr": [280.0]
    })

    aligned_df = align_point_in_time_data(market_sample, pit_sample)
    assert aligned_df is not None and len(aligned_df) == 8
    pre_publish = aligned_df[aligned_df["date"] < pd.Timestamp("2024-03-29")]
    assert pre_publish["eps"].isna().all()
    post_publish = aligned_df[aligned_df["date"] >= pd.Timestamp("2024-03-29")]
    assert (post_publish["eps"] == 1.25).all()

    # 测试 3: 脏数据校验
    dirty_pipeline_data = pd.DataFrame({
        "date": [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-02"), pd.Timestamp("2024-01-01")],
        "symbol": ["600000.SH", "600000.SH", "600000.SH"],
        "close": [10.0, -9.5, 10.2],
        "publish_date": [pd.Timestamp("2024-01-05"), pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-01")]
    })

    issues = validate_pipeline_integrity(dirty_pipeline_data)
    assert "LEAK_FUTURE_PUBLISH_DATE" in issues
    assert "OUT_OF_ORDER_TIMESTAMP" in issues
    assert "INVALID_NEGATIVE_DATA" in issues

    print("Lesson 03 参考实现全部断言通过 (Exit Code 0)！\n")

    print("=" * 80)
    print("【思考题标准答案深度解析 (Q1 ~ Q3)】")
    print("=" * 80)
    print("Q1 解析:")
    print("  (1) 为什么因子计算与技术分析必须用'前复权（Backward Adjustment）'：")
    print("      前复权以当前最新一日价格为基准（复权因子为 1.0），历史价格向下平移压缩。这使得最新生成的信号价位与实盘当前市价")
    print("      在同一绝对量纲下，所有基于绝对价位（如当前价格突破 MA20、ATR 通道、ATR 止损点数）的风控指令可以直接映射到当前交易所盘口。")
    print("  (2) 为什么长期 NAV 和 CAGR 建议用'后复权（Forward Adjustment）'：")
    print("      前复权存在一个严重副作用：每当未来发生新的除权除息时，历史的所有前复权价格序列会被整体重写（向下压缩）。如果一个策略从")
    print("      1990 年开始回测，茅台的前复权初始价格会变成几毛钱甚至负数，不仅失去经济学意义，还会导致早期微小的价格跳动产生夸张的")
    print("      百分比畸变。后复权以历史上最早一天为基准 1.0，历史价格永久冻结不可变，未来发生的除权仅向上累计放大，最适合评估资金复利净值曲线。")
    print("-" * 80)
    print("Q2 解析:")
    print("  (1) 幽灵超额产生机制：")
    print("      中国上市公司年报披露截止日为次年 4 月 30 日，一季报同为 4 月 30 日，半年报为 8 月 31 日，三季报为 10 月 31 日。")
    print("      若以 report_date（如 12-31）为对齐主键，则在 1 月 1 日至 4 月底整整 4 个月的时间里，策略使用了全市场所有公司尚未发布的")
    print("      真实净利润与 ROE。在现实中，这 4 个月正是年报暴雷或业绩超预期博弈最激烈的窗口期，回测相当于开启了'预知财报底牌'的神谕，")
    print("      测出来的所谓'价值投资 Alpha'完全是未来信息泄露的假象。")
    print("  (2) 工业级 PIT 数据湖表结构设计：")
    print("      必须设计为双时间戳不可变快照表（Bitemporal Architecture）：")
    print("      CREATE TABLE fundamental_pit (")
    print("          symbol VARCHAR(12),")
    print("          report_period DATE,       -- 报告期 (如 2023-12-31)")
    print("          publish_time TIMESTAMP,   -- 交易所官方公告实际披露时间戳 (如 2024-03-29 18:30:00)")
    print("          effective_date DATE,      -- 次日开盘生效日 (如 2024-04-01)")
    print("          version_id INT,           -- 财报修订版本号 (应对后续业绩修正公告)")
    print("          net_profit DECIMAL(18,4),")
    print("          PRIMARY KEY (symbol, report_period, publish_time, version_id)")
    print("      );")
    print("-" * 80)
    print("Q3 解析:")
    print("  (1) 交易所时钟与网络乱序痛点：")
    print("      深交所行情网关采用统一排队序列号（`ApplSeqNum`），严格保序；而各券商托管机房分发多路行情组播时，UDP 协议可能会因为交换机")
    print("      拥塞出现丢包重传或微秒级乱序，导致 $t_{arrive}$ 与 $t_{exchange}$ 不一致。")
    print("  (2) 水位线（Watermark）与滑动窗口重排算法：")
    print("      在数据摄取接入层（Ingestion Layer）设置基于微秒优先级的事件时间缓冲队列（Jitter Buffer，例如 5~10 ms 窗口）；")
    print("      设定 Watermark = max(EventTime) - DelayTolerance；所有早于 Watermark 的乱序数据直接在缓冲区内按 ApplSeqNum 插入排序；")
    print("      当序列号断号超时后，触发快照补包机制（TCP Replay），确保送入因子计算引擎的数据流具备绝对因果确定性。")
    print("=" * 80)
