r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 1/5 课
第 1 课：央行资产负债表与法币流动性净额传导模型 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么当财政部（Treasury）大幅提高国债发债规模补充 TGA 账户时，如果在逆回购（RRP）池子几乎见底枯竭的情况下，
标普500往往承受极其剧烈的下行压制？请从商业银行资产负债表与准备金的借贷记账法因果链推导：
- **借贷记账与准备金传导链**：
  1. 财政部发债吸收流动性时，一级交易商（Primary Dealers）或居民/机构投资者动用银行活期存款认购国债。
  2. 记账演化：投资者在商业银行的存款负债减少，商业银行在美联储的备付资产——**准备金（Reserves）**
     被划拨进财政部在美联储的账户——**TGA 账户**。
  3. 若美联储隔夜逆回购（ON RRP）规模庞大，货币市场基金（MMF）可以直接将停泊在联储的 RRP 资金取出去买高息短债，
     资金从 RRP 转移至 TGA，商业银行准备金完全不被消耗（净流动性实现缓冲中和）。
  4. 但一旦 RRP 蓄水池耗尽，财政部发债的所有资金都必须硬性由“商业银行准备金”买单。准备金的骤降直接导致
     银行法定/监管资本充足率紧缩、一级交易商资产负债表容量受限，回购利差（SOFR-IORB Spread）抬升。
  5. 交易商与多策略对冲基金被迫减少杠杆融资，权益市场资产估值折现率上升，引发系统性估值压缩与抛售。

【Q2 深度参考答案】
2023年美联储虽然持续进行量化紧缩（QT, 缩减资产负债表约 1 万亿美元），但美股（尤其是纳斯达克100）却走出单边大牛市。
请利用“Net Liquidity = Assets - TGA - RRP”模型，量化拆解该时期美联储净流动性为何不降反升？
- **流动性代数方程拆解**：
  1. 在 2022 年底，美联储 ON RRP 余额峰值曾超过 2.5 万亿美元，TGA 约为 4500 亿美元，Fed 总资产约为 8.5 万亿美元。
  2. 2023 全年，美联储缩表 $\Delta \text{Assets} \approx -1.0$ 万亿美元；但同期，由于财政部集中发行短期国库券（T-Bills）
     且收益率极具吸引力，货币市场基金（MMF）将大量资金从美联储 ON RRP 撤出，认购国库券。
  3. 结果是：ON RRP 余额在 2023 年暴跌了约 1.8 万亿美元（从 2.5 万亿跌至 7000 亿左右），而 TGA 保持在 6000 亿至 7500 亿区间。
  4. 代入公式：
     $$\Delta \text{Net\_Liquidity} = \Delta \text{Assets} - \Delta \text{TGA} - \Delta \text{RRP} \approx (-1.0) - (0.3) - (-1.8) = +0.5 \text{ 万亿美元}$$
  5. 结论：虽然美联储名义上在 QT 缩表，但实质上 ON RRP 这个巨型“货币蓄水池”的开闸放水（Drain），
     完全抵消了 QT 冲击，甚至为金融系统注入了逾 5000 亿美元的净超额准备金，驱动了以科技巨头为核心的估值大狂欢。

【Q3 深度参考答案】
为什么在中国市场，仅仅跟踪央行每日 OMO 逆回购的单日净投放往往是“噪音”，而必须跟踪“超额准备金率（超储率）”、
“政府债净缴款”与“DR007/DR001”利差才能真正穿透 A 股的宏观流动性底座？
- **多层次流动性分层机制**：
  1. **OMO 逆回购的短期平滑属性**：PBOC 每日开展的 7 天期逆回购主要用于对冲日内缴税、跨月流动性波动或跨季考核，
     到期日极短且滚动性强，代表的是央行维持资金面不发生脉冲式缺口的“温度计”，而非中长期流动性趋势。
  2. **超储率决定了银行体系的自由放贷水位**：商业银行持有的超额准备金才是驱动其购买信用债、给非银机构（公募、券商自营）
     拆借资金的弹药库。超储率一旦低于 1.2% 的警戒线，即使 OMO 净投放百亿，非银资金面依然会剧烈紧缩（非银质押溢价放大）。
  3. **政府债缴款是核心外生抽水因子**：地方政府专项债与国债发行集中缴款，直接将商业银行流动性抽离为财政库款，
     若央行不通过降准或降息平抑，银行间市场会出现流动性休克。
  4. **DR007 才是穿透性资金价格**：DR007（存款类金融机构间质押式 7 天回购利率）消除了信用风险溢价，
     当 DR007 持续运行在 PBOC 政策利率（7天 OMO 利率）下方时，代表流动性淤积在银行间体系；
     若溢价扩大且向非银机构传导（R007 - DR007 剪刀差拉大），则表明非银流动性干涸，A 股两融与机构持仓将受到显著负向抑制。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def calculate_fed_net_liquidity(fed_total_assets: pd.Series, tga: pd.Series, rrp: pd.Series) -> pd.Series:
    """
    计算美联储法币净流动性指标序列:
        Net_Liquidity = Fed_Total_Assets - (TGA + RRP)
    """
    df = pd.DataFrame({"assets": fed_total_assets, "tga": tga, "rrp": rrp})
    return df["assets"] - (df["tga"] + df["rrp"])


def compute_liquidity_impulse(net_liquidity: pd.Series, window: int = 4) -> pd.Series:
    """
    计算流动性脉冲 (Liquidity Impulse):
        Impulse_t = ((Net_Liquidity_t - Net_Liquidity_{t-window}) / Net_Liquidity_{t-window}) * 100.0
    """
    return net_liquidity.pct_change(periods=window) * 100.0


def calculate_pboc_net_injection(
    omo_inflow: pd.Series,
    omo_mature: pd.Series,
    mlf_net: pd.Series,
    rrr_cut_release: pd.Series,
) -> pd.Series:
    """
    计算中国央行 (PBOC) 综合流动性净投放 (亿元):
        Net_Injection = (omo_inflow - omo_mature) + mlf_net + rrr_cut_release
    """
    df = pd.DataFrame({
        "omo_in": omo_inflow,
        "omo_mat": omo_mature,
        "mlf": mlf_net,
        "rrr": rrr_cut_release,
    }).fillna(0.0)
    return (df["omo_in"] - df["omo_mat"]) + df["mlf"] + df["rrr"]


def estimate_liquidity_equity_transmission(
    net_liquidity: pd.Series,
    equity_index: pd.Series,
    lag_steps: List[int] = [0, 1, 2, 4],
) -> Dict[str, float]:
    """
    量化评估流动性变化向股票市场传导的时滞 (Transmission Lag) 与弹性 Beta
    """
    d_liq = net_liquidity.diff().dropna()
    d_eq = equity_index.diff().dropna()

    best_lag = 0
    best_corr = 0.0
    best_beta = 0.0

    for lag in lag_steps:
        # 对齐: d_eq 在 t 对应 d_liq 在 t - lag
        if lag == 0:
            s_liq = d_liq
            s_eq = d_eq
        else:
            s_liq = d_liq
            s_eq = d_eq.shift(-lag)

        combined = pd.DataFrame({"liq": s_liq, "eq": s_eq}).dropna()
        if len(combined) < 5:
            continue

        corr = float(combined["liq"].corr(combined["eq"]))
        var_liq = float(np.var(combined["liq"].values, ddof=1))
        if var_liq > 1e-12:
            cov = float(np.cov(combined["liq"].values, combined["eq"].values)[0, 1])
            beta = cov / var_liq
        else:
            beta = 0.0

        if abs(corr) > abs(best_corr):
            best_corr = corr
            best_lag = lag
            best_beta = beta

    return {
        "best_lag": int(best_lag),
        "best_corr": float(best_corr),
        "best_beta": float(best_beta),
    }


if __name__ == "__main__":
    # ---------------- 基础测试 1: 美联储净流动性与脉冲计算 ----------------
    dates = pd.date_range("2024-01-01", periods=5, freq="W")
    assets = pd.Series([77000.0, 76800.0, 76500.0, 76300.0, 76000.0], index=dates)
    tga = pd.Series([7500.0, 7800.0, 8000.0, 8200.0, 8500.0], index=dates)
    rrp = pd.Series([6500.0, 6200.0, 5800.0, 5500.0, 5200.0], index=dates)

    net_liq = calculate_fed_net_liquidity(assets, tga, rrp)
    assert net_liq is not None and len(net_liq) == 5, "Net liquidity 输出长度不符"
    assert net_liq.iloc[0] == 63000.0, f"Expected 63000.0, got {net_liq.iloc[0]}"
    assert net_liq.iloc[4] == 62300.0, f"Expected 62300.0, got {net_liq.iloc[4]}"

    imp = compute_liquidity_impulse(net_liq, window=2)
    expected_imp_idx2 = ((62700.0 - 63000.0) / 63000.0) * 100.0
    assert abs(imp.iloc[2] - expected_imp_idx2) < 1e-4, f"流动性脉冲计算偏差: {imp.iloc[2]}"

    # ---------------- 基础测试 2: PBOC 综合流动性核算 ----------------
    pboc_dates = pd.date_range("2024-03-01", periods=3, freq="D")
    omo_in = pd.Series([1000.0, 500.0, 2000.0], index=pboc_dates)
    omo_mat = pd.Series([800.0, 1200.0, 500.0], index=pboc_dates)
    mlf = pd.Series([0.0, 1000.0, 0.0], index=pboc_dates)
    rrr = pd.Series([5000.0, 0.0, 0.0], index=pboc_dates)

    pboc_net = calculate_pboc_net_injection(omo_in, omo_mat, mlf, rrr)
    assert pboc_net.iloc[0] == 5200.0, f"PBOC 第1天净投放应为 5200, 实际: {pboc_net.iloc[0]}"
    assert pboc_net.iloc[1] == 300.0, f"PBOC 第2天净投放应为 300, 实际: {pboc_net.iloc[1]}"
    assert pboc_net.iloc[2] == 1500.0, f"PBOC 第3天净投放应为 1500, 实际: {pboc_net.iloc[2]}"

    # ---------------- 基础测试 3: 流动性时滞传导模型与 Beta ----------------
    np.random.seed(42)
    t_len = 50
    synth_liq = 60000.0 + np.cumsum(np.random.normal(50.0, 150.0, t_len))
    synth_liq_s = pd.Series(synth_liq)
    # 模拟真实市场中 1 周时滞的传导机制: 股票收益受 t-1 期流动性脉冲驱动
    d_liq = synth_liq_s.diff().fillna(0)
    d_eq = 0.8 * d_liq.shift(1).fillna(0) + np.random.normal(0, 10.0, t_len)
    synth_eq_s = pd.Series(5000.0 + np.cumsum(d_eq))

    metrics = estimate_liquidity_equity_transmission(synth_liq_s, synth_eq_s, lag_steps=[0, 1, 2])
    assert metrics["best_lag"] == 1, f"应成功识别滞后1期为最佳传导时滞, 实际检测为: {metrics['best_lag']}"
    assert metrics["best_corr"] > 0.7, f"最佳滞后相关性应大于0.7, 实际为: {metrics['best_corr']}"
    assert 0.6 <= metrics["best_beta"] <= 1.0, f"最佳 Beta 应在 0.6~1.0 之间, 实际为: {metrics['best_beta']}"

    print("Lesson 01 Answer Verified!")
