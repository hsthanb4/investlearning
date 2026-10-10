r"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 2/5 课
第 2 课：真实盈利质量审查与 Beneish M-Score 排雷模型 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么许多 A 股与海外造假公司（如康美药业、康得新）都呈现出“大存大贷”（账面躺着几十亿现金，却同时借入数十亿高息短期借款并承担数亿利息支出）的反常特征？作为法务会计与买方量化研究员，你应设计哪些跨表比率指标来自动化捕捉这种造假嫌疑？
- **[存贷双高本质悖论与量化监控指标设计]**：
  - **[1. 商业常识逻辑悖论]**：正常经营的理性企业追求资本配置效率。若账面真实拥有 100 亿充裕活期存款，断无理由同时向银行借入 80 亿年化利率 5%~7% 的短期借款，并每年白白承受数亿元的刚性财务费用净支出。
  - **[2. 造假资金体外循环本质]**：所谓的“百亿账面存款”本质上是伪造的虚假银行对账单，或者该笔资金早已被控股股东私自作为违规质押担保而处于完全受限冻结状态；企业维持日常运营不得不依赖外部高息短贷续命，最终在债务到期无法偿付时谎言瞬间戳破。
  - **[3. 量化自动化排雷指标设计]**：
    - **利息收入率反常检验**：$\text{Implied Cash Return} = \frac{\text{利息收入}}{\text{平均货币资金}}$。若该比率常年低于 0.8%（远低于协定存款或大额存单利率），证明账面现金属于虚构；
    - **存贷双高偏离度指标**：$\text{Deposit-Loan Spread} = \frac{\text{货币资金}}{\text{总资产}} \times \frac{\text{有息负债}}{\text{总资产}}$。当二者占比同时超过 30% 时触发红色警报；
    - **财务费用与现金比率背离度**：$\frac{\text{净财务费用}}{\text{货币资金}}$ 显著异常偏高。

【Q2 投决会深度解析】
研发支出“资本化” vs “费用化”的主观裁量权如何被管理层用来粉饰当期财务报表？在 Beneish M-Score 模型中主要体现在哪个指数（AQI）？在分析现金流量表时，研发支出资本化如何人为美化经营现金流（CFO）而转嫁到投资现金流（CFI）？
- **[研发操纵会计魔术与现金流转嫁链]**：
  - **[1. 利润表层面的虚增利润]**：若将研发投入严格“费用化”，研发支出将全额计入当期研发费用，直接扣减当期营业利润与净利润；管理层通过主观判断技术具备“开发阶段可行性”，将巨额研发支出认定为“开发支出”进行“资本化”，该支出不计入利润表，而是变成资产负债表上的“无形资产”，从而人为虚增了数亿元的账面净利润。
  - **[2. 在 Beneish M-Score 中映射为 AQI 恶化]**：AQI 度量的是企业非流动资产中除硬资产（固定资产净额 PP&E）之外的劣质资产比例：
    $$\text{AQ} = 1 - \frac{\text{Current Assets} + \text{Net PP\&E}}{\text{Total Assets}}$$
    当研发支出被大量资本化堆积为“无形资产”或“商誉”时，AQ 指标显著上升，$\text{AQI} = \text{AQ}_t / \text{AQ}_{t-1} \gg 1.0$，直接拉高 M-Score 舞弊评分。
  - **[3. 现金流量表层面的会计转嫁魔术]**：
    - 费用化研发支出在现金流量表中属于“支付给职工以及为职工支付的现金”，严格计入经营活动流出（扣减 CFO）；
    - 资本化研发支出则被列为“购建固定资产、无形资产和其他长期资产支付的现金”，计入**投资活动现金流出（CFI）**；
    - 这一手法不仅美化了利润表，更人为制造了经营活动净现金流（CFO）高增的虚假强劲假象。分析师必须在排雷时将资本化支出强制还原回 CFO。

【Q3 投决会深度解析】
许多造假企业为了配平虚增的营业收入和净利润，通常在资产端做大“存货”或“固定资产在建工程”。如何通过“存货周转天数异常逆势攀升 + 毛利率逆势反常走高”这一经典背离形态，识破其“少结转营业成本虚增当期毛利”的财务操纵手法？
- **[存货蓄水池与营业成本少结转操纵机理]**：
  - **[1. 会计配平恒等式与成本暂存]**：企业营业毛利由收入减成本决定（$\text{Gross Profit} = \text{Revenue} - \text{COGS}$）。为了虚增当期利润，除了直接虚构销售发票，最隐蔽的手法是“少结转营业成本”。管理层将本应属于当期已售产品的生产成本、人工与制造折旧费用，蓄意滞留在资产负债表的“存货”科目中。
  - **[2. 商业常识的根本违背]**：若全行业由于供大于求或需求萎缩，产品滞销导致存货积压，企业的**存货周转天数（Inventory Days）**必然大幅拉长（周转率暴跌）。在正常竞争的市场法则下，库存积压必然伴随着打折促销或降价甩卖，毛利率理应断崖式下挫。
  - **[3. 剪刀差背离确证造假]**：当一家公司的存货周转天数从 60 天反常飙升至 180 天（表明产品根本卖不出去），而同期间报表毛利率却逆势暴涨 10~20 个百分点时，形成了不可调和的逻辑背离。这数学上确证了其通过将生产成本囤积在存货蓄水池中少算当期成本、人为打肿脸充胖子的高危操纵。后续随着存货不得不计提巨额存货跌价准备，企业将面临业绩大暴雷。
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


def calculate_beneish_mscore(prior_data: Dict[str, float], curr_data: Dict[str, float]) -> Dict[str, Any]:
    """
    计算完整的 Beneish M-Score 八变量指标与财务舞弊判别
    """
    # 1. DSRI (Days Sales in Receivables Index)
    dsri = (curr_data["receivables"] / curr_data["sales"]) / (prior_data["receivables"] / prior_data["sales"])

    # 2. GMI (Gross Margin Index)
    gm_prior = (prior_data["sales"] - prior_data["cogs"]) / prior_data["sales"]
    gm_curr = (curr_data["sales"] - curr_data["cogs"]) / curr_data["sales"]
    gmi = gm_prior / gm_curr

    # 3. AQI (Asset Quality Index)
    # AQ = 1 - (Current_Assets + PP&E_net) / Total_Assets
    aq_prior = 1.0 - (prior_data["current_assets"] + prior_data["ppe_net"]) / prior_data["total_assets"]
    aq_curr = 1.0 - (curr_data["current_assets"] + curr_data["ppe_net"]) / curr_data["total_assets"]
    aqi = aq_curr / max(aq_prior, 1e-7)

    # 4. SGI (Sales Growth Index)
    sgi = curr_data["sales"] / prior_data["sales"]

    # 5. DEPI (Depreciation Index)
    depr_rate_prior = prior_data["depreciation"] / (prior_data["depreciation"] + prior_data["ppe_net"])
    depr_rate_curr = curr_data["depreciation"] / (curr_data["depreciation"] + curr_data["ppe_net"])
    depi = depr_rate_prior / max(depr_rate_curr, 1e-7)

    # 6. SGAI (SG&A Expenses Index)
    sgai = (curr_data["sga"] / curr_data["sales"]) / (prior_data["sga"] / prior_data["sales"])

    # 7. LVGI (Leverage Index)
    lev_prior = prior_data["total_debt"] / prior_data["total_assets"]
    lev_curr = curr_data["total_debt"] / curr_data["total_assets"]
    lvgi = lev_curr / max(lev_prior, 1e-7)

    # 8. TATA (Total Accruals to Total Assets)
    tata = (curr_data["net_income"] - curr_data["cfo"]) / curr_data["total_assets"]

    # 线性加权 Beneish M-Score 公式
    m_score = (
        -4.84
        + 0.920 * dsri
        + 0.528 * gmi
        + 0.404 * aqi
        + 0.892 * sgi
        + 0.115 * depi
        - 0.172 * sgai
        + 4.037 * tata
        + 0.0327 * lvgi
    )

    is_suspect = m_score > -1.78

    return {
        "dsri": float(dsri),
        "gmi": float(gmi),
        "aqi": float(aqi),
        "sgi": float(sgi),
        "depi": float(depi),
        "sgai": float(sgai),
        "lvgi": float(lvgi),
        "tata": float(tata),
        "m_score": float(m_score),
        "is_manipulation_suspect": bool(is_suspect)
    }


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 02 参考实现与测试")
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

    assert abs(res_a["dsri"] - 1.0) < 1e-4
    assert abs(res_a["gmi"] - 1.0) < 1e-4
    assert abs(res_a["sgi"] - 1.10) < 1e-4
    assert abs(res_a["tata"] - (-5.0 / 1300.0)) < 1e-4
    assert res_a["m_score"] < -1.78
    assert res_a["is_manipulation_suspect"] is False

    # 2. 激进财务操纵企业样本 (Firm B)
    firm_b_prior = {
        "sales": 1000.0, "cogs": 600.0, "receivables": 100.0,
        "current_assets": 500.0, "ppe_net": 400.0, "total_assets": 1200.0,
        "depreciation": 50.0, "sga": 150.0, "total_debt": 400.0,
        "net_income": 100.0, "cfo": 90.0
    }
    firm_b_curr = {
        "sales": 1500.0, "cogs": 1050.0, "receivables": 350.0,
        "current_assets": 800.0, "ppe_net": 350.0, "total_assets": 1600.0,
        "depreciation": 20.0, "sga": 200.0, "total_debt": 800.0,
        "net_income": 220.0, "cfo": -30.0
    }

    res_b = calculate_beneish_mscore(firm_b_prior, firm_b_curr)
    print("Firm B (操纵嫌疑公司) M-Score 结果:", res_b["m_score"], "疑似造假:", res_b["is_manipulation_suspect"])

    assert abs(res_b["dsri"] - (350.0/1500.0)/(100.0/1000.0)) < 1e-4
    assert abs(res_b["tata"] - (250.0 / 1600.0)) < 1e-4
    assert res_b["m_score"] > -1.78
    assert res_b["is_manipulation_suspect"] is True

    print("Lesson 02 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：大存大贷背后的质押受限、资金虚构与自动化异动监控）：
1. “大存大贷”的反常商业逻辑：
   一家正常经营的企业若手握几十亿真实无限制现金，最理性的行为是偿还高成本债务以节约巨额财务费用，或者进行低风险现金管理。而造假企业之所以“既有巨款又借高利贷”，核心原因在于：
   - 账面货币资金完全是虚构的（银行假流水、假询证函）；
   - 或者账面资金已被大股东挪用、处于不可动用的对外定期存单质押担保状态（质押给银行开具银承汇票用于关联方融资，受限资产未合规披露）；
   - 经营需要真实资金周转，只能硬着头皮向金融机构借入昂贵短期贷款维持日常流动性，形成“利息收入微薄、利息支出惊人”的怪象。
2. 买方量化研究员应构建的跨表监控指标：
   - 货币资金综合收益率 = 利息收入 / 平均货币资金。若该收益率显著低于 7 天通知存款或 1 年期定存基准利率（例如低于 0.8%），极可能存在虚假存款；
   - 存贷利息差倒挂比率 = 利息支出率 - 利息收入率；
   - 净负债与现金比率：(短期借款 + 长期借款) / 货币资金；
   - 受限货币资金占比 = 受限保证金及质押存款 / 总货币资金。

Q2 标准解析（得分要点：研发资本化的魔术手、AQI 资产质量劣质化、跨现金流项目转嫁）：
1. 利润表粉饰：
   研发支出“费用化”会直接计入当期研发费用（EBIT 下降）；而“资本化”则将其确认为开发支出并转入“无形资产”，在当期不体现为费用，而是通过未来多年摊销，从而瞬间人为暴拉当期净利润。
2. Beneish M-Score 模型印证：
   研发资本化会直接推高“非流动无形资产”，使得流动资产与固定资产占总资产比重相对下降，直接导致 AQI（资产质量恶化指数）大幅上升（AQI > 1.0），在 M-Score 中获得正向加分，推升舞弊嫌疑值。
3. 现金流量表魔术：
   研发费用化属于经营活动现金流出（CFO 流出）；而研发支出一旦资本化，按照会计准则将被分类为“购建固定资产、无形资产和其他长期资产支付的现金”，列入投资活动现金流（CFI 流出）。
   因此，研发资本化同时达成了“粉饰净利润”和“美化经营活动现金流 CFO”的双重伪装效果，极具迷惑性。

Q3 标准解析（得分要点：存货与毛利的反常背离、少转成本的造假闭环）：
1. 经典操纵手法——少结转营业成本：
   毛利润 = 营业收入 - 营业成本。企业若虚构高额毛利率，除虚开发票虚构收入外，最常见的隐蔽手段是不结转或少结转营业成本，将本应计入损益表的销售成本挂在资产负债表的“存货”科目中。
2. 存货与毛利背离的量化特征：
   - 行业常识：当行业竞争加剧、产品滞销时，存货周转天数（Inventory Days = 365 * 存货 / 成本）应当拉长，同时伴随打折促销导致毛利率下降；
   - 舞弊异动：若某企业存货周转天数逐年暴增（存货严重滞销积压），但披露的毛利率却匪夷所思地逆势大幅走高甚至超过行业龙头，说明其存货账面价值严重虚高，本质是“将成本沉淀在存货中不予结转”。
   - 最终必然爆发巨额“存货跌价准备计提”或在审计抽盘中演变为“扇贝游走了”式的荒诞财务洗澡。
""")
