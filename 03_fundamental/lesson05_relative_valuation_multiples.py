"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 5/5 课
第 5 课：相对估值乘数体系、行业特化估值与横截面均值回归评分引擎
================================================================================

【考核标准】
- 代码填空并通过所有自动化断言：4 分
- Q1~Q3 深度思考题回答完整、逻辑严谨（各 2 分）：共 6 分
- 合格线：8/10 分

【理论精讲】
1. 相对估值乘数的第一性原理：
   相对估值（Relative Valuation）依托“一价定律（Law of One Price）”，通过可比资产的市场交易价格来推导目标资产的相对价值。
   核心估值乘数家族：
   - PE (市盈率 = 市值 / 净利润): 适用于盈利稳定、商业模式成熟、资本结构相似的消费与蓝筹股。
   - PB (市净率 = 市值 / 净资产): 适用于重资产制造、周期品与金融机构（银行、券商、保险）。
     核心数理纽带：PB-ROE 框架：P/B = (ROE - g) / (Ke - g)。高 ROE 理应享受高 PB 溢价。
   - PS (市销率 = 市值 / 营业收入): 适用于高增长但尚未盈利的 SaaS、Biotech 或处于价格战抢份额期的互联网平台。
   - EV/EBITDA (企业价值倍数): EV = 市值 + 有息负债 - 现金。
     剔除了资本结构（负债率不同导致的利息差异）与折旧摊销政策（税法与会计年限差异）的影响，是跨国并购与重工业对比的标准工具。
   - PEG (市盈率相对盈利增长比率): PEG = PE / (净利润长期预期年化增速 × 100)。
     彼得·林奇经典准则：PEG < 1.0 具备安全边际（GARP 策略）；PEG > 2.0 估值透支。

2. 周期股与成长股的估值特化：
   - 强周期股的“估值反转定律”：
     由于利润呈现暴利到巨亏的剧烈正弦波动，在景气顶峰利润爆表时，PE 往往只有 2~3 倍（低估假象实为历史大顶）；在景气冰点全行业亏损时，PE 畸高或为负数（实为周期大底）。
     周期股严禁看静态低 PE 买入，必须锚定 PB 分位数、重置成本或周期归一化利润（Through-the-Cycle Normalized Earnings）。
   - 高成长股的估值特化：
     软件与 SaaS 行业采用“40法则”（Rule of 40 = 营收增速 + FCF Margin >= 40%），并采用前瞻动态远期 EV/Sales 折算。

3. 横截面相对估值偏离度与均值回归评分：
   在量化多因子与基本面多头策略中，不能简单对比绝对估值大小，而必须在申万/GICS 细分行业横截面内计算“相对偏离度”：
   - 使用标准化 Z-Score 或分位数排名（Percentile Rank）消除量纲；
   - 结合基本面质量指标（ROE、资产负债率、现金流覆盖度）进行“质量过滤”，剔除“因质次而便宜”的价值陷阱（Value Trap）；
   - 输出行业均值回归潜力得分（Mean Reversion Potential Score, 0~100 分）。

【三个思考题 (Q1~Q3)】
Q1: 周期股“估值反转之谜”：为什么周期股（如航运中远海控、生猪养殖牧原股份、钢铁水泥）在市盈率极低（PE=2~3倍）时往往是股价周期的历史大顶，而在全行业巨亏导致 PE 畸高或为负数时反而是绝佳买点？买方机构在不同周期阶段应选用哪种估值框架（PB-ROE、重置成本或周期归一化盈利 Normalized Earnings）？
Q2: 银行与金融机构的“破净”常态：国内多数大中型商业银行长期处于 0.4~0.6 倍 PB 的深度折价状态。从财务与风险定价角度，这种低 PB 是否意味着估值严重低估？市场折价究竟反映了对银行“真实资产质量/不良贷款确认延后”以及“净息差（NIM）收窄与资本补充压力”的何种悲观预期？
Q3: 相对估值的横截面陷阱（Cross-sectional Trap）：“便宜的股票往往有便宜的理由（Value Trap）”。如何在量化相对估值模型中有效剔除“价值陷阱”？请结合 ROIC、利息保障倍数与盈利下修动量（Earnings Revisions）说明防御机制。
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
