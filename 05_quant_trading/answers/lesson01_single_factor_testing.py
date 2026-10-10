r"""
================================================================================
模块 05：量化投资多因子与统计套利 · 第 1/5 课
第 1 课：单因子检验评价框架与 IC / Rank IC / 分层回测 (参考答案版)
================================================================================

【Q1 深度参考答案】
普通 IC（Pearson）vs 秩 IC（Rank IC）：为什么在 A 股或美股量化多因子检验中，机构级投研体系几乎只考核 Rank IC 而非传统 Pearson IC？请从资产收益率的非正态分布、极端长尾异常值（Outliers）以及非线性单调映射的鲁棒性角度进行严格数学推导。
- **[收益率肥尾与皮尔逊相关系数的非稳健性]**：Pearson 相关系数建立在二元正态分布与线性因果假说之上。然而真实金融收益率呈现严重肥尾分布（Kurtosis > 10）。单只出现重大暴雷（-80%）或特大并购重组（+200%）的个股异常值，由于离差平方的敏感性，能瞬间主导整个截面的协方差计算，导致 Pearson IC 产生严重的虚假正向或负向偏倚。
- **[秩相关（Spearman Rank）对单调关系的非参数不变性]**：Rank IC 将绝对得分映射为均匀离散的次序排名（$1, 2, \dots, N$）。无论单只股票涨幅是 10% 还是 1000%，其在截面上的排名均为第一位，彻底将离群点影响限制在边界之内。此外，Rank IC 衡量的是“单调关系”而非“线性关系”——只要因子能正确识别出相对优劣排序，即使收益率与因子值之间是非线性的幂律关系，Rank IC 依然能准确捕捉。
- **[量化投资组合构建的本质契约]**：在多因子量化选股中，投资组合管理器的最终动作是“根据因子排序等权或倾斜配置前 10% 股票”。组合绩效严格取决于股票的相对排序精度，而非因子原始数值与绝对收益的线性比例。因此，Rank IC 与实际投资落地行为在数学形式上是完全同构且无偏的。

【Q2 深度参考答案】
因子中性化（Neutralization）与纯 Alpha 提纯：如果一个账面市值比（BP）因子在未经行业和市值中性化时年化多空夏普高达 2.5，但在通过 OLS 残差回归剔除申万一级行业哑变量与对数市值（Log Market Cap）后夏普骤降至 0.3，从投资组合风控视角看，这说明该因子真实赚取的是什么钱？为什么未经中性化的因子在风格剧烈轮动时极易发生致命回撤？
- **[收益来源穿透：被动风格暴露而非选股能力]**：该现象表明，未经中性化的 BP 因子之所以表现优异，并不是因为它在各行业内部挑出了被低估的优质个股，而是因为高 BP 股票高度集中在周期性重资产行业（如银行、钢铁、煤炭、地产）并且偏向中小市值。该因子的所谓“Alpha 收益”，90% 以上本质是这些传统行业与小市值股票在特定宏观顺周期中的 Beta 贝塔溢价。
- **[宏观风格反转时的脆弱性崩塌]**：在成长股大牛市或宏观流动性宽松周期中（如 2019~2020 年以白酒、新能源、半导体为主导的行情），周期重资产行业长期跑输，小市值因子遭遇贴水。未经中性化的多头组合由于被动满仓了高 BP 行业，将遭受毁灭性的单边持续回撤，夏普比率直接转负。
- **[纯 Alpha 提纯的投决会价值]**：通过对行业哑变量与对数市值进行 OLS 回归提取残差因子 $\epsilon_i$，能够确保组合在各行业内实现中性配置，将选股能力与宏观行业轮动彻底解耦。尽管中性化后夏普从 2.5 降至 0.3，但这是一个“纯净、低相关且可全天候复制的真 Alpha”，在多因子组合与杠杆对冲中具有无可替代的配置价值。

【Q3 深度参考答案】
因子分层回测单调性破坏（Monotonicity Decay）：如果在单因子 5 分位（Q1~Q5）多空分层测试中，Q5（多头）显著跑赢基准，但 Q2 和 Q3 收益出现倒挂（如 Q2 > Q3 > Q4），从统计学与投资学看意味着什么？能否直接用于多因子线性加权评分？应如何进行非线性分段修复？
- **[非线性凹凸性与结构性阈值效应]**：Q2 > Q3 倒挂意味着因子对股票中间梯队的区分能力完全失效，甚至呈现出 U 型或倒 U 型非线性特征。这通常发生在“极值具有边际效用、但中间态存在噪音扰动”的因子中（例如研发费用率：过高研发可能产生创新突破，过低研发可能节省成本，中等研发反而两头不讨好陷入泥潭）。
- **[线性加权模型的崩溃诱因]**：严禁将此类单调性破坏的因子直接代入多元线性回归或等权打分模型！线性模型假定 $X$ 每增加一个单位，$Y$ 获得固定的边际增量。若强行使用线性加权，处于 Q2 梯队的股票会被赋予较低权重，但其历史表现却优于 Q3 股票，直接导致组合优化器产生病态配置失误。
- **[非线性分段修复与工程治理方案]**：
  1. **分段虚拟哑变量化（Bucket Dummies）**：放弃连续数值，将因子离散化为仅奖励 Q5、惩罚 Q1，对中间 Q2~Q4 赋予零权重的分类特征；
  2. **非线性样条转换（Spline Regression）**：利用三次样条函数拟合因子与收益率之间的非线性曲率，将其转化为单调递增的新特征；
  3. **树模型非线性学习**：改用 GBDT 等树模型替代线性模型，利用树节点的离散分叉自动识别非单调区间的最佳切分点。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：拒绝虚假夏普，拥抱正交中性</div>
  <div class="callout-body">
    单因子测试是科学证伪的过程，而非美化回测的画皮。一个无法在分层单调性与行业市值中性化下生存的因子，绝不容许进入实盘多因子Alpha模型库。
  </div>
</div>
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def preprocess_factor_scores(scores: pd.Series, n_mad: float = 3.0) -> pd.Series:
    """
    因子横截面数据预处理：MAD 去极值与 Z-Score 截面标准化
    """
    s = scores.copy()
    valid = s.dropna()
    if len(valid) == 0:
        return s

    # 1. MAD 去极值
    median = valid.median()
    mad = (valid - median).abs().median()
    threshold = n_mad * 1.4826 * mad

    if threshold > 1e-12:
        s_clipped = s.clip(lower=median - threshold, upper=median + threshold)
    else:
        s_clipped = s

    # 2. Z-Score 标准化
    mean_val = s_clipped.mean()
    std_val = s_clipped.std()
    if std_val > 1e-12:
        s_norm = (s_clipped - mean_val) / std_val
    else:
        s_norm = s_clipped - mean_val

    return s_norm


def calculate_rank_ic(factor_scores: pd.Series, forward_returns: pd.Series) -> float:
    """
    计算单个时间截面上的 Spearman Rank IC（秩相关系数）
    """
    df = pd.DataFrame({"factor": factor_scores, "return": forward_returns}).dropna()
    if len(df) < 3:
        return 0.0

    res = stats.spearmanr(df["factor"], df["return"])
    corr = res.statistic
    if np.isnan(corr):
        return 0.0
    return float(corr)


def evaluate_factor_performance(
    factor_df: pd.DataFrame,
    forward_returns_df: pd.DataFrame,
    num_groups: int = 5,
    annual_periods: int = 252,
) -> Dict[str, Any]:
    """
    完整的单因子评价框架
    """
    dates = factor_df.index
    rank_ics = []
    group_returns_dict = {g: [] for g in range(num_groups)}

    for d in dates:
        f_row = factor_df.loc[d]
        r_row = forward_returns_df.loc[d]

        # 预处理
        f_clean = preprocess_factor_scores(f_row)
        df = pd.DataFrame({"factor": f_clean, "ret": r_row}).dropna()
        if len(df) < num_groups:
            continue

        # 计算 Rank IC
        res = stats.spearmanr(df["factor"], df["ret"])
        corr = float(res.statistic)
        if not np.isnan(corr):
            rank_ics.append(corr)

        # 5 分组回测：按因子得分从高到低排序 (组 0: Top, 组 num_groups-1: Bottom)
        df_sorted = df.sort_values(by="factor", ascending=False)
        chunks = np.array_split(df_sorted["ret"].values, num_groups)
        for g_idx in range(num_groups):
            group_returns_dict[g_idx].append(chunks[g_idx].mean())

    rank_ic_s = pd.Series(rank_ics)
    mean_ic = float(rank_ic_s.mean())
    std_ic = float(rank_ic_s.std(ddof=1))
    icir = float((mean_ic / std_ic) * np.sqrt(annual_periods)) if std_ic > 1e-12 else 0.0

    t_res = stats.ttest_1samp(rank_ic_s, 0.0)
    t_stat = float(t_res.statistic)
    p_val = float(t_res.pvalue)
    hit_ratio = float((rank_ic_s > 0).mean())

    # 各组年化收益率
    group_annual_returns = [float(np.mean(group_returns_dict[g]) * annual_periods) for g in range(num_groups)]

    # 多空对冲组合收益 (Top 组减 Bottom 组)
    top_rets = np.array(group_returns_dict[0])
    bottom_rets = np.array(group_returns_dict[num_groups - 1])
    ls_rets = top_rets - bottom_rets
    long_short_annual_return = float(np.mean(ls_rets) * annual_periods)
    ls_std = float(np.std(ls_rets, ddof=1) * np.sqrt(annual_periods))
    long_short_sharpe = float(long_short_annual_return / ls_std) if ls_std > 1e-12 else 0.0

    # 单调性得分：Top 组至 Bottom 组预期收益单调递减，对应组权重 [5, 4, 3, 2, 1] 的秩相关系数
    expected_order = list(range(num_groups, 0, -1))
    mono_res = stats.spearmanr(group_annual_returns, expected_order)
    monotonicity_score = float(mono_res.statistic)

    return {
        "mean_rank_ic": mean_ic,
        "std_rank_ic": std_ic,
        "icir": icir,
        "t_stat": t_stat,
        "p_value": p_val,
        "ic_hit_ratio": hit_ratio,
        "group_annual_returns": group_annual_returns,
        "long_short_annual_return": long_short_annual_return,
        "long_short_sharpe": long_short_sharpe,
        "monotonicity_score": monotonicity_score,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 01: 单因子检验框架单元测试与断言验证 (参考答案版)")
    print("=" * 70)

    # 1. 检验单截面预处理 (MAD 去极值 + Z-Score 标准化)
    raw_s = pd.Series([1.0, 2.0, 2.1, 1.9, 100.0, -50.0], index=[f"S{i}" for i in range(6)])
    clean_s = preprocess_factor_scores(raw_s, n_mad=3.0)
    assert clean_s is not None, "预处理函数不能返回 None"
    assert abs(clean_s.mean()) < 1e-6, "标准化后均值应为 0"
    assert abs(clean_s.std() - 1.0) < 1e-4, "标准化后方差应为 1"
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

    factor_mat = np.random.randn(n_days, n_stocks)
    noise_mat = np.random.randn(n_days, n_stocks)
    forward_ret_mat = 0.05 * factor_mat + 0.15 * noise_mat

    factor_panel = pd.DataFrame(factor_mat, index=dates, columns=stock_cols)
    returns_panel = pd.DataFrame(forward_ret_mat, index=dates, columns=stock_cols)

    metrics = evaluate_factor_performance(factor_panel, returns_panel, num_groups=5, annual_periods=252)

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

    print("Lesson 01 参考答案测试全部通过 (Exit Code 0)！")
