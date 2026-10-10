r"""
# 模块 07：行为金融学、交易心理与执行纪律 · 第 3 课：数字化交易日志与贝叶斯复盘归因

> 状态：**学习中（待提交）**  
> 本课程采用逐课通过制。请先独立完成练习题后再核对答案分支。

---
## 本课目标与完成标准

学完后你应能：
1. 搭建职业操盘手数字化交易日志数据模型，结构化记录交易上下文、执行偏离与心理情绪标记；
2. 深刻理解迈克尔·莫布森（Michael Mauboussin）“过程 vs 结果”决策四象限，辨别交易中的运气与技能；
3. 掌握经典期望收益模型（胜率、盈亏比、数学期望、Profit Factor）与情绪打分和盈亏的皮尔逊相关性分析；
4. 运用共轭先验贝叶斯推断（Beta-Binomial Model）动态更新策略真实胜率后验分布，破除小样本过度自信。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，剖析“坏过程带来好结果（有毒的运气）”对交易生涯的毁灭性影响。

---
## 核心心智模型与决策四象限

### 1. 过程 vs 结果四象限 (The Success Equation)

在具有高度随机性与不确定性的金融市场中，单笔交易的结果受到巨大方差（运气）的扰动：

```
                    ┌─────────────────────────┬─────────────────────────┐
                    │       好结果 (盈利)       │       坏结果 (亏损)       │
 ┌──────────────────┼─────────────────────────┼─────────────────────────┤
 │ 好过程 (遵守规则) │   理所应当的成功        │       合理的代价        │
 │                  │ (Deserved Success /     │ (Bad Break / Unlucky    │
 │                  │  Skill-Driven)          │  Variance, 坚守策略)    │
 ├──────────────────┼─────────────────────────┼─────────────────────────┤
 │ 坏过程 (违规侥幸) │       最致命的毒药      │       合乎逻辑的惩罚    │
 │                  │ (Dumb Luck / Toxic      │ (Poetic Justice /       │
 │                  │  Reinforcement, 促成大亏)│  违规被市场制裁)        │
 └──────────────────┴─────────────────────────┴─────────────────────────┘
```

- **理所应当的成功**：严格按计划开仓止损，顺应市场概率获利。
- **合理的代价**：入场逻辑、止损点设置完全合规，但因概率分布中的正常回撤被止损。这是经营交易生意的“必要成本”，必须平静接受并持续执行。
- **最致命的毒药（Dumb Luck）**：违反风控、死扛加仓、未设止损，但因为突发利好侥幸解套并大赚。这种“坏过程好结果”会在大脑中建立极其危险的正反馈回路，诱使交易员在未来重仓违规，直至单次黑天鹅导致爆仓。
- **合乎逻辑的惩罚**：违规交易并被市场重创，应当作为痛定思痛的警醒案例。

### 2. 贝叶斯胜率动态更新 (Beta-Binomial Conjugate Model)

面对前 10 笔交易中获胜 8 笔（样本胜率 80%）的策略，初学者容易陷入过度自信（Overconfidence）。
使用贝叶斯方法，假设先验分布为 $\text{Beta}(\alpha_0, \beta_0)$：
- 若观察到 $k$ 次盈利，$n-k$ 次亏损；
- 胜率 $p$ 的后验分布为 $\text{Beta}(\alpha_0 + k, \beta_0 + n - k)$；
- 后验均值期望胜率为：
$$
\mathbb{E}[p | \text{Data}] = \frac{\alpha_0 + k}{\alpha_0 + \beta_0 + n}
$$
这能有效通过先验信息平滑小样本噪声，给出理性期望。
"""

import math
from typing import List, Dict, Any, Tuple


class TradeJournalAnalyzer:
    """
    数字化交易日志量化复盘与绩效归因分析器。
    """

    def __init__(self, trades: List[Dict[str, Any]]):
        self.trades = trades

    def compute_performance_metrics(self) -> Dict[str, float]:
        """
        计算交易核心绩效指标：
        - 胜率 (win_rate)
        - 平均盈利额 (avg_win)
        - 平均亏损额 (avg_loss, 绝对值)
        - 盈亏比 (payoff_ratio = avg_win / avg_loss)
        - 单笔数学期望 (expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss)
        - 获利因子 (profit_factor = 总盈利额 / 总亏损额)
        - 最大单笔亏损 (max_single_loss, 绝对值正数)
        """
        # TODO: 提取胜率、平均盈亏、盈亏比、数学期望、获利因子及最大单笔亏损
        pass

    def calculate_emotion_pnl_correlation(self) -> float:
        """
        计算交易者心理情绪打分 (emotional_score: 1冷静 ~ 5焦虑狂躁) 与 实际盈亏 (pnl) 的皮尔逊相关系数。
        r = Cov(X, Y) / (Std(X) * Std(Y))
        """
        # TODO: 计算 X (emotional_score) 与 Y (pnl) 的皮尔逊相关系数，保留 4 位小数
        pass

    def bayesian_win_rate_update(self, prior_alpha: float = 2.0, prior_beta: float = 2.0) -> Dict[str, float]:
        """
        Beta-Binomial 贝叶斯共轭更新：
        - prior_alpha, prior_beta: 先验参数
        - k: 盈利交易笔数
        - n: 总交易笔数
        后验参数：alpha_post = prior_alpha + k, beta_post = prior_beta + n - k
        后验期望胜率：alpha_post / (alpha_post + beta_post)
        后验方差与标准差：Var = (alpha * beta) / ((alpha + beta)^2 * (alpha + beta + 1))
        """
        # TODO: 计算并返回后验参数、期望胜率与后验标准差
        pass

    def process_outcome_matrix(self) -> Dict[str, int]:
        """
        根据“过程执行度 (plan_followed)”与“结果 (pnl > 0)”划分决策四象限：
        - deserved_success: 遵守规则且盈利 (Skill)
        - bad_break: 遵守规则但亏损 (Unlucky Variance)
        - dumb_luck: 违规但盈利 (Toxic Luck)
        - poetic_justice: 违规且亏损 (Penalty)
        """
        # TODO: 遍历交易记录，统计落在四个象限中的交易笔数
        pass


# ==============================================================================
# Q1~Q3 深度思考题（请在作答区填写因果链推导）
# ==============================================================================
r"""
### Q1：为什么“坏过程 + 好结果（Dumb Luck / 侥幸获利）”被职业对冲基金经理视为操盘手生涯中最致命的毒药？请结合斯金纳箱（Skinner Box）操作性条件反射解释其机理。

**你的答案：**
[在此处写下你的分析：需阐述间歇性强化机制、错误奖赏回路建立，以及未来面对黑天鹅时的必然爆仓命运]


### Q2：当一套新量化策略在回测或小样本实盘中取得 10 战 8 胜（胜率 80%）的亮眼战绩时，贝叶斯推断（以 Beta(2,2) 为先验）如何有效抑制交易团队的过度拟合与过度自信？

**你的答案：**
[在此处写下你的分析：需推导样本方差与伪夏普现象，并结合 Beta-Binomial 共轭更新的均值收缩机制进行数值说明]


### Q3：在数字化交易日志中，为何必须将“情绪打分与盈亏的相关性（Pearson Correlation）”作为长周期风控评估项？

**你的答案：**
[在此处写下你的分析：需说明情绪倾侧对净值侵蚀的量化验证，以及如何据此建立客观的准入与风控熔断机制]
"""


# ==============================================================================
# 单元测试与断言校验（请勿修改）
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] TradeJournalAnalyzer Performance Metrics...")
    test_trades = [
        {"trade_id": 1, "pnl": 500.0, "plan_followed": True, "emotional_score": 1},
        {"trade_id": 2, "pnl": 300.0, "plan_followed": True, "emotional_score": 2},
        {"trade_id": 3, "pnl": -200.0, "plan_followed": True, "emotional_score": 2},
        {"trade_id": 4, "pnl": -100.0, "plan_followed": True, "emotional_score": 2},
        {"trade_id": 5, "pnl": 400.0, "plan_followed": False, "emotional_score": 4},
        {"trade_id": 6, "pnl": -600.0, "plan_followed": False, "emotional_score": 5},
    ]

    analyzer = TradeJournalAnalyzer(test_trades)
    metrics = analyzer.compute_performance_metrics()

    assert metrics["total_trades"] == 6
    assert metrics["win_rate"] == 0.5000
    assert metrics["payoff_ratio"] == 1.3333
    assert metrics["expectancy"] == 50.0
    assert metrics["profit_factor"] == 1.3333
    assert metrics["max_single_loss"] == 600.0

    print("[Testing] Emotional Score & PnL Correlation...")
    corr = analyzer.calculate_emotion_pnl_correlation()
    assert corr == -0.5338, f"Expected -0.5338, got {corr}"

    print("[Testing] Bayesian Win Rate Update...")
    bayes = analyzer.bayesian_win_rate_update(prior_alpha=2.0, prior_beta=2.0)
    assert bayes["posterior_alpha"] == 5.0
    assert bayes["posterior_beta"] == 5.0
    assert bayes["posterior_mean_win_rate"] == 0.5000
    assert abs(bayes["posterior_std"] - 0.1508) < 1e-4

    print("[Testing] Process vs Outcome Matrix...")
    quadrants = analyzer.process_outcome_matrix()
    assert quadrants["deserved_success"] == 2
    assert quadrants["bad_break"] == 2
    assert quadrants["dumb_luck"] == 1
    assert quadrants["poetic_justice"] == 1

    empty_analyzer = TradeJournalAnalyzer([])
    empty_metrics = empty_analyzer.compute_performance_metrics()
    assert empty_metrics["total_trades"] == 0
    assert empty_analyzer.calculate_emotion_pnl_correlation() == 0.0

    print("All assertions passed! Module 07 Lesson 03 verification successful.")
