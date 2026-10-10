"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 5/5 课
参考实现与标准问答解析
第 5 课：相对估值乘数体系、行业特化估值与横截面均值回归评分引擎
================================================================================
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
    """
    pe = market_cap / net_income
    pb = market_cap / book_equity
    ps = market_cap / revenue
    ev = market_cap + total_debt - cash
    ev_ebitda = ev / ebitda
    peg = pe / (earnings_growth_rate * 100.0)

    return {
        "pe": float(pe),
        "pb": float(pb),
        "ps": float(ps),
        "ev": float(ev),
        "ev_ebitda": float(ev_ebitda),
        "peg": float(peg)
    }


def cross_sectional_valuation_scoring(
    peer_df: pd.DataFrame,
    target_ticker: str
) -> Dict[str, Any]:
    """
    行业横截面相对估值偏离度计算与均值回归评分引擎
    """
    if target_ticker not in peer_df["ticker"].values:
        raise ValueError(f"标的代码 {target_ticker} 不在行业对标样本池中")

    target_row = peer_df[peer_df["ticker"] == target_ticker].iloc[0]

    # 计算各指标均值与总体标准差 (ddof=0)
    pe_mean, pe_std = peer_df["pe"].mean(), peer_df["pe"].std(ddof=0)
    pb_mean, pb_std = peer_df["pb"].mean(), peer_df["pb"].std(ddof=0)
    ev_mean, ev_std = peer_df["ev_ebitda"].mean(), peer_df["ev_ebitda"].std(ddof=0)

    z_pe = (target_row["pe"] - pe_mean) / max(pe_std, 1e-6)
    z_pb = (target_row["pb"] - pb_mean) / max(pb_std, 1e-6)
    z_ev_ebitda = (target_row["ev_ebitda"] - ev_mean) / max(ev_std, 1e-6)

    # 综合估值 Z 分数 (权重: PE 40%, PB 30%, EV/EBITDA 30%)
    composite_val_z = 0.4 * z_pe + 0.3 * z_pb + 0.3 * z_ev_ebitda

    # 质量过滤条件: ROE 不低于行业中位数，且产权比率不高于行业中位数
    median_roe = peer_df["roe"].median()
    median_debt_to_equity = peer_df["debt_to_equity"].median()

    quality_pass = bool(
        (target_row["roe"] >= median_roe) and
        (target_row["debt_to_equity"] <= median_debt_to_equity)
    )

    # 均值回归评分 (基准 50 分，偏离度反向加减，质量过滤加减 15 分)
    raw_score = 50.0 - (composite_val_z * 20.0) + (15.0 if quality_pass else -15.0)
    reversion_score = float(np.clip(raw_score, 0.0, 100.0))

    return {
        "target_ticker": str(target_ticker),
        "z_pe": float(z_pe),
        "z_pb": float(z_pb),
        "z_ev_ebitda": float(z_ev_ebitda),
        "composite_valuation_z": float(composite_val_z),
        "quality_pass": quality_pass,
        "reversion_score": float(reversion_score)
    }


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 05 参考实现与测试")
    print("=" * 60)

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

    assert abs(mults["pe"] - 20.0) < 1e-4
    assert abs(mults["pb"] - 2.0) < 1e-4
    assert abs(mults["ps"] - 1.25) < 1e-4
    assert abs(mults["ev"] - 1200.0) < 1e-4
    assert abs(mults["ev_ebitda"] - 10.0) < 1e-4
    assert abs(mults["peg"] - 0.8) < 1e-4

    peer_data = pd.DataFrame([
        {"ticker": "000001", "pe": 25.0, "pb": 3.0, "ev_ebitda": 14.0, "roe": 0.12, "debt_to_equity": 0.8},
        {"ticker": "000002", "pe": 20.0, "pb": 2.5, "ev_ebitda": 11.0, "roe": 0.15, "debt_to_equity": 0.5},
        {"ticker": "000003", "pe": 15.0, "pb": 1.8, "ev_ebitda": 8.0,  "roe": 0.18, "debt_to_equity": 0.4},
        {"ticker": "000004", "pe": 30.0, "pb": 4.0, "ev_ebitda": 16.0, "roe": 0.14, "debt_to_equity": 0.9},
        {"ticker": "000005", "pe": 12.0, "pb": 1.2, "ev_ebitda": 6.0,  "roe": 0.05, "debt_to_equity": 1.5},
    ])

    score_03 = cross_sectional_valuation_scoring(peer_data, "000003")
    print("标的 000003 (优质低估) 评分结果:", score_03)

    assert score_03["composite_valuation_z"] < 0
    assert score_03["quality_pass"] is True
    assert score_03["reversion_score"] >= 75.0

    score_05 = cross_sectional_valuation_scoring(peer_data, "000005")
    print("标的 000005 (价值陷阱) 评分结果:", score_05)
    assert score_05["quality_pass"] is False
    assert score_05["reversion_score"] < score_03["reversion_score"]

    print("Lesson 05 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：周期盈利的剧烈振荡、PE的周期倒挂与重置成本/PB-ROE锚定）：
1. 为什么周期股在 PE 极低时是历史大顶：
   - 强周期行业（如海运、大宗化工、生猪养殖）受宏观供需错配驱动，在供需极度短缺时运价/产品价格呈现非线性暴涨；
   - 此时全行业企业开足马力生产，录得数倍于历史均值的暴利，导致静态 PE 迅速被压缩至 2~3 倍；
   - 然而，暴利必然刺激全行业天量产能开工或新增造船订单，供求格局即将从短缺走向严重过剩。资本市场具有超前 6~12 个月定价机制，在业绩最辉煌时股价早已见顶崩跌；
   - 随之而来的是产品价格崩塌、产能过剩与巨额存货/资产减值，利润归零甚至巨亏，PE 飙升至数百倍或为负数（此时全行业减产出清，反而是周期的黎明大底）。
2. 买方专业估值框架：
   - 在周期底部与下行期：坚决弃用 PE，改用 PB-ROE（观察破净程度与资产重置成本 Replacement Cost）；
   - 在全周期平滑分析中：采用“周期归一化盈利”（Through-the-Cycle Normalized Earnings = 长期平均产销量 × 长期平均毛利 - 正常期间费用），以归一化 PE 判断长期内在价值。

Q2 标准解析（得分要点：银行高杠杆对不良资产的放大效应、未暴露隐性坏账与真实ROE折价）：
1. 银行高杠杆与账面净资产的真实性：
   - 商业银行本质是 10~12 倍高杠杆运营的金融中介（总资产是净资产的 10 倍以上）；
   - 若一家银行总资产中有 2% 的贷款彻底成为死账（坏账穿透），其损失将直接冲销 20%~25% 的股东净资产！
2. 市场给予 0.4~0.6 倍 PB 深度折价的核心定价逻辑：
   - 市场在用真金白银给银行资产负债表上的隐性不良资产打折：投资者认为银行官方披露的不良率（NPL，通常 1.2%~1.5%）未完全反映延期还本付息、关注类贷款或地方融资平台的潜在实质性违约风险；
   - 长期低利率环境下净息差（NIM）持续收窄，资产端收益率下行而负债端存款成本粘性较强，压制长期真实 ROE 预期；
   - 资本补充压力与分红不确定性：随着严格的巴塞尔协议与核心一级资本充足率要求，部分内生资本不足的银行面临被动配股或减税再融资风险。

Q3 标准解析（得分要点：价值陷阱的典型形态、量化防爆雷机制）：
1. 价值陷阱（Value Trap）的典型征兆：
   - 表面极低 PE/PB，但主营业务属于技术淘汰落后产能（如传统胶片、燃油车落后部件）；
   - 盈利能力（ROIC）长期低于资本成本 WACC，且持续恶化；
   - 负债率高企且短期债务压顶（利息保障倍数 < 2.0）；
   - 卖方一致预期盈利预测（Consensus Forecast）持续被大幅下修（Negative Earnings Revision Momentum）。
2. 量化相对估值中的防御机制：
   - 引入“质量因子门槛”（Quality Screening）：只在 ROIC > 12%、毛利率稳定、经营现金流/净利润 > 0.8 的池子中寻找低估标的；
   - 负债安全边际剔除：扣除债务偿付能力极弱（Debt/Equity > 行业 80 分位数 或 EBITDA 利息保障倍数极低）的垃圾资产；
   - 动量与分析师预期过滤：排除最近 3 个月分析师净下调盈利超过 10% 的股票，避免买在“基本面恶化未止”的半山腰。
""")
