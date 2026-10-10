r"""
================================================================================
模块 07：行为金融学、交易心理与执行纪律 · 第 3/4 课
第 3 课：数字化交易日志与贝叶斯复盘归因模型 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：过程与结果的因果解耦及贝叶斯胜率收敛
金融二级市场是一个充满非遍历性噪声与运气方差的随机博弈场。单笔交易的盈亏结果与决策过程的优劣并不具备强确定性对应关系。职业对冲基金的投决会复盘核心，在于彻底解耦“运气”与“技能”，通过迈克尔·莫布森决策四象限穿透违规侥幸的伪 Alpha，并利用 Beta-Binomial 贝叶斯共轭先验动态收缩真实胜率分布，杜绝小样本过度自信。
:::

- **[结果偏误与运气毒性]**：市场参与者容易患上“以结果论英雄（Outcome Bias）”的认知绝症。违规死扛却侥幸解套大赚（Dumb Luck）会在大脑多巴胺系统中形成致命正反馈，直接为未来的穿仓埋下雷管。
- **[统计学先验与小样本收缩]**：在样本量较小（如 N < 30）时，样本胜率的方差极大。必须引入基准先验分布（如 Beta(2,2)），通过贝叶斯推断对极端高胜率进行理性向均值收缩。
- **[生理情绪标记与归因相关性]**：数字化日志必须记录决策时刻的情绪温度（Emotional Score）。当情绪得分与交易盈亏呈现高度负相关时，表明交易员已被情绪劫持，需立即触发风控干预。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了迈克尔·莫布森“过程 vs 结果”决策四象限的商业本质与长期期望映射。

```mermaid
flowchart TD
    subgraph 决策过程维度
        GP["好过程: 坚守纪律 / 计划内执行"]
        BP["坏过程: 违规加仓 / 情绪化追涨"]
    end
    subgraph 单笔结果维度
        GO["好结果: 浮盈落袋 (+ PnL)"]
        BO["坏结果: 触及止损 (- PnL)"]
    end
    GP & GO --> Q1["象限 I：理所应当的成功<br/>(Deserved Success / 长期复利底座)"]
    GP & BO --> Q2["象限 II：合理的代价<br/>(Bad Break / 经商正常方差成本)"]
    BP & GO --> Q3["象限 III：最致命的毒药<br/>(Dumb Luck / 恶性神经回路强化)"]
    BP & BO --> Q4["象限 IV：合乎逻辑的惩罚<br/>(Poetic Justice / 违规被市场击杀)"]
```

- **[要点 1：合理的代价与从容止损]**：合规交易被市场止损属于系统经营的“正常货损成本”，交易员必须保持平静并继续机械执行下一笔高期望机会。
- **[要点 2：最致命的毒药与纪律惩处]**：违规死扛后碰巧因突发利好暴赚，投决会不仅不予奖励，反而必须记入合规违规黑名单并扣除绩效奖金，严防行为模式异化。
- **[要点 3：长期复利锚定好过程]**：大数定律下，只有象限 I 与象限 II 的组合能保证资本几何平均增长率 $g > 0$；依赖象限 III 的交易员最终 100% 走向破产吸收态。

锚点指引：下图展示了贝叶斯胜率后验概率密度随交易笔数样本扩充的动态收敛过程。

```mermaid
flowchart LR
    A["弱无信息先验 Beta(α0, β0)<br/>方差大 / 锚定中枢 50%"] --> B["观测交易样本 (Wins=k, Losses=n-k)"]
    B --> C["共轭更新后验 Beta(α0+k, β0+n-k)"]
    C --> D["大样本下后验均值逼近真实真实胜率<br/>标准差以 1/√n 速度快速收敛"]
```

- **[要点 1：先验信息平滑极端异常值]**：当策略以 10 战 8 胜开局时，贝叶斯后验均值将其理性拉回至 71.4%，阻断虚幻的 80% 胜率幻觉。
- **[要点 2：置信区间与方差感知]**：小样本下后验概率分布的高离散度直接向风控官揭示了真实胜率可能低于 60% 的下行风险，拒绝盲目放大风险敞口。
- **[要点 3：因果律单调递增性]**：随着样本容量 $N \to \infty$，后验分布自然收敛于大数定律真实参数，完成从主观先验向客观事实的无缝过渡。

【数学与估值模型】
贝叶斯共轭先验与后验概率分布方程：
$$
p \sim \text{Beta}(\alpha_0, \beta_0), \quad k \sim \text{Binomial}(n, p) \implies p | \text{Data} \sim \text{Beta}(\alpha_0 + k, \beta_0 + n - k)
$$
变量定义域与参数约束：
- $p \in [0, 1]$：策略潜在真实胜率参数。
- $\alpha_0, \beta_0 > 0$：先验伪计数参数，投决会无偏基准通常设 $\alpha_0 = \beta_0 = 2.0$。
- $n \in \mathbb{N}$：总交易笔数，$k \in [0, n]$ 为盈利交易笔数。

后验期望均值与后验方差表达式：
$$
\mathbb{E}[p | \text{Data}] = \frac{\alpha_0 + k}{\alpha_0 + \beta_0 + n}, \quad \text{Var}(p | \text{Data}) = \frac{(\alpha_0 + k)(\beta_0 + n - k)}{(\alpha_0 + \beta_0 + n)^2 (\alpha_0 + \beta_0 + n + 1)}
$$

情绪打分与实际损益皮尔逊相关系数：
$$
r = \frac{\sum_{i=1}^n (E_i - \bar{E})(\text{PnL}_i - \overline{\text{PnL}})}{\sqrt{\sum_{i=1}^n (E_i - \bar{E})^2} \sqrt{\sum_{i=1}^n (\text{PnL}_i - \overline{\text{PnL}})^2}}
$$
变量定义域：$E_i \in [1, 5]$ 为主观情绪分，$\text{PnL}_i \in \mathbb{R}$，相关系数 $r \in [-1, 1]$。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **胜率与赔率的代数平衡陷阱**：高胜率策略（如 80%）若盈亏比极低（如 0.2），单笔期望依然为负；单笔期望 $E = p \cdot b - (1 - p)$ 必须大于零才具备配置价值。
2. **后见之明偏误（Hindsight Bias）**：复盘时严禁用‘当时我就知道它会涨’的事后诸葛亮视角掩盖入场逻辑的瑕疵，所有复盘必须以入场时刻的快照为唯一判据。
3. **日志伪造与情绪瞒报**：未如实记录开仓情绪打分与执行偏离者，投决会暂停其交易权限 1 周，强制复训。
:::

【思考题】
Q1: 为什么“坏过程 + 好结果（Dumb Luck / 侥幸获利）”被职业对冲基金经理视为操盘手生涯中最致命的毒药？请结合斯金纳箱（Skinner Box）操作性条件反射解释其机理。
Q2: 当一套新量化策略在回测或小样本实盘中取得 10 战 8 胜（胜率 80%）的亮眼战绩时，贝叶斯推断（以 Beta(2,2) 为先验）如何有效抑制交易团队的过度拟合与过度自信？
Q3: 在数字化交易日志中，为何必须将“情绪打分与盈亏的相关性（Pearson Correlation）”作为长周期风控评估项？

【Q1 深度参考答案】
- **[间歇性强化的神经毒性机制]**：在斯金纳箱行为学实验中，不可预测的随机奖励（Intermittent Reinforcement）是最具成瘾性与习惯固化能力的刺激方式。交易员违规死扛却因外生突发利好侥幸大赚时，大脑多巴胺神经元产生强烈的奖赏峰值，将“违规死扛”这一致命行为错误编码为“高收益法宝”。
- **[马尔可夫吸收壁破产必然性]**：错误信念一旦建立，交易员在未来面对逆境时将更加变本加厉地撤销止损、追加杠杆。由于金融市场收益分布具有极端肥尾与单边流动性黑洞特征，死扛 9 次即使侥幸成功，第 10 次的黑天鹅踩踏将直接击穿账户净值导致彻底清盘。
- **[投决会负激励机制]**：顶级机构投决会对“坏过程好结果”的交易实施严厉罚款甚至吊销交易权限，核心在于斩断毒性条件反射在团队内部的传染蔓延。

【Q2 深度参考答案】
- **[小样本抽样方差的数学欺骗性]**：当样本容量 $N=10$ 时，频率学派点估计 $\hat{p} = 0.8$ 的标准误高达 $\sqrt{0.8 \times 0.2 / 10} \approx 12.65\%$。在充满高斯白噪声的随机漫步序列中，纯凭运气跑出 10 战 8 胜的先验概率高达 5.5%，极大概率是过拟合假象。
- **[贝叶斯共轭收缩（Bayesian Shrinkage）]**：引入 $\text{Beta}(2,2)$ 相当于引入了 4 次虚拟基准试验（2 胜 2 负，均值 50%）。更新后后验分布为 $\text{Beta}(10, 4)$，期望胜率自动收缩至 $\frac{10}{14} \approx 71.43\%$，且后验标准差高达 $11.66\%$。
- **[压制杠杆冲动的理性锚]**：后验置信区间明确揭示出该策略真实胜率有很大几率落在 55%~65% 的平庸区间，有效遏制了投研团队在策略上线初期盲目放大仓位的冒险冲动。

【Q3 深度参考答案】
- **[量化度量情绪倾侧对资本的侵蚀度]**：若皮尔逊相关系数呈现显著负相关（如 $r < -0.4$），这以客观统计证据证明：该交易员在情绪激动、焦虑或狂躁状态下的所有决策均属于系统性负期望下注。
- **[打破主观自恋与事实否认]**：人类交易员普遍存在“自利归因”倾向（赚钱归功于才智，亏钱归咎于运气，并坚信自己能带情绪操盘）。负相关系数用冰冷的数学铁证粉碎了交易员的心理防卫。
- **[建立自适应生理风控门禁]**：系统据此设定硬性准入规则：当交易员连续情绪打分超过警戒阈值时，网关直接锁定下单接口，实现从“事后批评”向“事前生理阻断”的质的跃升。
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

        payoff_ratio = avg_win / avg_loss if avg_loss > 0 else 0.0
        expectancy = win_rate * avg_win - (1.0 - win_rate) * avg_loss
        profit_factor = sum(wins) / sum(losses) if sum(losses) > 0 else 0.0
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
        if len(self.trades) < 2:
            return 0.0

        x_vals = [float(t.get("emotional_score", 3)) for t in self.trades]
        y_vals = [float(t.get("pnl", 0.0)) for t in self.trades]

        n = len(x_vals)
        mean_x = sum(x_vals) / n
        mean_y = sum(y_vals) / n

        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
        var_x = sum((x - mean_x) ** 2 for x in x_vals)
        var_y = sum((y - mean_y) ** 2 for y in y_vals)

        if var_x == 0 or var_y == 0:
            return 0.0

        r = cov / (math.sqrt(var_x) * math.sqrt(var_y))
        return round(r, 4)

    def bayesian_win_rate_update(self, prior_alpha: float = 2.0, prior_beta: float = 2.0) -> Dict[str, float]:
        """
        Beta-Binomial 贝叶斯共轭更新：
        - prior_alpha, prior_beta: 先验参数
        - k: 盈利交易笔数
        - n: 总交易笔数
        后验参数：alpha_post = prior_alpha + k, beta_post = prior_beta + n - k
        后验期望胜率：alpha_post / (alpha_post + beta_post)
        后验方差：(alpha_post * beta_post) / ((alpha_post + beta_post)^2 * (alpha_post + beta_post + 1))
        """
        k = sum(1 for t in self.trades if t.get("pnl", 0.0) > 0)
        n = len(self.trades)

        alpha_post = prior_alpha + k
        beta_post = prior_beta + (n - k)

        sum_ab = alpha_post + beta_post
        mean_win = alpha_post / sum_ab
        var_win = (alpha_post * beta_post) / ((sum_ab ** 2) * (sum_ab + 1))
        std_win = math.sqrt(var_win)

        return {
            "posterior_alpha": round(alpha_post, 4),
            "posterior_beta": round(beta_post, 4),
            "posterior_mean_win_rate": round(mean_win, 4),
            "posterior_std": round(std_win, 4)
        }

    def process_outcome_matrix(self) -> Dict[str, int]:
        """
        统计迈克尔·莫布森决策四象限分布：
        - plan_followed == True and pnl > 0: deserved_success (理所应当的成功)
        - plan_followed == True and pnl <= 0: bad_break (合理的代价 / 坏运气)
        - plan_followed == False and pnl > 0: dumb_luck (最致命的毒药 / 侥幸获利)
        - plan_followed == False and pnl <= 0: poetic_justice (合乎逻辑的惩罚 / 违规受罚)
        """
        counts = {
            "deserved_success": 0,
            "bad_break": 0,
            "dumb_luck": 0,
            "poetic_justice": 0
        }

        for t in self.trades:
            followed = t.get("plan_followed", False)
            pnl = t.get("pnl", 0.0)

            if followed and pnl > 0:
                counts["deserved_success"] += 1
            elif followed and pnl <= 0:
                counts["bad_break"] += 1
            elif not followed and pnl > 0:
                counts["dumb_luck"] += 1
            else:
                counts["poetic_justice"] += 1

        return counts


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

    # 边界测试：空日志
    empty_analyzer = TradeJournalAnalyzer([])
    empty_metrics = empty_analyzer.compute_performance_metrics()
    assert empty_metrics["total_trades"] == 0
    assert empty_analyzer.calculate_emotion_pnl_correlation() == 0.0

    print("All assertions passed! Module 07 Lesson 03 verification successful.")
