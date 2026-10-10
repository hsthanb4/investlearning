r"""
# 模块 07：行为金融学、交易心理与执行纪律 · 第 1 课：前景理论、处置效应与损失厌恶量化

> 状态：**参考答案版** (Reference Answer)
> 包含完整代码实现与问答题深度参考解析。独立思考后再核对答案。

---
## 本课目标与完成标准

学完后你应能：
1. 掌握丹尼尔·卡尼曼与阿莫斯·特沃斯基的前景理论（Prospect Theory）S 型价值函数及其数学性质；
2. 深刻理解散户“急于卖出盈利股，死扛亏损股”的处置效应（Disposition Effect）微观发生机制；
3. 掌握 Odean (1998) 经典处置效应量化度量算法（PGR 与 PLR）及经验损失厌恶系数计算；
4. 编写代码实现散户交易与持仓流水中的 PGR、PLR、DE（处置效应指数）统计与效用敏感度测算。

通过标准：
- 独立补齐实战代码中的 TODO 填空，并通过全部 assert 单元测试；
- 深入回答 Q1~Q3 思考题，因果链完整，揭示交易者大脑生理与演化心理学根源。

---
## 核心心智模型与数理推导

### 1. 前景理论 S 型价值函数 (Kahneman & Tversky, 1979/1992)

传统期望效用理论（EUT）假设人们基于绝对财富水平最大化效用，且投资者在所有状态下均为风险厌恶（效用函数二阶导小于 0）。
而前景理论发现：
1. **参考点依赖（Reference Dependence）**：投资者不是感知绝对财富，而是感知相对于“买入成本（参考点）”的财富增量或减量 $x$。
2. **边际敏感性递减（Diminishing Sensitivity）**：盈利区域表现为凹函数（风险规避），亏损区域表现为凸函数（风险寻求）。
3. **损失厌恶（Loss Aversion）**：面对相同幅度的得失，亏损带来的痛苦约为盈利带来快乐的 2~2.5 倍。

数学形式（Cumulative Prospect Theory）：
$$
v(x) = \begin{cases}
x^\alpha, & x \ge 0 \\
-\lambda (-x)^\beta, & x < 0
\end{cases}
$$
经验参数通常取 $\alpha \approx \beta \approx 0.88$，损失厌恶系数 $\lambda \approx 2.25$。

```
              价值 v(x) (快乐)
                     |       / (盈利区域：凹函数，风险厌恶)
                     |     /
                     |   /
                     | /
  -------------------+------------------- 收益/亏损 x (参考点=0)
                   / |
                 /   |
               /     |
             /       | (亏损区域：凸函数，风险寻求，斜率陡峭 λ≈2.25)
            /        |
          /          |
                     | (痛苦)
```

### 2. 处置效应的数学度量 (Terrance Odean, 1998)

为什么普通散户总是“小赚就跑，大亏死扛”？
- 盈利头寸处于 S 曲线的右上凹面：再涨 10% 带来的效用增量远小于保住已有利润的效用，投资者产生强烈的“落袋为安”确定性冲动；
- 亏损头寸处于 S 曲线的左下凸面：再跌 10% 带来的边际痛苦递减，而反弹回本带来的效用跃升巨大，投资者倾向于赌徒般的“死扛搏反弹”。

Odean (1998) 提出了量化度量处置效应的标准框架。对于任意交易日 $t$ 的投资者账户：
- **已实现盈利 (Realized Gain, RG)**：当日卖出且卖出价 > 买入成本的头寸笔数。
- **账面未实现盈利 (Paper Gain, PG)**：当日未卖出，但收盘价 > 买入成本的持有头寸笔数。
- **已实现亏损 (Realized Loss, RL)**：当日卖出且卖出价 < 买入成本的头寸笔数。
- **账面未实现亏损 (Paper Loss, PL)**：当日未卖出，但收盘价 < 买入成本的持有头寸笔数。

整个周期内的比率定义：
$$
\text{PGR} = \frac{\sum \text{RG}}{\sum \text{RG} + \sum \text{PG}}, \quad
\text{PLR} = \frac{\sum \text{RL}}{\sum \text{RL} + \sum \text{PL}}
$$
处置效应测度（Disposition Effect, DE）：
$$
\text{DE} = \text{PGR} - \text{PLR}
$$
若 $\text{DE} > 0$，表明投资者在盈利时实现收益的倾向显著大于亏损时割肉止损的倾向，存在显著处置效应。
"""

import math
from typing import List, Dict, Any


def kahneman_tversky_value(x: float, alpha: float = 0.88, beta: float = 0.88, lambda_: float = 2.25) -> float:
    """
    计算前景理论下的心理价值 v(x)。
    
    :param x: 相对参考点的盈亏金额 (x > 0 为盈利，x < 0 为亏损)
    :param alpha: 收益端凹度敏感系数 (通常为 0.88)
    :param beta: 亏损端凸度敏感系数 (通常为 0.88)
    :param lambda_: 损失厌恶系数 (通常为 2.25)
    :return: 心理价值评分
    """
    if x >= 0:
        return math.pow(x, alpha)
    else:
        return -lambda_ * math.pow(-x, beta)


def calculate_disposition_effect(daily_snapshots: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    依据 Odean (1998) 算法，计算账户的 PGR、PLR 与处置效应指数 (DE)。
    """
    sum_rg = 0
    sum_pg = 0
    sum_rl = 0
    sum_pl = 0

    for day in daily_snapshots:
        # 处理当日已实现卖单
        for sale in day.get("sales", []):
            cost = sale["cost_basis"]
            sell_price = sale["sell_price"]
            if sell_price > cost:
                sum_rg += 1
            elif sell_price < cost:
                sum_rl += 1

        # 处理当日未卖出的账面持仓
        for holding in day.get("holdings", []):
            cost = holding["cost_basis"]
            current = holding["current_price"]
            if current > cost:
                sum_pg += 1
            elif current < cost:
                sum_pl += 1

    pgr = sum_rg / (sum_rg + sum_pg) if (sum_rg + sum_pg) > 0 else 0.0
    plr = sum_rl / (sum_rl + sum_pl) if (sum_rl + sum_pl) > 0 else 0.0
    de = pgr - plr

    return {
        "realized_gains": sum_rg,
        "paper_gains": sum_pg,
        "realized_losses": sum_rl,
        "paper_losses": sum_pl,
        "pgr": round(pgr, 4),
        "plr": round(plr, 4),
        "disposition_effect": round(de, 4)
    }


def estimate_implied_loss_aversion(gamble_win: float, gamble_loss: float, alpha: float = 0.88, beta: float = 0.88) -> float:
    """
    根据投资者在 50/50 抛硬币博弈中的无差异点（接受与拒绝概率相等），反推经验损失厌恶系数 lambda。
    即期望效用为 0： 0.5 * v(gamble_win) + 0.5 * v(-gamble_loss) = 0
    (gamble_win)^alpha = lambda * (gamble_loss)^beta
    => lambda = (gamble_win^alpha) / (gamble_loss^beta)
    """
    numerator = math.pow(gamble_win, alpha)
    denominator = math.pow(gamble_loss, beta)
    return round(numerator / denominator, 4)


# ==============================================================================
# Q1~Q3 深度思考题参考解析
# ==============================================================================
r"""
### Q1：为什么散户在盈利时表现出高度“风险厌恶”，但在亏损时却表现出极端的“风险寻求”？请从前景理论 S 型价值函数推导这一心理异化机制。

参考答案：
1. 核心数学机理：
   前景理论的价值函数以买入参考点（成本价）为零原点。
   - 在盈利区间（x > 0），函数为凹函数（v''(x) < 0）。这意味着第一笔浮盈带来的心理满足感最强，后续涨幅带来的边际心理增量急剧递减。
     例如浮盈 10% 心理分数为 10^0.88 ≈ 7.59；若再涨 10% 到 20%，增量仅为 20^0.88 - 10^0.88 = 13.93 - 7.59 = 6.34。
     但如果吐回盈利归零，承受的心理损失为 7.59。因此，面对“锁定确定性浮盈”与“博弈更大涨幅但可能回吐”，投资者表现出极度厌恶风险的保本落袋行为。
   - 在亏损区间（x < 0），函数为凸函数（v''(x) > 0）。一旦发生亏损，亏损带来的心理痛苦陡峭增加（-2.25 * |-10|^0.88 ≈ -17.07）。
     但随着亏损幅度进一步扩大（例如从 -20% 扩大至 -30%），边际痛苦反而递减（麻木感）。
     此时，投资者若卖出股票，就必须在心理账簿上“敲章确认”这一无法逆转的剧烈痛苦；
     而死扛甚至补仓，虽然可能亏更多，但保留了“反弹回本抹平痛苦”的微弱希望。投资者为了逃避确定性现实，主动拥抱了更高方差的危险风险，表现为极端的“风险寻求”。

### Q2：在 Odean (1998) 的实证研究中，为何只统计“买卖胜率”无法识别出处置效应，必须引入“账面未实现收益 (PG) 与账面未实现亏损 (PL)”作为分母？

参考答案：
1. 样本空间与机会集合的偏差：
   如果仅观察已平仓交易的胜率（Realized Gain / (Realized Gain + Realized Loss)），一个具有极强处置效应的严重亏损散户，其胜率往往高达 70%~90%。
   因为他把所有赚钱的单子全在涨 2%~5% 时兑现了（大量的 RG），而所有亏损的单子统统死扛着不平仓（只有极少被迫爆仓的 RL）。只看胜率会误以为此人是“常胜将军”。
2. 机会发生率的归一化：
   Odean 的核心洞察在于，交易员每天都在面临决策：“在所有我可以卖出的盈利股票中，我卖了多少比例（PGR）；在所有我可以割肉的亏损股票中，我割了多少比例（PLR）”。
   分母（RG + PG）代表了所有“存在盈利机会”的集合，分母（RL + PL）代表了所有“面临亏损惩罚”的集合。
   只有比较 PGR 与 PLR，才能剥离出投资者是否对“兑现盈利”具有统计学上的系统性偏好。

### Q3：在结构性熊市或个股突发基本面暴雷事件中，处置效应如何导致“阻力位上移”与“成交量冻结”？对量化多头策略的流动性管理有何启示？

参考答案：
1. 市场微观结构与筹码挂单阻力（Overhang）：
   由于大量散户在下跌过程中死扛被套（累积了巨额的 Paper Losses），这些套牢盘的心理参考点均锚定在其买入成本。
   一旦股价在基本面反弹中回升到套牢密集区，被套筹码的亏损痛苦迅速缓解，投资者的首要诉求从“死扛逃避”切换为“回本保本即走（Breakeven Effect）”。
   这导致历史密集套牢区形成沉重的挂单抛压（筹码堰塞湖），严重阻碍价格的顺畅回升。
2. 成交量冻结（Volume Freezing）：
   在没有催化剂的阴跌过程中，散户既不愿割肉（PLR 极低），场外增量资金亦无意愿买入，导致成交量急剧萎缩。
   对于量化多头基金而言，若所选个股陷入处置效应筹码套牢区，其主动流动性将急剧衰减；在建仓与平仓时必须严格计算冲击成本（Market Impact），
   避免在筹码套牢阻力位前重仓追高，同时应将筹码分布与成本锚定偏离度作为因子的风险剔除项。
"""


# ==============================================================================
# 单元测试与断言校验
# ==============================================================================
if __name__ == "__main__":
    print("[Testing] Kahneman-Tversky Value Function...")
    v_win = kahneman_tversky_value(100.0, alpha=0.88, beta=0.88, lambda_=2.25)
    v_loss = kahneman_tversky_value(-100.0, alpha=0.88, beta=0.88, lambda_=2.25)
    assert round(v_win, 4) == 57.5440, f"Expected 57.5440, got {round(v_win, 4)}"
    assert round(v_loss, 4) == -129.4740, f"Expected -129.4740, got {round(v_loss, 4)}"
    assert abs(-v_loss / v_win - 2.25) < 1e-4

    print("[Testing] Implied Loss Aversion Estimation...")
    lambda_est = estimate_implied_loss_aversion(gamble_win=225.0, gamble_loss=100.0, alpha=1.0, beta=1.0)
    assert lambda_est == 2.25, f"Expected 2.25, got {lambda_est}"

    print("[Testing] Odean Disposition Effect Quantification...")
    test_snapshots = [
        {
            "date": "2026-03-01",
            "sales": [
                {"symbol": "A", "sell_price": 105.0, "cost_basis": 100.0},
                {"symbol": "B", "sell_price": 95.0, "cost_basis": 100.0},
            ],
            "holdings": [
                {"symbol": "C", "current_price": 110.0, "cost_basis": 100.0},
                {"symbol": "D", "current_price": 90.0, "cost_basis": 100.0},
                {"symbol": "E", "current_price": 85.0, "cost_basis": 100.0},
            ]
        },
        {
            "date": "2026-03-02",
            "sales": [
                {"symbol": "C", "sell_price": 112.0, "cost_basis": 100.0},
            ],
            "holdings": [
                {"symbol": "D", "current_price": 88.0, "cost_basis": 100.0},
                {"symbol": "E", "current_price": 80.0, "cost_basis": 100.0},
                {"symbol": "F", "current_price": 108.0, "cost_basis": 100.0},
            ]
        }
    ]

    metrics = calculate_disposition_effect(test_snapshots)
    assert metrics["realized_gains"] == 2
    assert metrics["paper_gains"] == 2
    assert metrics["realized_losses"] == 1
    assert metrics["paper_losses"] == 4
    assert metrics["pgr"] == 0.5000
    assert metrics["plr"] == 0.2000
    assert metrics["disposition_effect"] == 0.3000

    empty_metrics = calculate_disposition_effect([])
    assert empty_metrics["pgr"] == 0.0
    assert empty_metrics["plr"] == 0.0
    assert empty_metrics["disposition_effect"] == 0.0

    print("All assertions passed! Module 07 Lesson 01 verification successful.")
