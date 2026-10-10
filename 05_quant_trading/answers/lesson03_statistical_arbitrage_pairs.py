r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 3/5 课
第 3 课：统计套利与配对交易 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么两只股票相关系数很高（Correlation = 0.95）并不等同于它们具有协整关系（Cointegration）？请用“醉汉与狗”的比喻和数学差分推导解释伪回归（Spurious Regression）：
- **相关性与协整的数学本质差异**：
  1. 相关性（Correlation）度量的是两个序列在样本期内同期波动的共线性，对非平稳过程来说，只要两只股票都存在单向向上的宏观牛市时间趋势（漂移项），其样本相关系数便可轻易达到 0.90 以上；
  2. 协整（Cointegration）度量的是两个非平稳时间序列是否存在一个长期的、平稳的均衡关系（残差为平稳序列 $I(0)$）。
- **伪回归数学推导**：
  设 $X_t = X_{t-1} + u_t, \; Y_t = Y_{t-1} + v_t$，其中 $u_t, v_t$ 为相互独立的高斯白噪声（无任何因果与联动纽带）。
  直接将 $Y_t$ 对 $X_t$ 回归：$Y_t = \alpha + \beta X_t + e_t$。
  由于非平稳序列的方差随时间 $t$ 线性发散（$\text{Var}(X_t) \propto t$），传统的 OLS 统计推断崩溃，回归分析中 $t$ 统计量发散至无穷大，$R^2$ 虚高，呈现出极高的“伪相关性”。但其残差价差 $e_t$ 本身依然是随机游走过程，方差无限发散，永远不会均值回归。
- **“醉汉与狗”经典比喻（Murray, 1994）**：
  - **高相关无协整**：一个从酒吧出来的醉汉在广场上漫无目的地随机游走，广场另一边的另一个醉汉也在漫无目的地随机游走。由于两人都在被同一阵风吹向广场东北角，两人的轨迹相关系数高达 0.95。但由于两人毫无关联，他们的距离会随时间无限拉大，如果基于此做“距离收敛”套利，投资者将倾家荡产。
  - **协整关系**：醉汉带着一条拴着皮绳的宠物狗。醉汉自己走得跌跌撞撞（$I(1)$ 随机游走），狗也四处乱跑（$I(1)$ 随机游走）。但因为中间有一根弹性皮绳（基本面替代与套利纽带），无论狗跑多远，一旦皮绳绷紧，拉力就会强迫狗拉回醉汉身边。两者的距离（价差）是一个平稳序列（$I(0)$）。这才是配对交易具有统计正期望值的物理本质。

【Q2 深度参考答案】
怎样利用 Ornstein-Uhlenbeck 随机过程拟合价差序列并估算均值回归半衰期（Half-life）？如果拟合出的自回归系数 $b \ge 0$，在统计与交易上意味着什么？
- **OU 连续过程与离散 AR(1) 映射**：
  连续时间 OU 随机微分方程为：
  $$d S_t = \theta (\mu - S_t) dt + \sigma dW_t$$
  其中 $\theta$ 为均值回归速率，$\mu$ 为均衡中心，$\sigma$ 为扩散系数。
  在离散采样时间步长 $\Delta t = 1$（日频）下，积分求解其期望递推：
  $$\mathbb{E}[S_t - \mu \mid S_{t-1}] = (S_{t-1} - \mu) e^{-\theta}$$
  将其改写为差分自回归形式：
  $$\Delta S_t = S_t - S_{t-1} = \mu(1 - e^{-\theta}) + (e^{-\theta} - 1) S_{t-1} + \epsilon_t = a + b S_{t-1} + \epsilon_t$$
  由此建立 OLS 回归模型，自变量为 $S_{t-1}$，因变量为 $\Delta S_t$，回归斜率 $b = e^{-\theta} - 1 \approx -\theta$。
- **半衰期数学计算**：
  当价差偏离均衡水平时，衰减至偏离幅度一半所消耗的时间 $T_{1/2}$ 满足 $e^{-\theta T_{1/2}} = 0.5$。
  两边取自然对数得：
  $$T_{1/2} = \frac{\ln 2}{\theta} = -\frac{\ln 2}{b}$$
- **$b \ge 0$ 的统计与交易学意义**：
  1. 若 $b = 0$，则 $\Delta S_t = a + \epsilon_t$，价差退化为纯随机游走过程（单位根），均值回归引力彻底消失，半衰期为正无穷；
  2. 若 $b > 0$，则 $e^{-\theta} > 1 \implies \theta < 0$，意味着价差偏离均值越远，向外发散的加速度越大，呈现爆炸性发散状态（Explosive Process）；
  3. **实盘交易禁令**：在量化工程中，若某资产对滚动半衰期计算出 $b \ge 0$（或 Half-life $\le 0$），必须立即熔断并禁止开仓。因为此时逆势下注均值回归等于徒手接飞刀，必然遭遇单向无限亏损。

【Q3 深度参考答案】
在 A 股等融券做空受限、借券成本高企的环境下，量化机构如何落地配对交易？（例如行业 ETF 替代、股指期货套保或相对价值多头增强）：
- **国内融券落地摩擦**：
  A 股融券市场存在券源高度稀缺、出借利息昂贵（通常年化 6%~10%）、且存在突发借券召回（Recall Risk）与涨停板无法借券等非对称限制，传统海外“个股对个股一多一空”难以承载大资金容量。
- **工业界三大替代破局路径**：
  1. **纯多头相对价值轮动（Long-Only Relative Value Alpha）**：
     在底仓持有特定行业赛道（如白酒、煤炭、银行）的大型组合中，利用协整 Z-Score 动态调节成份股权重。例如茅台与五粮液协整，当茅台价差相对高估（$Z > 1.5$）时，将原本各 50% 的持仓动态调整为 20% 茅台 + 80% 五粮液；当价差收敛时反向调回。全流程不产生任何做空借券成本，即可无风险提取纯 Alpha 增厚；
  2. **行业 ETF / 龙头股与股指期货（IF/IC/IM）对冲**：
     利用股指期货极具流动性且做空成本极低的优势，寻找与期货标的具有协整关系的特定股票篮子。当基差与一篮子股票价差异常偏离时，做多个股篮子并做空股指期货，构建低交易摩擦的统计套利中性策略；
  3. **可转债（CB）与正股配对套利**：
     可转债具有债券底价与转股期权的天然属性。当市场出现恐慌导致转债价格跌破平价（负转股溢价率）时，做多可转债并利用融券或隔日转股在二级市场抛售锁定收益，实现类无风险统计套利。
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
