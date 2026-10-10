r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 4/5 课
第 4 课：美元指数、汇率弹性与资本流动冲击指数 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么人民币汇率快速贬值（如 USD/CNH 向上突破关键心理关口 7.20 / 7.30）时，往往伴随着北向资金（陆股通）的巨额净流出和 A 股核心资产的剧烈估值踩踏？
- **[外币净值结算与对冲成本约束链]**：
  - **[1. 外币 NAV 核算的汇兑损失]**：绝大多数全球配置型主权财富基金、海外养老金与 ETF（如跟踪 MSCI 中国指数的海外产品）的基准核算币种为美元。当 USD/CNH 汇率快速贬值时，即便 A 股以人民币计价的股价持平，换算成美元净值直接产生汇兑账面亏损。
  - **[2. 远期锁汇对冲成本过高]**：中美利差深度倒挂使得离岸人民币买入远期汇率贴水严重。海外基金若在离岸外汇衍生品市场进行完全对冲（FX Hedging），其对冲成本年化高达 3%~5%，直接吃光权益投资的所有预期超额 Alpha，导致基金经理放弃对冲、选择直接抛售现货减仓。
  - **[3. VaR 风险预算超限引发被动去杠杆]**：汇率波动率飙升导致组合以美元计价的日度风险价值（Value-at-Risk）突破风控硬阈值。按照多资产风险平价与波动率控制准则，量化系统必须无条件强制平仓以压缩权益敞口。
  - **[4. 流动性优先变现陷阱]**：外资在面临被动大单赎回时，无法抛售缺乏流动性的中小盘股票，只能优先在流动性充裕的“核心资产”（贵州茅台、宁德时代、招商银行）上集中打出市价单，造成白马权重股估值倍数的非理性被动下修。

【Q2 投决会深度解析】
什么是跨国套利交易（Carry Trade）？2024年8月初“日元套息交易大崩溃”（Yen Carry Trade Unwind）为什么会在短短几天内引发日经225单日暴跌12%、美股七巨头重挫和全球恐慌指数 VIX 飙升至 65？
- **[跨国低息借贷加杠杆与去杠杆螺旋]**：
  - **[1. 套息交易物理架构]**：过去多年日本央行实施极度宽松的零/负利率政策，全球对冲基金借入几乎零息成本的日元（JPY），并在即期市场卖出日元换成美元，加杠杆配置美股高流动性科技巨头（如英伟达、微软）或墨西哥比索等高息资产，赚取息差与资产资本利得双重收益。
  - **[2. 双重触发点引爆平仓]**：2024年7月底，日本央行出人意料宣布加息至 0.25% 并计划削减购债规模；与此同时美国公布疲软的 7 月非农就业数据引发衰退恐慌，美债收益率骤降，日美利差瞬间大幅收窄。
  - **[3. 日元急剧升值的逼仓踩踏]**：借入日元的套息盘面临严重的借贷本金偿付亏损（日元对美元从 161 快速升值至 141，升幅超 12%）。做空日元的浮亏迫使对冲基金在极短时间内抛售多头资产（美股科技股、日经指数成分股），换回美元再买入日元平仓偿还日元债务。
  - **[4. 连环流动性挤兑]**：这一买入日元平仓的行为反向进一步推高日元汇率，逼迫更多杠杆套息盘爆仓抛售，形成跨国去杠杆清算螺旋，引发全球主要风险资产无差别惨烈闪崩。

【Q3 投决会深度解析】
央行外汇管理工具箱中，“中间价逆周期调节因子（Counter-Cyclical Factor）”、“外汇存款准备金率”与“离岸央票发行”如何通过影响离岸人民币流动性成本来击退空头？在量化微观层面会留下怎样的特征信号？
- **[政策工具箱与微观信号穿透]**：
  - **[1. 中间价逆周期因子锚定市场预期]**：做市商在每日报价时引入逆周期因子，对顺周期情绪导致的单边贬值动量进行数学过滤。量化微观信号：在即期汇率开盘前，每日早间 9:15 披露的人民币对美元汇率中间价显著强于前夜彭博市场模型测算预期（预期差常达到 500~1500 点），向全市场传递央行坚定维稳汇率的强力先验政策信号。
  - **[2. 离岸央票发行抽干离岸做空流动性]**：PBOC 在香港常态化或突发性发行离岸人民币央行票据，直接从香港离岸银行间市场回收 CNH 现款，沉淀在央行账上。量化微观信号：离岸人民币隔夜拆借利率（CNH HIBOR）瞬间脉冲式暴涨（如从 2% 飙升至 10%~20%），空头机构借入离岸人民币砸盘的隔夜展期借贷成本达到不可承受的天价，迫使其主动空头平仓斩仓。
  - **[3. 下调外汇存款准备金率释放外汇供给]**：央行降低金融机构外汇存款准备金率（如由 6% 下调至 4%），直接允许商业银行释放数百亿美元外币现汇流动性，增加国内银行间外汇市场的美元供给，有效缓解美元短缺导致的贬值抛压。
"""

from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd


def calculate_capital_flow_pressure(us_yield: pd.Series, cn_yield: pd.Series, dxy_change: pd.Series) -> pd.Series:
    """
    资本外流压力评分指数:
    Spread_diff = us_yield - cn_yield (美中国债利差倒挂程度, %)
    Pressure = Spread_diff * 0.6 + dxy_change * 0.4
    """
    spread_diff = us_yield - cn_yield
    return spread_diff * 0.6 + dxy_change * 0.4


def calculate_exchange_rate_elasticity(cnh_returns: pd.Series, equity_returns: pd.Series) -> float:
    """
    计算股票资产对人民币汇率变动的弹性系数 (Beta):
        Elasticity = Cov(equity_returns, cnh_returns) / Var(cnh_returns)
    """
    df = pd.DataFrame({"cnh": cnh_returns, "eq": equity_returns}).dropna()
    var_cnh = float(np.var(df["cnh"].values, ddof=1))
    if var_cnh < 1e-12:
        return 0.0
    cov = float(np.cov(df["eq"].values, df["cnh"].values)[0, 1])
    return float(cov / var_cnh)


def compute_composite_cfsi(
    us_yield: pd.Series,
    cn_yield: pd.Series,
    dxy_pct: pd.Series,
    cnh_pct: pd.Series,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[pd.Series, pd.Series]:
    """
    计算多因子综合资本流动冲击指数 (CFSI) 与体制标签:
        Spread = us_yield - cn_yield
        CFSI = w_spread * Spread + w_dxy * dxy_pct + w_cnh * cnh_pct
    状态判定规则:
        - CFSI > 2.0 -> 'Extreme_Shock'
        - 1.0 < CFSI <= 2.0 -> 'Warning'
        - CFSI <= 1.0 -> 'Normal'
    """
    if weights is None:
        weights = {"spread": 0.4, "dxy": 0.3, "cnh": 0.3}

    spread = us_yield - cn_yield
    cfsi = weights["spread"] * spread + weights["dxy"] * dxy_pct + weights["cnh"] * cnh_pct

    regimes = []
    for val in cfsi:
        if val > 2.0:
            regimes.append("Extreme_Shock")
        elif val > 1.0:
            regimes.append("Warning")
        else:
            regimes.append("Normal")

    return cfsi, pd.Series(regimes, index=cfsi.index)


if __name__ == "__main__":
    # ---------------- 基础测试 1: 利差与流动压力 ----------------
    us_y = pd.Series([4.5, 4.8, 5.0])
    cn_y = pd.Series([2.5, 2.4, 2.2])
    dxy_pct = pd.Series([0.5, 1.2, -0.8])
    pressure = calculate_capital_flow_pressure(us_y, cn_y, dxy_pct)
    assert abs(pressure.iloc[0] - (2.0 * 0.6 + 0.5 * 0.4)) < 1e-4, f"压力计算偏差: {pressure.iloc[0]}"
    assert abs(pressure.iloc[1] - (2.4 * 0.6 + 1.2 * 0.4)) < 1e-4, f"压力计算偏差: {pressure.iloc[1]}"

    # ---------------- 基础测试 2: 汇率敏感弹性 ----------------
    np.random.seed(42)
    synth_cnh_ret = pd.Series(np.random.normal(0.2, 0.5, 40))
    synth_eq_ret = -1.5 * synth_cnh_ret + pd.Series(np.random.normal(0.0, 0.1, 40))
    elasticity = calculate_exchange_rate_elasticity(synth_cnh_ret, synth_eq_ret)
    assert -1.7 <= elasticity <= -1.3, f"弹性回归系数应在 -1.7 ~ -1.3 之间, 实际为: {elasticity}"

    # ---------------- 基础测试 3: 综合 CFSI 冲击指数 ----------------
    us_t = pd.Series([3.0, 4.5, 5.2])
    cn_t = pd.Series([2.8, 2.3, 2.0])
    dxy_t = pd.Series([0.2, 1.0, 2.5])
    cnh_t = pd.Series([0.1, 0.8, 2.0])

    cfsi, regimes = compute_composite_cfsi(us_t, cn_t, dxy_t, cnh_t)
    assert cfsi.iloc[0] < 1.0, f"第0期应为平稳常态, 实际为: {cfsi.iloc[0]}"
    assert regimes.iloc[0] == 'Normal', f"预期 Normal, 实际为: {regimes.iloc[0]}"

    assert 1.0 < cfsi.iloc[1] <= 2.0, f"第1期应为预警状态, 实际为: {cfsi.iloc[1]}"
    assert regimes.iloc[1] == 'Warning', f"预期 Warning, 实际为: {regimes.iloc[1]}"

    assert cfsi.iloc[2] > 2.0, f"第2期应为极端冲击, 实际为: {cfsi.iloc[2]}"
    assert regimes.iloc[2] == 'Extreme_Shock', f"预期 Extreme_Shock, 实际为: {regimes.iloc[2]}"

    print("Lesson 04 Answer Verified!")
