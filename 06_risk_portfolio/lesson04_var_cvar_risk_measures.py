r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 4/5 课
第 4 课：风险价值 (VaR)、条件风险价值 (CVaR) 与动态回撤熔断控制
================================================================================

【课程定位与第一性原理】
在现代金融机构风控与对冲基金资本充足率监管体系中，波动率（$\sigma_p$）已不足以衡量非对称的左侧极端尾部损失。
巴塞尔协议（Basel Accords）确立了两大核心风险度量标准：

1. 风险价值（Value at Risk, VaR）：
   - 在置信水平 $1 - \alpha$（如 95% 或 99%）及持有期 $\Delta t$ 内，组合预期发生的最大潜在损失：
     $$P(\text{Loss} \le \text{VaR}_{\alpha}) = 1 - \alpha \iff P(R \le -\text{VaR}_{\alpha}) = \alpha$$
   - **致命缺陷（Artzner et al. 1999）**：
     - **黑天鹅盲区**：VaR 仅回答了“在 95% 的正常情况下最坏亏损是多少”，却完全无法回答“在剩下 5% 的黑天鹅灾难发生时究竟会亏损多少”；
     - **非一致性风险度量（Non-subadditive）**：VaR 不满足次可加性公理 $\rho(X + Y) \le \rho(X) + \rho(Y)$。
       在特定非线性期权或极度肥尾组合中，分散化组合的 VaR 可能会大于单资产 VaR 之和，违背了投资学常识。

2. 条件风险价值（Conditional VaR / Expected Shortfall, CVaR）：
   - 一旦损失击穿 VaR 阈值时，极端尾部损失的条件数学期望：
     $$\text{CVaR}_{\alpha} = \mathbb{E}[\text{Loss} \mid \text{Loss} \ge \text{VaR}_{\alpha}] = -\frac{1}{\alpha} \int_0^{\alpha} F^{-1}(p) dp$$
   - **数理优越性**：Rockafellar & Uryasev (2000) 证明 CVaR 满足凸性与次可加性，是一致性风险度量指标；
     巴塞尔协议 III（Basel III）已全面强制以 97.5% CVaR 替代 99% VaR 作为银行与资管机构风险准备金的计提底座。

3. 计量方法对比：
   - 参数法（Parametric / Variance-Covariance Method）：假定收益率服从正态分布 $R \sim \mathcal{N}(\mu, \sigma^2)$：
     $$\text{VaR}_{\alpha}^{\text{param}} = z_{\alpha} \sigma - \mu, \quad \text{CVaR}_{\alpha}^{\text{param}} = \sigma \frac{\phi(z_{\alpha})}{\alpha} - \mu$$
     其中 $\phi(\cdot)$ 为标准正态概率密度函数，$z_{0.05} \approx 1.6449$。
   - 非参数历史模拟法（Historical Simulation）：
     直接从历史真实收益率经验分布中提取 $\alpha$ 分位数：
     $$\text{VaR}_{\alpha}^{\text{hist}} = -Q_{\alpha}(R), \quad \text{CVaR}_{\alpha}^{\text{hist}} = -\frac{1}{|R \le -Q_{\alpha}|} \sum_{R_t \le -Q_{\alpha}} R_t$$
     不依赖任何理论分布假设，能够真实保留历史厚尾、极端暴跌与流动性抽干。

4. 动态高水位回撤控制与阶梯式熔断器（Drawdown Sentinel）：
   - 动态回撤率：$DD_t = (W_t - H_t) / H_t$，其中 $H_t = \max_{s \le t} W_s$ 为历史最高水位线（High Water Mark）；
   - 阶梯式自动风控规则（必须滞后 1 期执行以防止前视未来偏差）：
     - 正常仓位：$DD > -5\%$，仓位乘数 $M = 1.0$；
     - 一级预警：$-10\% < DD \le -5\%$，仓位乘数压缩至 $M = 0.5$（主动降杠杆以平抑波动）；
     - 二级硬熔断：$DD \le -10\%$，仓位强制清零 $M = 0.0$（全仓现金止损熔断，切断深不见底的主跌浪）。

【核心流程与心智模型】
```mermaid
stateDiagram-v2
    [*] --> 正常运行状态 (Normal: 100%仓位)
    
    正常运行状态 (Normal: 100%仓位) --> 一级预警状态 (Warning: 50%仓位): 回撤突破预警线 (DD <= -5%)
    一级预警状态 (Warning: 50%仓位) --> 正常运行状态 (Normal: 100%仓位): 净值修复 (DD > -5%)
    
    一级预警状态 (Warning: 50%仓位) --> 二级硬熔断状态 (Halted: 0%现金): 灾难回撤突破熔断线 (DD <= -10%)
    正常运行状态 (Normal: 100%仓位) --> 二级硬熔断状态 (Halted: 0%现金): 单日闪崩暴跌突破熔断线 (DD <= -10%)
    
    二级硬熔断状态 (Halted: 0%现金) --> [*]: 强制终止交易并进入投委会复盘审查
```

【工业界实战场景与风控陷阱】
1. 正态高斯假说的“黑天鹅粉饰”：
   在真实金融市场中，收益率严重肥尾（Kurtosis 往往在 6~30 以上）。若盲信参数法正态 VaR，
   2008 年金融危机与 2020 年流动性踩踏将连续出现理论概率为“数万年一次”的 6-Sigma 事件，引发瞬间穿仓。
2. 历史模拟法的数据样本窗口选择（Windowing Trade-off）：
   窗口过短（如 60 天）在牛市中会严重低估熊市杀伤力；窗口过长（如 5 年）则无法及时捕捉近期微观波动率聚集。
3. 动态回撤熔断后的“踏空综合征”与冷冻期设计：
   熔断清仓后若市场瞬间 V 型反弹，策略可能面临踏空。机构风控必须引入“波动率回落至历史中枢”或“大盘站上均线”等客观解冻条件。

【思考题】
Q1: 为什么假设正态分布计算的参数法 VaR 在金融危机爆发时会低估真实亏损几十倍甚至上百倍？（肥尾与极端离群值）。
Q2: 历史模拟法与参数法计算 VaR / CVaR 各有何优劣？巴塞尔协议 III 为何要求商业银行与投行全面以 97.5% CVaR 取代 99% VaR 作为资本充足率计量底座？
Q3: 怎样利用高水位线回撤（Drawdown from High Water Mark）设计量化系统的动态阶梯降仓与硬熔断止损器？在回撤触发熔断清仓后，量化团队应如何设置科学的冷冻期与再进场条件，避免“追涨杀跌两头挨巴掌”？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现参数法 VaR 与 CVaR 正态解析计算 (1分)；
  2. 准确实现历史模拟法经验分位数 VaR 与 CVaR 计算 (1.5分)；
  3. 准确实现动态高水位阶梯式回撤熔断器模拟并验证最大回撤大幅压降 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须从次可加性公理、厚尾极值与实盘熔断解冻机制深入展开；
- 通过线：8/10 分。一票否决：回测中引入前视未来净值、损失符号定义颠倒、删除断言校验。
"""

from typing import Tuple, Dict, Any, List
import numpy as np
import pandas as pd
from scipy import stats


def calculate_parametric_var_cvar(
    returns: np.ndarray,
    confidence: float = 0.95,
) -> Tuple[float, float]:
    """
    基于正态分布假定的参数法单期 VaR 与 CVaR (以正数表示损失率)：
        alpha = 1 - confidence
        VaR_param = z_alpha * sigma - mu
        CVaR_param = sigma * (phi(z_alpha) / alpha) - mu

    参数:
        returns: 资产历史收益率数组 (一维)
        confidence: 置信水平 (默认 0.95)

    返回:
        Tuple[float, float]: (参数法 VaR, 参数法 CVaR)
    """
    # TODO: 实现参数法正态 VaR 与 CVaR
    pass


def calculate_historical_var_cvar(
    returns: np.ndarray,
    confidence: float = 0.95,
) -> Tuple[float, float]:
    """
    基于经验分布的历史模拟法单期 VaR 与 CVaR (以正数表示损失率)：
        alpha = 1 - confidence
        cutoff = percentile(returns, alpha * 100)
        VaR_hist = -cutoff
        CVaR_hist = -mean(returns[returns <= cutoff])

    参数:
        returns: 资产历史收益率数组 (一维)
        confidence: 置信水平 (默认 0.95)

    返回:
        Tuple[float, float]: (历史模拟法 VaR, 历史模拟法 CVaR)
    """
    # TODO: 实现非参数历史模拟法 VaR 与 CVaR
    pass


def simulate_dynamic_drawdown_sentinel(
    raw_returns: pd.Series,
    warning_dd: float = -0.05,
    cut_ratio: float = 0.50,
    circuit_breaker_dd: float = -0.10,
) -> Dict[str, Any]:
    """
    基于历史高水位线 (HWM) 的动态阶梯式回撤风控哨兵：
    逐日滚动跟踪策略累计财富 W_t 与历史最高水位线 HWM_t = max_{s <= t} W_s：
    回撤率: DD_t = (W_t - HWM_t) / HWM_t

    风控执行规则 (决策必须滞后 1 期执行以防止前视偏差):
    - 若上一日 DD > warning_dd: 仓位乘数 pos = 1.0 (正常)
    - 若上一日 circuit_breaker_dd < DD <= warning_dd: 仓位乘数 pos = cut_ratio (0.5 降仓预警)
    - 若上一日 DD <= circuit_breaker_dd: 仓位乘数 pos = 0.0 (硬熔断平仓冷冻)

    参数:
        raw_returns: 未受风控约束的原始资产单日收益率 Series
        warning_dd: 一级降仓预警回撤阈值 (负数, 默认 -0.05)
        cut_ratio: 一级预警状态下的仓位压缩乘数 (默认 0.50)
        circuit_breaker_dd: 二级硬熔断回撤阈值 (负数, 默认 -0.10)

    返回字典包含:
        - "raw_max_drawdown": 原始策略最大回撤 (负值)
        - "controlled_max_drawdown": 受控策略最大回撤 (负值)
        - "controlled_returns": 受控策略每日收益率 Series
        - "drawdown_reduction_pct": 最大回撤削减幅度 ((ctrl_dd - raw_dd) / abs(raw_dd))
        - "circuit_breaker_tripped": 是否触发了二级硬熔断 (bool)
    """
    # TODO: 实现动态回撤风控哨兵模拟引擎
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 04: VaR / CVaR 与动态回撤熔断单元测试")
    print("=" * 70)

    # 1. 验证简单离散样本下的历史模拟法 VaR 与 CVaR
    rets_simple = np.array([-0.10, -0.06, -0.05, -0.02, 0.01, 0.02, 0.03, 0.04, 0.05, 0.08])
    h_var90, h_cvar90 = calculate_historical_var_cvar(rets_simple, confidence=0.90)
    print(f"简单样本 90% 历史 VaR: {h_var90*100:.2f}%, 历史 CVaR: {h_cvar90*100:.2f}%")
    assert h_var90 > 0.0, "VaR 以正损失率表达"
    assert h_cvar90 >= h_var90, "根据定义, 极端条件期望 CVaR 必须大于等于 VaR"

    # 2. 对比厚尾分布 (Student-t, df=3) 下参数法与历史模拟法的巨大反差
    np.random.seed(42)
    # 模拟 2000 个带厚尾特性的金融资产日收益率
    t_rets = stats.t.rvs(df=3, loc=0.0005, scale=0.015, size=2000)

    p_var, p_cvar = calculate_parametric_var_cvar(t_rets, confidence=0.95)
    h_var, h_cvar = calculate_historical_var_cvar(t_rets, confidence=0.95)

    print(f"\n厚尾数据 95% 参数法 VaR: {p_var*100:.2f}%, 参数法 CVaR: {p_cvar*100:.2f}%")
    print(f"厚尾数据 95% 历史法 VaR: {h_var*100:.2f}%, 历史法 CVaR: {h_cvar*100:.2f}%")

    assert p_cvar >= p_var, "参数法 CVaR 必须大于等于参数法 VaR"
    assert h_cvar >= h_var, "历史模拟法 CVaR 必须大于等于历史法 VaR"
    # 在极度厚尾数据下，真实历史 CVaR 必须显著高于正态分布假定的参数法 CVaR
    assert h_cvar > p_cvar, f"厚尾极端损失预期应显著击穿正态假设: 历史 CVaR ({h_cvar}) > 参数 CVaR ({p_cvar})"

    # 3. 验证动态高水位回撤控制与阶梯式熔断器
    n_days = 252
    raw_rets_arr = np.random.normal(0.001, 0.015, n_days)
    # 在第 100~150 天注入持续深幅崩盘行情
    raw_rets_arr[100:150] = np.random.normal(-0.008, 0.02, 50)
    raw_series = pd.Series(raw_rets_arr)

    sentinel_res = simulate_dynamic_drawdown_sentinel(
        raw_series,
        warning_dd=-0.05,
        cut_ratio=0.50,
        circuit_breaker_dd=-0.10,
    )

    print(f"\n未受控原始策略最大回撤: {sentinel_res['raw_max_drawdown']*100:.2f}%")
    print(f"受控策略最大回撤: {sentinel_res['controlled_max_drawdown']*100:.2f}%")
    print(f"回撤削减幅度: {sentinel_res['drawdown_reduction_pct']*100:.2f}%")
    print(f"是否触发硬熔断: {sentinel_res['circuit_breaker_tripped']}")

    assert sentinel_res["raw_max_drawdown"] < -0.30, "原始策略在暴跌注入期间应发生深幅回撤 (< -30%)"
    # 动态熔断器应将最大回撤牢牢锁定在熔断线附临近区间 (不发生大于 -15% 的深度穿仓)
    assert sentinel_res["controlled_max_drawdown"] > -0.15, f"受控策略最大回撤应受控在 -15% 以内, 实际: {sentinel_res['controlled_max_drawdown']*100:.2f}%"
    assert sentinel_res["drawdown_reduction_pct"] > 0.50, "回撤削减幅度应超过 50%"
    assert sentinel_res["circuit_breaker_tripped"] is True, "暴跌行情应成功触发二级硬熔断保护"

    print("Lesson 04 风险计量与动态回撤风控单元测试全部通过！")
