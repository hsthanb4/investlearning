"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 2/5 课
第 2 课：财务造假识别与法务会计 Beneish M-Score 评分器
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 深度思考题回答完整、逻辑严谨（各 2 分）：共 6 分
- 合格线：8/10 分

【理论精讲】
1. 法务会计与利润操纵检验哲学：
   在权责发生制下，管理层拥有大量的会计估计、资产减值、收入确认时点与费用资本化的自由裁量权。
   当企业面临业绩承诺、债务违约或市值管理压力时，极易产生财务粉饰与欺诈动机。
   法务会计的核心原则是：“业务有逻辑，数据有印证，异常显端倪，现金不撒谎。”

2. Beneish M-Score 八变量概率模型（1999）：
   印第安纳大学 Messod Beneish 教授基于离散选择 Probit 模型构建的经典财务操纵预警系统（曾成功提前预警安然 Enron 财务舞弊）：
   
   M_Score = -4.84 + 0.920*DSRI + 0.528*GMI + 0.404*AQI + 0.892*SGI + 0.115*DEPI - 0.172*SGAI + 4.037*TATA + 0.0327*LVGI
   
   八大分项指数定义与经济学逻辑：
   (1) DSRI (Days Sales in Receivables Index，应收账款指数):
       DSRI = (Receivables_t / Sales_t) / (Receivables_{t-1} / Sales_{t-1})
       若 DSRI > 1，表明应收账款增速快于营业收入，提示可能存在激进收入确认、虚构应收账款或放宽信贷条件促销。
   (2) GMI (Gross Margin Index，毛利率恶化指数):
       Gross Margin = (Sales - COGS) / Sales
       GMI = Gross_Margin_{t-1} / Gross_Margin_t
       当本期毛利率恶化时，GMI > 1。毛利率承压的企业具有强烈的操纵利润以维持高景气假象的动机。
   (3) AQI (Asset Quality Index，资产质量恶化指数):
       AQ = 1 - (Current_Assets + Net_PP&E) / Total_Assets
       AQI = AQ_t / AQ_{t-1}
       衡量企业将不可见成本资本化为无形资产、长期待摊费用等非硬资产的比例。AQI > 1 意味着资产质量劣质化。
   (4) SGI (Sales Growth Index，营业收入增长指数):
       SGI = Sales_t / Sales_{t-1}
       高增长本身并非造假，但成长型企业在增长失速时财务造假概率最高。
   (5) DEPI (Depreciation Index，折旧率放缓指数):
       Depr_Rate = Depr / (Depr + Net_PP&E)
       DEPI = Depr_Rate_{t-1} / Depr_Rate_t
       若 DEPI > 1，表明折旧计提比例放缓，管理层可能通过延长固定资产折旧年限来增加当期净利润。
   (6) SGAI (SG&A Expenses Index，销售及管理费用指数):
       SGAI = (SG&A_t / Sales_t) / (SG&A_{t-1} / Sales_{t-1})
       用于捕捉期间费用控制失调。
   (7) LVGI (Leverage Index，财务杜杆跳升指数):
       Leverage = (Total_Debt) / Total_Assets  （总负债 / 总资产）
       LVGI = Leverage_t / Leverage_{t-1}
       杠杆攀升增加了违反债务契约的风险，推高造假概率。
   (8) TATA (Total Accruals to Total Assets，总应计项比率):
       TATA = (Net_Income_t - CFO_t) / Total_Assets_t
       核心应计盈余质量指标。当利润缺乏经营现金流支撑时，TATA 显著为正。

3. 阈值与判别标准：
   - 基准阈值：-1.78
   - 若 M-Score > -1.78（例如 -1.49, -0.80），模型判定该企业存在极高的财务粉饰或造假概率（High Probability of Manipulation）。
   - 若 M-Score <= -1.78（例如 -2.22, -2.80），模型判定为低风险正常企业。

【三个思考题 (Q1~Q3)】
Q1: 为什么许多 A 股与海外造假公司（如康美药业、康得新）都呈现出“大存大贷”（账面躺着几十亿现金，却同时借入数十亿高息短期借款并承担数亿利息支出）的反常特征？作为法务会计与买方量化研究员，你应设计哪些跨表比率指标来自动化捕捉这种造假嫌疑？
Q2: 研发支出“资本化” vs “费用化”的主观裁量权如何被管理层用来粉饰当期财务报表？在 Beneish M-Score 模型中主要体现在哪个指数（AQI）？在分析现金流量表时，研发支出资本化如何人为美化经营现金流（CFO）而转嫁到投资现金流（CFI）？
Q3: 许多造假企业为了配平虚增的营业收入和净利润，通常在资产端做大“存货”或“固定资产在建工程”。如何通过“存货周转天数异常逆势攀升 + 毛利率逆势反常走高”这一经典背离形态，识破其“少结转营业成本虚增当期毛利”的财务操纵手法？
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
