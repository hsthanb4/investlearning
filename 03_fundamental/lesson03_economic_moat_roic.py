"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 3/5 课
第 3 课：商业护城河量化、ROIC-WACC 价值创造与竞争优势衰减模型
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 深度思考题回答完整、逻辑严谨（各 2 分）：共 6 分
- 合格线：8/10 分

【理论精讲】
1. 护城河（Economic Moat）的财务本质：
   沃伦·巴菲特（Warren Buffett）与查理·芒格（Charlie Munger）指出：只有具备持久竞争壁垒（宽阔护城河）的企业，才能在长周期内抵御行业资本的疯狂涌入和超额利润的均值回归。
   在现代公司金融与量化价值投资中，护城河绝非抽象的叙事，而是能够被数学精确度量的：
   那就是企业能否在漫长时间跨度内，维持：
   
       投入资本回报率 (ROIC) 显著且持续地高于 加权平均资本成本 (WACC)

2. 核心公式与概念：
   - 投入资本 (Invested Capital, IC):
     资产端视角：IC = 总资产 - 无息流动负债（如应付账款、预收款） - 超额现金及交易性金融资产
     融资端视角：IC = 股东权益 + 有息负债（短期借款 + 长期借款 + 应付债券） - 超额现金
   - 息前税后经营利润 (NOPAT, Net Operating Profit After Tax):
     NOPAT = EBIT × (1 - 有效所得税率 t)
   - 投入资本回报率 (ROIC):
     ROIC = NOPAT / Invested_Capital
   - 加权平均资本成本 (WACC):
     WACC = (E / (D + E)) × Ke + (D / (D + E)) × Kd × (1 - t)
     其中 Ke 由资本资产定价模型 CAPM 给出：Ke = Rf + β × ERP
   - 超额利差 (Economic Spread) 与经济增加值 (EVA):
     Spread = ROIC - WACC
     EVA = Invested_Capital × (ROIC - WACC) = NOPAT - (Invested_Capital × WACC)
     * 若 ROIC > WACC (EVA > 0)：企业在真实地创造股东财富！
     * 若 ROIC < WACC (EVA < 0)：企业看似有利润，但资本成本无法覆盖，增长即毁灭！

3. 竞争优势存续期（Competitive Advantage Period, CAP）与 ROIC 衰减动力学：
   迈克尔·波特行业竞争理论：超额收益像蜜糖吸引熊一样吸引竞争对手进入。
   随着行业成熟与技术扩散，无壁垒公司的 ROIC 会迅速向行业平均资本成本（WACC）收敛。
   经典指数衰减模型：
   
       ROIC(t) = WACC + (ROIC_0 - WACC) * exp(-λ * t)
       
   - λ (Decay Rate，衰减系数)：
     * 宽护城河企业（Wide Moat，如奢侈品垄断、操作系统壁垒）：λ 极小（0.03 ~ 0.06），半衰期达 15~20 年以上；
     * 无护城河企业（No Moat，如普通代工、低门槛大宗品）：λ 较大（0.20 ~ 0.35），超额利润在 3~5 年内迅速被竞争抹平。

【三个思考题 (Q1~Q3)】
Q1: 为什么高 ROE 不必然代表企业具备护城河，而长期持续高 ROIC（>15%~20%）才是真正的护城河量化试金石？请从“财务杠杆放大”与“非经营性金融资产套利”的角度进行深度剖析。
Q2: 晨星（Morningstar）定义的五大护城河来源（无形资产/品牌与专利、客户转换成本、网络效应、成本优势、有效规模）在财务报表中的微观映射分别是什么？请各列举一个财务指标特征与对应典型行业案例。
Q3: 为什么当一家企业的 ROIC < WACC 时，管理层雄心勃勃的“营收与资产规模翻倍扩产”反而是对股东财富的巨大毁灭？在买方价值评估中，这如何导致“规模不经济”和价值毁灭？
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
