r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 4/5 课
第 4 课：美元指数、汇率弹性与资本流动冲击指数 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么人民币汇率快速贬值（如 USD/CNH 向上突破关键心理关口 7.20 / 7.30）时，往往伴随着
北向资金（陆股通）的巨额净流出和 A 股核心资产的剧烈估值踩踏？
- **三重约束下的跨国减配机制**：
  1. **美元本币计价的收益折损与回撤控制**：海外长线资金（全球多资产基金、主权财富基金、养老金）的底层业绩基准通常为
     美元计价（USD-denominated）。即便 A 股以人民币计价未发生大幅波动，汇率贬值 5% 直接导致其美元净值账面缩水 5%。
     当净值逼近内部止损红线时，基金经理触发硬性主动降仓机制。
  2. **外汇风险敞口对冲成本（FX Hedging Cost）暴增**：在抛补利率平价（CIP）框架下，外汇对冲成本本质由跨国利差决定。
     当中美利差深度倒挂（美债收益率 4.5% vs 中债 2.2%），海外对冲基金持有人民币资产的同时做空美元对冲汇率风险的年化对冲成本
     高达 2.5%~3.0%。这一高昂成本直接侵蚀了持有 A 股的全部股息率与超额 Alpha，使资金选择离场观望。
  3. **指数权重股的流动性提款机效应**：北向资金配置高度集中于沪深300和富时中国A50核心权重股（贵州茅台、宁德时代、招商银行等）。
     当外资发生系统性被动流出时，交易算法只能在这些流动性最充裕的核心资产中挂市价单抛售，导致优质龙头遭遇无差别的流动性踩踏。

【Q2 深度参考答案】
什么是跨国套利交易（Carry Trade）？2024年8月初“日元套息交易大崩溃”（Yen Carry Trade Unwind）
为什么会在短短几天内引发日经225单日暴跌12%、美股七巨头重挫和全球恐慌指数 VIX 飙升至 65？
- **高杠杆套利链条与去杠杆正反馈**：
  1. **套利交易物理机制**：过去数十年日本央行长期维持负利率政策（NIRP），日元借贷成本极低且波动率低。
     全球宏观对冲基金与私人银行客户大量借入廉价日元（Funding Currency），在外汇市场抛售兑换为美元，
     并全仓押注于高收益资产（如美债 5%、美股 AI 科技巨头英伟达/微软/苹果、甚至加密货币）。
  2. **多重引线交织引爆**：2024年7月底，日本央行（BOJ）意外宣布加息至 0.25% 并计划削减购债；几乎同一时间，
     美国非农就业数据疲软触发“萨姆规则（Sahm Rule）”引发衰退恐慌，美债收益率暴跌。美日利差瞬间收窄。
  3. **逼空与正反馈强制平仓（Short Squeeze）**：日元兑美元在极短时间内从 161 狂飙升值至 141（日元升值近 12%）。
     所有借日元买美股的套利者遭遇双重暴击：负债端（日元债务）价值暴涨，资产端（美股）下跌。
     券商与做市商下发追加保证金通知（Margin Call）。套利者被迫以任何价格抛售美股资产、买回日元平仓偿还借款。
  4. **全球流动性真空**：这一去杠杆浪潮瞬间吸干了全球主经纪商（Prime Broker）的信贷额度，
     日经指数单日重挫 12.4% 创 1987 年以来最大跌幅，VIX 瞬间冲破 65，演变为典型的现代微观流动性黑天鹅。

【Q3 深度参考答案】
央行外汇管理工具箱中，“中间价逆周期调节因子（Counter-Cyclical Factor）”、“外汇存款准备金率”
与“离岸央票发行”如何通过影响离岸人民币流动性成本来击退空头？在量化微观层面会留下怎样的特征信号？
- **工具箱的作用物理路径与微观特征信号**：
  1. **中间价逆周期调节因子（信号弹与预期锚定）**：
     - 机制：在每日早间 9:15 人民币中间价形成机制中，通过调整模型中的“逆周期因子”，抵消由于前夜离岸贬值情绪带来的顺周期羊群效应，
       引导中间价显著强于市场模型测算的一致预期。
     - 微观信号：中间价与即期模型测算价出现数百基点的大幅偏离（中间价顶格偏强），向全市场传递明确的央行政策底限意志。
  2. **外汇存款准备金率（释放金融机构美元流动性）**：
     - 机制：下调境内金融机构外汇存款准备金率（如由 6% 下调至 4%），直接向境内商业银行体系释放数百亿美元外汇现汇，
       增加在岸外汇市场美元供给，缓解境内结售汇逆差。
  3. **离岸央票发行（抽干离岸空头做空弹药，提高借贷做空成本）**：
     - 机制：中国央行在香港离岸市场常态化或突发增发人民币央行票据（Central Bank Bills）。
       离岸投资者购买央票后，资金直接沉淀在央行账户，直接回收香港离岸市场的离岸人民币资金（CNH Deposits）。
     - 微观特征信号：香港离岸人民币隔夜/短期拆借利率（CNH HIBOR）瞬间从 2% 飙升至 8%~15% 甚至更高。
       由于做空外汇必须先借入 CNH 并卖出，HIBOR 飙升使空头每日隔夜借贷成本（Borrowing Cost）极其高昂，
       形成物理级逼空（Short Squeeze），迫使投机空头止损踩踏砍仓。
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
