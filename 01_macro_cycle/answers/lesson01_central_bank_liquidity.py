r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 1/5 课
第 1 课：央行资产负债表与法币流动性净额传导模型 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么当财政部（Treasury）大幅提高国债发债规模补充 TGA 账户时，如果在逆回购（RRP）池子几乎见底枯竭的情况下，标普500往往承受极其剧烈的下行压制？请从商业银行资产负债表与准备金借贷记账因果链推导：
- **[借贷记账与准备金传导链]**：
  - **[1. 投资者认购与资产流转]**：财政部增发国债时，机构投资者与居民动用商业银行活期存款认购。记账演化：投资者在商业银行的存款负债减少，商业银行在美联储的备付资产——**准备金（Reserves）**被等额划拨转移至财政部在美联储的活期账户——**TGA 账户**。
  - **[2. RRP 缓冲池枯竭的传导恶化]**：当美联储隔夜逆回购（ON RRP）规模充裕时，货币市场基金（MMF）可直接将停留在联储的 RRP 资金取出去买入高息短期国债（T-Bills），资金流由 ON RRP 转移至 TGA，商业银行准备金完全不被损耗；但当 RRP 耗尽至近零水平，财政部发债的所有现金流都必须 100% 由商业银行准备金硬性扣减。
  - **[3. 资产负债表容量收缩]**：准备金骤降导致商业银行流动性覆盖率（LCR）与一级资本充足率边际恶化，一级交易商（Primary Dealers）资产负债表承载力骤减，回购借贷利差（SOFR-IORB Spread）被动走阔。
  - **[4. 权益估值乘数压制]**：非银杠杆机构被迫去杠杆平仓，权益资产 DCF 模型分母端无风险利率与股权风险溢价（ERP）同步飙升，标普500承受严重的系统性估值折现杀跌。

【Q2 投决会深度解析】
2023年美联储虽然持续进行量化紧缩（QT, 缩减资产负债表约 1 万亿美元），但美股（尤其是纳斯达克100）却走出单边大牛市。请利用“Net Liquidity = Assets - TGA - RRP”模型，量化拆解该时期美联储净流动性为何不降反升？
- **[净流动性代数方程拆解]**：
  - **[1. 历史基数与参数变化]**：2022年底，美联储 ON RRP 余额峰值曾超过 2.5 万亿美元，TGA 约为 4500 亿美元，Fed 总资产约为 8.5 万亿美元。
  - **[2. 缩表与泄洪的分项测算]**：2023 全年，美联储资产端按每月 600 亿美债 + 350 亿 MBS 的上限缩减，总资产变动 $\Delta \text{Assets} \approx -1.0$ 万亿美元；然而在负债端，美国财政部发行了海量高收益短期限国库券（T-Bills），促使货币市场基金（MMF）将大量闲置在美联储 ON RRP 的资金疯狂取出并买入国库券，ON RRP 余额在年内从 2.5 万亿断崖式暴跌至 7000 亿美元左右（$\Delta \text{RRP} \approx -1.8$ 万亿美元），TGA 账户仅微幅波动增加约 2000 亿美元（$\Delta \text{TGA} \approx +0.2$ 万亿美元）。
  - **[3. 净流动性代数代入]**：
    $$\Delta \text{Net Liquidity} = \Delta \text{Assets} - \Delta \text{TGA} - \Delta \text{RRP} \approx (-1.0) - (0.2) - (-1.8) = +0.6 \text{ 万亿美元}$$
  - **[4. 结论与商业本质]**：虽然美联储在资产端名义缩表 1 万亿美元，但 ON RRP 这个巨型“场外蓄水池”的泄洪效应完全抵消了紧缩，反向向银行间系统净注入超过 6000 亿美元的超额准备金。净流动性不降反升，驱动以科技七巨头（Magnificent Seven）为核心的估值倍数大扩张。

【Q3 投决会深度解析】
为什么在中国市场，仅仅跟踪央行每日 OMO 逆回购的单日净投放往往是“噪音”，而必须跟踪“超额准备金率（超储率）”、“政府债净缴款”与“DR007/DR001”利差才能真正穿透 A 股的宏观流动性底座？
- **[多层次流动性分层机制]**：
  - **[1. OMO 逆回购的日间平滑属性]**：PBOC 每日开展的 7 天期逆回购主要用于应对税期、跨月或法定缴准等短期脉冲缺口，滚动性极高，体现的是央行防范资金面异常波动的“温度计”，而非中长期流动性扩张趋势。单日净投放百亿往往在下周即等额回笼，属于日频高噪信号。
  - **[2. 超储率决定商业银行放贷底座]**：超额准备金率（超储率）是商业银行扣除法定准备金后自主支配的现金自由水位。当超储率低于 1.2% 的警戒线时，即便央行单日开展 OMO 净投放，大行拆借意愿依然极低，非银机构流动性溢价迅速放大。
  - **[3. 政府债缴款是真实外生抽水因子]**：地方政府专项债与国债发行集中缴款，直接将商业银行在央行的准备金抽离并沉淀为财政国库存款。若央行未能提前通过降准或大额买断式逆回购给予对冲，银行间体系将遭遇实质性流动性失血。
  - **[4. DR007 与信用利差反映真实传导效率]**：DR007 剔除了非银金融机构的信用违约风险，能最纯粹反映银行体系资金成本。当 DR007 持续高于政策利率（7天 OMO 利率）且 R007 - DR007 剪刀差急剧扩大时，代表流动性无法顺畅传导至券商自营、公募基金与两融杠杆，A 股微观流动性格局将遭受实质压制。
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
