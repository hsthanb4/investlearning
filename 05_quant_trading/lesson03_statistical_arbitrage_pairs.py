r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 3/5 课
第 3 课：统计套利与配对交易 (Statistical Arbitrage & Pairs Trading)
================================================================================

【课程定位与第一性原理】
在现代量化投资与对冲基金体系中，配对交易（Pairs Trading）被誉为市场中性（Market-Neutral）策略的鼻祖。
其核心思想源自 1980 年代摩根士丹利（Morgan Stanley）量化团队：寻找具有深层经济学绑定关系或共同基本面驱动
的两只资产（如贵州茅台 vs 五粮液，可口可乐 vs 百事可乐，中国神华 vs 陕西煤业）。

1. 协整理论与伪回归（Cointegration & Spurious Regression）：
   - 两项资产的时间序列价格本身通常是非平稳的单位根过程：$P_A, P_B \sim I(1)$（一阶单整）；
   - 简单的价格相关系数（Correlation）可能高达 0.95，但这可能仅仅是由大盘整体牛市的时间趋势驱动；若两者不具备真正的协整纽带，
     其价差可能发生单向发散，盲目逆势加仓将遭遇无限爆仓亏损；
   - 诺贝尔经济学奖 Granger 协整理论：若存在线性组合使得残差价差序列平稳：
     $$e_t = \ln(P_{A,t}) - \alpha - \beta \ln(P_{B,t}) \sim I(0)$$
     则称两资产 $(P_A, P_B)$ 存在 $(1, 1)$ 阶协整关系，$\beta$ 为理论最优对冲比率（Hedge Ratio）。

2. 连续均值回归模型：Ornstein-Uhlenbeck (OU) 过程与半衰期（Half-life）：
   - 价差波动建模为一维随机微分方程（SDE）：
     $$d S_t = \theta (\mu - S_t) dt + \sigma dW_t$$
     其中 $\theta$ 为均值回归速度参数，$\mu$ 为长期均衡价差，$\sigma$ 为扩散波动率，$W_t$ 为标准布朗运动；
   - 离散化自回归估计（AR(1) 形式）：
     $$\Delta S_t = S_t - S_{t-1} = a + b S_{t-1} + \epsilon_t$$
     其中回归斜率 $b = -(1 - e^{-\theta \Delta t}) \approx -\theta \Delta t$；
   - 均值回归半衰期（Half-life）：
     $$T_{1/2} = \frac{\ln 2}{\theta} = -\frac{\ln 2}{b}$$
     半衰期衡量价差偏离后回归中枢一半所需的预期交易日天数。若半衰期过长（如 > 60日），资金周转率极低；
     若 $b \ge 0$，表明价差发散，均值回归失效。

3. 动态标准化 Z-Score 套利策略机制：
   - 滚动 Z-Score：$Z_t = \frac{S_t - \text{MA}(S_t, W)}{\text{STD}(S_t, W)}$；
   - 交易状态机：
     - $Z_t > z_{\text{open}}$: 价差极端高估，做空 A 同时做多 B（持仓头寸 -1）；
     - $Z_t < -z_{\text{open}}$: 价差极端低估，做多 A 同时做空 B（持仓头寸 +1）；
     - $|Z_t| \le z_{\text{exit}}$: 价差回归均值，平仓锁定利润（持仓头寸 0）；
     - $|Z_t| \ge z_{\text{stop}}$: 异常单向发散突破阈值，触发硬性止损平仓（防止基本面逻辑解绑）。

【核心流程与心智模型】
```mermaid
stateDiagram-v2
    [*] --> 空仓观望 (Position=0)
    
    空仓观望 (Position=0) --> 做空价差 (Short Spread: -1): Z > +z_open (价差高估)
    空仓观望 (Position=0) --> 做多价差 (Long Spread: +1): Z < -z_open (价差低估)
    
    做空价差 (Short Spread: -1) --> 空仓观望 (Position=0): Z <= +z_exit (均值回归平仓)
    做空价差 (Short Spread: -1) --> 止损出局 (Stop Loss: 0): Z >= +z_stop (协整破裂硬止损)
    
    做多价差 (Long Spread: +1) --> 空仓观望 (Position=0): Z >= -z_exit (均值回归平仓)
    做多价差 (Long Spread: +1) --> 止损出局 (Stop Loss: 0): Z <= -z_stop (协整破裂硬止损)
    
    止损出局 (Stop Loss: 0) --> 空仓观望 (Position=0): 等待下一轮重新检验协整
```

【工业界实战场景与风控陷阱】
1. 协整关系破裂（Cointegration Breakdown）与黑天鹅分化：
   历史协整并不保证未来协整。当其中一家公司突发专利暴雷、高管被捕、核心产品被颠覆（如当年柯达 vs 富士）时，
   两者基本面发生永久性结构断裂。若无硬性止损保护，逆势策略将蒙受毁灭性损失。
2. 腿部执行风险（Execution Legging Risk）与流动性冲击：
   配对交易必须同时对双边资产下单。在市场剧烈波动时，一边成交而另一边卡单可能导致“被动裸多/裸空”。
3. 借券做空成本与融券受限：
   国内 A 股市场融券券源稀缺且年化借券利息高达 6%~10%。实盘中量化机构往往采用“行业 ETF / 指数期货多头替代”或
   “双向相对价值多头轮动”（调仓增配低估股、减配高估股）来规避裸空限制。

【思考题】
Q1: 为什么两只股票相关系数很高（Correlation = 0.95）并不等同于它们具有协整关系（Cointegration）？请用“醉汉与狗”的比喻和数学差分推导解释伪回归（Spurious Regression）。
Q2: 怎样利用 Ornstein-Uhlenbeck 随机过程拟合价差序列并估算均值回归半衰期（Half-life）？如果拟合出的自回归系数 $b \ge 0$，在统计与交易上意味着什么？
Q3: 在 A 股等融券做空受限、借券成本高企的环境下，量化机构如何落地配对交易？（例如行业 ETF 替代、股指期货套保或相对价值多头增强）。

【评分与通过规则】
- 代码 4 分：
  1. 准确实现 Engle-Granger 两步法协整检验与 ADF 平稳性检验 (1.5分)；
  2. 准确实现 Ornstein-Uhlenbeck 过程拟合与半衰期估算 (1分)；
  3. 准确实现基于滚动 Z-Score 的配对交易策略回测与绩效度量 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须说明底层统计机制、SDE 数学推导与 A 股融券约束应对；
- 通过线：8/10 分。一票否决：回测中引入前视信号未滞后一期、删除断言校验。
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
    Engle-Granger 两步法协整检验：
    Step 1: OLS 回归 ln(Price_A) = alpha + beta * ln(Price_B) + e
    Step 2: 对残差序列 e 进行 ADF 单位根平稳性检验

    参数:
        price_a: 资产 A 价格时间序列
        price_b: 资产 B 价格时间序列

    返回字典包含:
        - "hedge_ratio": 对冲比率 beta
        - "intercept": 截距 alpha
        - "spread": 对数价差残差序列 Series (ln(P_A) - beta * ln(P_B) - alpha)
        - "adf_statistic": ADF 检验统计量
        - "p_value": ADF 检验 p 值
        - "is_cointegrated": p_value < 0.05 是否显著协整 (bool)
    """
    # TODO: 实现 Engle-Granger 协整检验
    pass


def estimate_ou_half_life(spread: pd.Series) -> float:
    """
    基于离散 Ornstein-Uhlenbeck (OU) 过程估算价差均值回归半衰期 (Half-life)：
        Delta S_t = S_t - S_{t-1} = a + b * S_{t-1} + epsilon_t
        均值回归速度 theta = -b
        半衰期 Half-life = -ln(2) / b

    参数:
        spread: 资产对价差序列

    返回:
        float: 均值回归半衰期 (天数)。若 b >= 0 (不具备均值回归)，返回 float('inf')。
    """
    # TODO: 实现 OU 过程回归与半衰期估算
    pass


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
    基于滚动 Z-Score 的配对交易策略回测引擎：
    1. 计算对数对冲价差: spread_t = ln(Price_A_t) - hedge_ratio * ln(Price_B_t)
    2. 计算滚动均值与滚动标准差，生成 Z-Score: (spread - roll_mean) / roll_std
    3. 生成交易持仓信号 (必须滞后 1 期执行以防止前视偏差):
       - Z > z_open ➔ Short Spread (-1)
       - Z < -z_open ➔ Long Spread (+1)
       - |Z| <= z_exit ➔ 平仓 (0)
       - |Z| >= z_stop ➔ 止损平仓 (0)
    4. 计算组合日收益率:
       ret_spread_t = ret_A_t - hedge_ratio * ret_B_t
       strat_ret_t = position_{t-1} * ret_spread_t

    返回字典包含:
        - "zscore": 滚动 Z-Score 序列 Series
        - "positions": 每日持仓信号 Series (-1, 0, 1)
        - "daily_returns": 策略日收益率序列 Series
        - "total_return": 策略累计复合收益率
        - "annualized_return": 策略年化收益率
        - "annualized_volatility": 策略年化波动率
        - "sharpe_ratio": 年化夏普比率
        - "max_drawdown": 最大回撤 (负值)
    """
    # TODO: 实现完整的配对交易策略回测
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 03: 统计套利与配对交易单元测试")
    print("=" * 70)

    # 1. 构造具有真实经济学协整纽带的仿真资产价格对
    np.random.seed(42)
    n_days = 500
    dates = pd.date_range("2023-01-01", periods=n_days, freq="B")

    # 共同长期趋势 (随机游走)
    macro_trend = np.cumsum(np.random.normal(0, 0.01, n_days))

    # 真实对冲比率与 OU 均值回归价差
    true_hedge_ratio = 1.2
    theta_true = 0.08  # 预期半衰期 ~ ln(2)/0.08 = 8.66 天
    spread_ou = np.zeros(n_days)
    for t in range(1, n_days):
        spread_ou[t] = spread_ou[t - 1] - theta_true * spread_ou[t - 1] + np.random.normal(0, 0.015)

    log_pb = 4.0 + macro_trend
    log_pa = 1.0 + true_hedge_ratio * log_pb + spread_ou
    price_a_series = pd.Series(np.exp(log_pa), index=dates)
    price_b_series = pd.Series(np.exp(log_pb), index=dates)

    # 2. 协整检验
    coint_res = engle_granger_cointegration_test(price_a_series, price_b_series)
    print(f"估计对冲比率 Hedge Ratio: {coint_res['hedge_ratio']:.4f}")
    print(f"ADF 统计量: {coint_res['adf_statistic']:.4f}, p 值: {coint_res['p_value']:.4e}")
    print(f"是否显著协整: {coint_res['is_cointegrated']}")

    assert coint_res["is_cointegrated"] is True, "两资产应通过 95% 置信度协整检验"
    assert abs(coint_res["hedge_ratio"] - true_hedge_ratio) < 0.25, "对冲比率估计偏差过大"

    # 3. 估算 OU 半衰期
    half_life = estimate_ou_half_life(coint_res["spread"])
    print(f"估算的价差均值回归半衰期 Half-life: {half_life:.2f} 天")
    assert 5.0 <= half_life <= 15.0, f"半衰期估算应在 5~15 天范围内, 实际: {half_life:.2f}"

    # 4. 回测配对交易策略
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

    print("Lesson 03 统计套利与配对交易单元测试全部通过！")
