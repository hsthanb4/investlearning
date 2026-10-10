r"""
================================================================================
模块 05：量化投资多因子与统计套利 · 第 4/5 课
第 4 课：机器学习多因子组合与非线性特征挖掘 (ML Factor Combination & Purged Walk-Forward)
================================================================================

【课程定位与第一性原理】
传统多因子模型采用线性加权（OLS 或 IC 权重），默认假定各个因子对收益率的贡献是相互独立且线性可加的。
然而，真实金融市场中充斥着复杂的非线性交互作用（如：高动量只有在低估值与高 ROIC 共振时才爆发）。
机器学习（如 GBDT、LightGBM、随机森林）能够自动挖掘深层非线性特征，但极易掉入“回测过拟合”的万劫不复深渊。
投资委员会在审视机器学习量化策略时，首要审查其是否严格执行了金融时序的因果清洗契约。

- **[金融机器学习的样本重叠泄漏]**：传统 K-Fold 随机切分在金融时序中彻底失效；前向多期持有收益标签的重叠（Overlapping Labels）会导致严重的未来信息渗透。
- **[Purged & Embargoed 滚动交叉验证]**：必须对训练集与测试集边界实施样本清洗（Purging）与隔离缓冲（Embargo），建立绝对零前视偏差的时序交叉验证。
- **[树模型集成与特征重要性]**：利用 GBDT 树模型的决策分叉提取因子非线性重要性，并以样本外（OOS）Rank IC 与多空收益作为唯一验收标准。

【核心概念与就近图文排版】

1. Purged & Embargoed 滚动步进交叉验证：
观察下图关于金融时序防泄漏交叉验证的样本重叠清洗与隔离期拓扑架构：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.4.1：金融机器学习 Purged &amp; Embargoed 滚动步进时序交叉验证</span>
    <span class="diagram-tag">PURGED-CV</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l04_purged_walk_forward_cv.svg -->
  </div>
</div>

- **[Purging 样本重叠清洗]**：若训练集样本的预测持有期跨越到了测试集的起始点，必须强制从训练集中剔除该样本，防止标签泄露。
- **[Embargo 隔离期缓冲]**：在测试集结束后追加一定时长的隔离期（通常为因子的自相关半衰期），防止时序自回归记忆泄露。
- **[Walk-Forward 步进推进]**：测试窗口随时间向前滚动推进，严格模拟实盘样本外无前视预测环境。

2. 梯度提升树因子非线性特征重要性：
下图展示了集成树模型自动学习多因子非线性交互后的特征重要性（SHAP）分解：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.4.2：梯度提升树 (GBDT / LightGBM) 因子非线性交互与 SHAP 重要度分解</span>
    <span class="diagram-tag">FEATURE-IMPORTANCE</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l04_tree_ensemble_feature_importance.svg -->
  </div>
</div>

- **[基本面与动量非线性共振]**：树模型优先以 ROIC-WACC 差额进行根节点切分，随后在优质资产子集内部切分动量与换手率。
- **[特征贡献度绝对归一]**：特征增益（Gain）重要性严格归一化为 100%，反映各维因子在集成预测中的边际决策权重。
- **[树深度与正则化约束]**：金融数据的信噪比极低，树最大深度必须控制在 3~5 层以内，防止拟合随机市场噪声。

3. 回测多重检验陷阱与伪发现率：
下图展示了随着模型尝试试验次数激增，样本内虚假夏普比率的非线性膨胀与样本外真实表现衰减：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.4.3：量化回测多重检验陷阱与伪发现率 (False Discovery Rate) 衰减律</span>
    <span class="diagram-tag">P-HACKING-DEFENSE</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m05_l04_overfitting_backtest_trap.svg -->
  </div>
</div>

- **[多重假设检验陷阱]**：测试 10,000 个随机特征必然能筛选出数个样本内夏普 $> 3.0$ 的假特征。
- **[折损夏普比率 DSR]**：显式对试验次数 $N$、收益偏度与超额峰度施加数学惩罚，推导真实未被过拟合污染的置信度。
- **[经济学因果链前置]**：任何因子在进入机器学习模型前，必须先具备扎实的商业逻辑与会计恒等支撑。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：金融数据与计算机视觉/NLP 的本质差异</div>
  <div class="callout-body">
    图像与自然语言的物理规律是静态不变的（猫永远是猫）；而金融市场是非平稳、对抗博弈、低信噪比（Signal-to-Noise Ratio < 5%）的自适应复杂系统。在金融领域盲目套用深度过参数化大模型，99% 的概率是在精确拟合历史噪声。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁使用未经 Purging 和 Embargo 隔离的时序数据作为模型回测证明！任何样本内夏普高达 4.0 但未经严格样本外步进验证的机器学习策略，实盘上线后必然遭遇净值永久归零。
  </div>
</div>

【数学与验证模型】
$$\text{Train\_Idx} = \{t \mid t \le T_{\text{train\_end}} - \text{Label\_Horizon}\}$$
$$\text{Test\_Idx} = \{t \mid T_{\text{test\_start}} \le t \le T_{\text{test\_end}}\}, \quad T_{\text{test\_start}} = T_{\text{train\_end}} + \text{Embargo}$$
$$\text{DSR} = \Phi\left(\frac{(\text{SR} - \text{SR}^*)\sqrt{T-1}}{\sqrt{1 - \gamma_3 \text{SR} + \frac{\gamma_4 - 1}{4}\text{SR}^2}}\right)$$
定义域：$\text{Train\_Len} > \text{Test\_Len} > \text{Embargo} \ge 0, \quad \text{DSR} \in [0, 1]$。

【思考题】
Q1: 金融时序中的样本重叠与 Purging / Embargo 机制：传统机器学习的 K-Fold 随机交叉验证为什么在金融资产回报率预测中是完全失效的？请从前向持有期重叠（Overlapping Labels）导致的严重信息泄露（Information Leakage）推导 López de Prado 的 Purged K-Fold 算法设计原理。
Q2: 线性多因子加权 vs 树模型集成（GBDT/LightGBM）：在挖掘 Alpha 时，树模型相比传统线性 IC 加权的核心优势是什么？树模型如何天然捕获多因子之间的“非线性条件交互”（例如：只有在低估值且高研发支出时，动量因子才显著有效）？
Q3: 多重假设检验（Multiple Testing）与折损夏普比率（Deflated Sharpe Ratio, DSR）：如果量化研究员尝试了 10,000 个公式化 Alpha 因子，筛选出一个样本内夏普高达 3.0 的因子，为什么投决会必须使用 Bailey & López de Prado 的 DSR 算法对试验次数 $N$ 进行严厉惩罚？伪发现率（FDR）如何摧毁实盘表现？

【评分与通过规则】
- 代码 4 分：时序 Purged & Embargoed 滚动切分生成器 (2分) + 随机森林/GBDT 因子集成与样本外验证 (2分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：从时序交叉验证、特征非线性交互与过拟合数学惩罚展开
- 通过线：8/10 分。一票否决：交叉验证存在时间倒流前视泄漏、样本外 Rank IC 计算错误
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
    生成带封锁隔离期 (Embargo) 的前向滚动时间序列交叉验证切分：
    - 训练集索引区间: [start, start + train_size)
    - 封锁隔离期 (Embargo): [start + train_size, start + train_size + embargo_size) 丢弃以阻断自相关泄露
    - 测试集索引区间: [start + train_size + embargo_size, start + train_size + embargo_size + test_size)
    - 每次向前滑动步长: test_size

    参数:
        n_samples: 总样本数量
        train_size: 训练集窗口长度
        test_size: 测试集窗口长度
        embargo_size: 封锁隔离窗口长度 (默认 1)

    返回:
        List[Tuple[np.ndarray, np.ndarray]]: 每折的 (train_indices, test_indices) 列表
    """
    # TODO: 实现带 Embargo 的前向滚动切分算法
    pass


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
    基于树模型的滚动 Walk-Forward 因子非线性合成与评价引擎：
    1. 调用 purged_walk_forward_splits 生成滚动切分；
    2. 遍历各折：
       - 使用训练集训练 RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)；
       - 对测试集执行样本外 (OOS) 预测；
       - 记录本折的特征重要性 (feature_importances_)；
    3. 拼接所有折的样本外预测得分序列与对应实际收益序列；
    4. 计算全区间样本外 Spearman Rank IC 与 p 值；
    5. 计算全区间特征平均重要性；
    6. 计算样本外预测打分最高 20% 组与最低 20% 组的单期平均多空收益差。

    返回字典包含:
        - "oos_predictions": 样本外预测得分 Series
        - "oos_actuals": 样本外真实收益 Series
        - "oos_rank_ic": 样本外 Spearman Rank IC
        - "oos_p_value": 样本外 Rank IC 显著性 p 值
        - "mean_feature_importances": 字典 {feature_name: importance}
        - "num_splits": 滚动切分折数
        - "oos_long_short_return": 样本外 Top 20% - Bottom 20% 单期平均超额
    """
    # TODO: 实现完整的滚动训练、样本外推断与评估流水线
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("运行 Lesson 04: 机器学习因子组合与 Walk-Forward 验证单元测试")
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
        # 验证时序严格前向因果关系与 Embargo 隔离
        assert max(tr_idx) + emb_len < min(te_idx), f"第 {fold_i} 折未严格满足训练集与测试集间的 Embargo 隔离约束"

    # 2. 构造具有非线性交互特征的多因子面板仿真数据
    np.random.seed(42)
    N = 300
    feature_names = ["VAL", "MOM", "QUAL", "VOL", "GROWTH"]
    n_feats = len(feature_names)

    X_mat = np.random.randn(N, n_feats)
    # 构造非线性复合关系:
    # 当 VAL > 0 且 QUAL > 0 时 (高价值且高质量)，收益有大幅非线性增益；同时 MOM 具有平稳正向动量
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
    # 核心有效特征 VAL 和 MOM 重要性应名列前茅
    assert (
        res["mean_feature_importances"]["VAL"] > 0.10
        and res["mean_feature_importances"]["MOM"] > 0.10
    ), "核心特征 VAL 或 MOM 重要性未能被模型有效识别"

    print("Lesson 04 机器学习因子组合单元测试全部通过！")
