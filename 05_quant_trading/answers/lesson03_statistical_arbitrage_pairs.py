r"""
================================================================================
模块 05：量化投资多因子与统计套利 · 第 3/5 课
第 3 课：统计套利与配对交易：协整检验与 OU 均值回归过程 (参考答案版)
================================================================================

【Q1 深度参考答案】
伪相关（Spurious Correlation）与协整（Cointegration）的本质对立：两只股票的价格序列相关系数可能高达 0.98，但它们为什么在配对套利中仍然可能会导致毁灭性的单边发散穿仓？请从单位根过程 $I(1)$ 与均值平稳 $I(0)$ 的鞅性质推导 Engle-Granger 协整检验的第一性原理。
- **[单位根非平稳时间序列的伪回归幻觉]**：绝大多数资产价格序列 $P_t$ 是具有随机游走漂移的非平稳一阶单整序列 $I(1)$。两个完全无关的 $I(1)$ 序列（例如“中国降雨量”与“标普500指数”），若同时存在确定性时间趋势项，直接计算皮尔逊相关系数往往会得出高达 0.9 甚至 0.99 的荒谬伪相关性（Granger & Newbold, 1974）。基于伪相关的价差其方差随着时间 $t$ 线性无界发散，根本不存在回归均值的物理向心力。
- **[协整检验的经济物理本质]**：协整关系要求存在唯一的线性和对冲比率 $\beta$，使得两者的线性组合残差 $\epsilon_t = P_A - \beta P_B$ 彻底消除单位根，降维为严格平稳的零阶单整序列 $I(0)$。平稳时间序列意味着其期望均值、自协方差均不随时间漂移，受到物理弹性皮筋的强力约束。
- **[Engle-Granger 检验的严谨逻辑]**：通过 OLS 拟合长期均衡方程，并对残差执行增强迪基-富勒检验（ADF Test）。只有当检验统计量显著击穿临界值（$p < 0.05$）、数学上完全拒绝“残差服从单位根随机游走”的原假设时，策略才能确信该资产对子具备长期均值回归的套利可行性。

【Q2 深度参考答案】
Ornstein-Uhlenbeck (OU) 均值回归速率 $\theta$ 与半衰期 $T_{\text{half}}$ 的资金管理约束：在套利交易中，若通过 AR(1) 离散化估算的价差半衰期高达 120 个交易日，为什么该配对对于高换手量化基金而言是“不可交易的”？持仓时间过长会引入哪些致命的宏观体制漂移风险？
- **[资金时间价值与年化复合收益率杀伤]**：半衰期是指价差偏离收敛回均值一半所需的平均时间。若 $T_{\text{half}} = 120$ 天，意味着一次完整的套利建仓到平仓往往需要 6~12 个月。即使单笔交易能斩获 3% 的毛利，年化下来资金收益率仅有可怜的 3%~5%，扣除两融借券成本与交易费用后收益几乎归零，严重违背量化基金追求高资金周转率的商业目标。
- **[宏观经济体制漂移（Regime Shift）风险]**：金融市场的基本面环境不是静态常数。在长达半年的持仓周期中，极易遭遇央行突发加息降息、行业产业政策突变、关税壁垒调整等宏观体制突变。原本假定恒定的对冲比率 $\beta$ 在长周期中会发生严重漂移，静态模型将被彻底摧毁。
- **[对冲基金的可交易边界]**：实盘量化统计套利通常严格规定：资产对子的半衰期必须受控在 5 至 20 个交易日之间。唯有在此黄金区间内，策略才能在高周转率、充足样本频次与稳健均值回归之间取得最优的年化夏普比率（Sharpe > 2.0）。

【Q3 深度参考答案】
协整关系破裂（Structural Break）与硬止损断路器：当配对价差突破 $+3.5\sigma$ 时，数学期望告诉你这是“更佳的加仓做空均值回归机会”，但对冲基金风控手册为何强制要求在此处无条件截断止损？请列举导致协整关系不可逆永久断裂的企业基本面事件（如私有化要约收购、破产重组、核心技术专利被废）。
- **[极端离群值背后的结构性断裂（Structural Break）]**：在正态或稳健分布下，价差突破 3.5 倍标准差的理论概率不足 0.05%。在实盘交易中，一旦价格击穿 $3.5\sigma$，绝非简单的“情绪过度悲观”，而是大概率预示着底层的协整物理基底已经发生永久性断裂，历史参数 $\beta$ 和 $\mu$ 瞬间作废。
- **[企业微观黑天鹅事件列举]**：
  1. **溢价并购与私有化要约**：标的公司突发收到溢价 40% 的现金私有化要约，其股价瞬间跳空并被牢牢锁定在要约价附近，而对手方资产保持不动，价差永远不会再回归；
  2. **债务违约与破产重组**：配对中的某家公司突发暴雷进入破产清算，股票进入无底洞暴跌停牌，做多端本金永久损失；
  3. **核心专利被废或反垄断制裁**：公司的核心商业壁垒被瞬间摧毁，导致其长期 ROIC 发生断崖式下移，与对标竞品的盈利能力永久脱钩。
- **[硬止损断路器的投委会铁律]**：量化统计套利的生存底线是“承认模型的认知边界”。当市场以 $3.5\sigma$ 的暴力脱锚向你发出预警时，必须无条件执行止损斩仓，将亏损截断在可承受范围内，严禁主观死扛或加杠杆补仓。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：尊重结构断裂，严禁向破裂的均值下注</div>
  <div class="callout-body">
    任何统计套利模型都建立在过去经验平稳的假设上。当微观现实打破历史平稳性时，死守数理公式只会招致灭顶之灾。唯有无条件止损才能在极端黑天鹅频发的市场中活到最后。
  </div>
</div>
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def engle_granger_cointegration_test(
    price_a: pd.Series,
    price_b: pd.Series,
) -> Dict[str, Any]:
    """
    Engle-Granger 两步法协整检验
    """
    df = pd.concat([price_a.rename("pa"), price_b.rename("pb")], axis=1).dropna()
    log_a = np.log(df["pa"].values)
    log_b = np.log(df["pb"].values)
    n = len(log_a)

    # Step 1: OLS 回归 log(P_A) = alpha + beta * log(P_B) + e
    X = np.column_stack([np.ones(n), log_b])
    beta_hat, _, _, _ = np.linalg.lstsq(X, log_a, rcond=None)
    alpha = float(beta_hat[0])
    hedge_ratio = float(beta_hat[1])

    # 残差价差序列
    spread = log_a - (alpha + hedge_ratio * log_b)
    spread_series = pd.Series(spread, index=df.index)

    # Step 2: ADF 平稳性检验
    adf_res = adfuller(spread, autolag="AIC")
    adf_stat = float(adf_res[0])
    p_val = float(adf_res[1])
    is_coint = bool(p_val < 0.05)

    return {
        "hedge_ratio": hedge_ratio,
        "intercept": alpha,
        "spread": spread_series,
        "adf_statistic": adf_stat,
        "p_value": p_val,
        "is_cointegrated": is_coint,
    }


def estimate_ou_half_life(spread: pd.Series) -> float:
    """
    基于离散 Ornstein-Uhlenbeck (OU) 过程估算价差均值回归半衰期
    """
    s = spread.dropna().values
    if len(s) < 10:
        return float("inf")

    delta_s = np.diff(s)
    s_lag = s[:-1]

    X = np.column_stack([np.ones_like(s_lag), s_lag])
    beta_hat, _, _, _ = np.linalg.lstsq(X, delta_s, rcond=None)
    b = float(beta_hat[1])

    if b >= 0.0:
        return float("inf")

    # Half-life = -ln(2) / b
    half_life = -float(np.log(2.0) / b)
    return half_life


def backtest_pairs_trading_strategy(
    price_a: pd.Series,
    price_b: pd.Series,
    hedge_ratio: float,
    window: int = 30,
    z_open: float = 1.5,
    z_exit: float = 0.2,
    z_stop: float = 3.5,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    基于滚动 Z-Score 的配对交易策略回测引擎
    """
    df = pd.concat([price_a.rename("pa"), price_b.rename("pb")], axis=1).dropna()
    dates = df.index
    n = len(df)

    log_a = np.log(df["pa"])
    log_b = np.log(df["pb"])
    spread = log_a - hedge_ratio * log_b

    roll_mean = spread.rolling(window=window).mean()
    roll_std = spread.rolling(window=window).std()
    zscore = (spread - roll_mean) / roll_std

    # 生成持仓信号状态机
    positions = np.zeros(n)
    curr_pos = 0

    for t in range(window, n):
        z = zscore.iloc[t]
        if np.isnan(z):
            continue

        # 止损检测
        if abs(z) >= z_stop:
            curr_pos = 0
        elif curr_pos == 0:
            if z > z_open:
                curr_pos = -1  # 做空价差: 空 A 多 B
            elif z < -z_open:
                curr_pos = 1   # 做多价差: 多 A 空 B
        elif curr_pos == 1:
            if z >= -z_exit:
                curr_pos = 0   # 均值回归平仓
        elif curr_pos == -1:
            if z <= z_exit:
                curr_pos = 0   # 均值回归平仓

        positions[t] = curr_pos

    # 执行信号必须滞后 1 期以防止前视未来偏差
    pos_series = pd.Series(positions, index=dates).shift(1).fillna(0)

    # 资产单日收益率
    ret_a = df["pa"].pct_change().fillna(0.0)
    ret_b = df["pb"].pct_change().fillna(0.0)
    spread_ret = ret_a - hedge_ratio * ret_b
    strat_ret = pos_series * spread_ret

    # 绩效度量
    cum_ret = (1.0 + strat_ret).cumprod()
    total_ret = float(cum_ret.iloc[-1] - 1.0)
    ann_ret = float(strat_ret.mean() * annual_periods)
    ann_vol = float(strat_ret.std(ddof=1) * np.sqrt(annual_periods))
    sharpe = float(ann_ret / ann_vol) if ann_vol > 1e-12 else 0.0

    # 最大回撤
    roll_max = cum_ret.cummax()
    dd = (cum_ret - roll_max) / roll_max
    max_dd = float(dd.min())

    return {
        "zscore": zscore,
        "positions": pos_series,
        "daily_returns": strat_ret,
        "total_return": total_ret,
        "annualized_return": ann_ret,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 03: 统计套利与配对交易单元测试 (参考答案版)")
    print("=" * 70)

    np.random.seed(42)
    n_days = 500
    dates = pd.date_range("2023-01-01", periods=n_days, freq="B")

    macro_trend = np.cumsum(np.random.normal(0, 0.01, n_days))

    true_hedge_ratio = 1.2
    theta_true = 0.08
    spread_ou = np.zeros(n_days)
    for t in range(1, n_days):
        spread_ou[t] = spread_ou[t - 1] - theta_true * spread_ou[t - 1] + np.random.normal(0, 0.015)

    log_pb = 4.0 + macro_trend
    log_pa = 1.0 + true_hedge_ratio * log_pb + spread_ou
    price_a_series = pd.Series(np.exp(log_pa), index=dates)
    price_b_series = pd.Series(np.exp(log_pb), index=dates)

    coint_res = engle_granger_cointegration_test(price_a_series, price_b_series)
    print(f"估计对冲比率 Hedge Ratio: {coint_res['hedge_ratio']:.4f}")
    print(f"ADF 统计量: {coint_res['adf_statistic']:.4f}, p 值: {coint_res['p_value']:.4e}")
    print(f"是否显著协整: {coint_res['is_cointegrated']}")

    assert coint_res["is_cointegrated"] is True, "两资产应通过 95% 置信度协整检验"
    assert abs(coint_res["hedge_ratio"] - true_hedge_ratio) < 0.25, "对冲比率估计偏差过大"

    half_life = estimate_ou_half_life(coint_res["spread"])
    print(f"估算的价差均值回归半衰期 Half-life: {half_life:.2f} 天")
    assert 5.0 <= half_life <= 15.0, f"半衰期估算应在 5~15 天范围内, 实际: {half_life:.2f}"

    bt_res = backtest_pairs_trading_strategy(
        price_a_series,
        price_b_series,
        hedge_ratio=coint_res["hedge_ratio"],
        window=30,
        z_open=1.5,
        z_exit=0.2,
        z_stop=3.5,
    )

    print(f"配对策略累计收益率: {bt_res['total_return']*100:.2f}%")
    print(f"年化收益率: {bt_res['annualized_return']*100:.2f}%")
    print(f"年化夏普比率: {bt_res['sharpe_ratio']:.2f}")
    print(f"最大回撤: {bt_res['max_drawdown']*100:.2f}%")

    assert bt_res["total_return"] > 0.30, f"协整套利策略累计收益应大于 30%, 实际: {bt_res['total_return']*100:.2f}%"
    assert bt_res["sharpe_ratio"] > 1.20, f"夏普比率应大于 1.20, 实际: {bt_res['sharpe_ratio']:.2f}"
    assert -0.25 < bt_res["max_drawdown"] < 0.0, f"最大回撤控制应优于 -25%, 实际: {bt_res['max_drawdown']*100:.2f}%"

    print("Lesson 03 参考答案测试全部通过 (Exit Code 0)！")
