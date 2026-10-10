"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 3/5 课
参考实现与标准问答解析
第 3 课：商业护城河量化、ROIC-WACC 价值创造与竞争优势衰减模型
================================================================================
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
    """
    nopat = ebit * (1.0 - tax_rate)
    invested_capital = equity + debt - excess_cash
    roic = nopat / invested_capital

    total_capital = equity + debt
    w_e = equity / total_capital
    w_d = debt / total_capital
    after_tax_kd = cost_of_debt * (1.0 - tax_rate)
    wacc = w_e * cost_of_equity + w_d * after_tax_kd

    spread = roic - wacc
    eva = invested_capital * spread

    return {
        "nopat": float(nopat),
        "invested_capital": float(invested_capital),
        "roic": float(roic),
        "wacc": float(wacc),
        "economic_spread": float(spread),
        "eva": float(eva)
    }


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
    """
    half_life = float(np.log(2.0) / decay_rate)
    roic_trajectory: List[float] = []
    eva_trajectory: List[float] = []
    cumulative_pv_eva = 0.0

    for t in range(1, years + 1):
        roic_t = wacc + (initial_roic - wacc) * np.exp(-decay_rate * t)
        ic_t = initial_ic * ((1.0 + ic_growth_rate) ** t)
        eva_t = ic_t * (roic_t - wacc)
        pv_eva_t = eva_t / ((1.0 + wacc) ** t)

        roic_trajectory.append(float(roic_t))
        eva_trajectory.append(float(eva_t))
        cumulative_pv_eva += float(pv_eva_t)

    return {
        "roic_trajectory": roic_trajectory,
        "eva_trajectory": eva_trajectory,
        "cumulative_pv_eva": float(cumulative_pv_eva),
        "half_life_years": float(half_life)
    }


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 03 参考实现与测试")
    print("=" * 60)

    # 1. 基础 ROIC 与 EVA 测试
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

    assert abs(metric_res["nopat"] - 300.0) < 1e-4
    assert abs(metric_res["invested_capital"] - 1500.0) < 1e-4
    assert abs(metric_res["roic"] - 0.20) < 1e-4
    expected_wacc = (1200.0 / 1800.0) * 0.10 + (600.0 / 1800.0) * 0.05 * (1 - 0.25)
    assert abs(metric_res["wacc"] - expected_wacc) < 1e-5
    assert abs(metric_res["eva"] - 1500.0 * (0.20 - expected_wacc)) < 1e-4

    # 2. 护城河衰减模型对比测试:
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
    assert wide_moat["cumulative_pv_eva"] > 2.0 * no_moat["cumulative_pv_eva"]

    print("Lesson 03 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：ROE受杠杆与非经常损益扭曲、ROIC直指核心主营资本回报率）：
1. 杠杆扭曲：
   根据杜邦公式，ROE = ROA × 权益乘数。一家完全没有产品竞争力和定价权的企业，只要大肆借入高风险有息负债放大财务杠杆（如极端负债率房企），其账面 ROE 可以虚高至 30% 以上，但这绝非护城河，而是悬崖边缘的财务杂技；
2. 闲置资金与金融损益干扰：
   ROE 分母是全部股东权益，分子包含炒股、理财收益、处置子公司等非经常性损益。而 ROIC 严格聚焦于经营资产（扣除超额现金与金融资产）与经营利润（NOPAT），排除了资本结构（负债比例）、税收优惠波动以及闲置现金拖累的干扰，纯粹度量“主营业务本身投入一元钱资本能换回多少真金白银的息前税后利润”，因此只有长年持续维持高 ROIC（>15%~20%）才证明具备坚固壁垒。

Q2 标准解析（得分要点：五大护城河来源、量化财务指标与对应行业案例）：
1. 无形资产（Intangible Assets，如专利、特许经营权、高端品牌）：
   - 财务特征：极高的毛利率（Gross Margin > 70%）与高 NOPAT 利润率，强定价权，成本转嫁能力极强。
   - 代表行业/案例：高端白酒（贵州茅台）、创新药专利药企（辉瑞、礼来）。
2. 转换成本（Switching Costs）：
   - 财务特征：高客户留存率（Net Retention Rate > 110%），销售费用率极低且逐年下降，高经营现金流稳定性。
   - 代表行业/案例：企业级基础软件/ERP（SAP、微软 Windows/Office、Salesforce）。
3. 网络效应（Network Effects）：
   - 财务特征：边际成本趋近于零，资产周转率高，随着用户规模扩大营业利润率呈现非线性爆发增长。
   - 代表行业/案例：清算网络（Visa、Mastercard）、社交网络平台（腾讯微信）。
4. 成本优势（Cost Advantages）：
   - 财务特征：更低的单位营业成本、存货周转率远超同行，在行业低谷时同行全行业亏损而其仍能维持盈利。
   - 代表行业/案例：大型仓储会员零售（Costco）、半导体晶圆代工制造（台积电 TSMC 凭借良率与巨额 CapEx 规模摊薄成本）。
5. 有效规模（Efficient Scale）：
   - 财务特征：高进入门槛，重资产、低运营成本，区域排他性寡头垄断，ROIC 长期稳定在 10%~12% 之间。
   - 代表行业/案例：输油/天然气管道网、干线铁路、大型枢纽机场。

Q3 标准解析（得分要点：负超额利差下的增长陷阱、毁灭价值的量化推导）：
1. 价值创造的数理推导：
   企业价值增量主要来源于 EVA = IC × (ROIC - WACC)。
   若 ROIC < WACC，则每单位新增投入资本所带来的 NOPAT 收益无法补偿投资者（债权人与股东）所要求的最低资本成本（Spread < 0）。
2. 规模越大，毁灭越惨：
   在此情况下，管理层盲目扩产、扩大投入资本 ΔIC，新增价值 ΔEVA = ΔIC × (ROIC - WACC) < 0。
   投入的资本越多，企业内在价值缩水越严重。这就是典型的“成长陷阱（Growth Trap）”——在资本成本高于回报率的恶性竞争行业（如曾经的光伏恶性内卷周期、共享单车补贴大战），规模扩张本质上是在加速烧毁股东财富！
""")
