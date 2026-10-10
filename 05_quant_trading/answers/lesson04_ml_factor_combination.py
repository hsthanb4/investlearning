r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 4/5 课
第 4 课：机器学习因子合成与带隔离时序交叉验证 (参考答案版)
================================================================================

【Q1 深度参考答案】
什么是金融机器学习中的“前视偏差”（Lookahead Bias）与“标签重叠”（Label Overlap）？如果采用未来 5 天收益率作为预测目标，为何未经 Purging 的标准交叉验证会导致样本外模型彻底失效？
- **前视偏差与标签重叠机制**：
  1. **前视偏差（Lookahead Bias）**：指在时序特征工程、截面标准化或模型训练时，直接或间接渗入了在做决策时刻尚未发生或未公开的未来信息（例如：在计算历史因子分位数时使用了包含了未来的全样本均值/标准差；或者未按实际披露公告日对齐上市公司财报）；
  2. **标签重叠（Label Overlap）**：当预测目标为跨越多期的累积收益率（如未来 5 日收益 $Y_t = \frac{P_{t+5} - P_t}{P_t}$）时，样本 $t$ 的标签时间跨度为 $[t, t+5]$，样本 $t+1$ 的标签跨度为 $[t+1, t+6]$。两者共享了 $t+1 \to t+5$ 共计 4 个交易日的真实收益率信息。
- **未经 Purging 的标准 CV 致命性**：
  在常规机器学习的 K-Fold 随机打乱切分中，样本 $t$ 可能被划入测试集，而样本 $t+1$ 被划入训练集。
  由于标签重叠，训练集中的模型实质上已经预先“偷看”了测试集在接下来 4 天内的价格走势。模型在训练和验证时会表现出极高、虚假的准确率与夏普比率（过拟合到自相关噪声上）。
  但一旦部署至实盘，真实交易日永远无法提前获取未来的重叠信息，模型必然遭遇断崖式的样本外失效甚至重大穿仓亏损。
- **Purging（净化）与 Embargo（封锁）解决方案**：
  Marcos López de Prado (2018) 在《Advances in Financial Machine Learning》中确立了工业标准：
  - **Purging**：在训练集中，凡是标签生命周期与测试集任何样本产生交集的数据点，必须硬性强制剔除；
  - **Embargo**：在测试集时间窗口之后，额外增设一个相当于自相关半衰期的冷却隔离期（Embargo Zone），阻断序列自回归记忆对后续训练集的残余泄露。

【Q2 深度参考答案】
为什么在树模型特征重要性中，某些高频高波动的量价特征虽然被频繁分裂（Split Gain / MDI 很高），但在样本外预测时却导致灾难性过拟合？工业界如何用 Permutation Importance (MDA) 进行纠偏？
- **MDI（不纯度减少 / Split Gain）的结构性缺陷**：
  树模型默认的 MDI 特征重要性统计的是在所有决策树节点上分裂时，目标变量方差或基尼不纯度的累计下降总和。
  1. **高基数特征偏向（High Cardinality Bias）**：高频、连续且波动剧烈的量价特征（如日内分钟极差、微观成交量震荡）具有几乎无限的候选分裂阈值点；
  2. 决策树贪心算法（Greedy Search）极容易在这些高方差噪声特征上找到能够碰巧契合历史特定样本的局部切分，从而被频繁选为分裂节点，虚假推高了 MDI 得分；
  3. 实质上，模型只是在利用高维特征“死记硬背”历史样本的随机游走噪声，根本不具备统计因果规律。
- **MDA（Mean Decrease Accuracy / Permutation Importance）纠偏原理**：
  1. 必须在**完全独立的样本外测试集（Out-of-Sample）**上执行置换检验；
  2. 首先计算模型在完整 OOS 测试集上的基准预测损失 $\mathcal{L}_{\text{base}}$（如 MSE 或负 Rank IC）；
  3. 固定其他特征不变，将目标特征 $X_j$ 在测试集样本维度进行随机打乱（Permute/Shuffle），彻底破坏该特征与未来收益的真实对应关系；
  4. 计算打乱后的样本外预测损失 $\mathcal{L}_{\text{perm}, j}$，特征 $j$ 的置换重要性定义为：
     $$\text{MDA}_j = \mathcal{L}_{\text{perm}, j} - \mathcal{L}_{\text{base}}$$
  5. 若某个在训练集高频分裂的高频噪声特征在测试集被打乱后，模型损失几乎没有上升甚至反而下降（$\text{MDA} \le 0$），即可铁证该特征纯属过拟合噪声，工业界应立即将其从因子库中剔除。

【Q3 深度参考答案】
怎样利用 SHAP (SHapley Additive exPlanations) 框架穿透机器学习黑盒模型？在量化投研报告或投资委员会答辩时，如何向合规与投资人解释单只股票的非线性综合打分因果逻辑？
- **Shapley 值的合作博弈论公理体系**：
  SHAP 基于诺贝尔经济学奖得主 Lloyd Shapley 的合作博弈价值分配理论。它将输入模型的每一个特征视为参与收益分配的“博弈玩家”，输出打分等于基线期望与各特征边际贡献之和：
  $$f(x) = \phi_0 + \sum_{j=1}^M \phi_j(x)$$
  满足效率性（Efficiency）、对称性（Symmetry）、虚拟性（Dummy）与可加性（Additivity）四大唯一定价公理。
- **工业界投研汇报与合规穿透实战**：
  1. **单只股票打分的水瀑图穿透（Waterfall / Force Plot）**：
     在投资委员会上，若模型推荐重仓某股票（如给某芯片龙头打出 0.88 的超高综合分，全市场排名前 0.5%），量化总监可以向合规官清晰穿透分解因果链条：
     - 全市场基础打分期望 $\phi_0 = 0.50$；
     - 近期研发投入占比激增（Growth 特征）贡献了边际增益 $+0.18$；
     - 毛利率处在行业前 5%（Quality 特征）贡献了 $+0.14$；
     - 过去 20 日特质波动率处于极低分位数（Low Vol 特征）贡献了 $+0.10$；
     - 尽管静态市盈率偏高（Value 特征）产生了负向惩罚 $-0.04$；
     - 最终合成得分 $0.50 + 0.18 + 0.14 + 0.10 - 0.04 = 0.88$。因果清晰，彻底终结黑盒黑箱质疑；
  2. **非线性交互曲面的直观展示（SHAP Dependence Plot）**：
     通过绘制“估值因子 SHAP 贡献值随着盈利质量 ROE 变化的散点图”，向投资人直观证实：模型学会了“当 ROE < 0 时，低估值不仅不加分反而被惩罚（识别价值陷阱）；只有当 ROE > 15% 时，低估值才触发指数级加分”。这不仅打消了客户对纯算法的疑虑，更证明了量化系统契合深层金融经济学常理。
"""

from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestRegressor


def purged_walk_forward_splits(
    n_samples: int,
    train_size: int,
    test_size: int,
    embargo_size: int = 1,
) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    生成带封锁隔离期 (Embargo) 的前向滚动时间序列交叉验证切分
    """
    splits = []
    start = 0
    while start + train_size + embargo_size + test_size <= n_samples:
        train_idx = np.arange(start, start + train_size)
        test_start = start + train_size + embargo_size
        test_idx = np.arange(test_start, test_start + test_size)
        splits.append((train_idx, test_idx))
        start += test_size
    return splits


def train_and_evaluate_ml_factor_combination(
    features_df: pd.DataFrame,
    target_returns: pd.Series,
    train_size: int = 120,
    test_size: int = 30,
    embargo_size: int = 2,
    n_estimators: int = 30,
    max_depth: int = 3,
) -> Dict[str, Any]:
    """
    基于树模型的滚动 Walk-Forward 因子非线性合成与评价引擎
    """
    splits = purged_walk_forward_splits(
        len(features_df),
        train_size=train_size,
        test_size=test_size,
        embargo_size=embargo_size,
    )

    oos_preds = []
    oos_actuals = []
    feature_importances_list = []

    for tr_idx, te_idx in splits:
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
        )
        X_tr = features_df.iloc[tr_idx]
        y_tr = target_returns.iloc[tr_idx]
        model.fit(X_tr, y_tr)

        X_te = features_df.iloc[te_idx]
        preds = model.predict(X_te)

        oos_preds.extend(preds)
        oos_actuals.extend(target_returns.iloc[te_idx].values)
        feature_importances_list.append(model.feature_importances_)

    oos_preds_s = pd.Series(oos_preds)
    oos_actuals_s = pd.Series(oos_actuals)

    # 计算样本外 Spearman Rank IC 与显著性
    ric, p_val = stats.spearmanr(oos_preds_s, oos_actuals_s)

    # 归一化平均特征重要性
    mean_fi = np.mean(feature_importances_list, axis=0)
    total_fi = np.sum(mean_fi)
    if total_fi > 1e-12:
        mean_fi_norm = mean_fi / total_fi
    else:
        mean_fi_norm = mean_fi
    fi_dict = {col: float(mean_fi_norm[i]) for i, col in enumerate(features_df.columns)}

    # 样本外 Top 20% vs Bottom 20% 多空平均单期超额
    eval_df = pd.DataFrame({"pred": oos_preds_s, "actual": oos_actuals_s})
    q_top = eval_df["pred"].quantile(0.8)
    q_bot = eval_df["pred"].quantile(0.2)
    top_ret = eval_df[eval_df["pred"] >= q_top]["actual"].mean()
    bot_ret = eval_df[eval_df["pred"] <= q_bot]["actual"].mean()
    ls_ret = float(top_ret - bot_ret)

    return {
        "oos_predictions": oos_preds_s,
        "oos_actuals": oos_actuals_s,
        "oos_rank_ic": float(ric),
        "oos_p_value": float(p_val),
        "mean_feature_importances": fi_dict,
        "num_splits": len(splits),
        "oos_long_short_return": ls_ret,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 04: 机器学习因子组合与 Walk-Forward 验证单元测试 (参考答案版)")
    print("=" * 70)

    # 1. 验证带 Embargo 的 Walk-Forward 切分正确性
    n_total = 20
    tr_len = 8
    te_len = 3
    emb_len = 2
    splits = purged_walk_forward_splits(n_total, tr_len, te_len, embargo_size=emb_len)

    assert len(splits) > 0, "切分结果列表不能为空"
    for fold_i, (tr_idx, te_idx) in enumerate(splits):
        assert len(tr_idx) == tr_len, f"第 {fold_i} 折训练集长度不符"
        assert len(te_idx) == te_len, f"第 {fold_i} 折测试集长度不符"
        assert max(tr_idx) + emb_len < min(te_idx), f"第 {fold_i} 折未严格满足训练集与测试集间的 Embargo 隔离约束"

    # 2. 构造具有非线性交互特征的多因子面板仿真数据
    np.random.seed(42)
    N = 300
    feature_names = ["VAL", "MOM", "QUAL", "VOL", "GROWTH"]
    n_feats = len(feature_names)

    X_mat = np.random.randn(N, n_feats)
    y_raw = (
        0.35 * X_mat[:, 0] * (X_mat[:, 2] > 0.0)
        + 0.25 * X_mat[:, 1]
        - 0.15 * (X_mat[:, 3] ** 2)
        + 0.40 * np.random.randn(N)
    )

    feat_df = pd.DataFrame(X_mat, columns=feature_names)
    ret_series = pd.Series(y_raw)

    res = train_and_evaluate_ml_factor_combination(
        feat_df,
        ret_series,
        train_size=120,
        test_size=30,
        embargo_size=2,
        n_estimators=30,
        max_depth=3,
    )

    print(f"总计完成 Walk-Forward 滚动折数: {res['num_splits']}")
    print(f"样本外预测点数量: {len(res['oos_predictions'])}")
    print(f"样本外 Spearman Rank IC: {res['oos_rank_ic']:.4f} (p-val: {res['oos_p_value']:.4e})")
    print(f"样本外 Top-Bottom 20% 平均单期多空收益: {res['oos_long_short_return']:.4f}")
    print("各因子平均特征重要性:")
    for f_name, imp in res["mean_feature_importances"].items():
        print(f"  {f_name:8s}: {imp:.4f}")

    # 3. 统计断言检验
    assert res["num_splits"] >= 4, f"切分折数应至少为 4, 实际: {res['num_splits']}"
    assert len(res["oos_predictions"]) == len(res["oos_actuals"]), "样本外预测与真实标签长度必须一致"
    assert res["oos_rank_ic"] > 0.30, f"非线性合成因子样本外 Rank IC 应显著大于 0.30, 实际: {res['oos_rank_ic']:.4f}"
    assert res["oos_long_short_return"] > 0.10, f"样本外多空组合收益应大于 0.10, 实际: {res['oos_long_short_return']:.4f}"
    assert abs(sum(res["mean_feature_importances"].values()) - 1.0) < 1e-4, "特征重要性总和应归一化为 1.0"
    assert (
        res["mean_feature_importances"]["VAL"] > 0.10
        and res["mean_feature_importances"]["MOM"] > 0.10
    ), "核心特征 VAL 或 MOM 重要性未能被模型有效识别"

    print("Lesson 04 参考答案单元测试全部通过 (Exit Code 0)！")
