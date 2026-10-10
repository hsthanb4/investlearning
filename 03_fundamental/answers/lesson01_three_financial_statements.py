r"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 1/5 课
第 1 课：财务三表勾稽关系与五因子杜邦拆解引擎 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么“经营活动现金流量净额持续小于净利润”是上市公司业绩可能严重掺水甚至暴雷的核心红线？请从收付实现制与权责发生制背离、激进收入确认与营运资本失控的微观财务逻辑推导：
- **[应计制缺陷与现金流真实性校验链]**：
  - **[1. 权责发生制的纸面富贵漏洞]**：在权责发生制下，企业只要向渠道客户发出货物并开具发票，即便一分钱现金未收到，亦可在利润表上确认为营业收入与净利润。这为管理层通过“渠道塞货（Channel Stuffing）”、伪造阴阳合同或向关联方赊销来虚增利润提供了巨大寻租空间。
  - **[2. 营运资本（NWC）的剧烈失血]**：依据现金流间接法调节方程：
    $$\text{CFO} = \text{Net Income} + \text{D\&A} - \Delta \text{Accounts Receivable} - \Delta \text{Inventory} + \Delta \text{Accounts Payable}$$
    当净利润居高不下而 CFO 持续为负或显著萎缩时，代数上严格证明企业产生巨额的 $\Delta \text{NWC} > 0$（应收账款与存货无序膨胀，大量真金白银被沉淀在应收账款坏账风险与存货跌价风险中）。
  - **[3. 庞氏融资破产终局]**：企业账面利润虽光鲜亮丽，但缺乏自由现金流无法支付员工工资、供应商货款、税金与刚性债务利息，只能持续依赖外部借新还旧或股权增发输血。一旦宏观流动性收紧或银行抽贷，信用链条瞬间断裂，财务造假即刻引爆。

【Q2 投决会深度解析】
为什么仅依靠财务杠杆（Equity Multiplier）单引擎拉升的 ROE 具有极高的周期脆弱性与破产风险？买方机构在估值模型中应如何对其施加折现率惩罚？
- **[财务杠杆双刃剑与破产利息侵蚀机理]**：
  - **[1. 杠杆虚胖的微观本质]**：如果一家企业的营业利润率（EBIT Margin）和总资产周转率（Asset Turnover）持续下滑，而 ROE 却逆势上升，其唯一原因是通过大量借入有息债务扩大资产负债表规模（权益乘数 $A/E$ 飙升）。这表明企业正在用高成本借款填补低效资产的运营黑洞。
  - **[2. 利息保障倍数（ICR）崩塌]**：刚性债务利息支出不会因行业景气下行而减少。一旦宏观进入衰退期，资产周转率稍有下滑，经营利润 EBIT 将无法覆盖利息费用（$\text{EBT} / \text{EBIT} \to 0$），财务杠杆瞬间由“放大收益”反转为“加速亏损”，甚至直接穿透净资产引发资不抵债。
  - **[3. 买方估值折现率惩罚准则]**：
    - 在 DCF 估值中，分析师必须依据哈马达方程（Hamada's Equation）提高其财务杠杆 Beta：$\beta_L = \beta_U [1 + (1-t) D/E]$，直接大幅抬高股权资本成本 $K_e$ 与 WACC 贴现率，对其远期现金流实施严厉的现值折让；
    - 在相对估值中，对高负债驱动型公司实施目标 PB 与 PE 倍数 30%~50% 的“脆弱性折价惩罚”。

【Q3 投决会深度解析】
区分重资产制造型企业（如晶圆代工厂）与轻资产互联网软件企业在杜邦五因子驱动力上的本质差异。商誉（Goodwill）减值会对当期经营现金流产生何种影响，在基本面量化建模中应如何处理？
- **[商业模式分化与商誉法务会计处理]**：
  - **[1. 商业模式与杜邦引擎的对映]**：
    - **重资产制造业（如台积电、中芯国际）**：固定资产规模庞大，核心驱动力在于“产能利用率”驱动的“总资产周转率”与“规模经济摊薄折旧带来的经营利润率”。其经营杠杆（Operating Leverage）极高，景气向上时利润爆发力极强；
    - **轻资产 SaaS/平台型企业（如微软、腾讯）**：无需大量厂房设备，固定资产周转率意义弱化；其核心驱动力在于极高的“营业利润率（EBIT Margin）”与“负营运资本模式”（利用先款后货的递延收入无息占用客户资金）。
  - **[2. 商誉减值的现金流独立性]**：商誉是在历史并购时溢价支付产生的静态无形资产。当被收购标的业绩暴雷时计提的商誉减值损失（Impairment Loss），属于纯粹的“账面非付现减值准备”，**对当期经营活动现金流量净额（CFO）毫无任何直接影响（为 0 冲击）**。
  - **[3. 基本面量化排雷与扣除准则]**：
    - 商誉减值虽然不影响现金流，但会永久性摧毁账面所有者权益，并可能触发商业银行债务违约契约条款；
    - 在严谨的基本面量化因子库中，计算真实净资产与投入资本时，必须强制扣除全部商誉，计算有形净资产收益率（Tangible ROE）与有形资本回报率（Tangible ROIC = NOPAT / (IC - Goodwill)）；若商誉占净资产比例超过 30%，量化排雷模型直接赋予一票否决式清仓评级。
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


def verify_financial_articulation(
    bs_prior: Dict[str, float],
    bs_curr: Dict[str, float],
    is_curr: Dict[str, float],
    cfs_curr: Dict[str, float],
    tolerance: float = 1e-4
) -> Dict[str, Any]:
    """
    财报三张表底层动态勾稽平衡校验器
    """
    # 1. 资产负债表平衡校验: Assets == Liabilities + Equity
    bs_diff = abs(bs_curr["total_assets"] - (bs_curr["total_liabilities"] + bs_curr["total_equity"]))
    bs_balanced = bs_diff <= tolerance

    # 2. 货币资金变动与现金流量表净现金变动勾稽: Cash_curr - Cash_prior == Net Change in Cash
    cash_delta = bs_curr["cash"] - bs_prior["cash"]
    cash_diff = abs(cash_delta - cfs_curr["net_change_in_cash"])
    cash_passed = cash_diff <= tolerance

    # 3. 留存收益变动勾稽: RE_curr - RE_prior == Net Income - Dividends Paid
    re_delta = bs_curr["retained_earnings"] - bs_prior["retained_earnings"]
    re_expected = is_curr["net_income"] - cfs_curr["dividends_paid"]
    re_diff = abs(re_delta - re_expected)
    re_passed = re_diff <= tolerance

    # 4. 间接法 CFO 校验: CFO ≈ Net Income + D&A - ΔNWC
    # ΔNWC = Δnon_cash_current_assets - Δnon_debt_current_liabilities
    delta_nwc = (
        (bs_curr["non_cash_current_assets"] - bs_prior["non_cash_current_assets"]) -
        (bs_curr["non_debt_current_liabilities"] - bs_prior["non_debt_current_liabilities"])
    )
    cfo_estimated = is_curr["net_income"] + cfs_curr["dep_amort"] - delta_nwc
    cfo_error = abs(cfs_curr["cfo"] - cfo_estimated)
    cfo_passed = cfo_error <= tolerance

    all_passed = bs_balanced and cash_passed and re_passed and cfo_passed

    return {
        "balance_sheet_balanced": bs_balanced,
        "cash_articulation_passed": cash_passed,
        "retained_earnings_passed": re_passed,
        "cfo_reconciliation_error": float(cfo_error),
        "is_all_passed": all_passed
    }


def dupont_5factor_analysis(data: Dict[str, float]) -> Dict[str, float]:
    """
    现代五因子杜邦分析引擎
    """
    net_income = data["net_income"]
    ebt = data["ebt"]
    ebit = data["ebit"]
    revenue = data["revenue"]
    total_assets = data["total_assets"]
    total_equity = data["total_equity"]

    # 五因子拆解
    tax_burden = net_income / ebt
    interest_burden = ebt / ebit
    operating_margin = ebit / revenue
    asset_turnover = revenue / total_assets
    financial_leverage = total_assets / total_equity

    computed_roe = tax_burden * interest_burden * operating_margin * asset_turnover * financial_leverage
    direct_roe = net_income / total_equity

    return {
        "tax_burden": float(tax_burden),
        "interest_burden": float(interest_burden),
        "operating_margin": float(operating_margin),
        "asset_turnover": float(asset_turnover),
        "financial_leverage": float(financial_leverage),
        "computed_roe": float(computed_roe),
        "direct_roe": float(direct_roe)
    }


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 01 参考实现与测试")
    print("=" * 60)

    bs_prior_sample = {
        "cash": 1200.0,
        "total_assets": 10000.0,
        "total_liabilities": 4000.0,
        "total_equity": 6000.0,
        "retained_earnings": 3500.0,
        "non_cash_current_assets": 2800.0,
        "non_debt_current_liabilities": 1500.0
    }

    bs_curr_sample = {
        "cash": 1650.0,
        "total_assets": 11800.0,
        "total_liabilities": 4600.0,
        "total_equity": 7200.0,
        "retained_earnings": 4700.0,
        "non_cash_current_assets": 3200.0,
        "non_debt_current_liabilities": 1700.0
    }

    is_curr_sample = {
        "revenue": 15000.0,
        "operating_expenses": 12000.0,
        "ebit": 3000.0,
        "interest_expense": 500.0,
        "ebt": 2500.0,
        "tax_expense": 500.0,
        "net_income": 2000.0
    }

    cfs_curr_sample = {
        "cfo": 2300.0,
        "cfi": -1200.0,
        "cff": -650.0,
        "net_change_in_cash": 450.0,
        "dividends_paid": 800.0,
        "dep_amort": 500.0
    }

    check_res = verify_financial_articulation(bs_prior_sample, bs_curr_sample, is_curr_sample, cfs_curr_sample)
    print("勾稽校验结果:", check_res)
    assert check_res["balance_sheet_balanced"] is True
    assert check_res["cash_articulation_passed"] is True
    assert check_res["retained_earnings_passed"] is True
    assert abs(check_res["cfo_reconciliation_error"]) < 1e-4
    assert check_res["is_all_passed"] is True

    dupont_data = {
        "net_income": 2000.0,
        "ebt": 2500.0,
        "ebit": 3000.0,
        "revenue": 15000.0,
        "total_assets": 11800.0,
        "total_equity": 7200.0
    }
    dupont_res = dupont_5factor_analysis(dupont_data)
    print("五因子杜邦拆解结果:", dupont_res)

    assert abs(dupont_res["tax_burden"] - (2000.0 / 2500.0)) < 1e-5
    assert abs(dupont_res["interest_burden"] - (2500.0 / 3000.0)) < 1e-5
    assert abs(dupont_res["operating_margin"] - (3000.0 / 15000.0)) < 1e-5
    assert abs(dupont_res["asset_turnover"] - (15000.0 / 11800.0)) < 1e-5
    assert abs(dupont_res["financial_leverage"] - (11800.0 / 7200.0)) < 1e-5
    assert abs(dupont_res["computed_roe"] - dupont_res["direct_roe"]) < 1e-5
    assert abs(dupont_res["direct_roe"] - (2000.0 / 7200.0)) < 1e-5

    print("Lesson 01 参考实现全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：应计制与收付实现制背离、激进收入确认与营运资本失控）：
1. 风险定性：净利润高增而 CFO 为负，且应收账款与存货大幅跑赢营收，表明公司的账面利润大部分属于“未收现的纸面富贵”。这通常指向两种严峻风险：
   - 渠道塞货（Channel Stuffing）或虚构收入：为了维持高增长假象，向前置渠道透支发货或放宽信用政策促销，坏账风险极高；
   - 存货积压与滞销：产品竞争力下滑导致产成品堆积，未来将面临巨额存货跌价准备计提。
2. 现金流间接法调整净利润：
   分析师应当从 Net Income 出发：
   CFO = 净利润 + 非付现折旧摊销 - Δ应收账款 - Δ存货 + Δ应付账款。
   当 ΔAR 和 ΔInventory 剧烈膨胀时，产生巨大的负向营运资本变动（ΔNWC > 0），大幅吃光净利润，揭示企业真实的自由现金流创造能力枯竭，依赖外部债务输血（Ponz-like cash flow）。

Q2 标准解析（得分要点：杠杆驱动的高脆弱性、利息侵蚀与财务纾困风险、估值乘数惩罚）：
1. 脆弱性本质：当 ROE 提升仅由财务杠杆（Equity Multiplier）单引擎拉动，而利息负担率下降（利息支出激增侵蚀 EBIT）和资产周转率下降（资产使用效率低下）时，说明企业正在用借来的高成本负债填补低效运营的资产黑洞。
2. 破产与下行风险：一旦宏观流动性收紧、利率上行或行业景气度边际下行，资产周转率稍有下滑，经营现金流将无法覆盖刚性债务利息（利息保障倍数崩塌），触发债务违约危机。
3. 估值折价惩罚：买方分析师在进行 DCF 估值时，必须提高权益资本成本 Ke（贝塔系数显著提高），提高 WACC 贴现率；在相对估值上，应大幅扣减目标 PB 与 PE 乘数（通常在基准行业乘数上折价 30%~50%），以反映其极度恶化的偿债安全垫与非经营性财务脆弱性。

Q3 标准解析（得分要点：资本密度与商业模式差异、商誉的沉没属性与减值炸弹）：
1. 商业模式与杜邦驱动力差异：
   - 重资产制造型企业（如晶圆厂）：核心在于“产能利用率”驱动的“资产周转率（Asset Turnover）”与“规模经济带来的营业利润率”。巨额固定资产折旧产生高经营杠杆，资产周转率的小幅提升对 ROE 具有巨大弹性拉动；
   - 轻资产互联网/软件企业：资产基数极小，固定资产周转率意义弱化，其核心驱动力在于“极高的营业利润率（Operating Margin）”与“负营运资本模式（高预收账款/递延收入无息借用上下游资金）”。
2. 商誉（Goodwill）的量化处理：
   - 商誉本质是历史并购时支付的溢价，不产生任何直接生产力，且在资产负债表上面临突发大额“商誉减值”的灰犀牛风险；
   - 在严谨的基本面量化中，计算真实经营 ROE 和投入资本回报率（ROIC）时，应剔除商誉（Tangible Book Value & Tangible ROIC = NOPAT / (IC - Goodwill)）；若保留商誉，则需在压力测试中模拟商誉一次性 100% 减值对净资产的毁灭性穿透，以测算企业的真实安全边际。
""")
