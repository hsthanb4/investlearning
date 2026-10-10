r"""
================================================================================
模块 05：量化投资、多因子模型与统计套利 · 第 4/5 课
第 4 课：机器学习因子合成与带隔离时序交叉验证 (Machine Learning Factor Combination)
================================================================================

【课程定位与第一性原理】
在多因子量化投资的前沿实践中，传统的线性因子合成（等权加权、IC 加权、ICIR 倒数协方差加权）
建立在两个过于理想化的假设之上：
1. 因子与未来收益之间呈现恒定的线性正比关系；
2. 各因子之间相互独立，不存在非线性条件约束或高阶交互。

然而，真实的资本市场充满了深度的非线性结构与条件概率：
- 价值陷阱（Value Trap）：低估值（低 PE）若搭配恶化的盈利质量（负 ROE）与高财务杠杆，往往是濒临破产的信号；
  只有当高估值折扣与高资产回报率（High Quality）同时满足时，估值因子才释放强烈的正向 Alpha；
- 动量与波动非线性：高动量策略只有在低特质波动率（Low Volatility）环境下才具备极高的夏普比率，
  在极端高波动环境下盲目追逐高动量则极易发生灾难性的“动量崩溃（Momentum Crash）”。

梯度提升树（GBDT / Random Forest / LightGBM / XGBoost）能够天然学习特征空间的正交轴向切分，
自动捕捉高阶交互作用。但金融时间序列机器学习存在一个致命的死穴——数据泄露（Data Leakage）与伪泛化：
- 严禁使用普通统计机器学习的 K-Fold 随机打乱交叉验证！将未来的数据作为训练集预测过去的数据，
  会导致模型学习到未来的未来函数特征，产生虚假的高准确率，实盘必死无疑；
- 必须采用**带净化与封锁的前向滚动时序验证（Purged & Embargoed Walk-Forward Validation）**：
  训练窗口 $[t - T_{\text{train}}, t]$ $\to$ 封锁隔离期（Embargo） $\to$ 样本外测试窗口 $[t + \tau, t + \tau + T_{\text{test}}]$。

【核心流程与心智模型】
```mermaid
flowchart TD
    RawFactors["多因子特征面板 [VAL, MOM, QUAL, VOL, GROWTH]"] --> Standardize["截面 MAD 去极值 + 截面 Z-Score 标准化"]
    Standardize --> PurgedSplit["Purged Walk-Forward 滚动窗口切分 (训练集 + 封锁隔离期 + 测试集)"]
    
    subgraph 滚动时序推断流水线 (Walk-Forward Loops)
        PurgedSplit --> TrainWindow["训练集窗口 [t-T_train, t] ➔ 拟合随机森林/GBDT"]
        TrainWindow --> Embargo["封锁隔离期 (Embargo) ➔ 阻断自相关标签泄漏"]
        Embargo --> TestWindow["测试集窗口 [t+embargo, t+embargo+T_test] ➔ 样本外预测 OOS"]
        TestWindow --> RollStep["窗口向前滚动滑动步长 ➔ 迭代下一折"]
    end
    
    RollStep --> Aggregate["拼接全区间样本外预测时序 (OOS Composite Score)"]
    Aggregate --> OOS_Eval["样本外性能评价: OOS Rank IC / 特征重要性排序 / 多空分层收益"]
```

【工业界实战场景与风控陷阱】
1. 标签重叠（Label Overlap）与序列自相关污染：
   若模型预测目标为未来 5 天收益率（$R_{t \to t+5}$），则 $t$ 期的标签与 $t+1, \dots, t+4$ 期的标签共享了
   相同的价格波动信息。若不在训练集与测试集边界剔除重叠期（Purging），模型会直接“抄袭”未闭环的历史价格。
2. 特征重要性过拟合假象（MDI vs MDA）：
   树模型默认的基尼/方差不纯度减少（MDI）天然偏向连续型高方差噪音特征。工业界应结合置换特征重要性
   （Permutation Importance / MDA），通过破坏单列特征后观察样本外损失上升幅度，鉴别真正的有效特征。
3. 结构性体制断裂（Structural Regime Shift）：
   模型在低利率牛市环境训练出的非线性规则，在进入激进加息熊市时往往迅速失效。滚动窗口大小（Lookback Window）
   需要平衡“历史样本丰富度”与“最新市场体制适应性”。

【思考题】
Q1: 什么是金融机器学习中的“前视偏差”（Lookahead Bias）与“标签重叠”（Label Overlap）？如果采用未来 5 天收益率作为预测目标，为何未经 Purging 的标准交叉验证会导致样本外模型彻底失效？
Q2: 为什么在树模型特征重要性中，某些高频高波动的量价特征虽然被频繁分裂（Split Gain / MDI 很高），但在样本外预测时却导致灾难性过拟合？工业界如何用 Permutation Importance (MDA) 进行纠偏？
Q3: 怎样利用 SHAP (SHapley Additive exPlanations) 框架穿透机器学习黑盒模型？在量化投研报告或投资委员会答辩时，如何向合规与投资人解释单只股票的非线性综合打分因果逻辑？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现带封锁隔离期（Embargo）的 Walk-Forward 滚动切分生成器 (1.5分)；
  2. 准确构建树模型滚动训练与样本外预测拼接流水线 (1.5分)；
  3. 准确计算样本外 Rank IC、特征重要性与多空年化超额 (1分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须从时序因果链、特征重叠机制与金融可解释性展开；
- 通过线：8/10 分。一票否决：出现测试集时间先于训练集的反向泄露、删除断言校验。
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
