r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 1/5 课
第 1 课：单因子检验框架与 IC / Rank IC / 分组回测 (Single Factor Testing)
================================================================================

【课程定位与第一性原理】
在现代多因子量化选股体系（Factor Investing）中，单因子检验是整个投研流水线的“入海口”与“试金石”。
一个在统计学上合格的选股因子，必须满足三个层面的严苛检验：
1. 预测能力（Predictive Power）：因子在横截面（Cross-Section）上对股票未来收益（Forward Return）
   具有统计显著的线性或排序预测能力；
2. 稳定性与信噪比（Stability & Information Ratio）：预测能力在时间序列上持续稳定，回撤周期短，
   而非仅靠单期极端行情的偶然贡献；
3. 单调性（Monotonicity）：按因子得分分组后，各组投资组合收益必须呈现严格的阶梯式单调递增（或递减），
   确保策略具有广谱的选股区分度，而非仅在极小市值或极端边缘资产上偶发有效。

【核心数理定义与量化评价指标】
1. 因子预处理标准流程（三部曲）：
   - 去极值（Winsorization / MAD）：中位数绝对偏差（Median Absolute Deviation）
     $$\text{Median} = \text{median}(F), \quad \text{MAD} = \text{median}(|F - \text{Median}|)$$
     对超出 $[\text{Median} - 3 \times 1.4826 \times \text{MAD}, \text{Median} + 3 \times 1.4826 \times \text{MAD}]$ 的值进行截断截平；
   - 截面标准化（Z-Score Normalization）：
     $$Z_i = \frac{F_i - \mu_F}{\sigma_F}$$
   - 中性化（Neutralization）：通过截面 OLS 回归剔除行业（Industry Dummies）与市值（Log Market Cap）风格污染，
     提取纯净的残差收益。

2. 因子预测能力评估（IC体系）：
   - Normal IC (Pearson Correlation)：
     $$IC_t = \text{corr}(F_{i,t}, R_{i, t+1})$$
     易受极值与厚尾收益污染。
   - Rank IC (Spearman Rank Correlation)：
     $$\text{Rank IC}_t = \text{corr}(\text{rank}(F_{i,t}), \text{rank}(R_{i, t+1}))$$
     衡量因子的横截面相对排序预测能力，对离群值高度鲁棒，是工业界公认的核心指标。
   - 信息比率（ICIR）：
     $$\text{ICIR} = \frac{\mathbb{E}[\text{Rank IC}]}{\text{std}(\text{Rank IC})} \times \sqrt{T_{\text{annual}}}$$
     通常以日频 $\sqrt{252}$ 或月频 $\sqrt{12}$ 进行年化。优秀的选股因子年化 ICIR 通常应大于 1.5。
   - t 统计量与显著性（t-statistic）：
     $$t = \frac{\overline{\text{Rank IC}}}{\text{std}(\text{Rank IC}) / \sqrt{N}}$$

3. 分组回测与单调性分析（Quantile Portfolios）：
   - 每个调仓截面将股票按因子得分均匀划分为 $K$ 组（通常取 $K=5$ 或 $K=10$）；
   - Top 组（组 1，买入建议）与 Bottom 组（组 5，卖出建议）；
   - 多空对冲收益（Long-Short Spread）：$R_{\text{LS}} = R_{\text{Top}} - R_{\text{Bottom}}$；
   - 单调性得分（Monotonicity Score）：各组平均收益率向量与组号 $[1, 2, \dots, K]$ 的 Spearman 秩相关系数，
     绝对值越接近 1.0 表明分层单调性越强。

【核心流程与心智模型】
```mermaid
flowchart TD
    Raw["原始因子截面数据 (Factor Scores)"] --> Preprocess["数据预处理: MAD 去极值 + Z-Score 截面标准化"]
    Preprocess --> Align["严格对齐未来 T+1 期收益 (Forward Return) - 杜绝前视偏差"]
    Align --> RankIC["计算各期 Spearman Rank IC"]
    RankIC --> ICTS["IC 时序聚合: 均值 / 波动率 / ICIR / t统计量 / 胜率"]
    Align --> Quantiles["截面划分为 5 等分投资组合 (Q1 ~ Q5)"]
    Quantiles --> GroupRet["计算各组等权收益率时序"]
    GroupRet --> Monotonic["计算年化收益率、多空净值对冲曲线、单调性得分"]
    ICTS --> Verdict["综合决策: ICIR > 1.0 且单调性 > 0.8 ➔ 准入因子库"]
    Monotonic --> Verdict
```

【工业界实战场景与风控陷阱】
1. 前视偏差（Lookahead Bias）：
   计算 $t$ 期的因子得分时，严禁使用 $t$ 期的当日收盘价或未来未披露数据。对齐下期收益率时，
   因子的生效点必须在收益统计区间开始之前（例如 T 日收盘计算因子，预测 T+1 日开盘买入至 T+2 日开盘的收益）。
2. 因子衰减（Alpha Decay）与换手率黑洞：
   高频量价因子可能半衰期仅有 2~3 天，若按月调仓则 Alpha 消耗殆尽；而基本面因子（如 ROE、EP）具有长半衰期（3~6个月）。
   必须测算因子自相关系数衰减曲线，权衡调仓收益与双边换手摩擦成本（印花税+佣金+冲击成本）。
3. 伪因子的极端值驱动假象：
   某些未经去极值的微盘股由于暴涨暴跌，导致 Normal IC 虚高，但转换为 Rank IC 后显著性消失，说明策略无法在大容量资金上落地。

【思考题】
Q1: 为什么在 A 股做因子预处理时，必须进行“去极值”（如三倍中位数绝对偏差 MAD）和“行业市值中性化”？如果未经市值中性化，一个估值因子（低 PE / 低 PB）可能会退化成什么？
Q2: 什么是因子衰减（Factor Decay）？如何绘制因子自相关衰减曲线，并据此科学确定最佳调仓换手周期（周频/月频/季频）？
Q3: 为什么单因子在不计交易成本时可能展现出高达 25% 的年化多空对冲收益，但一旦扣除双边万分之五佣金、千分之一印花税与市场冲击滑点后，净值曲线会迅速归零甚至倒亏？量化研究员应如何引入换手率惩罚与调仓缓冲带（Buffer Zone）？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现 MAD 去极值与标准化预处理 (1分)；
  2. 准确实现截面 Rank IC 与时序 ICIR / t 统计量 (1.5分)；
  3. 准确实现 5 分位数分组收益率、多空年化超额与单调性检验 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须说明底层金融逻辑、统计因果链与机构摩擦成本；
- 通过线：8/10 分。一票否决：引入前视未来数据、删除断言校验、直接返回硬编码数值。
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def preprocess_factor_scores(scores: pd.Series, n_mad: float = 3.0) -> pd.Series:
    """
    因子横截面数据预处理：
    1. 中位数绝对偏差 (MAD) 去极值：
       - 计算中位数 median 与 MAD = median(|x - median|)
       - 设定上下界: [median - n_mad * 1.4826 * MAD, median + n_mad * 1.4826 * MAD]
       - 将超出范围的值截平 (clip)
    2. Z-Score 标准化：
       - (x - mean) / std，使得截面均值为 0，方差为 1

    参数:
        scores: 单个时间截面上的股票因子得分 Series (index 为股票代码)
        n_mad: MAD 倍数，默认 3.0

    返回:
        pd.Series: 预处理后的因子得分 Series
    """
    # TODO: 实现 MAD 去极值与 Z-Score 截面标准化
    pass


def calculate_rank_ic(factor_scores: pd.Series, forward_returns: pd.Series) -> float:
    """
    计算单个时间截面上的 Spearman Rank IC（秩相关系数）：
    - 剔除 NaN 缺失值；
    - 计算两者的 Spearman 秩相关系数；
    - 若有效股票数量小于 3，返回 0.0。

    参数:
        factor_scores: 股票因子得分 Series
        forward_returns: 对应的下期收益率 Series

    返回:
        float: Rank IC 值 (范围 [-1.0, 1.0])
    """
    # TODO: 计算单截面 Spearman Rank IC
    pass


def evaluate_factor_performance(
    factor_df: pd.DataFrame,
    forward_returns_df: pd.DataFrame,
    num_groups: int = 5,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    完整的单因子评价框架：
    输入为面板数据（index 为日期，columns 为股票代码）。

    评估内容：
    1. IC 体系：
       - 逐日计算 Rank IC 时序序列；
       - mean_rank_ic: Rank IC 均值；
       - std_rank_ic: Rank IC 标准差；
       - icir: 年化 ICIR = (mean / std) * sqrt(annual_periods)；
       - t_stat: t 统计量 = mean / (std / sqrt(T))；
       - p_value: 双尾 t 检验 p 值；
       - ic_hit_ratio: Rank IC > 0 的周期占比；
    2. 分组收益体系：
       - 每个日期截面，按因子得分将股票均匀分为 num_groups 组（组 1 为最高得分组，组 5 为最低得分组）；
       - 计算各组在各期的等权平均收益率；
       - group_annual_returns: 长度为 num_groups 的列表，各组的年化复合收益率 (CAGR 或简单年化: mean * annual_periods)；
       - long_short_annual_return: 多空组合 (Q1 - Q5) 的年化收益率；
       - long_short_sharpe: 多空组合的年化夏普比率 (假设无风险利率为 0)；
       - monotonicity_score: 各组平均收益率与组排序序号 [1, 2, ..., num_groups] 的 Spearman 秩相关系数。

    返回:
        Dict[str, Any]: 包含上述所有评价指标的字典
    """
    # TODO: 实现全流程单因子评价框架
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 01: 单因子检验框架单元测试与断言验证")
    print("=" * 70)

    # 1. 检验单截面预处理 (MAD 去极值 + Z-Score 标准化)
    raw_s = pd.Series([1.0, 2.0, 2.1, 1.9, 100.0, -50.0], index=[f"S{i}" for i in range(6)])
    clean_s = preprocess_factor_scores(raw_s, n_mad=3.0)
    assert clean_s is not None, "预处理函数不能返回 None"
    assert abs(clean_s.mean()) < 1e-6, "标准化后均值应为 0"
    assert abs(clean_s.std() - 1.0) < 1e-4, "标准化后方差应为 1"
    # 极值 100.0 和 -50.0 应该被显著抑制，不应远大于其他样本
    assert clean_s.max() < 3.0 and clean_s.min() > -3.0, "MAD 去极值未有效限制离群点"

    # 2. 检验单个截面 Rank IC 计算
    f_test = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0], index=[f"S{i}" for i in range(5)])
    r_test = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05], index=[f"S{i}" for i in range(5)])
    perfect_ic = calculate_rank_ic(f_test, r_test)
    assert abs(perfect_ic - 1.0) < 1e-4, f"完全正相关时 Rank IC 应为 1.0, 实际为 {perfect_ic}"

    r_inv = pd.Series([0.05, 0.04, 0.03, 0.02, 0.01], index=[f"S{i}" for i in range(5)])
    inv_ic = calculate_rank_ic(f_test, r_inv)
    assert abs(inv_ic - (-1.0)) < 1e-4, f"完全负相关时 Rank IC 应为 -1.0, 实际为 {inv_ic}"

    # 3. 构造 100 个交易日、30 只股票的仿真多因子选股面板数据进行全面评估
    np.random.seed(42)
    n_days = 100
    n_stocks = 30
    dates = pd.date_range("2024-01-01", periods=n_days, freq="B")
    stock_cols = [f"Stock_{i:02d}" for i in range(n_stocks)]

    # 构造因子暴露矩阵：具有稳健的正向选股能力
    factor_mat = np.random.randn(n_days, n_stocks)
    # 下期收益率 = 真实信号 (0.15 * factor) + 特质噪音 (0.85 * noise)
    noise_mat = np.random.randn(n_days, n_stocks)
    forward_ret_mat = 0.05 * factor_mat + 0.15 * noise_mat

    factor_panel = pd.DataFrame(factor_mat, index=dates, columns=stock_cols)
    returns_panel = pd.DataFrame(forward_ret_mat, index=dates, columns=stock_cols)

    metrics = evaluate_factor_performance(factor_panel, returns_panel, num_groups=5, annual_periods=252)

    # 验证指标存在且符合统计常理
    assert "mean_rank_ic" in metrics and "icir" in metrics, "缺少 IC 核心指标"
    assert "group_annual_returns" in metrics, "缺少分组年化收益率"
    assert "monotonicity_score" in metrics, "缺少单调性得分"

    print(f"Rank IC 均值: {metrics['mean_rank_ic']:.4f}")
    print(f"年化 ICIR: {metrics['icir']:.4f}")
    print(f"t 统计量: {metrics['t_stat']:.4f} (p-value: {metrics['p_value']:.4e})")
    print(f"IC 胜率: {metrics['ic_hit_ratio']*100:.2f}%")
    print(f"5 组年化收益率: {[round(x, 4) for x in metrics['group_annual_returns']]}")
    print(f"多空组合年化收益: {metrics['long_short_annual_return']:.4f}, 夏普比率: {metrics['long_short_sharpe']:.4f}")
    print(f"单调性得分: {metrics['monotonicity_score']:.4f}")

    assert metrics["mean_rank_ic"] > 0.10, f"构造的有效因子 Rank IC 应显著大于 0.10, 实际: {metrics['mean_rank_ic']}"
    assert metrics["icir"] > 1.0, f"年化 ICIR 应大于 1.0, 实际: {metrics['icir']}"
    assert metrics["t_stat"] > 3.0, f"t 统计量应具备高统计显著性 (>3.0), 实际: {metrics['t_stat']}"
    assert len(metrics["group_annual_returns"]) == 5, "分组收益数量必须等于 5"
    assert metrics["long_short_annual_return"] > 0.0, "多空组合年化收益必须为正"
    assert metrics["monotonicity_score"] > 0.70, f"分组单调性应大于 0.70, 实际: {metrics['monotonicity_score']}"

    print("Lesson 01 单因子检验框架单元测试全部通过！")
