r"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 4/5 课
第 4 课：自由现金流折现 (DCF) 估值引擎与蒙特卡洛敏感性分析 (DCF Valuation & Monte Carlo)
================================================================================

::: {.callout-note}
### 投决会估值第一性原理：资产的内在价值等于未来存续期全部自由现金流的现值总和
- **[绝对估值第一性原理]**：企业的内在价值（Intrinsic Value）严格等于其在剩余存续寿命期内所能产生的全部自由现金流的现值总和。这一原理彻底穿透了会计权责发生制的账面利润迷雾，回归收付实现制的真实购买力。
- **[FCFF 与 FCFE 的适用边界]**：
  - **企业自由现金流 (FCFF)**：归属于所有资本提供者（债权人+股东）。折现率必须使用全资本加权平均成本 WACC，得出企业价值 EV，再扣除净有息负债得出股权价值；
  - **股权自由现金流 (FCFE)**：扣除税后利息支付与债务净本金后的现金流。折现率必须使用股权资本要求回报率 Ke，直接得出股权价值。金融机构（银行、券商）因高杠杆负债为运营资产，必须使用 FCFE 或股利折现模型（DDM）。
:::

- **[FCFF 严密会计推导方程]**：

$$
\text{FCFF}_t = \text{EBIT}_t \times (1 - t) + \text{D\&A}_t - \text{CapEx}_t - \Delta \text{NWC}_t = \text{CFO}_t + \text{Interest Expense}_t \times (1 - t) - \text{CapEx}_t
$$

- **[两阶段 DCF 估值数学模型]**：
  - 阶段 1：显性预测期（Explicit Forecast Period，通常 5~10 年）：
    $$\text{PV}_{\text{Forecast}} = \sum_{t=1}^N \frac{\text{FCFF}_t}{(1 + \text{WACC})^t}$$
  - 阶段 2：永续终值期（Terminal Value, TV，基于戈登增长模型 Gordon Growth）：
    $$\text{TV}_N = \frac{\text{FCFF}_N \times (1 + g)}{\text{WACC} - g}, \quad \text{PV}_{\text{TV}} = \frac{\text{TV}_N}{(1 + \text{WACC})^N}$$
  - 企业价值与每股内在价值桥梁：
    $$\text{EV} = \text{PV}_{\text{Forecast}} + \text{PV}_{\text{TV}}, \quad \text{Value per Share} = \frac{\text{EV} - (\text{Total Debt} - \text{Cash})}{\text{Shares Outstanding}}$$

- **[变量定义域与参数约束]**：
  - $\text{WACC} > g$：永续增长率 $g$ 理论上必须严格小于长期名义 GDP 增速（通常取 2%~3%），否则模型数学发散。

- **[引导句锚点 1]**：如下时序架构所示，两阶段 DCF 将企业价值分解为显性期现值与终值现值：

```mermaid
flowchart LR
    subgraph ExplicitPhase["阶段 1: 显性预测期 (年 1 ~ 5)"]
        Y1["FCFF 1 折现"]
        Y2["FCFF 2 折现"]
        Y5["FCFF 5 折现"]
    end
    subgraph TerminalPhase["阶段 2: 永续终值期 (戈登模型)"]
        TV["TV = FCFF_5 * (1+g) / (WACC - g)"]
    end
    ExplicitPhase --> EV["企业价值 EV (占比 25%~35%)"]
    TerminalPhase --> EV["企业价值 EV (占比 65%~75%)"]
    EV --> NetDebtBridge["扣除净负债 Net Debt"]
    NetDebtBridge --> EquityVal["每股内在价值 Intrinsic Value"]
```

- **[架构要点拆解 1]**：
  - **[1. 终值占比主导]**：终值现值通常占据企业价值的 65%~80%，模型对 WACC 与 $g$ 极其敏感。
  - **[2. 消除精确的错误]**：单一点位预测毫无意义，必须引入敏感性网格与蒙特卡洛随机模拟。
  - **[3. 反向 DCF 逆推]**：将市价代入模型，倒推市场隐含的长期增长率与自由现金流转化率。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[参数微调倒推市价陷阱]**：华尔街分析师常通过将 WACC 下调 0.5% 或将 $g$ 上调 0.5% 来迎合市价，这属于欺骗性估值。
- **[资本开支与折旧永久错配]**：在永续期假设中，严禁长期假设资本开支（CapEx）远低于折旧（D&A），长期来看资本开支至少必须等于折旧以维持资产重置。
:::

【思考题】
Q1: 为什么华尔街常说“DCF 是理论上最完美、实践中最容易被操纵的估值模型”？贴现率 WACC 变动 1% 对终值（Terminal Value）会产生多大程度的放大效应？分析师该如何防范“为了迎合市价而倒推输入参数”的估值造假？
Q2: 区分 FCFF 与 FCFE 的适用边界。对于高杠杆金融机构（如商业银行、证券公司），为什么无法使用常规 FCFF 模型，而必须采用股利折现模型（DDM）或超额收益模型？
Q3: 什么是“反向 DCF”（Reverse DCF）？在对高估值成长股（如英伟达 Nvidia、特斯拉 Tesla）进行投研时，如何通过当前市价反推市场隐含的长期营收增速与自由现金流转化率？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现两阶段 DCF 折现引擎与每股内在价值计算 (2分)；
  2. 准确输出 WACC-g 敏感性矩阵与蒙特卡洛置信区间 (2分)；
- Q1~Q3 问答题各 2 分（共 6 分）：深入剖析现金流折现数理边界与敏感性机理；
- 通过线：8/10 分。一票否决：终值公式除数算反、股权价值未扣净负债、删除断言。
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any


def two_stage_dcf_valuation(
    fcff_forecast: List[float],
    wacc: float,
    terminal_g: float,
    net_debt: float,
    shares_outstanding: float
) -> Dict[str, float]:
    """
    两阶段 DCF 估值引擎
    
    参数:
    fcff_forecast: 显性预测期各年 FCFF 列表 [t1, t2, ..., tN] (单位: 亿元)
    wacc: 加权平均资本成本 (例如 0.09)
    terminal_g: 永续增长率 (例如 0.025，必须严格小于 wacc)
    net_debt: 净有息负债 (有息负债 - 现金及现金等价物)
    shares_outstanding: 总股本 (亿股)
    
    返回字典:
    - pv_forecast: 预测期现金流折现现值和
    - terminal_value: 终值 TV_N
    - pv_terminal: 终值折现现值
    - enterprise_value: 企业价值 EV
    - equity_value: 股权内在价值
    - per_share_value: 每股内在价值 (元)
    """
    # TODO: 请实现两阶段 DCF 折现计算
    pass


def dcf_sensitivity_matrix(
    fcff_forecast: List[float],
    wacc_list: List[float],
    g_list: List[float],
    net_debt: float,
    shares_outstanding: float
) -> pd.DataFrame:
    """
    构建 WACC 与 永续增长率 g 的二维每股内在价值敏感性矩阵
    行索引为 wacc，列索引为 g
    """
    # TODO: 循环计算二维矩阵
    pass


def monte_carlo_dcf(
    fcff_forecast: List[float],
    base_wacc: float,
    wacc_std: float,
    base_g: float,
    g_std: float,
    net_debt: float,
    shares_outstanding: float,
    n_simulations: int = 1000,
    random_seed: int = 42
) -> Dict[str, float]:
    """
    基于蒙特卡洛模拟生成 DCF 每股内在价值置信分布
    
    参数:
    wacc 服从正态分布 N(base_wacc, wacc_std^2)
    terminal_g 服从正态分布 N(base_g, g_std^2)
    (需保证抽样中 wacc > terminal_g + 0.005，防止分母趋零或负数)
    
    返回:
    - mean: 每股价值均值
    - median: 中位数 (p50)
    - p5: 5% 悲观分位数
    - p95: 95% 乐观分位数
    - std: 标准差
    """
    # TODO: 实现蒙特卡洛抽样折现模拟
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 04: DCF 估值引擎与蒙特卡洛敏感性分析测试")
    print("=" * 60)

    # 1. 基础两阶段 DCF 估值测试
    # 5 年预测期 FCFF: [100, 115, 130, 145, 160] 亿元
    # WACC = 9.0%, terminal_g = 2.5%
    # 净负债 = 200 亿元, 总股本 = 10 亿股
    forecast = [100.0, 115.0, 130.0, 145.0, 160.0]
    wacc_val = 0.09
    g_val = 0.025
    net_debt_val = 200.0
    shares_val = 10.0

    dcf_res = two_stage_dcf_valuation(forecast, wacc_val, g_val, net_debt_val, shares_val)
    print("两阶段 DCF 估值结果:", dcf_res)

    assert dcf_res is not None, "结果不能为 None"
    # 手动验算预测期现值:
    # 100/1.09 + 115/1.09^2 + 130/1.09^3 + 145/1.09^4 + 160/1.09^5 ≈ 91.74 + 96.79 + 100.38 + 102.72 + 103.99 ≈ 495.62
    assert abs(dcf_res["pv_forecast"] - 495.62) < 1.0
    # 终值 TV_5 = 160 * 1.025 / (0.09 - 0.025) = 164.0 / 0.065 ≈ 2523.08
    assert abs(dcf_res["terminal_value"] - 2523.08) < 1.0
    # 终值折现 PV_TV = 2523.08 / (1.09^5) ≈ 1639.81
    assert abs(dcf_res["pv_terminal"] - 1639.81) < 1.0
    # EV ≈ 495.62 + 1639.81 = 2135.43
    assert abs(dcf_res["enterprise_value"] - 2135.43) < 1.5
    # 股权价值 = 2135.43 - 200 = 1935.43
    assert abs(dcf_res["equity_value"] - 1935.43) < 1.5
    # 每股价值 = 1935.43 / 10 ≈ 193.54 元
    assert abs(dcf_res["per_share_value"] - 193.54) < 0.2

    # 2. 敏感性矩阵测试
    wacc_grid = [0.08, 0.09, 0.10]
    g_grid = [0.02, 0.025, 0.03]
    matrix = dcf_sensitivity_matrix(forecast, wacc_grid, g_grid, net_debt_val, shares_val)
    print("敏感性矩阵 (每股价值):\n", matrix)

    # 验证单调性: WACC 越低、g 越高，每股估值越高
    assert matrix.loc[0.08, 0.03] > matrix.loc[0.09, 0.025] > matrix.loc[0.10, 0.02]

    # 3. 蒙特卡洛模拟测试
    mc_res = monte_carlo_dcf(
        forecast, base_wacc=0.09, wacc_std=0.005,
        base_g=0.025, g_std=0.003,
        net_debt=net_debt_val, shares_outstanding=shares_val,
        n_simulations=1000, random_seed=42
    )
    print("蒙特卡洛估值区间:", mc_res)

    assert mc_res["p5"] < mc_res["median"] < mc_res["p95"]
    assert abs(mc_res["median"] - dcf_res["per_share_value"]) < 15.0

    print("Lesson 04 练习题测试全部通过！")
