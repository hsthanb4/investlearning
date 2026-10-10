r"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 2/5 课
第 2 课：真实盈利质量审查与 Beneish M-Score 排雷模型 (Forensic Accounting & Beneish M-Score)
================================================================================

::: {.callout-note}
### 投决会排雷哲学：业务逻辑有印证，资产质量显端倪，应计粉饰看现金
- **[法务会计第一性原理]**：权责发生制赋予了管理层在收入确认时点、费用资本化、资产减值准备与公允价值重估上的巨大自由裁量权。当企业面临再融资契约、大股东股权质押或业绩对赌压力时，极易产生利润操纵动机。
- **[Beneish 教授的 Probit 检验体系]**：Messod Beneish (1999) 基于离散选择模型构建的 M-Score 是华尔街最经典的财务舞弊预警系统（曾成功在安然暴雷前一年精准确诊其欺诈行为）。模型通过 8 个维度的非财务勾稽指数综合评估上市公司粉饰财务报表的概率。
:::

- **[Beneish M-Score 八变量概率模型数学方程]**：

$$
M = -4.84 + 0.920 \cdot \text{DSRI} + 0.528 \cdot \text{GMI} + 0.404 \cdot \text{AQI} + 0.892 \cdot \text{SGI} + 0.115 \cdot \text{DEPI} - 0.172 \cdot \text{SGAI} + 4.037 \cdot \text{TATA} + 0.0327 \cdot \text{LVGI}
$$

- **[八大分项指数定义与经济学逻辑]**：
  - **[1. DSRI (应收账款指数)]**：$\text{DSRI} = \frac{\text{Receivables}_t / \text{Sales}_t}{\text{Receivables}_{t-1} / \text{Sales}_{t-1}}$。DSRI > 1 意味着应收账款增速超越营收，提示激进确认收入或提前塞货。
  - **[2. GMI (毛利率恶化指数)]**：$\text{GMI} = \frac{\text{Margin}_{t-1}}{\text{Margin}_t}$。当毛利率恶化时 GMI > 1，企业面临强烈的利润粉饰动机。
  - **[3. AQI (资产质量恶化指数)]**：衡量非硬资产比例增加，捕捉研发费用违规资本化与商誉膨胀。
  - **[4. SGI (营收增长指数)]**：高成长企业增长失速时财务造假概率最高。
  - **[5. DEPI (折旧放缓指数)]**：$\text{DEPI} > 1$ 提示企业人为延长折旧年限以少提折旧虚增当期利润。
  - **[6. SGAI (期间费用指数)]**：监控销售及管理费用失调。
  - **[7. LVGI (杠杆跳升指数)]**：负债率攀升增加违约破产风险。
  - **[8. TATA (总应计项比率)]**：$\text{TATA} = \frac{\text{Net Income}_t - \text{CFO}_t}{\text{Total Assets}_t}$。核心盈余质量指标，权重高达 +4.037。

- **[判别准则与阈值界限]**：
  - 基准阈值：$M_{\text{threshold}} = -1.78$。
  - 若 $M > -1.78$（如 $-1.49, -0.80$）：模型判定该企业存在极高的财务造假概率（High Probability of Manipulation）。
  - 若 $M \le -1.78$（如 $-2.20, -2.80$）：模型判定为低风险正常企业。

- **[引导句锚点 1]**：如下架构拓扑所示，Beneish M-Score 八大财务操纵监控雷达覆盖了企业会计的所有粉饰路径：

```mermaid
flowchart TD
    RawFinance["三张财务报表连续两期原始数据"] --> EightPillars["Beneish 八大指数计算引擎"]
    EightPillars --> DSRI["DSRI: 应收账款异常超跑 (激进塞货) [+]"]
    EightPillars --> GMI["GMI: 毛利率真实恶化 (造假动机) [+]"]
    EightPillars --> AQI["AQI: 资产劣质化/无形资产暴增 [+]"]
    EightPillars --> TATA["TATA: 核心应计项缺乏现金支撑 (+4.037 权重) [+]"]
    EightPillars --> Others["SGI + DEPI + SGAI + LVGI (成长放缓与杠杆)"]
    DSRI --> MScoreCalc["加权线性方程求解 M-Score"]
    GMI --> MScoreCalc
    AQI --> MScoreCalc
    TATA --> MScoreCalc
    Others --> MScoreCalc
    MScoreCalc --> ThresholdCheck{"M-Score > -1.78 ?"}
    ThresholdCheck -->|是| FraudAlert["高舞弊概率预警 ➔ 机构坚决一票否决清仓"]
    ThresholdCheck -->|否| CleanPass["财务质量正常稳健 ➔ 通过基本面排雷初筛"]
```

- **[架构要点拆解 1]**：
  - **[1. 应计项权重绝对压倒]**：TATA 的回归系数（4.037）是所有变量中最高的，表明现金流与净利润的背离是财务操纵的决定性证据。
  - **[2. 跨表自洽验证]**：资产负债表资产质量恶化（AQI）与利润表折旧放缓（DEPI）相互印证，彻底揭开资本化包装的面具。
  - **[3. 概率判别稳定性]**：经过 30 年全球股票市场实证检验，M-Score 在提前识别重大财务舞弊上保持极高命中率。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[存贷双高典型地雷]**：账面躺着数十亿货币资金，却同时借入数十亿高息短期借款并承担数亿利息支出（康美药业、康得新典型特征）。所谓百亿存款通常属于受限质押或虚假流水造假。
- **[存货与毛利率逆势背离]**：存货周转天数大幅攀升（产品严重积压滞销），而账面毛利率却反常走高。这通常指向企业通过少结转营业成本、将生产成本违规囤积在存货资产中的恶劣操纵。
:::

【思考题】
Q1: 为什么许多 A 股与海外造假公司（如康美药业、康得新）都呈现出“大存大贷”（账面躺着几十亿现金，却同时借入数十亿高息短期借款并承担数亿利息支出）的反常特征？作为法务会计与买方量化研究员，你应设计哪些跨表比率指标来自动化捕捉这种造假嫌疑？
Q2: 研发支出“资本化” vs “费用化”的主观裁量权如何被管理层用来粉饰当期财务报表？在 Beneish M-Score 模型中主要体现在哪个指数（AQI）？在分析现金流量表时，研发支出资本化如何人为美化经营现金流（CFO）而转嫁到投资现金流（CFI）？
Q3: 许多造假企业为了配平虚增的营业收入和净利润，通常在资产端做大“存货”或“固定资产在建工程”。如何通过“存货周转天数异常逆势攀升 + 毛利率逆势反常走高”这一经典背离形态，识破其“少结转营业成本虚增当期毛利”的财务操纵手法？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现 Beneish M-Score 八变量计算 (2.5分)；
  2. 准确输出舞弊概率判定与阈值状态 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：深入剖析法务会计因果链与微观造假操纵手段；
- 通过线：8/10 分。一票否决：M-Score 系数错误、判定阈值符号颠倒、删除断言。
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


def calculate_beneish_mscore(prior_data: Dict[str, float], curr_data: Dict[str, float]) -> Dict[str, Any]:
    """
    计算完整的 Beneish M-Score 八变量指标与财务舞弊判别
    
    参数字典包含键:
    - sales: 营业收入
    - cogs: 营业成本
    - receivables: 应收账款
    - current_assets: 流动资产
    - ppe_net: 固定资产净额
    - total_assets: 资产总计
    - depreciation: 当期折旧与摊销
    - sga: 销售与管理费用
    - total_debt: 包含流动负债与长期负债的总负债
    - net_income: 净利润
    - cfo: 经营活动现金流量净额
    
    返回字典:
    - dsri, gmi, aqi, sgi, depi, sgai, lvgi, tata: 各分项指数
    - m_score: 最终加权 Beneish M-Score 得分
    - is_manipulation_suspect: 是否疑似财务操纵 (bool, 阈值 -1.78)
    """
    # TODO: 请实现完整的 Beneish M-Score 八维指标与加权求和
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 02: 财务造假识别与 Beneish M-Score 评分器测试")
    print("=" * 60)

    # 1. 正常守法合规企业样本 (Firm A)
    firm_a_prior = {
        "sales": 1000.0, "cogs": 600.0, "receivables": 100.0,
        "current_assets": 500.0, "ppe_net": 400.0, "total_assets": 1200.0,
        "depreciation": 40.0, "sga": 150.0, "total_debt": 400.0,
        "net_income": 120.0, "cfo": 130.0
    }
    firm_a_curr = {
        "sales": 1100.0, "cogs": 660.0, "receivables": 110.0,
        "current_assets": 550.0, "ppe_net": 420.0, "total_assets": 1300.0,
        "depreciation": 45.0, "sga": 165.0, "total_debt": 420.0,
        "net_income": 135.0, "cfo": 140.0
    }

    res_a = calculate_beneish_mscore(firm_a_prior, firm_a_curr)
    print("Firm A (正常公司) M-Score 结果:", res_a["m_score"], "疑似造假:", res_a["is_manipulation_suspect"])

    assert res_a is not None, "返回结果不能为 None"
    # DSRI = (110/1100) / (100/1000) = 0.10 / 0.10 = 1.0
    assert abs(res_a["dsri"] - 1.0) < 1e-4
    # GMI: prior GM = 400/1000 = 0.40, curr GM = 440/1100 = 0.40, GMI = 1.0
    assert abs(res_a["gmi"] - 1.0) < 1e-4
    # SGI: 1100 / 1000 = 1.10
    assert abs(res_a["sgi"] - 1.10) < 1e-4
    # TATA: (135 - 140) / 1300 = -5 / 1300 ≈ -0.003846
    assert abs(res_a["tata"] - (-5.0 / 1300.0)) < 1e-4
    # Firm A 应为低风险公司，M-score 远低于 -1.78
    assert res_a["m_score"] < -1.78
    assert res_a["is_manipulation_suspect"] is False

    # 2. 激进财务操纵企业样本 (Firm B: 虚增应收、毛利恶化但做账掩盖、折旧放缓、利润缺乏现金)
    firm_b_prior = {
        "sales": 1000.0, "cogs": 600.0, "receivables": 100.0,
        "current_assets": 500.0, "ppe_net": 400.0, "total_assets": 1200.0,
        "depreciation": 50.0, "sga": 150.0, "total_debt": 400.0,
        "net_income": 100.0, "cfo": 90.0
    }
    firm_b_curr = {
        "sales": 1500.0, "cogs": 1050.0, "receivables": 350.0, # 营收增50%, 应收增250%!
        "current_assets": 800.0, "ppe_net": 350.0, "total_assets": 1600.0,
        "depreciation": 20.0, "sga": 200.0, "total_debt": 800.0, # 折旧大幅放缓, 负债激增
        "net_income": 220.0, "cfo": -30.0                        # 利润大涨, 经营现金流却暴跌为负
    }

    res_b = calculate_beneish_mscore(firm_b_prior, firm_b_curr)
    print("Firm B (操纵嫌疑公司) M-Score 结果:", res_b["m_score"], "疑似造假:", res_b["is_manipulation_suspect"])

    # DSRI = (350/1500) / (100/1000) = 0.23333 / 0.10 = 2.3333
    assert abs(res_b["dsri"] - (350.0/1500.0)/(100.0/1000.0)) < 1e-4
    # TATA = (220 - (-30)) / 1600 = 250 / 1600 = 0.15625
    assert abs(res_b["tata"] - (250.0 / 1600.0)) < 1e-4
    # Firm B 触发财务舞弊预警，M-score 显著大于 -1.78
    assert res_b["m_score"] > -1.78
    assert res_b["is_manipulation_suspect"] is True

    print("Lesson 02 练习题测试全部通过！")
