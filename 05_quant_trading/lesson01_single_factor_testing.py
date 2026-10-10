r"""
================================================================================
模块 05：量化投资多因子与统计套利 · 第 1/5 课
第 1 课：单因子检验评价框架与 IC / Rank IC / 分层回测 (Single Factor Evaluation Pipeline)
================================================================================

【课程定位与第一性原理】
在现代量化资产管理与对冲基金多因子选股体系中，单因子检验（Single Factor Testing）
是验证任何特征是否具备独立超额收益预测能力的绝对科学基石。
投决会审视量化研究员提交的因子报告时，严禁使用未经清洗的裸数据或过度拟合的样本内参数，
必须基于统计物理与稳健估计的第一性原理，建立全流程因果闭环。

- **[数据清洗的统计稳健性]**：金融收益率序列具有显著的肥尾与离群点，必须使用中位数绝对偏差（MAD）进行非正态去极值，辅以 Z-score 标准化消除量纲。
- **[因子评价的核心指标矩阵]**：Rank IC（斯皮尔曼秩相关）度量因子预测排名的相关度，ICIR（信息比率）度量相关性的时间稳定性，t 统计量度量显著性。
- **[分层回测的单调性检验]**：将股票池按因子得分等分为 5 组，Q1~Q5 组合年化收益必须呈现严格单调递增；任何单调性倒挂均揭示因子存在非线性结构缺陷。

【核心概念与就近图文排版】

1. 生产级单因子数据预处理流水线：
观察下图关于原始因子得分经过去极值、标准化与中性化清洗的标准工业流水线：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.1.1：生产级单因子数据清洗与正交预处理流水线 (Factor Pipeline)</span>
    <span class="diagram-tag">FACTOR-PREPROCESSING</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l01_factor_evaluation_pipeline.svg -->
  </div>
</div>

- **[MAD 稳健去极值]**：计算中位数 $\text{med}$ 与绝对离差中位数 $\text{MAD} = \text{median}(|X - \text{med}|)$，将边界截断在 $[\text{med} - 3 \times 1.4826 \text{MAD}, \text{med} + 3 \times 1.4826 \text{MAD}]$。
- **[截面 Z-Score 标准化]**：对去极值后的横截面得分做均值归零与方差归一，确保全截面 $\mu = 0, \sigma = 1$。
- **[行业与市值中性化 OLS]**：通过多元线性回归剥离申万一级行业哑变量与对数市值暴露，提取纯净 Alpha 残差 $\epsilon_i$。

2. 截面 Rank IC 时序分布与 IR 稳定性：
下图展示了月度截面斯皮尔曼秩相关系数的时序波动与 ICIR 统计评估模型：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.1.2：截面 Rank IC 时序分布与 IR (信息比率) 稳定性检验</span>
    <span class="diagram-tag">RANK-IC-STATS</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l01_rank_ic_distribution.svg -->
  </div>
</div>

- **[Rank IC 秩相关系数]**：$\text{Rank IC}_t = \text{Corr}(\text{rank}(X_t), \text{rank}(R_{t+1}))$，完全消除非线性异常值的扭曲。
- **[ICIR 稳定性比率]**：$\text{ICIR} = \frac{\text{Mean}(\text{Rank IC})}{\text{Std}(\text{Rank IC})} \times \sqrt{T}$，年化 $\text{ICIR} > 0.5$ 视为优质因子。
- **[半衰期衰减分析]**：跟踪滞后 $k$ 期因子的 Rank IC 衰减速率，决定量化策略的最佳调仓换手周期。

3. 五分位数分层回测与多空单调性：
下图展示了股票池按因子得分五等分组合的收益单调性与累计多空净值曲线：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.1.3：因子五分位数 (Quantiles) 分层回测单调性与多空净值对决</span>
    <span class="diagram-tag">QUANTILE-BACKTEST</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l01_quantile_monotonicity.svg -->
  </div>
</div>

- **[多空组合收益]**：买入得分最高 Q5 组同时做空得分最低 Q1 组，剥离 Beta 风险，检验纯超额 Alpha。
- **[单调性检验得分]**：计算各组收益与组号 $[1, 2, 3, 4, 5]$ 的斯皮尔曼秩相关，单调性得分必须 $> 0.70$。
- **[换手率交易磨损]**：高 IC 因子若伴随超高换手率（> 100% 每期），净值会被交易滑点与印花税完全侵蚀。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：格林诺德基本定律 (Fundamental Law of Active Management)</div>
  <div class="callout-body">
    主动投资的信息比率决定于因子技能与广度的乘积：$\text{IR} \approx \text{IC} \times \sqrt{\text{Breadth}}$。追求超高 IC 是不切实际的，量化对冲基金的核心竞争力是在全市场数千只股票与数百个周期上稳定复制哪怕微弱的正向 IC。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁使用未经行业与市值中性化的原始因子参与组合！未经中性化的所谓高收益因子，80% 以上只是在被动裸露小市值溢价或某些行业的贝塔敞口，风格反转时将遭遇毁灭性回撤。
  </div>
</div>

【数学与评价模型】
$$\text{Rank IC} = 1 - \frac{6 \sum_{i=1}^N d_i^2}{N(N^2 - 1)}, \quad \text{其中 } d_i = \text{rank}(X_i) - \text{rank}(R_i)$$
$$\text{ICIR} = \frac{\bar{\text{IC}}}{\sigma_{\text{IC}}} \times \sqrt{12} \quad (\text{月频年化})$$
$$\text{Monotonicity} = \text{SpearmanCorr}([1, 2, 3, 4, 5], [\bar{R}_{Q1}, \bar{R}_{Q2}, \bar{R}_{Q3}, \bar{R}_{Q4}, \bar{R}_{Q5}])$$
定义域：$N \ge 30, \quad \text{Rank IC} \in [-1, 1], \quad \sigma_{\text{IC}} > 0$。

【思考题】
Q1: 普通 IC（Pearson）vs 秩 IC（Rank IC）：为什么在 A 股或美股量化多因子检验中，机构级投研体系几乎只考核 Rank IC 而非传统 Pearson IC？请从资产收益率的非正态分布、极端长尾异常值（Outliers）以及非线性单调映射的鲁棒性角度进行严格数学推导。
Q2: 因子中性化（Neutralization）与纯 Alpha 提纯：如果一个账面市值比（BP）因子在未经行业和市值中性化时年化多空夏普高达 2.5，但在通过 OLS 残差回归剔除申万一级行业哑变量与对数市值（Log Market Cap）后夏普骤降至 0.3，从投资组合风控视角看，这说明该因子真实赚取的是什么钱？为什么未经中性化的因子在风格剧烈轮动时极易发生致命回撤？
Q3: 因子分层回测单调性破坏（Monotonicity Decay）：如果在单因子 5 分位（Q1~Q5）多空分层测试中，Q5（多头）显著跑赢基准，但 Q2 和 Q3 收益出现倒挂（如 Q2 > Q3 > Q4），从统计学与投资学看意味着什么？能否直接用于多因子线性加权评分？应如何进行非线性分段修复？

【评分与通过规则】
- 代码 4 分：MAD去极值与标准化 (1分) + Rank IC 向量化计算 (1分) + 分层回测与单调性度量 (2分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：必须从稳健统计量、风险模型与中性化展开论述
- 通过线：8/10 分。一票否决：未实现 Rank 秩转换、单调性得分计算错误
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
