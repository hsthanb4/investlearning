r"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 5/5 课
第 5 课：相对估值模型矩阵与倍数法评估 (Relative Valuation & Multiples Matrix)
================================================================================

::: {.callout-note}
### 投决会相对估值公理：乘数是增长率、风险溢价与资产回报率的压缩表象
- **[一价定律相对映射]**：相对估值依托“一价定律（Law of One Price）”，通过可比资产的市场交易价格来推导目标资产的相对价值。
- **[核心估值乘数矩阵与数理纽带]**：
  - **PE (市盈率)**：适用于盈利平稳、资本结构相似的成熟消费与蓝筹；
  - **PB-ROE 纽带方程**：$\frac{P}{B} = \frac{\text{ROE} - g}{K_e - g}$。高 ROE 企业理应享有高 PB 溢价；
  - **PS (市销率)**：适用于高增长尚未盈利的创新药（Biotech）或 SaaS；
  - **EV/EBITDA**：剔除了资本结构（负债差异）与折旧摊销政策干扰，跨国并购的标准工具；
  - **PEG**：$\text{PEG} = \frac{\text{PE}}{g_{\%} \times 100}$，彼得·林奇 GARP 策略准则（PEG < 1.0 低估）。
:::

- **[企业价值 EV 与估值乘数计算模型]**：

$$
\text{EV} = \text{Market Cap} + \text{Total Debt} - \text{Cash}, \quad \text{EV/EBITDA} = \frac{\text{EV}}{\text{EBITDA}}
$$

- **[横截面偏离度与价值陷阱（Value Trap）防御打分引擎]**：
  - 在细分行业内计算 PE 相对标准分 Z-Score，并引入 ROIC 质量门槛过滤：

$$
Z_{\text{PE}} = \frac{\text{PE}_i - \mu_{\text{Industry}}}{\sigma_{\text{Industry}}}
$$

$$
\text{Score} = \text{clip}\left(50.0 - 20.0 \cdot Z_{\text{PE}} + 30.0 \cdot (\text{ROIC} - 0.10), 0.0, 100.0\right)
$$

- **[变量定义域与参数映射]**：
  - 若单纯 PE 极低（$Z_{\text{PE}} < -1.5$）但企业 $\text{ROIC} < 0.05$（质次充饥），惩罚项将抵消低估分，有效剔除价值陷阱。

- **[引导句锚点 1]**：各大类估值乘数的行业适用性决策树如下架构所示：

```mermaid
flowchart TD
    AssetType{"目标公司商业模式特质 ?"}
    AssetType -->|盈利稳定 / 消费蓝筹| PE["P/E 市盈率 (GARP 策略配合 PEG < 1.0)"]
    AssetType -->|重资产制造 / 银行金融| PB["P/B 市净率 (必须结合 PB-ROE 框架)"]
    AssetType -->|强周期大宗 / 航运生猪| NormalizedPE["周期归一化利润 / 重置成本 (警惕周期顶峰低PE陷阱)"]
    AssetType -->|SaaS / 生物医药高增长未盈利| PS["P/S 市销率 / 40 法则 (Rule of 40)"]
    AssetType -->|重组并购 / 高杠杆基建| EVEBITDA["EV/EBITDA 倍数 (资本结构中性)"]
```

- **[架构要点拆解 1]**：
  - **[1. 盈利可预测性]**：PE 仅适用于未来 3 年净利润具有高确定性的企业；对于暴利后随之巨亏的周期品，静态 PE 具有致命误导性。
  - **[2. 资产有形性]**：银行与重资产以净资产为基石，通过 PB 结合不良率与 ROIC 评估安全垫。
  - **[3. 资本结构中性]**：EV/EBITDA 衡量整个企业经营性资产的现金产出，适合负债率差异极大的重工业对比。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[强周期股低市盈率陷阱]**：周期品（航运、钢铁、生猪养殖）在景气顶峰利润爆表时，PE 往往只有 2~3 倍，看似极度低估实为历史大顶；在全行业巨亏出清时 PE 畸高或为负数，反而是周期大底。
- **[质次价廉价值陷阱]**：低市净率（PB < 0.5）通常反映了市场对未确认坏账或资产减值的悲观折价，缺乏 ROIC 支撑的低估值往往是长期阴跌的死水。
:::

【思考题】
Q1: 周期股“估值反转之谜”：为什么周期股（如航运中远海控、生猪养殖牧原股份、钢铁水泥）在市盈率极低（PE=2~3倍）时往往是股价周期的历史大顶，而在全行业巨亏导致 PE 畸高或为负数时反而是绝佳买点？买方机构在不同周期阶段应选用哪种估值框架（PB-ROE、重置成本或周期归一化盈利 Normalized Earnings）？
Q2: 银行与金融机构的“破净”常态：国内多数大中型商业银行长期处于 0.4~0.6 倍 PB 的深度折价状态。从财务与风险定价角度，这种低 PB 是否意味着估值严重低估？市场折价究竟反映了对银行“真实资产质量/不良贷款确认延后”以及“净息差（NIM）收窄与资本补充压力”的何种悲观预期？
Q3: 相对估值的横截面陷阱（Cross-sectional Trap）：“便宜的股票往往有便宜的理由（Value Trap）”。如何在量化相对估值模型中有效剔除“价值陷阱”？请结合 ROIC、利息保障倍数与盈利下修动量（Earnings Revisions）说明防御机制。

【评分与通过规则】
- 代码 4 分：
  1. 准确实现多维估值乘数家族计算 (2分)；
  2. 准确输出横截面均值回归评分与价值陷阱过滤 (2分)；
- Q1~Q3 问答题各 2 分（共 6 分）：深入阐明相对估值适用边界与周期品反转逻辑；
- 通过线：8/10 分。一票否决：周期股估值逻辑颠倒、价值陷阱未过滤、删除断言。
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


def calculate_valuation_multiples(
    market_cap: float,
    net_income: float,
    book_equity: float,
    revenue: float,
    ebitda: float,
    total_debt: float,
    cash: float,
    earnings_growth_rate: float
) -> Dict[str, float]:
    """
    计算目标公司的基础相对估值乘数家族
    
    参数:
    market_cap: 股权总市值 (亿元)
    net_income: 当期归母净利润 (亿元)
    book_equity: 归母所有者权益 (亿元)
    revenue: 营业收入 (亿元)
    ebitda: 息税折旧摊销前利润 (亿元)
    total_debt: 有息负债总额 (亿元)
    cash: 货币资金及等价物 (亿元)
    earnings_growth_rate: 预期长期盈利增速 (如 0.20 代表 20%)
    
    返回字典:
    - pe: 市盈率 (P/E)
    - pb: 市净率 (P/B)
    - ps: 市销率 (P/S)
    - ev: 企业价值 (EV = MarketCap + TotalDebt - Cash)
    - ev_ebitda: EV/EBITDA 倍数
    - peg: PEG 乘数 (PE / (earnings_growth_rate * 100))
    """
    # TODO: 请实现基础估值乘数的严谨计算
    pass


def cross_sectional_valuation_scoring(
    peer_df: pd.DataFrame,
    target_ticker: str
) -> Dict[str, Any]:
    """
    行业横截面相对估值偏离度计算与均值回归评分引擎
    
    参数 peer_df 包含同行业所有标的列:
    - 'ticker': 股票代码 (str)
    - 'pe': 动态市盈率 (float)
    - 'pb': 市净率 (float)
    - 'ev_ebitda': EV/EBITDA 倍数 (float)
    - 'roe': 净资产收益率 (float，例如 0.18)
    - 'debt_to_equity': 产权比率 (负债/净资产，例如 0.6)
    
    算法步骤:
    1. 计算行业横截面中位数与均值、标准差；
    2. 计算目标标的在 PE、PB、EV_EBITDA 上的 Z-Score:
       Z = (x - mean) / std
       综合估值偏离度 val_z = 0.4 * z_pe + 0.3 * z_pb + 0.3 * z_ev_ebitda (越低越便宜)
    3. 质量门槛 (Quality Filter):
       若 target_roe >= 行业中位数 且 target_debt_to_equity <= 行业中位数，判定为高质量企业 (quality_pass = True)
    4. 均值回归打分 (0 ~ 100 分):
       - 基准分 50 分；
       - 估值偏离惩罚/奖励: - val_z * 20 (即比行业均值低 1 个标准差加 20 分，高 1 个标准差扣 20 分)；
       - 若 quality_pass 为 True，奖励加 15 分；若未通过质量门槛，惩罚扣 15 分；
       - 分数裁剪在 [0, 100] 区间。
    """
    # TODO: 请实现横截面偏离度与评分逻辑
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 05: 相对估值乘数体系与行业均值回归评分测试")
    print("=" * 60)

    # 1. 基础估值乘数计算测试
    # 市值 1000 亿, 净利润 50 亿, 净资产 500 亿, 营收 800 亿, EBITDA 120 亿, 负债 300 亿, 现金 100 亿, 盈利增速 25%
    mults = calculate_valuation_multiples(
        market_cap=1000.0,
        net_income=50.0,
        book_equity=500.0,
        revenue=800.0,
        ebitda=120.0,
        total_debt=300.0,
        cash=100.0,
        earnings_growth_rate=0.25
    )
    print("估值乘数计算结果:", mults)

    assert mults is not None, "结果不能为 None"
    # PE = 1000 / 50 = 20.0
    assert abs(mults["pe"] - 20.0) < 1e-4
    # PB = 1000 / 500 = 2.0
    assert abs(mults["pb"] - 2.0) < 1e-4
    # PS = 1000 / 800 = 1.25
    assert abs(mults["ps"] - 1.25) < 1e-4
    # EV = 1000 + 300 - 100 = 1200.0
    assert abs(mults["ev"] - 1200.0) < 1e-4
    # EV/EBITDA = 1200 / 120 = 10.0
    assert abs(mults["ev_ebitda"] - 10.0) < 1e-4
    # PEG = 20.0 / (0.25 * 100) = 20.0 / 25.0 = 0.8
    assert abs(mults["peg"] - 0.8) < 1e-4

    # 2. 行业横截面估值偏离与均值回归评分测试
    # 模拟行业 5 家可比公司数据
    peer_data = pd.DataFrame([
        {"ticker": "000001", "pe": 25.0, "pb": 3.0, "ev_ebitda": 14.0, "roe": 0.12, "debt_to_equity": 0.8},
        {"ticker": "000002", "pe": 20.0, "pb": 2.5, "ev_ebitda": 11.0, "roe": 0.15, "debt_to_equity": 0.5},
        {"ticker": "000003", "pe": 15.0, "pb": 1.8, "ev_ebitda": 8.0,  "roe": 0.18, "debt_to_equity": 0.4}, # 优质低估标的
        {"ticker": "000004", "pe": 30.0, "pb": 4.0, "ev_ebitda": 16.0, "roe": 0.14, "debt_to_equity": 0.9},
        {"ticker": "000005", "pe": 12.0, "pb": 1.2, "ev_ebitda": 6.0,  "roe": 0.05, "debt_to_equity": 1.5}, # 劣质价值陷阱标的
    ])

    score_03 = cross_sectional_valuation_scoring(peer_data, "000003")
    print("标的 000003 (优质低估) 评分结果:", score_03)

    assert score_03["composite_valuation_z"] < 0, "000003 估值应低于行业均值"
    assert score_03["quality_pass"] is True, "000003 必须通过质量过滤"
    assert score_03["reversion_score"] >= 75.0, "优质低估标的均值回归得分应高于 75 分"

    score_05 = cross_sectional_valuation_scoring(peer_data, "000005")
    print("标的 000005 (价值陷阱) 评分结果:", score_05)
    assert score_05["quality_pass"] is False, "000005 质次高杠杆，不应通过质量过滤"
    assert score_05["reversion_score"] < score_03["reversion_score"]

    print("Lesson 05 练习题测试全部通过！")
