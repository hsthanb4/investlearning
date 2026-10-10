r"""
# 模块 09：特殊事件驱动与低风险套利 · 第 2 课：可转债定价、纯债底与双低轮动策略

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

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
    # TODO: 实现转股价值、转股溢价率、纯债溢价率与双低值的向量化计算
    pass


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
    # TODO: 依据条件过滤，计算指标，并返回排序后的前 top_k 只转债
    pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么中国可转债市场特有的“向下修正转股价（下修条款）”被视为熊市中绝佳的看跌期权保护？上市公司在何种动力下会主动提议下修？

**你的答案：**
[在此处写下你的分析：需阐述下修对转股价值与转债期权内在价值的阶跃式修复，并从上市公司规避刚性还本付息兑付危机的强烈诉求分析内生动力]


### Q2：什么是可转债的“强制赎回条款（强赎）”？为什么当上市公司正式发布“提前赎回公告”后，拥有高转股溢价率的转债会遭遇踩踏式断崖暴跌？

**你的答案：**
[在此处写下你的分析：需推导强赎触发条件、面值赎回引发的巨额亏损风险，以及持有人不计成本转股或抛售导致的溢价强制归零杀跌机制]


### Q3：为什么“双低轮动策略”在长期能够取得高夏普比率与超额 Alpha？其因子背后的微观驱动力是什么？

**你的答案：**
[在此处写下你的分析：需从低价格的纯债底保护、低溢价的正股弹性，以及定期再平衡（香农恶魔）高抛低吸兑现波动率红利的机理展开]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
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

    row_a = df_metrics[df_metrics["symbol"] == "113050"].iloc[0]
    assert abs(row_a["conversion_value"] - 95.0) < 1e-4
    assert abs(row_a["premium_rate_pct"] - 13.6842) < 1e-3
    assert abs(row_a["double_low_score"] - 121.6842) < 1e-3
    assert abs(row_a["bond_floor_premium_pct"] - 5.8824) < 1e-3

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

    assert len(selected) == 2
    assert list(selected["symbol"]) == ["128030", "113050"]
    assert selected.iloc[0]["double_low_score"] < selected.iloc[1]["double_low_score"]

    print("All assertions passed! Module 09 Lesson 02 verification successful.")
