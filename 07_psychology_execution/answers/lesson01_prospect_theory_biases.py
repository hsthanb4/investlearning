r"""
================================================================================
模块 07：行为金融学、交易心理与执行纪律 · 第 1/4 课
第 1 课：前景理论、处置效应与损失厌恶量化模型 (参考答案版)
================================================================================

【课程定位与投决会核心心智模型】
::: callout-note
### 📌 投决会核心心智模型：人类进化生理缺陷对二级市场交易的诅咒
人类大脑在数十万年丛林演化中形成了对确定性食物的渴求与对物理创伤的规避本能。然而在金融资产价格随机波动的时间序列中，这种生物进化本能表现为“微赚即跑、大亏死扛”的处置效应（Disposition Effect）。这与资产组合管理中“截断亏损、让利润奔跑（Cut losses short, let profits run）”的第一性原理完全背道而驰。
:::

- **[参考点依赖与主观效用映射]**：市场参与者并不以绝对财富终值作为效用函数自变量，而是将持仓成本作为坐标原点（参考点），对盈亏增量表现出非线性的主观感知。
- **[风险态度的非对称翻转]**：在盈利区间，效用函数表现为凹函数，投资者急于兑现确定性浮盈（过度风险厌恶）；在亏损区间，效用函数表现为凸函数，投资者为逃避确定性割肉痛苦而主动拥抱更高方差的死扛甚至加仓赌徒行为（非理性风险偏好）。
- **[损失厌恶系数的非对称痛感]**：经验实证表明损失厌恶系数 $\lambda \approx 2.25$，即同等绝对金额的亏损带来的心理痛苦是盈利带来快乐的 2 倍以上。

【微观机理与三位一体就近图文剖析】

锚点指引：下图展示了卡尼曼-特沃斯基经典 S 型主观效用价值函数的几何形态与曲率分界。

```mermaid
flowchart LR
    A["持仓成本参考点 (Reference Point)"] --> B{"头寸损益状态"}
    B -->|浮盈区 x > 0| C["凹函数 v''(x) < 0<br/>急于兑现确定性微利 (卖出赢家)"]
    B -->|浮亏区 x < 0| D["凸函数 v''(x) > 0<br/>损失厌恶 λ≈2.25 放大痛苦 (死抱输家)"]
    C --> E["处置效应偏误 DE = PGR - PLR > 0"]
    D --> E
    E --> F["组合长期几何增长率严重受损 (Alpha 耗损)"]
```

- **[要点 1：浮盈区凹函数与过早止盈]**：边际效用递减导致持仓浮盈扩大时新增心理收益急剧衰减，诱发非理性平仓，扼杀了长期肥尾牛股的复利爆发力。
- **[要点 2：浮亏区凸函数与风险偏好异化]**：边际痛苦递减导致浮亏从 10% 扩大至 20% 的边际新增痛感钝化，交易员产生麻木心理并寄托于微弱的“回本反弹”，拒绝执行风控指令。
- **[要点 3：参考点锁定与筹码阻力堰塞湖]**：大量散户成本锚定在历史高位，使得价格反弹至套牢密集区时遭遇强烈的“解套解脱性抛压”，直接压制资产中枢上行空间。

锚点指引：下图拆解了 Odean (1998) 处置效应账户状态空间的四象限划分与度量公式。

```mermaid
flowchart TD
    subgraph 账户决策全集
        subgraph 已实现交易 Realized
            RG["已实现盈利 (Realized Gain)"]
            RL["已实现亏损 (Realized Loss)"]
        end
        subgraph 账面未实现持仓 Paper
            PG["账面盈利未卖 (Paper Gain)"]
            PL["账面亏损未卖 (Paper Loss)"]
        end
    end
    RG & PG --> PGR["盈利实现比率 PGR = ΣRG / (ΣRG + ΣPG)"]
    RL & PL --> PLR["亏损实现比率 PLR = ΣRL / (ΣRL + ΣPL)"]
    PGR & PLR --> DE["处置效应指数 DE = PGR - PLR"]
```

- **[要点 1：分母机会全集的科学归一]**：不能单纯观察平仓胜率，必须将未平仓的账面浮盈（PG）与浮亏（PL）纳入总机会基数，消除散户“只平盈利单、胜率虚高”的统计假象。
- **[要点 2：PGR 显著高于 PLR 的毒性]**：当 DE > 0 时，证实投资者在面对盈利机会时的兑现速度系统性快于面对亏损惩罚时的止损速度。
- **[要点 3：负偏斜收益分布形成]**：处置效应必然导致策略底层单笔收益分布呈现厚重的左尾（巨额拖延亏损）与截断的右尾（过早扼杀的大牛股）。

【数学与估值模型】
卡尼曼-特沃斯基累积前景理论价值函数定义域与独立公式：
$$
v(x) = \begin{cases}
x^\alpha, & x \ge 0 \\
-\lambda (-x)^\beta, & x < 0
\end{cases}
$$
变量定义域与参数约束：
- $x \in (-\infty, +\infty)$：相对于成本参考点的损益绝对额或百分比（以货币计价或收益率计价）。
- $\alpha, \beta \in (0, 1]$：经验参数，通常取 $\alpha \approx \beta \approx 0.88$，决定价值函数的曲率。
- $\lambda > 1$：损失厌恶系数，经典实证标定取值 $\lambda \approx 2.25$。

Odean 处置效应指数方程：
$$
\text{DE} = \text{PGR} - \text{PLR} = \frac{\sum_{t} \text{RG}_t}{\sum_{t} \text{RG}_t + \sum_{t} \text{PG}_t} - \frac{\sum_{t} \text{RL}_t}{\sum_{t} \text{RL}_t + \sum_{t} \text{PL}_t}
$$
变量定义域：$\text{RG}, \text{PG}, \text{RL}, \text{PL} \in \mathbb{N}$，比率 $\text{PGR}, \text{PLR} \in [0, 1]$，指数 $\text{DE} \in [-1, 1]$。

::: callout-warning
### ⚠️ 投决会风控红线与认知陷阱防范
1. **胜率欺骗性陷阱**：在缺乏 PGR/PLR 审计的情况下，90% 胜率的账户可能正在死扛 10% 的致命单边穿仓头寸，实际处于净资产清零边缘。
2. **移动参考点陷阱**：当头寸发生严重亏损后，交易员心理上将“最高浮盈点”作为新的锚定参考点，误将浮盈回吐视作“实际亏损”，进而做出激进的报复性锁仓操作。
3. **被动转长线价值投资的借口**：短线投机单在被套后单方面宣布转为“长线价值投资”，本质是前景理论下逃避现实亏损确认的心理防卫机制。
:::

【思考题】
Q1: 为什么散户在买入股票被套 10% 时不愿止损，而在被套 50% 时反而彻底“躺平”不再看盘？请从心理账户与前景理论 S 型价值函数的边际效用一阶导数推导。
Q2: 在 Odean (1998) 的实证研究中，为何只统计“买卖胜率”无法识别出处置效应，必须引入“账面未实现收益 (PG) 与账面未实现亏损 (PL)”作为分母？
Q3: 怎样利用程序化强制硬止损（Stop-Loss Order）与交易所原子化条件单（OCO），在微观物理层彻底剥夺人类大脑杏仁核劫持决策的机会？

【Q1 深度参考答案】
- **[原点凹凸性与导数递减分析]**：前景理论价值函数在亏损区间为严格凸函数（$v''(x) > 0$ for $x < 0$），这意味着边际效用一阶导数随着亏损幅度加大而急剧衰减（$|v'(-50)| \ll |v'(-10)|$）。
- **[边际痛苦顿感与心理账簿隔离]**：在亏损 10% 时，边际痛苦斜率极高，止损割肉会迫使交易员在心理账簿上物理确认一笔剧烈的心理减值；而当亏损扩大至 50% 后，再亏 10% 带来的边际痛感几乎微不可察，交易员大脑产生认知麻木与逃避机制。
- **[实物资产与虚拟记账的心理分工]**：通过“卸载炒股软件、不看盘”，交易员在心理认知上把未平仓浮亏归类为“未发生的虚拟事件”，以欺骗自尊心的方式无限期推迟确认损失，直至破产清算。

【Q2 深度参考答案】
- **[样本选择偏差的统计学陷阱]**：仅基于已实现交易平仓记录（Closed Trades）计算的胜率存在极端严重的幸存者选择偏差。具备恶性处置效应的散户通常会在浮盈 2%~5% 时光速平仓兑现，而把所有亏损 20%~80% 的单子死扛在持仓中。
- **[胜率指标与账户破产的背离]**：此类交易员的已实现胜率往往高达 80% 甚至 90%，但总净值却持续崩塌并面临清盘，传统胜率完全丧失了风控甄别效力。
- **[机会空间归一化（Normalizing Opportunity Sets）]**：Odean 的卓越贡献在于将每一个交易日所有可供选择的头寸划分为“盈利机会集（RG + PG）”与“亏损惩罚集（RL + PL）”，通过 PGR 与 PLR 的差值精准刻画交易员对待两类机会的条件概率偏离，彻底穿透了死扛账面浮亏的虚伪胜率。

【Q3 深度参考答案】
- **[生理神经中枢的时延与劫持]**：在价格突发跳水或穿仓威胁下，人类交感神经系统被杏仁核完全主导，理性前额叶皮层的概率计算能力在毫秒级被抑制，导致交易员产生肢体僵硬、撤销止损、抱侥幸幻想的典型应激反应。
- **[原子化开仓即止损契约（OCO Contingency）]**：投决会工程规范要求，任何主动开仓报单必须与止损单构成原子化委托包（One-Cancels-the-Other / Bracket Order），在送入交易所网关前已完成撮合锁死，禁止裸单暴露。
- **[物理隔离与权限收敛]**：止损触发条件由柜台撮合引擎硬编码执行，交易员本人被彻底剥夺撤销或下移止损价的权限。任何止损参数的变更必须经过风控合规委员会双人复核秘钥审批，以系统确定性对冲人性的非理性冲动。
"""

import math
from typing import List, Dict, Any, Union


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


def calculate_disposition_effect(daily_snapshots_or_pgr: Union[List[Dict[str, Any]], float], plr: float = None) -> Union[Dict[str, float], float]:
    """
    计算处置效应指标:
    - 若传入 (pgr: float, plr: float): 返回 DE = pgr - plr (标量 float)
    - 若传入 (daily_snapshots: List[Dict]): 返回字典包含 realized/paper 统计量与 PGR, PLR, DE
    """
    # 标量兼容模式
    if plr is not None and isinstance(daily_snapshots_or_pgr, (int, float)):
        return round(float(daily_snapshots_or_pgr - plr), 4)

    # 列表快照模式
    daily_snapshots = daily_snapshots_or_pgr if isinstance(daily_snapshots_or_pgr, list) else []
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
    plr_val = sum_rl / (sum_rl + sum_pl) if (sum_rl + sum_pl) > 0 else 0.0
    de = pgr - plr_val

    return {
        "realized_gains": sum_rg,
        "paper_gains": sum_pg,
        "realized_losses": sum_rl,
        "paper_losses": sum_pl,
        "pgr": round(pgr, 4),
        "plr": round(plr_val, 4),
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

    # 标量断言兼顾
    assert calculate_disposition_effect(0.65, 0.25) == 0.40

    print("All assertions passed! Module 07 Lesson 01 verification successful.")
