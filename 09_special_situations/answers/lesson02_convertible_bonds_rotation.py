r"""
# 模块 09：特殊事件驱动与低风险套利 · 第 2 课：可转债定价、纯债底与双低轮动策略

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握中国特色可转债（Convertible Bonds）的非对称契约条款：转股价、纯债底、向下修正条款（下修）与提前赎回条款（强赎）；
2. 深刻理解转股价值（Conversion Value）、转股溢价率（CPR）与纯债价值的数理定价模型；
3. 掌握“双低策略（Double-Low Strategy）”在牛熊周期中实现“跌有下界、涨不封顶”的因子暴露机理；
4. 编写代码实现可转债多维度指标量化计算，并设计具备信用评级过滤、强赎剔除与价格上限约束的多券动态轮动算法。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，阐述下修条款的博弈心理与强赎公告后的溢价杀跌机制。

---
## 核心心智模型与数理推导

### 1. 可转债的核心指标与数学定义

可转债面值通常为 100 元，其价值由“纯债价值（Bond Floor）”与“正股看涨期权（Call Option）”两部分复合而成：

- **转股价值（Conversion Value, CV / 平价）**：
  将一张 100 元面值的可转债按照转股价转换为股票后的市值：
  $$\text{CV} = \frac{S}{P_{\text{conv}}} \times 100$$
  其中 $S$ 为正股当前收盘价，$P_{\text{conv}}$ 为可转债当前约定的转股价格。

- **转股溢价率（Conversion Premium Rate, CPR）**：
  可转债二级市场市价相对于转股价值的溢价幅度：
  $$\text{CPR} = \frac{P_{\text{bond}} - \text{CV}}{\text{CV}} \times 100\%$$
  - 若 $\text{CPR} \approx 0\%$ 或为负：转债跟正股涨跌高度同步（偏股型，进攻性强）；
  - 若 $\text{CPR} \gg 50\%$：转债几乎不跟正股涨跌，主要受纯债底支撑（偏债型，防守性强）。

- **纯债底保护（Pure Bond Floor）**：
  假设公司不转股，按约定票息与到期赎回价折现的债券内在价值。通常在 90~110 元之间，为转债提供了几乎不可跌破的坚固防线。

- **双低指标（Double-Low Score）**：
  $$\text{DoubleLow} = P_{\text{bond}} + \text{CPR}(\%)$$
  例如：转债现价 110 元，转股溢价率为 12%，则双低值 $= 110 + 12 = 122$。
  - **低价格**（$P_{\text{bond}}$ 低）：靠近纯债底，下行空间被刚性封死；
  - **低溢价**（$\text{CPR}$ 低）：正股一旦反弹，转债能迅速享受期权 Delta 的同向收益。

### 2. 双低轮动算法逻辑 (Double-Low Rotation)

```
        ┌────────────────────────────────────────────────────────┐
        │                 全市场可转债候选标的池                  │
        └────────────────────────────┬───────────────────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │ 步骤 1：硬约束风控过滤                                 │
        │ - 剔除已发布提前强赎公告的标的 (防止溢价踩踏)           │
        │ - 剔除信用评级低于 AA- 的低资质品种 (防暴雷与违约)     │
        │ - 剔除现价高于 135 元的高价品种 (防纯债底失效)          │
        └────────────────────────────┬───────────────────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │ 步骤 2：多因子特征计算                                 │
        │ - 计算转股价值 Conversion Value                        │
        │ - 计算转股溢价率 Premium Rate (%)                      │
        │ - 计算双低值 Double Low Score = 现价 + 溢价率(%)       │
        └────────────────────────────┬───────────────────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │ 步骤 3：升序排序并构建轮动持仓                         │
        │ - 按 Double-Low Score 升序排列                         │
        │ - 选取排名前 Top-K 的优质双低转债等权持有与定期轮动    │
        └────────────────────────────────────────────────────────┘
```
"""

import pandas as pd
from typing import List, Set


def calculate_convertible_bond_metrics(bonds_df: pd.DataFrame) -> pd.DataFrame:
    """
    计算可转债核心指标矩阵：
    - conversion_value: 转股价值 = (stock_price / convert_price) * 100
    - premium_rate_pct: 转股溢价率 (%) = (cb_price - conversion_value) / conversion_value * 100
    - bond_floor_premium_pct: 纯债溢价率 (%) = (cb_price - pure_bond_value) / pure_bond_value * 100
    - double_low_score: 双低值 = cb_price + premium_rate_pct
    """
    df = bonds_df.copy()

    # 1. 转股价值
    df["conversion_value"] = (df["stock_price"] / df["convert_price"]) * 100.0

    # 2. 转股溢价率 (%)
    df["premium_rate_pct"] = ((df["cb_price"] - df["conversion_value"]) / df["conversion_value"]) * 100.0

    # 3. 纯债溢价率 (%)
    if "pure_bond_value" in df.columns:
        df["bond_floor_premium_pct"] = ((df["cb_price"] - df["pure_bond_value"]) / df["pure_bond_value"]) * 100.0

    # 4. 双低值
    df["double_low_score"] = df["cb_price"] + df["premium_rate_pct"]

    return df


def select_double_low_rotation_portfolio(
    bonds_df: pd.DataFrame,
    max_price: float = 135.0,
    valid_ratings: Set[str] = {"AAA", "AA+", "AA", "AA-"},
    top_k: int = 3
) -> pd.DataFrame:
    """
    可转债双低轮动选股算法：
    1. 过滤：
       - 排除已公告强赎的转债 (is_called == False)
       - 排除现价高于 max_price 的转债 (保底保护弱化)
       - 排除信用评级不在 valid_ratings 范围内的标的 (信用风险控制)
    2. 计算多因子特征 (调用 calculate_convertible_bond_metrics)
    3. 按 double_low_score 升序排列，提取前 top_k 只转债构建轮动组合。
    """
    # 步骤 1: 硬过滤
    cond = (
        (bonds_df["is_called"] == False) &
        (bonds_df["cb_price"] <= max_price) &
        (bonds_df["credit_rating"].isin(valid_ratings))
    )
    filtered_df = bonds_df[cond].copy()

    if filtered_df.empty:
        return pd.DataFrame()

    # 步骤 2: 计算特征
    metrics_df = calculate_convertible_bond_metrics(filtered_df)

    # 步骤 3: 排序并选取 Top-K
    sorted_df = metrics_df.sort_values(by="double_low_score", ascending=True)
    selected_portfolio = sorted_df.head(top_k).copy()

    # 格式化数值字段保留 4 位小数
    cols_to_round = ["conversion_value", "premium_rate_pct", "double_low_score"]
    for c in cols_to_round:
        if c in selected_portfolio.columns:
            selected_portfolio[c] = selected_portfolio[c].round(4)

    return selected_portfolio


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么中国可转债市场特有的“向下修正转股价（下修条款）”被视为熊市中绝佳的看跌期权保护？上市公司在何种动力下会主动提议下修？

参考答案：
1. 下修条款对转股价值的阶跃式修复：
   - 当正股大幅阴跌（如跌破转股价的 85% 持续 15 天），转股价值腰斩（如跌至 50 元），转股溢价率被动飙升至 100%，转债几乎丧失进攻性。
   - 若上市公司董事会提议并经股东大会通过下修转股价（例如将转股价从 20 元直接向下修正至当前市价 10 元）：
     转股价值瞬间从 $\frac{10}{20} \times 100 = 50$ 跃升至 $\frac{10}{10} \times 100 = 100$！
   - 转债市价瞬间被注入丰厚的内在期权价值，产生 10%~20% 的脉冲式上涨。
2. 上市公司的内生动力（消除刚性还债压力）：
   - 中国绝大多数上市公司发行可转债的本质诉求是“股权融资（延期增发）”，而非真正承担每年的刚性付息并在到期日掏出数亿甚至数十亿真金白银偿还本金；
   - 一旦转债到期未转股，公司面临巨大的流动性兑付危机；
   - 主动下修转股价能大幅降低转股门槛，促使持有人转股，从而在会计上直接将负债端清零、转入所有者权益（净资产增加），实现“不用掏钱还债”的完美结局。

### Q2：什么是可转债的“强制赎回条款（强赎）”？为什么当上市公司正式发布“提前赎回公告”后，拥有高转股溢价率的转债会遭遇踩踏式断崖暴跌？

参考答案：
1. 强赎契约触发机制：
   - 绝大多数转债约定：在转股期内，若正股收盘价连续 30 个交易日中有 15 个交易日高于转股价的 130%（即转股价值超过 130 元），公司有权按照“面值 + 当期应计利息”（通常仅 101~103 元）强制赎回未转股的债券。
2. 溢价率强制归零杀跌：
   - 假设某转债在正股暴涨刺激下，市价被资金炒作至 160 元，而实际转股价值仅为 130 元（存在高达 23% 的高溢价率）；
   - 一旦公司发布强赎公告并确定最后交易日与赎回日，所有投资者面临生死抉择：
     - 若持有到期被公司按 102 元强赎：净亏损 $(160 - 102) / 160 \approx -36.25\%$！
     - 唯一理性的选择是：在二级市场直接砸盘卖出，或者转股为股票并在二级市场抛售。
   - 无论何种选择，原本支撑在 160 元的虚高溢价会在短短数日内被强制压缩归零（市价迅速暴跌向转股价值 130 元贴合）。
   - 这就是著名的“强赎杀溢价踩踏”，因此量化双低策略严禁持有已公告强赎的标的。

### Q3：为什么“双低轮动策略”在长期能够取得高夏普比率与超额 Alpha？其因子背后的微观驱动力是什么？

参考答案：
1. 均值回归与动态再平衡红利：
   - 处于全市场双低排名第一梯队的转债，通常处于“被市场暂时冷落但正股并未死透、价格在 105~115 元附近徘徊”的防守区间。
   - 此时向下有纯债底兜底（即便正股继续跌，转债受债息支撑仅微跌）；
   - 一旦正股出现行业轮动反弹，低溢价使得转债迅速捕捉到 Delta 涨幅，价格上冲至 125~135 元；
   - 此时该转债的双低分值变大，轮动算法自动触发“止盈卖出高价转债，切换调仓至新的低价低溢价标的”。
2. 自动化“高抛低吸”的凸性收益（Shannon's Demon）：
   通过每周或每两周的机械化轮动，策略不断将“已经上涨兑现期权价值的资产”置换为“具备厚重安全垫与潜在弹性的新资产”，
   把市场的随机漫步波动转化为确定性的正向复利，完美践行了格雷厄姆“安全边际”哲学。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Convertible Bond Metrics Calculation...")
    raw_data = [
        {
            "symbol": "113050",
            "name": "A转债",
            "cb_price": 108.0,
            "stock_price": 9.5,
            "convert_price": 10.0,
            "pure_bond_value": 102.0,
            "credit_rating": "AA",
            "is_called": False
        },
        {
            "symbol": "128030",
            "name": "B转债",
            "cb_price": 115.0,
            "stock_price": 12.0,
            "convert_price": 10.0,
            "pure_bond_value": 98.0,
            "credit_rating": "AA+",
            "is_called": False
        },
        {
            "symbol": "110060",
            "name": "C转债",
            "cb_price": 142.0,
            "stock_price": 15.0,
            "convert_price": 10.0,
            "pure_bond_value": 95.0,
            "credit_rating": "AAA",
            "is_called": False
        },
        {
            "symbol": "123010",
            "name": "D转债",
            "cb_price": 105.0,
            "stock_price": 8.0,
            "convert_price": 10.0,
            "pure_bond_value": 85.0,
            "credit_rating": "BBB",
            "is_called": False
        },
        {
            "symbol": "113500",
            "name": "E转债",
            "cb_price": 125.0,
            "stock_price": 13.0,
            "convert_price": 10.0,
            "pure_bond_value": 100.0,
            "credit_rating": "AA",
            "is_called": True
        }
    ]
    df_raw = pd.DataFrame(raw_data)

    df_metrics = calculate_convertible_bond_metrics(df_raw)

    # 验证 A转债:
    # 转股价值 = 9.5 / 10.0 * 100 = 95.0
    # 转股溢价率 = (108 - 95) / 95 * 100 ≈ 13.6842%
    # 双低值 = 108.0 + 13.6842 = 121.6842
    # 纯债溢价率 = (108 - 102) / 102 * 100 ≈ 5.8824%
    row_a = df_metrics[df_metrics["symbol"] == "113050"].iloc[0]
    assert abs(row_a["conversion_value"] - 95.0) < 1e-4
    assert abs(row_a["premium_rate_pct"] - 13.6842) < 1e-3
    assert abs(row_a["double_low_score"] - 121.6842) < 1e-3
    assert abs(row_a["bond_floor_premium_pct"] - 5.8824) < 1e-3

    # 验证 B转债:
    # 转股价值 = 12.0 / 10.0 * 100 = 120.0
    # 转股溢价率 = (115 - 120) / 120 * 100 = -4.1667% (折价)
    # 双低值 = 115.0 + (-4.1667) = 110.8333
    row_b = df_metrics[df_metrics["symbol"] == "128030"].iloc[0]
    assert abs(row_b["conversion_value"] - 120.0) < 1e-4
    assert abs(row_b["premium_rate_pct"] - (-4.1667)) < 1e-3
    assert abs(row_b["double_low_score"] - 110.8333) < 1e-3

    print("[Testing] Double-Low Rotation Selection Engine...")
    selected = select_double_low_rotation_portfolio(
        df_raw,
        max_price=135.0,
        valid_ratings={"AAA", "AA+", "AA", "AA-"},
        top_k=2
    )

    # 过滤校验：
    # C转债现价 142 > 135 被过滤
    # D转债评级 BBB 低于 AA- 被过滤
    # E转债已公告强赎 (is_called==True) 被过滤
    # 合格候选池仅剩 B转债 (双低 110.8333) 与 A转债 (双低 121.6842)
    assert len(selected) == 2
    assert list(selected["symbol"]) == ["128030", "113050"]
    assert selected.iloc[0]["double_low_score"] < selected.iloc[1]["double_low_score"]

    print("All assertions passed! Module 09 Lesson 02 verification successful.")
