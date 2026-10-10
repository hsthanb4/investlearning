r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 1/5 课
第 1 课：单因子检验框架与 IC / Rank IC / 分组回测 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么在 A 股做因子预处理时，必须进行“去极值”（如三倍中位数绝对偏差 MAD）和“行业市值中性化”？如果未经市值中性化，一个估值因子（低 PE / 低 PB）可能会退化成什么？
- **MAD 去极值的必要性**：
  A 股市场存在资产重组、微利股（净利润接近 0 导致 PE 放大数千倍）、商誉减值以及极端涨跌停板，均值和标准差极易受到 1~2 个离群值的严重扭曲（样本崩溃点仅为 $1/N$）。
  三倍 MAD 采用中位数作为中心，具有高达 50% 的破损点（Breakdown Point），能够精准截断厚尾离群噪音，保障后续标准化与统计推断的稳健性。
- **行业与市值中性化的本质**：
  若不对低 PE 因子进行中性化，由于银行、建筑、煤炭等重资产高杠杆周期行业的估值长期显著低于半导体、软件等成长行业，低 PE 因子选出的股票将 80% 以上集中在传统金融周期板块。
  此时，策略赚取或亏损的并非“便宜公司修复”的真正选股 Alpha，而是承担了巨大的**周期行业 Beta 敞口**和**大盘蓝筹风格敞口**。一旦市场风格切换至成长科技牛市，该因子将遭遇长期灾难性回撤。
  通过行业虚拟变量与对数市值的截面回归：$F_i = \sum \beta_{\text{ind}} I_{i,\text{ind}} + \gamma \ln(\text{Cap}_i) + \epsilon_i$，提取残差 $\epsilon_i$，方能剥离外生风格，获得纯粹的选股能力。

【Q2 深度参考答案】
什么是因子衰减（Factor Decay）？如何绘制因子自相关衰减曲线，并据此科学确定最佳调仓换手周期（周频/月频/季频）？
- **因子衰减的经济学机制**：
  因子衰减是指因子得分所蕴含的预测信息随着预测窗口拉长（Lag $k$），由于市场交易者的套利消化与新信息涌入，其预测力（Rank IC）随时间单调递减的过程。
- **衰减测算与曲线绘制**：
  1. 因子自相关系数（Autocorrelation）：计算不同滞后期因子得分的截面相关性 $\rho(k) = \text{Corr}(F_t, F_{t+k})$；
  2. 跨期预测 IC 衰减结构：计算当前因子对未来第 $k$ 期收益率的预测力 $\text{Rank IC}(k) = \text{Corr}(\text{Rank}(F_t), \text{Rank}(R_{t+k-1 \to t+k}))$。
- **调仓周期确定准则**：
  - 高频微观量价因子（如日内订单流不平衡、反转因子）：自相关系数在 3~5 个交易日内迅速跌破 0.3，半衰期短，必须匹配日频或 2~3 日调仓，否则 Alpha 衰减殆尽；
  - 基本面因财务报表公布（如 ROE、毛利率变化）：信息半衰期长达 1~2 个季度，自相关系数在 20~40 日内仍保持在 0.8 以上，此时应匹配月频（Monthly）或季频（Quarterly）调仓，避免不必要的过度换手消耗成本。

【Q3 深度参考答案】
为什么单因子在不计交易成本时可能展现出高达 25% 的年化多空对冲收益，但一旦扣除双边万分之五佣金、千分之一印花税与市场冲击滑点后，净值曲线会迅速归零甚至倒亏？量化研究员应如何引入换手率惩罚与调仓缓冲带（Buffer Zone）？
- **成本复利侵蚀机制**：
  若一个单因子策略多空组合的单边换手率为 80%/周，年化双边换手率可高达 $80\% \times 2 \times 52 \approx 8320\%$。
  在 A 股市场，单次完整双边交易成本（印花税 0.05% + 佣金万 2.5 + 买卖价差冲击滑点万 5 $\approx 0.15\% \sim 0.2\%$）。
  全年仅摩擦成本就会硬生生吞噬资金：$83.2 \times 0.2\% \approx 16.64\%$。若再加上融券做空成本（融券年化利差通常在 6%~10%），25% 的纸面收益将被彻底归零，甚至大幅亏损。
- **量化工程应对方案**：
  1. **调仓缓冲带（Buffer Zone）**：引入迟滞区间。假设目标组合持有因子排名前 20%（例如前 20 只股票），再平衡时，只有当老持仓跌出前 30 名才执行调仓剔除；新候选股票必须升至前 10 名才触发买入。此举可将因临界位名次抖动产生的无效换手率压降 40%~60%。
  2. **换手率惩罚二次规划（Turnover Penalty Optimization）**：在多因子组合权重优化时，在效用函数中引入换手惩罚项：
     $$\max_w \; w^T \mu - \frac{\lambda}{2} w^T \Sigma w - c \sum_{i} |w_i - w_{i, \text{prev}}|$$
     迫使优化器仅在预期边际 Alpha 显著大于交易冲击成本时才调整持仓仓位。
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
