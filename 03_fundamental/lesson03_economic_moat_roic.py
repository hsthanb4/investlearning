r"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 3/5 课
第 3 课：商业护城河量化、ROIC-WACC 价值创造与竞争优势衰减模型 (Economic Moat & ROIC Engine)
================================================================================

::: {.callout-note}
### 投决会价值创造公理：ROIC 持续高于 WACC 是商业护城河存在的唯一数学真理
- **[商业护城河本质]**：沃伦·巴菲特与查理·芒格强调的“经济护城河（Economic Moat）”在公司金融中绝非文学叙事，而是能够被数学精确度量的客观实体：那就是企业能否在漫长的时间跨度内，维持投入资本回报率（ROIC）显著且持续地超越其加权平均资本成本（WACC）。
- **[投入资本 (Invested Capital) 的双重视角守恒]**：
  - 资产端：$\text{IC} = \text{净营运资本 (NWC)} + \text{固定资产净额 (Net PP\&E)} + \text{无形资产} - \text{超额闲置现金}$；
  - 融资端：$\text{IC} = \text{股东权益} + \text{有息负债总额} - \text{超额现金}$。
- **[经济增加值 (EVA) 财富判定公理]**：
  - 若 $\text{ROIC} > \text{WACC}$（$\text{EVA} > 0$）：企业每追加一元资本开支，均在为股东创造真实超额财富；
  - 若 $\text{ROIC} < \text{WACC}$（$\text{EVA} < 0$）：企业利润虽为正，但资本成本无法覆盖，盲目扩产投资等同于毁灭股东财富！
:::

- **[核心财务公式与变量定义]**：
  - 息前税后经营利润（NOPAT）：

$$
\text{NOPAT} = \text{EBIT} \times (1 - t)
$$

  - 投入资本回报率（ROIC）：

$$
\text{ROIC} = \frac{\text{NOPAT}}{\text{Invested Capital}}
$$

  - 加权平均资本成本（WACC）：

$$
\text{WACC} = \left(\frac{E}{D + E}\right) \times K_e + \left(\frac{D}{D + E}\right) \times K_d \times (1 - t)
$$

  - 经济增加值（EVA）与超额利差：

$$
\text{Spread} = \text{ROIC} - \text{WACC}, \quad \text{EVA} = \text{Invested Capital} \times (\text{ROIC} - \text{WACC})
$$

- **[变量定义域与参数约束]**：
  - $t \in [0, 0.40]$：有效所得税率。$K_e$ 由 CAPM 模型给出：$K_e = R_f + \beta \cdot \text{ERP}$。$K_d$ 为税前债务借贷成本。

- **[竞争优势存续期 (CAP) 与 ROIC 指数衰减动力学]**：
  - 行业竞争理论指出：超额资本回报必然引来竞争对手的疯狂资本涌入，使超额利差向 WACC 收敛：

$$
\text{ROIC}(t) = \text{WACC} + (\text{ROIC}_0 - \text{WACC}) \cdot \exp(-\lambda t)
$$

- **[变量定义域与衰减系数 λ]**：
  - 宽护城河（Wide Moat，奢侈品、操作系统）：$\lambda \in [0.02, 0.05]$，半衰期达 15~20 年以上；
  - 无护城河（No Moat，普通代工、低门槛大宗品）：$\lambda \in [0.20, 0.40]$，超额利润在 3~5 年内迅速被竞争抹平。

- **[引导句锚点 1]**：如下架构拓扑所示，ROIC-WACC 剪刀差决定了企业是在真实创造价值还是毁灭价值：

```mermaid
flowchart TD
    EBIT["息税前利润 EBIT"] --> NOPAT["息前税后利润 NOPAT = EBIT * (1 - t)"]
    ICCalc["投入资本 IC (资产端/融资端守恒)"] --> ROIC["ROIC = NOPAT / IC"]
    CAPM["资本市场成本: Ke (CAPM) + Kd (债务)"] --> WACC["加权平均资本成本 WACC"]
    ROIC --> Spread{"超额利差: ROIC - WACC"}
    WACC --> Spread
    Spread -->|ROIC > WACC (EVA > 0)| ValueCreation["价值创造型优质企业 ➔ 扩产追加投资复合放大财富"]
    Spread -->|ROIC < WACC (EVA < 0)| ValueDestruction["价值毁灭型陷阱企业 ➔ 账面有利润实为股东失血黑洞"]
```

- **[架构要点拆解 1]**：
  - **[1. 剔除财务杠杆噪音]**：ROIC 衡量的是全资本（债权人+股东）的真实经营回报率，不受资本结构负债率的虚假扭曲。
  - **[2. 真实资本占用约束]**：通过扣减与经营无关的超额现金，精确测算企业维持当前经营所需的纯资产规模。
  - **[3. 资本配置决策基石]**：当 ROIC 远高于 WACC 时，留存收益再投资能够实现完美的复利滚雪球。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[盲目扩产价值毁灭陷阱]**：当一家企业的 ROIC 仅为 5% 而 WACC 为 8% 时，管理层雄心勃勃的“营收翻倍大扩产”不仅不值得庆贺，反而是对股东财富的剧烈毁灭。
- **[高 ROE 虚假繁荣]**：严禁仅看高 ROE。依靠 80% 负债率高杠杆或者依靠理财投资收益等非经常性损益拼凑的高 ROE，在 ROIC 显微镜下一览无余。
:::

【思考题】
Q1: 为什么高 ROE 不必然代表企业具备护城河，而长期持续高 ROIC（>15%~20%）才是真正的护城河量化试金石？请从“财务杠杆放大”与“非经营性金融资产套利”的角度进行深度剖析。
Q2: 晨星（Morningstar）定义的五大护城河来源（无形资产/品牌与专利、客户转换成本、网络效应、成本优势、有效规模）在财务报表中的微观映射分别是什么？请各列举一个财务指标特征与对应典型行业案例。
Q3: 为什么当一家企业的 ROIC < WACC 时，管理层雄心勃勃的“营收与资产规模翻倍扩产”反而是对股东财富的巨大毁灭？在买方价值评估中，这如何导致“规模不经济”和价值毁灭？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现投入资本 IC、NOPAT、ROIC 与 WACC 测算 (2分)；
  2. 准确测算经济增加值 EVA 与 ROIC 跨期指数衰减序列 (2分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须深入说明微观金融原理与资本配置决策逻辑；
- 通过线：8/10 分。一票否决：IC 资产端算错、EVA 符号颠倒、删除断言。
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List


def calculate_roic_and_eva(
    ebit: float,
    tax_rate: float,
    equity: float,
    debt: float,
    excess_cash: float,
    cost_of_equity: float,
    cost_of_debt: float
) -> Dict[str, float]:
    """
    计算投入资本 (Invested Capital)、NOPAT、ROIC、WACC 与经济增加值 (EVA)
    
    参数:
    ebit: 息税前利润
    tax_rate: 所得税率 (例如 0.25)
    equity: 股东权益市场价值或账面价值
    debt: 有息负债总额
    excess_cash: 超额现金与闲置金融资产
    cost_of_equity: 股权资本成本 Ke (例如 0.10)
    cost_of_debt: 债务税前资本成本 Kd (例如 0.05)
    
    返回:
    dict: {
        "nopat": float,
        "invested_capital": float,
        "roic": float,
        "wacc": float,
        "economic_spread": float,  # ROIC - WACC
        "eva": float               # IC * (ROIC - WACC)
    }
    """
    # TODO: 请实现投入资本、ROIC、WACC与EVA的计算逻辑
    pass


def model_roic_decay_and_value_creation(
    initial_roic: float,
    wacc: float,
    decay_rate: float,
    initial_ic: float,
    ic_growth_rate: float,
    years: int = 10
) -> Dict[str, Any]:
    """
    基于指数衰减动力学模拟竞争优势期 (CAP) 内的 ROIC 衰减轨迹与企业累计价值创造
    
    衰减公式:
        ROIC(t) = WACC + (initial_roic - WACC) * exp(-decay_rate * t)
        IC(t) = initial_ic * (1 + ic_growth_rate) ** t
        EVA(t) = IC(t) * (ROIC(t) - WACC)
        PV_EVA(t) = EVA(t) / ((1 + WACC) ** t)
        
    参数:
    initial_roic: 期初 ROIC (例如 0.25)
    wacc: 资本成本 (例如 0.08)
    decay_rate: 竞争优势衰减速率 lambda (例如 0.08 为宽护城河, 0.25 为无护城河)
    initial_ic: 期初投入资本总额
    ic_growth_rate: 投入资本再投资年增长率
    years: 模拟年限 (例如 10 年)
    
    返回:
    dict: {
        "roic_trajectory": List[float],    # t=1..years 各年 ROIC
        "eva_trajectory": List[float],     # t=1..years 各年 EVA
        "cumulative_pv_eva": float,        # 累计贴现创造的经济价值总和 (PV of EVA)
        "half_life_years": float           # 超额收益半衰期: ln(2) / decay_rate
    }
    """
    # TODO: 请实现 ROIC 衰减动力学与累计价值创造折现计算
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 03: 商业护城河量化与竞争优势衰减模型测试")
    print("=" * 60)

    # 1. 基础 ROIC 与 EVA 测试
    # EBIT 400, 税率 25% -> NOPAT = 300
    # Equity 1200, Debt 600, 现金 300 -> IC = 1200 + 600 - 300 = 1500
    # ROIC = 300 / 1500 = 20.0%
    # Ke = 10%, Kd = 5%, 税率 25% -> Kd_after_tax = 3.75%
    # 资本总额 D+E = 1800, WACC = (1200/1800)*0.10 + (600/1800)*0.0375 = 0.066667 + 0.0125 = 7.9167%
    # Spread = 20.0% - 7.9167% = 12.0833%
    # EVA = 1500 * Spread = 181.25
    metric_res = calculate_roic_and_eva(
        ebit=400.0,
        tax_rate=0.25,
        equity=1200.0,
        debt=600.0,
        excess_cash=300.0,
        cost_of_equity=0.10,
        cost_of_debt=0.05
    )
    print("ROIC & EVA 计算结果:", metric_res)

    assert metric_res is not None, "结果不能为 None"
    assert abs(metric_res["nopat"] - 300.0) < 1e-4
    assert abs(metric_res["invested_capital"] - 1500.0) < 1e-4
    assert abs(metric_res["roic"] - 0.20) < 1e-4
    expected_wacc = (1200.0 / 1800.0) * 0.10 + (600.0 / 1800.0) * 0.05 * (1 - 0.25)
    assert abs(metric_res["wacc"] - expected_wacc) < 1e-5
    assert abs(metric_res["eva"] - 1500.0 * (0.20 - expected_wacc)) < 1e-4

    # 2. 护城河衰减模型对比测试:
    # 宽护城河企业 (Wide Moat): lambda = 0.05 (半衰期约 13.86 年)
    # 无护城河企业 (No Moat): lambda = 0.35 (半衰期约 1.98 年)
    wide_moat = model_roic_decay_and_value_creation(
        initial_roic=0.25, wacc=0.08, decay_rate=0.05,
        initial_ic=1000.0, ic_growth_rate=0.05, years=10
    )
    no_moat = model_roic_decay_and_value_creation(
        initial_roic=0.25, wacc=0.08, decay_rate=0.35,
        initial_ic=1000.0, ic_growth_rate=0.05, years=10
    )

    print("宽护城河企业半衰期:", wide_moat["half_life_years"], "第10年ROIC:", wide_moat["roic_trajectory"][-1])
    print("无护城河企业半衰期:", no_moat["half_life_years"], "第10年ROIC:", no_moat["roic_trajectory"][-1])
    print("宽护城河累计折现EVA:", wide_moat["cumulative_pv_eva"])
    print("无护城河累计折现EVA:", no_moat["cumulative_pv_eva"])

    assert abs(wide_moat["half_life_years"] - (np.log(2) / 0.05)) < 1e-4
    assert wide_moat["roic_trajectory"][-1] > no_moat["roic_trajectory"][-1]
    # 宽护城河企业创造的累计经济价值显著高于无护城河企业
    assert wide_moat["cumulative_pv_eva"] > 2.0 * no_moat["cumulative_pv_eva"]

    print("Lesson 03 练习题测试全部通过！")
