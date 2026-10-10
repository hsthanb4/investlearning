r"""
================================================================================
模块 10：量化回测避坑指南与实盘系统工程 · 第 3/4 课
第 3 课：现代量化数据管道：复权算法与 Point-in-Time 时序对齐校验 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：垃圾进垃圾出，数据管道纯净度是量化系统的生命中枢
“Garbage In, Garbage Out”。量化策略的生与死，70% 决定于底层数据管道（Data Pipeline）的严密性与工程纯净度。本课聚焦量化数据工程的两大核心支柱：价格除权除息（前复权/后复权）的数学连续性，与 Point-in-Time (PIT) 财报时序对齐的因果物理隔离。任何在报告期截止日（3-31）直接取用财务指标的行为，都是对实盘未来信息的神谕盗窃；任何未做复权处理的日线回测，都会把机械性分红除权误判为断崖暴跌。
:::

- **[除权参考价与累计前复权因子法]**：现金分红与送转股引发的股价跳空属于纯会计除权，必须通过单期折算因子 $f_t = P_{\text{ex}, t} / P_{\text{close}, t-1}$ 向下折算历史价格，保持最新一天的绝对价格与交易所盘口完全保真。
- **[Point-in-Time 双时间戳不可变快照]**：工业级基本面数据湖必须分离‘业务归属期（Report Period）’与‘法定披露时间戳（Publish Time）’，只允许基于 $t_{\text{publish}} \le T_{\text{decision}}$ 进行向后非等值对齐（`merge_asof`）。
- **[异常数据防御网]**：数据流接入必须经过严格的断号重排、未来时间戳检测、时间戳单调性校验以及极端负值价格拦截。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了除权除息机械跳空与累计前复权因子的折算传导机制。

```mermaid
flowchart TD
    Raw["原始未复权价格 (Raw Price)<br/>分红送股导致机械断崖跳空"] --> CalcEx["计算除权参考价: P_ex = (P_prev - D) / (1 + R_split)"]
    CalcEx --> Factor["单期折算因子: f_t = P_ex / P_prev"]
    Factor --> Accum["累计前复权因子: AdjFactor_t = Π_{k=t+1}^T f_k (最新日为 1.0)"]
    Accum --> Smooth["生成连续前复权价格: P_adj = P_raw × AdjFactor (均线指标消除假死叉)"]
```

- **[要点 1：最新价保真性]**：前复权保持最新交易日价格与实盘完全一致，使得当前生成的均线突破与止损触发价位可直接对齐交易所盘口。
- **[要点 2：指标假死叉的消除]**：若不进行前复权，10 送 10 除权会导致 5 日均线向下假破位，诱发策略错误清仓。
- **[要点 3：复权历史重写特性]**：前复权在每次新分红发生时会重写全部历史价格，因此长期 NAV 评价必须切换为后复权。

锚点指引：下图展示了 Point-in-Time (PIT) 数据湖双时序不可变快照架构。

```mermaid
flowchart LR
    A["财报披露源头: 报告期 2023-12-31 / 披露日 2024-04-20"] --> B["双时间戳存储: Valid Time (业务所属) + System Time (物理入湖)"]
    B --> C["时序快照追加: 若发生财报更正，以新版本不可变追加"]
    C --> D["AS-OF 历史切片查询: SELECT * WHERE publish_date <= T_decision"]
```

- **[要点 1：版本不可变性（Immutability）]**：对于发生差错更正的财报，严禁覆盖历史旧记录，必须以版本号（Version ID）追加存储。
- **[要点 2：非等值向后对齐（merge_asof）]**：在任意交易日 $T$，策略仅可见在此之前已依法公开披露的最新财务指标。
- **[要点 3：消灭幽灵超额（Ghost Alpha）]**：严格 PIT 对齐杜绝了在次年 1~4 月提前偷看年报净利润的神谕作弊。

【数学与估值模型】
除权参考价与单期折算因子公式：
$$
P_{\text{ex}, t} = \frac{P_{\text{close}, t-1} - D_t + P_{\text{rights}} \cdot R_{\text{rights}}}{1 + R_{\text{split}} + R_{\text{rights}}}, \quad f_t = \frac{P_{\text{ex}, t}}{P_{\text{close}, t-1}}
$$
累计前复权乘数方程（最新日 $T$ 为基准）：
$$
\text{AdjFactor}_T = 1.0, \quad \text{AdjFactor}_{\tau} = \prod_{k=\tau+1}^{T} f_k \quad (\tau < T)
$$
$$
P_{\text{adj}, \tau} = P_{\text{raw}, \tau} \times \text{AdjFactor}_{\tau}
$$
变量定义域与参数约束：
- $D_t \ge 0$：每股派发现金红利（元）；$R_{\text{split}} \ge 0$：每股送转股比例。
- $P_{\text{close}, t-1} > 0$：除权日前一日收盘价。
- $f_t \in (0, 1]$：单期折算因子。若当日无分红送转，$f_t = 1.0$。

Point-in-Time 数据可见性约束：
$$
\text{FundamentalFeature}_T = \operatorname{arg\,max}_{t_{\text{publish}} \le T} \{\text{FilingData}(t_{\text{report}}, t_{\text{publish}}, v)\}
$$

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **前复权回测长期复利的负价格荒谬性**：超长历史（如 20 年）前复权会导致早期股价被压缩至几分钱甚至负数，百分比涨跌幅严重扭曲，长期 CAGR 评估必须使用后复权。
2. **爬虫报告期主键前视陷阱**：开源数据源直接将 12-31 作为交易日主键关联财报，导致 4 个月的前视穿透，测出的价值因子全部是作弊假象。
3. **乱序行情破坏撮合因果链**：交易所 UDP 组播行情网络丢包抖动会导致接收时间与撮合时间倒挂，必须建立 Watermark 水位线重排机制。
:::

【思考题】
Q1: 为什么在做量化多因子回测与技术指标计算时必须使用“前复权（Backward Adjustment）”，而在统计长期投资组合资产净值（NAV）与复合年化收益率（CAGR）时更推荐使用“后复权（Forward Adjustment）”？
Q2: 很多开源量化库从通用财经网站爬取财务报表时，直接以“报告期（如 06-30、12-31）”作为时序主键。请说明这种做法会给中低频基本面量化策略带来几个月的“幽灵超额（Ghost Alpha）”，并在系统架构层面给出设计工业级 PIT 数据湖的元数据表结构方案。
Q3: 在高频 L2 Tick 行情数据管道中，深交所逐笔成交（Trade）与逐笔委托（Order）均带有严格单调递增的 `ApplSeqNum`（业务消息序列号），而上交所历史数据曾存在乱序广播与合并分包。面对跨交易所的网络抖动与乱序数据流，如何设计滑动窗口（Sliding Window）与水位线（Watermark）重排算法保证因果确定性？

【Q1 深度参考答案】
- **[前复权与当前盘口报价的空间保真]**：前复权将当前最新一天的复权因子固定为 1.0，历史所有价格向下平移压缩。这使得策略当前生成的均线突破价、ATR 通道与止损线绝对数值与交易所当前实时行情处于同一真实量纲，可直接用于下单与风控。
- **[前复权历史价格重写的致命缺陷]**：每当未来发生新的分红送转，历史前复权序列会被全局重写。若从 1990 年开始回测，茅台等牛股的前复权初始价会变成几毛钱甚至负数，微小的 1 分钱跳价会引发几倍的百分比畸变。
- **[后复权永久冻结历史的复利评价优势]**：后复权以最早初始日为 1.0，历史价格永久冻结不可篡改，未来除权仅向上累计放大，最适合真实反映资金池的长期真实复利增长率（CAGR 与 NAV）。

【Q2 深度参考答案】
- **[报告期主键引发的 4 个月神谕穿越]**：A 股年报与一季报法定披露截止日为次年 4 月 30 日。若以 12-31 为主键关联，相当于策略在 1 月 1 日开盘就提前掌握了全市场尚未公布的第四季度利润，而 1~4 月正是业绩暴雷与分红炒作最激烈的窗口期，产生的超额完全是未来信息泄露的伪 Alpha。
- **[Bitemporal 工业级 PIT 数据湖架构]**：
  必须设计双时间戳不可变快照表：
  `CREATE TABLE fundamental_pit ( symbol VARCHAR(12), report_period DATE, publish_time TIMESTAMP, effective_date DATE, version_id INT, eps DECIMAL(18,4), net_profit DECIMAL(18,4), PRIMARY KEY (symbol, report_period, publish_time, version_id) );`
- **[AS-OF 查询隔离机制]**：回测引擎仅基于 `publish_time <= T_decision` 关联最新生效快照，彻底物理封死时序穿越。

【Q3 深度参考答案】
- **[乱序消息对因果链的致命破坏]**：高频行情 UDP 组播在交换机拥塞或多链路合并时会发生微秒级乱序，导致物理到达时间与交易所业务生成时间错位，产生错误的盘口买卖队列推导。
- **[水位线（Watermark）与抖动缓冲区架构]**：在数据接入层设置事件时间 Jitter Buffer（如 5~10 ms 窗口）；设定 Watermark = $\max(\text{EventTime}) - \text{DelayTolerance}$；所有早于 Watermark 的乱序数据在缓冲区内按消息序号插入排序。
- **[超时断号与快照补包协议]**：当检测到序列号断号超时，触发 TCP Replay 补包机制，确保下游因子计算引擎接收到的是严格保序、无未来信息倒挂的确定性数据流。
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
    计算日线行情的精准累计前复权价格 (保持最新一天价格不变，历史价格向下折算):
    
    计算步骤:
    1. 将原始日线 market_df 与分红送转 dividend_df 按照 ['date', 'symbol'] 关联。
       缺失的分红和送股填 0.0。
    2. 按交易日期升序排序。
    3. 逐日计算单期除权因子 f_t:
       若当日无分红送转: f_t = 1.0
       若当日有分红送转:
           prev_close = P_{close, t-1}
           P_{ex, t} = (prev_close - cash_dividend) / (1.0 + split_ratio)
           f_t = P_{ex, t} / prev_close
    4. 计算累计前复权乘数 adj_factor_t:
       最后一天 T 的 adj_factor_T = 1.0
       历史任一天 t 的 adj_factor_t = f_{t+1} * f_{t+2} * ... * f_{T}
    5. 计算复权价:
       open_adj = open * adj_factor
       high_adj = high * adj_factor
       low_adj = low * adj_factor
       close_adj = close * adj_factor
    """
    df = pd.merge(raw_market_df, dividend_df, on=["date", "symbol"], how="left")
    df["cash_dividend"] = df["cash_dividend"].fillna(0.0)
    df["split_ratio"] = df["split_ratio"].fillna(0.0)
    df = df.sort_values(by="date", ascending=True).reset_index(drop=True)

    n = len(df)
    f_factors = np.ones(n)

    for t in range(1, n):
        div = df.loc[t, "cash_dividend"]
        split = df.loc[t, "split_ratio"]

        if div > 0.0 or split > 0.0:
            prev_close = df.loc[t - 1, "close"]
            p_ex = (prev_close - div) / (1.0 + split)
            f_factors[t] = p_ex / prev_close
        else:
            f_factors[t] = 1.0

    adj_factors = np.ones(n)
    for t in range(n - 2, -1, -1):
        adj_factors[t] = adj_factors[t + 1] * f_factors[t + 1]

    df["adj_factor"] = adj_factors
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
    将日线市场行情与 Point-in-Time 基本面财务数据严格对齐，杜绝因财报披露滞后导致的前视偏差。
    """
    m_df = market_df.sort_values(by="date").reset_index(drop=True)
    f_df = fundamental_pit_df.sort_values(by="publish_date").reset_index(drop=True)

    aligned = pd.merge_asof(
        m_df,
        f_df,
        by="symbol",
        left_on="date",
        right_on="publish_date",
        direction="backward"
    )

    return aligned


# ==============================================================================
# 算法 3：量化数据管道纯净度与完整性自动化质检器
# ==============================================================================

def validate_pipeline_integrity(df: pd.DataFrame) -> List[str]:
    """
    对清洗对齐后的量化数据集执行全量质检与未来信息反向扫描。
    """
    issues = []

    # 1. 检查是否存在未来泄露
    if "publish_date" in df.columns and "date" in df.columns:
        valid_pub = df.dropna(subset=["publish_date"])
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
