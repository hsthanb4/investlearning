r"""
# 模块 07：行为金融学、交易心理与执行纪律 · 第 3 课：数字化交易日志与贝叶斯复盘归因

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

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
        if not self.trades:
            return {
                "total_trades": 0,
                "win_rate": 0.0,
                "payoff_ratio": 0.0,
                "expectancy": 0.0,
                "profit_factor": 0.0,
                "max_single_loss": 0.0
            }

        wins = [t["pnl"] for t in self.trades if t["pnl"] > 0]
        losses = [abs(t["pnl"]) for t in self.trades if t["pnl"] < 0]

        total_trades = len(self.trades)
        win_rate = len(wins) / total_trades if total_trades > 0 else 0.0

        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = sum(losses) / len(losses) if losses else 0.0

        payoff_ratio = (avg_win / avg_loss) if avg_loss > 0 else 0.0
        expectancy = win_rate * avg_win - (1.0 - win_rate) * avg_loss

        sum_wins = sum(wins)
        sum_losses = sum(losses)
        profit_factor = (sum_wins / sum_losses) if sum_losses > 0 else (float("inf") if sum_wins > 0 else 0.0)

        max_single_loss = max(losses) if losses else 0.0

        return {
            "total_trades": total_trades,
            "win_rate": round(win_rate, 4),
            "payoff_ratio": round(payoff_ratio, 4),
            "expectancy": round(expectancy, 4),
            "profit_factor": round(profit_factor, 4),
            "max_single_loss": round(max_single_loss, 4)
        }

    def calculate_emotion_pnl_correlation(self) -> float:
        """
        计算交易者心理情绪打分 (emotional_score: 1冷静 ~ 5焦虑狂躁) 与 实际盈亏 (pnl) 的皮尔逊相关系数。
        r = Cov(X, Y) / (Std(X) * Std(Y))
        """
        n = len(self.trades)
        if n < 2:
            return 0.0

        x = [float(t.get("emotional_score", 3)) for t in self.trades]
        y = [float(t["pnl"]) for t in self.trades]

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n))

        if var_x <= 1e-12 or var_y <= 1e-12:
            return 0.0

        corr = cov / (math.sqrt(var_x) * math.sqrt(var_y))
        return round(corr, 4)

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
        wins = [t for t in self.trades if t["pnl"] > 0]
        k = len(wins)
        n = len(self.trades)

        post_alpha = prior_alpha + k
        post_beta = prior_beta + (n - k)

        total_post = post_alpha + post_beta
        post_mean = post_alpha / total_post
        post_var = (post_alpha * post_beta) / (math.pow(total_post, 2) * (total_post + 1))
        post_std = math.sqrt(post_var)

        return {
            "posterior_alpha": round(post_alpha, 4),
            "posterior_beta": round(post_beta, 4),
            "posterior_mean_win_rate": round(post_mean, 4),
            "posterior_std": round(post_std, 4)
        }

    def process_outcome_matrix(self) -> Dict[str, int]:
        """
        根据“过程执行度 (plan_followed)”与“结果 (pnl > 0)”划分决策四象限：
        - deserved_success: 遵守规则且盈利 (Skill)
        - bad_break: 遵守规则但亏损 (Unlucky Variance)
        - dumb_luck: 违规但盈利 (Toxic Luck)
        - poetic_justice: 违规且亏损 (Penalty)
        """
        counts = {
            "deserved_success": 0,
            "bad_break": 0,
            "dumb_luck": 0,
            "poetic_justice": 0
        }

        for t in self.trades:
            followed = t.get("plan_followed", True)
            is_win = t["pnl"] > 0

            if followed and is_win:
                counts["deserved_success"] += 1
            elif followed and not is_win:
                counts["bad_break"] += 1
            elif not followed and is_win:
                counts["dumb_luck"] += 1
            else:
                counts["poetic_justice"] += 1

        return counts


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么“坏过程 + 好结果（Dumb Luck / 侥幸获利）”被职业对冲基金经理视为操盘手生涯中最致命的毒药？请结合斯金纳箱（Skinner Box）操作性条件反射解释其机理。

参考答案：
1. 神经生物学与错误条件反射强化：
   在心理学中，不可预测的间歇性强化（Intermittent Reinforcement）是最具成瘾性和强化效率的机制。
   当交易员违规（如突破止损位不平仓、逆势重仓死扛、凭冲动盘中追高），却碰巧因为外力利好爆发而反败为胜甚至获取暴利时，
   大脑的多巴胺系统会给前额叶发送极为强烈的奖赏信号，将“违规死扛”这一致命危险行为错误编码为“高收益秘籍”。
2. 毁灭性破产的必然性：
   由于建立了这一错误信念，交易员在下一次遭遇正常逆境时，会更加毫不犹豫地违规死扛、加大赌注。
   但由于金融市场存在肥尾和吸收态破产属性，死扛 10 次成功 9 次，第 10 次的单边暴跌就会将交易员的账户净值彻底归零（爆仓淘汰）。
   因此，职业对冲基金的风控系统甚至会对“违反纪律但赚了钱”的交易员施加严厉扣罚或辞退。

### Q2：当一套新量化策略在回测或小样本实盘中取得 10 战 8 胜（胜率 80%）的亮眼战绩时，贝叶斯推断（以 Beta(2,2) 为先验）如何有效抑制交易团队的过度拟合与过度自信？

参考答案：
1. 样本方差与伪夏普陷阱：
   当样本量 $N=10$ 时，频率学派的胜率估计 $\hat{p} = 8/10 = 80\%$ 具有极大的标准误（$\text{SE} \approx \sqrt{0.8 \times 0.2 / 10} \approx 12.6\%$）。
   在自由度极高或噪声极大的金融时间序列中，纯随机漫步（类似 10 次抛硬币）出现 8 次或以上正收益的概率本身就高达约 5.5%，这极大概率是过拟合或运气成分。
2. 贝叶斯共轭收缩（Bayesian Shrinkage）：
   先验分布 $\text{Beta}(2,2)$ 相当于在开局前引入了 4 笔基准观察（2 胜 2 负，对应先验期望胜率 50%，方差较大）。
   在观测到 8 胜 2 负后，后验分布更新为 $\text{Beta}(2+8, 2+2) = \text{Beta}(10, 4)$。
   后验期望胜率收缩为 $\frac{10}{10+4} = \frac{10}{14} \approx 71.43\%$，而不是盲信 80%；
   且后验标准差高达 $\sqrt{\frac{10 \times 4}{14^2 \times 15}} \approx 11.66\%$。
   这一后验置信区间清晰告知团队：真实胜率完全可能在 50%~60% 的平庸区间内，有效遏制了策略上线初期的狂妄加杠杆冲动。

### Q3：在数字化交易日志中，为何必须将“情绪打分与盈亏的相关性（Pearson Correlation）”作为长周期风控评估项？

参考答案：
1. 量化感知“情绪倾侧（Tilt）对净值的侵蚀程度”：
   如果交易员的 $r(\text{emotional\_score}, \text{PnL})$ 呈现高度负相关（如 $r < -0.4$），这以客观数学数据证明：
   交易员在焦虑、愤怒、FOMO（情绪分 4~5）状态下做出的决策具有系统性的负期望值。
2. 建立精准的自律干预触发阈值：
   很多交易员主观上坚称“我即便情绪激动也能理性做单”。而数字化相关系数用无可辩驳的数据切断了其主观否认。
   合规与风控部门可据此设定规则：当系统检测到交易员单日心理情绪问卷打分达到 4 分以上时，强制收回当日下单权限，
   实现从“事后批评”向“事前/事中生理阻断”的科学跃迁。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] TradeJournalAnalyzer Performance Metrics...")
    test_trades = [
        {"trade_id": 1, "pnl": 500.0, "plan_followed": True, "emotional_score": 1},
        {"trade_id": 2, "pnl": 300.0, "plan_followed": True, "emotional_score": 2},
        {"trade_id": 3, "pnl": -200.0, "plan_followed": True, "emotional_score": 2},
        {"trade_id": 4, "pnl": -100.0, "plan_followed": True, "emotional_score": 2},
        {"trade_id": 5, "pnl": 400.0, "plan_followed": False, "emotional_score": 4}, # 违规赚钱 (Dumb Luck)
        {"trade_id": 6, "pnl": -600.0, "plan_followed": False, "emotional_score": 5}, # 违规大亏 (Poetic Justice)
    ]

    analyzer = TradeJournalAnalyzer(test_trades)
    metrics = analyzer.compute_performance_metrics()

    # 3 胜 (500, 300, 400 = 1200, 均值 400)
    # 3 负 (200, 100, 600 = 900, 均值 300)
    # 胜率 3/6 = 0.5000
    # 盈亏比 400 / 300 = 1.3333
    # 单笔期望 = 0.5 * 400 - 0.5 * 300 = 50.0
    # profit_factor = 1200 / 900 = 1.3333
    # 最大单笔亏损 = 600.0
    assert metrics["total_trades"] == 6
    assert metrics["win_rate"] == 0.5000
    assert metrics["payoff_ratio"] == 1.3333
    assert metrics["expectancy"] == 50.0
    assert metrics["profit_factor"] == 1.3333
    assert metrics["max_single_loss"] == 600.0

    print("[Testing] Emotional Score & PnL Correlation...")
    corr = analyzer.calculate_emotion_pnl_correlation()
    # 情绪分 1, 2, 2, 2, 4, 5 对应 500, 300, -200, -100, 400, -600
    # 呈现显著负相关
    assert corr == -0.5338, f"Expected -0.5338, got {corr}"

    print("[Testing] Bayesian Win Rate Update...")
    # 先验 Beta(2, 2), 观测到 3 胜 3 负
    # 后验 Beta(2+3, 2+3) = Beta(5, 5)
    # 后验期望胜率 = 5 / 10 = 0.5000
    # 后验方差 = (5 * 5) / (100 * 11) = 25 / 1100 ≈ 0.022727 -> std ≈ 0.150756
    bayes = analyzer.bayesian_win_rate_update(prior_alpha=2.0, prior_beta=2.0)
    assert bayes["posterior_alpha"] == 5.0
    assert bayes["posterior_beta"] == 5.0
    assert bayes["posterior_mean_win_rate"] == 0.5000
    assert abs(bayes["posterior_std"] - 0.1508) < 1e-4

    print("[Testing] Process vs Outcome Matrix...")
    quadrants = analyzer.process_outcome_matrix()
    # 1: followed=True, win=True -> 500 (deserved_success)
    # 2: followed=True, win=True -> 300 (deserved_success)
    # 3: followed=True, win=False -> -200 (bad_break)
    # 4: followed=True, win=False -> -100 (bad_break)
    # 5: followed=False, win=True -> 400 (dumb_luck)
    # 6: followed=False, win=False -> -600 (poetic_justice)
    assert quadrants["deserved_success"] == 2
    assert quadrants["bad_break"] == 2
    assert quadrants["dumb_luck"] == 1
    assert quadrants["poetic_justice"] == 1

    # 边界测试：空日志
    empty_analyzer = TradeJournalAnalyzer([])
    empty_metrics = empty_analyzer.compute_performance_metrics()
    assert empty_metrics["total_trades"] == 0
    assert empty_analyzer.calculate_emotion_pnl_correlation() == 0.0

    print("All assertions passed! Module 07 Lesson 03 verification successful.")
