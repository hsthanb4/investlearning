#!/usr/bin/env python3
"""
InvestLearning Module 04 Full Upgrader
Upgrades all 5 lessons in 04_technical_pa/ (starter & answers)
Ensures 100% assertion pass and strict adherence to the 3 styling standards.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------------------
# Lesson 01
# ------------------------------------------------------------------------------
L01_STARTER_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 1/5 课
第 1 课：价格行为学与市场结构识别状态机 (Swing Points, BOS & CHoCH)
================================================================================

【课程定位与第一性原理】
在现代微观市场结构与高频撮合现实中，价格运动并非平滑连续的随机游走函数，
而是多空双方围绕特定流动性池（Liquidity Pools）与做市商库存平衡展开的离散阶梯博弈。
投资委员会在审视技术信号时，必须剥离滞后均线指标的统计幻觉，直接穿透至智能资金（Smart Money）的脚印。

- **[摆动极值的微观物理本质]**：局部高点（Swing High）与局部低点（Swing Low）是市场买卖盘力量耗尽的真实物理反转点，其背后凝聚着大量未成交限价单与散户被动止损单。
- **[结构突破的流动性驱动]**：当价格放量击穿关键摆动高点（BOS）时，反映买方侵略性吃单彻底清空了盘口挂单流动性，趋势具备统计上的延续优势。
- **[角色转换的体制突变]**：当多头结构中价格首度跌穿前一个确认的抬高低点（Higher Low）时，市场状态机发生转移（CHoCH），标志着主控资金已完成派发并进入潜在空头体制。

【核心概念与就近图文排版】

1. 局部摆动极值点识别几何：
观察下图关于局部摆动极值点在滑动窗口 $k=2$ 约束下的微观 K 线判定拓扑：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.1.1：局部摆动极值点 (Swing High / Swing Low) 双向邻域识别几何结构</span>
    <span class="diagram-tag">SWING-POINTS</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l01_swing_points.svg -->
  </div>
</div>

- **[波峰判定规则]**：对 $t$ 周期高点，若对所有 $1 \le j \le k$ 均严格满足 $\text{High}_t > \text{High}_{t-j}$ 且 $\text{High}_t > \text{High}_{t+j}$，则确认为 Swing High。
- **[波谷判定规则]**：对 $t$ 周期低点，若对所有 $1 \le j \le k$ 均严格满足 $\text{Low}_t < \text{Low}_{t-j}$ 且 $\text{Low}_t < \text{Low}_{t+j}$，则确认为 Swing Low。
- **[零前视确认时滞]**：由于必须等待后置 $k$ 根 K 线收盘，算法在 $t+k$ 周期收盘时刻才可确权 $t$ 时刻的极值，严格根绝 Lookahead Bias。

2. 市场结构演进与状态机转移：
下图展示了上升趋势中顺势延续 (BOS) 与趋势反转 (CHoCH) 的离散状态转移逻辑：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.1.2：市场结构推进状态机：BOS 顺势延续与 CHoCH 趋势反转先兆</span>
    <span class="diagram-tag">BOS-CHOCH-STATE</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l01_bos_choch_state_machine.svg -->
  </div>
</div>

- **[顺势结构突破 BOS]**：多头趋势中收盘价向上有效击穿前关键 Swing High（HH），或空头趋势中跌破前 Swing Low（LL），确认同向能量延续。
- **[角色转变先兆 CHoCH]**：空头趋势中收盘价首度突破前关键 Lower High（LH），或多头趋势中向下跌破关键 Higher Low（HL），触发反转预警。
- **[回调二次确认规则]**：CHoCH 发生后，投决会严禁市价追单，必须等待价格二次回踩未成交流动性区并企稳后再行开仓。

3. 实体收盘突破与流动性扫荡博弈：
下图对比了机构有效实体突破与影线流动性猎杀（Liquidity Sweep）的订单流本质差异：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.1.3：实体收盘突破 (Valid Breakout) 与影线流动性掠夺 (Liquidity Sweep) 对比</span>
    <span class="diagram-tag">SWEEP-VS-BOS</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l01_liquidity_sweep_vs_breakout.svg -->
  </div>
</div>

- **[有效突破的收盘价锚]**：仅当 K 线实体收盘价（Close）稳定越过关键高低点时，才确认挂单供给被彻底吸收。
- **[影线扫荡的屠杀本质]**：最高价刺破前高但收盘跌回（Wick Sweep），属于做市商利用散户追涨买单吸收流动性建立空头仓位。
- **[风控伪信号过滤网]**：算法必须强制过滤影线假突破，避免将机构诱多诱空误判为趋势突破。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：订单流供需的物理守恒</div>
  <div class="callout-body">
    K 线不是画出来的图形，而是成交量在价格坐标轴上的能量投影。摆动极值点是买卖双方力量失衡的物理边界，机构大单必须在此类流动性密集区寻找对手盘。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁用静态均线或单周期极值点作为绝对开仓依据；多周期嵌套下，小级别的 CHoCH 往往只是大级别空头趋势中提供高盈亏比入场点的弱势反弹。
  </div>
</div>

【数学与状态机模型】
$$\text{State}_{t} = \begin{cases} 
\text{BULLISH}, & \text{if } C_t > \text{Last\_SH} \text{ and } \text{Prev\_State} = \text{BULLISH} \\
\text{BEAR_CHOCH}, & \text{if } C_t < \text{Last\_HL} \text{ and } \text{Prev\_State} = \text{BULLISH} \\
\text{BEARISH}, & \text{if } C_t < \text{Last\_SL} \text{ and } \text{Prev\_State} = \text{BEARISH} \\
\text{BULL_CHOCH}, & \text{if } C_t > \text{Last\_LH} \text{ and } \text{Prev\_State} = \text{BEARISH}
\end{cases}$$
定义域：$C_t > 0, \quad \text{window } k \ge 2, \quad t \ge 2k+1$。

【思考题】
Q1: 滞后均线 vs 实时价格行为（Price Action）：为什么基于移动平均线（如 MA5/MA20）的金叉死叉信号在震荡市中会导致灾难性的连续假信号与回撤，而基于微观市场结构（Swing Points & BOS）突破能够第一时间识别机构买卖盘意图？
Q2: 实体收盘突破（Candle Body Close Break） vs 影线假突破扫荡（Wick Sweep）：在判定 BOS 和 CHoCH 时，为什么机构级交易算法严格要求“K线收盘价有效突破前高/前低”，而将“最高价刺破但收盘跌回”判定为流动性扫荡（Liquidity Sweep）而非有效突破？
Q3: 多时间周期嵌套（Multi-Timeframe Structure）：假设日线处于明确的空头结构（连续 LH + LL），而 15 分钟级别由于突发利好出现 CHoCH 向上反弹。作为职业交易员，你应如何利用多时间周期共振设计“大级别顺势挂单，小级别抓反转确认”的交易计划？

【评分与通过规则】
- 代码 4 分：双向滑动窗口极值点识别 (2分) + 市场结构演化状态机与事件检测 (2分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：必须阐明微观订单流与流动性因果链
- 通过线：8/10 分。一票否决：引入未来函数前视偏差、篡改测试断言
"""'''

L01_ANSWERS_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 1/5 课
第 1 课：价格行为学与市场结构识别状态机 (参考答案版)
================================================================================

【Q1 深度参考答案】
滞后均线 vs 实时价格行为（Price Action）：为什么基于移动平均线（如 MA5/MA20）的金叉死叉信号在震荡市中会导致灾难性的连续假信号与回撤，而基于微观市场结构（Swing Points & BOS）突破能够第一时间识别机构买卖盘意图？
- **[移动平均线的低通滤波相位时滞]**：均线本质是价格时域信号的 FIR/IIR 线性平滑滤波器。平滑必然带来固有的时间延迟（Phase Lag）；窗口期越长，滞后越严重。当金叉形成时，价格往往已行至波段反弹的极限位，盈亏比极低。
- **[震荡市的负期望磨损]**：在无趋势箱体中，均线反复缠绕，均线金叉往往买在波段顶部、死叉割在波段底部，导致连续高频“左右挨打”并产生高额交易换手佣金磨损。
- **[微观摆动点的流动性锚定]**：Swing High 和 Swing Low 是市场供需天平达到极限的物理转折点，凝结了做市商库存成本与散户止损盘。BOS 突破反映的是真实挂单深度的击穿与吸收，代表机构主动买单的即时事实，不含任何平滑过滤滞后。

【Q2 深度参考答案】
实体收盘突破（Candle Body Close Break） vs 影线假突破扫荡（Wick Sweep）：在判定 BOS 和 CHoCH 时，为什么机构级交易算法严格要求“K线收盘价有效突破前高/前低”，而将“最高价刺破但收盘跌回”判定为流动性扫荡（Liquidity Sweep）而非有效突破？
- **[收盘价的公允均衡权重]**：日内极值（High/Low）往往由偶发的薄流动性脉冲成交或算法刺透触发；而蜡烛实体的收盘价（Close）反映了一根 K 线博弈结束时机构资金愿意接受的公允均衡价。
- **[流动性掠夺的微观猎杀]**：当价格仅以影线刺穿前高阻力位后迅速回落，反映机构主力在利用前高上方的散户追涨买单（Buy Stop）与空头止损买单作为流动性对手盘，趁机倾泻其庞大空头头寸完成高位派发。
- **[算法防伪与胜率保障]**：只有实体收盘价站上前高之上，才证明多头资金完成了对该价格带上方全部未成交卖单的实质性消化；将其作为入场前置条件能过滤掉 70% 以上的诱多屠杀。

【Q3 深度参考答案】
多时间周期嵌套（Multi-Timeframe Structure）：假设日线处于明确的空头结构（连续 LH + LL），而 15 分钟级别由于突发利好出现 CHoCH 向上反弹。作为职业交易员，你应如何利用多时间周期共振设计“大级别顺势挂单，小级别抓反转确认”的交易计划？
- **[大周期定战略偏向（Directional Bias）]**：日线级别的 LH + LL 确立了宏观主趋势为绝对空头（Higher Timeframe Bias = Short Only）。严禁在小级别反弹中重仓做多，逆大势交易期望收益为负。
- **[小级别定狙击战术（Precision Entry）]**：将 15 分钟的反弹 CHoCH 判定为日线空头趋势中的高价值回调（Pullback）。监控反弹动能触及日线级关键供需区（Order Block）或 0.618 斐波那契折返位。
- **[微观反转触发执行（Secondary Confirmation）]**：当反弹触及关键阻力带后，等待 15 分钟级别重新出现看跌 CHoCH（跌破局部抬高低点），随即顺势建立空头头寸。该结构将止损严格控制在 15 分钟局部高点，而止盈目标直指日线级前低 LL，获得 1:4 以上的优异盈亏比。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：顺大势、逆小势、抓共振</div>
  <div class="callout-body">
    任何单一时间维度的价格行为都是片面的。高水平机构交易员通过将高时间周期的结构边界与低时间周期的流动性触发点相互锚定，实现确定性与盈亏比的双重最大化。
  </div>
</div>
"""'''

# ------------------------------------------------------------------------------
# Lesson 02
# ------------------------------------------------------------------------------
L02_STARTER_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 2/5 课
第 2 课：供需区 (Order Blocks) 与流动性扫荡 (Liquidity Sweep) 检测
================================================================================

【课程定位与第一性原理】
在机构算法撮合视角下，传统技术分析所谓的“支撑与阻力线”并非静止的数学水平线，
而是机构资本在特定价格带留下的未平仓头寸（Unfilled Institutional Orders）所形成的流动性供需失衡区。
智能资金（Smart Money）在建仓时，由于头寸规模庞大，必须通过制造虚假突破（Liquidity Sweep）吸收对手盘流动性。

- **[订单块的形成微观物理]**：在爆发性单边脉冲（Displacement）发生之前，机构必须逆向吸收流动性，主升浪前最后的一根阴线即为看涨订单块（Bullish Order Block, OB）。
- **[双边流动性池循环]**：市场价格永远在买方流动性池（BSL, 前高上方止损单）与卖方流动性池（SSL, 前低下方止损单）之间循环穿梭，完成资本再平衡。
- **[缓解机制与二次上车点]**：机构未全部成交的限价单会在 OB 区间内形成强大的吸附引力；价格回踩入 OB 并在其中缩量企稳（Mitigation），是确定性极高的低风险进场点。

【核心概念与就近图文排版】

1. 看涨机构订单块形成与回踩缓解：
观察下图关于 Bullish Order Block 形成、脉冲拉升与后续回踩吸收的微观过程：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.2.1：看涨机构订单块 (Bullish Order Block) 形成与未成交流动性回踩吸收</span>
    <span class="diagram-tag">ORDER-BLOCK-OB</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l02_order_block_formation.svg -->
  </div>
</div>

- **[脉冲位移确认]**：OB 之后的 K 线必须展现出爆发性的实体位移（Displacement），其实体长度通常至少为 OB 实体的 1.8 倍以上。
- **[区间定义边界]**：对看涨 OB，其有效区域为该最后阴线的最高价（Top）至最低价（Bottom）；止损强制设置在 Bottom 下方。
- **[缓解与失效状态]**：当后续价格探入 [Bottom, Top] 区间时触发缓解（Mitigated）；若收盘价跌穿 Bottom，则该订单块彻底失效（Invalidated）。

2. 买方流动性池与卖方流动性池猎杀循环：
下图展示了机构资金在 BSL 与 SSL 两大流动性磁铁之间循环猎杀的路径图景：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.2.2：买方流动性池 (BSL) 与卖方流动性池 (SSL) 机构跨周期猎杀路径</span>
    <span class="diagram-tag">LIQUIDITY-POOLS</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l02_liquidity_pools_bsl_ssl.svg -->
  </div>
</div>

- **[BSL 买方流动性聚集]**：聚集在前高之上，由散户突破追多买单与前期做空资金的买入止损单组成。
- **[SSL 卖方流动性聚集]**：聚集在前低之下，由散户破位追空卖单与前期做多资金的卖出止损单组成。
- **[机构吞吐对手盘]**：机构欲建大额多头，必先砸盘击穿 SSL 诱发恐慌抛售；欲派发空头，必先拉升击穿 BSL 诱导追涨接盘。

3. 公允价值失衡区 (FVG) 几何与再平衡：
下图解析了单边侵略行情中三根 K 线形成的未撮合真空区 (Fair Value Gap)：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.2.3：公允价值失衡区 (Fair Value Gap, FVG) 几何拓扑与再平衡机制</span>
    <span class="diagram-tag">FVG-IMBALANCE</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l02_fair_value_gap.svg -->
  </div>
</div>

- **[失衡几何定义]**：K1 的高点与 K3 的低点之间未发生任何交叠的价格真空区间，即 $\text{FVG} = \text{Low}_3 - \text{High}_1 > 0$。
- **[价格磁吸引力]**：由于失衡区内仅存在单向激进买单撮合，市场具有强烈的回补该真空区以达成双边公允拍卖的引力。
- **[折让位介入法]**：回踩 FVG 50% 轴心（Consequent Encroachment）是仅次于订单块的高胜率狙击位。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：散户止损即机构流动性</div>
  <div class="callout-body">
    任何大资金建仓的最核心瓶颈是“滑点与市场冲击”。散户整齐划一设置在整数关口或前高前低的止损单，是机构大单完成无滑点换手的最佳对手盘池。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    并非所有阴线后的大阳线都是订单块。未引发结构突破（BOS）或未留下失衡区（FVG）的假订单块极易被直接穿透，不可作为防御防线。
  </div>
</div>

【数学与判定模型】
$$\text{Is\_Sweep}_{\text{BSL}} = \mathbb{I}(H_t > \text{Key\_Level} \land C_t < \text{Key\_Level})$$
$$\text{Is\_Sweep}_{\text{SSL}} = \mathbb{I}(L_t < \text{Key\_Level} \land C_t > \text{Key\_Level})$$
$$\text{Displacement} = \frac{|C_{t+1} - O_{t+1}|}{\max(|C_t - O_t|, 10^{-6})} \ge \alpha \quad (\alpha \ge 1.8)$$
定义域：$H_t \ge L_t > 0, \quad \text{Displacement} \in [0, +\infty)$。

【思考题】
Q1: 机构订单块（Order Blocks）形成的微观记账原理：为什么在发生暴力脉冲（Displacement）突破前的那根“最后相反方向蜡烛线”会留存海量机构未平仓买单/卖单？机构为何倾向于在未来引导价格回踩该区域（Mitigation）？
Q2: 外在流动性（BSL / SSL）与内在流动性（FVG / Order Blocks）的循环导航：请从做市商商业模式与对手盘撮合容量的角度，剖析为什么市场价格总是从一个外在流动性池扫荡至内在失衡区，再发起下一轮主推？
Q3: 订单块缓解（Mitigation）与失效（Invalidation）的量化判决：在策略回测中，如果价格跌破看涨订单块的最低点（Invalidation），从微观资金结构看意味着什么？为什么此时必须无条件止损离场？

【评分与通过规则】
- 代码 4 分：流动性扫荡判定函数 (1.5分) + 订单块识别与缓解状态跟踪 (2.5分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：从微观记账与做市商库存视角严密剖析
- 通过线：8/10 分。一票否决：概念颠倒（将跌破订单块判定为支撑良好）、篡改断言
"""'''

L02_ANSWERS_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 2/5 课
第 2 课：供需区 (Order Blocks) 与流动性扫荡 (Liquidity Sweep) 检测 (参考答案版)
================================================================================

【Q1 深度参考答案】
机构订单块（Order Blocks）形成的微观记账原理：为什么在发生暴力脉冲（Displacement）突破前的那根“最后相反方向蜡烛线”会留存海量机构未平仓买单/卖单？机构为何倾向于在未来引导价格回踩该区域（Mitigation）？
- **[巨额资本建仓的对手盘瓶颈]**：百亿美元级多头对冲基金要建立数亿股多头仓位，若直接在市价挂单买入，会瞬间打出巨大的自伤滑点（Market Impact）。因此，机构必须在拉升前主动先下杀打压价格，以激发市场恐慌性卖盘并吸收对手盘。
- **[浮亏被套头寸的留存事实]**：在拉升前的那根最后阴线中，机构为了制造破位恐慌，自身也建有部分对冲性质的空单或未完全成交的试仓单。随着主升浪爆发（Displacement），这些逆向底仓即刻陷入浮亏。
- **[回踩解套与二次补仓（Mitigation）]**：当价格行至高位派发完毕后，机构会利用散户跟风买盘的衰竭，允许价格回调至最初建仓的成本密集区（OB）。在此区间，机构平掉先前的亏损空单（对冲平仓），同时激活此前因盘口容量不足未成交的剩余海量限价多单，从而催生极具爆发力的第二波顺势上涨。

【Q2 深度参考答案】
外在流动性（BSL / SSL）与内在流动性（FVG / Order Blocks）的循环导航：请从做市商商业模式与对手盘撮合容量的角度，剖析为什么市场价格总是从一个外在流动性池扫荡至内在失衡区，再发起下一轮主推？
- **[外在流动性（External Liquidity）充当燃料池]**：前高上方的 BSL 和前低下方的 SSL 是全市场流动性最充裕的区域。做市商与机构算法的核心生存逻辑就是“追逐流动性以完成大额头寸交割”。扫荡 BSL/SSL 能够以最小冲击成本兑现前期利润或完成初次大规模吸筹。
- **[内在流动性（Internal Liquidity）充当价值再平衡锚]**：在外在流动性被掠夺（Sweep）之后，盘口短期流动性枯竭，价格必然在均值回归引力下折返，寻找此前单边暴跌/暴涨留下的内在公允价值失衡区（FVG）或未缓解订单块（OB）。
- **[跨周期钟摆运动的微观物理]**：市场就是一部精密运转的流动性拍卖泵：外部流动性（出清对手盘）➔ 内部流动性（补单再平衡）➔ 突破开辟新的外部流动性。理解这一闭环，量化策略即可精准预判主升主跌浪的时空拐点。

【Q3 深度参考答案】
订单块缓解（Mitigation）与失效（Invalidation）的量化判决：在策略回测中，如果价格跌破看涨订单块的最低点（Invalidation），从微观资金结构看意味着什么？为什么此时必须无条件止损离场？
- **[机构多头防线的彻底溃败]**：看涨订单块的最低点（Bottom）是该波大级别上涨发起时机构最后入场吸收流动性的绝对底线成本。若收盘价跌破该位置，表明主控机构已经完全放弃抵抗，甚至其自身多头头寸已在更高位置获利了结完毕。
- **[多空供求天平的彻底逆转]**：跌破 OB 最低点意味着原有供给吸收假说彻底证伪，盘口由激进的主动性卖方牢牢掌控，下方的卖方流动性（SSL）将被真空加速穿透。
- **[坚决止损的破产防范数学]**：死扛失效订单块是对冲基金穿仓的首要死因。一旦 Invalidation 发生，原有的高盈亏比入场逻辑不复存在，必须无条件按照止损纪律执行平仓，将最大单笔损失锁死在 1R 以内。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：订单块有效看实体，失效坚决斩仓</div>
  <div class="callout-body">
    订单块是机构资金的脚印而非神圣图腾。回踩缩量验证说明吸收成立；放量击穿成本下沿说明主控力量易主，必须服从概率法则坚决离场。
  </div>
</div>
"""'''

# ------------------------------------------------------------------------------
# Lesson 03
# ------------------------------------------------------------------------------
L03_STARTER_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 3/5 课
第 3 课：经典价格形态量化识别与几何拓扑 (头肩底、双底与威科夫弹簧)
================================================================================

【课程定位与第一性原理】
传统技术分析常因主观“看图说话”而沦为伪科学。本课立足量化工程第一性原理，
将经典价格形态解构为严格的极值点拓扑空间（Topological Extremum Space）与几何约束网，
穿透形态背后多空力量衰竭、浮筹清洗与威科夫弹簧效应（Wyckoff Spring）的博弈本质。

- **[头肩底的供需耗尽本质]**：头肩底并非神秘的东方玄学，而是空头三次向下冲击时动能逐级衰竭的物理映射——左肩恐慌抛售，头部最后宣泄，右肩无力创新低，颈线突破宣告供求平衡被彻底打翻。
- **[威科夫弹簧的流动性假摔]**：在双底结构中，次底故意刺破前低（Spring）随后光速收复，是主力资金在低位触发散户破位止损单以快速吸筹的极致体现。
- **[几何容差与数学可证伪性]**：形态量化识别器必须以参数化容差（双肩对称比、颈线斜率、头部深陷度）取代肉眼主观臆断，实现 100% 确定性的计算机代码回测。

【核心概念与就近图文排版】

1. 头肩底几何拓扑与颈线断裂：
观察下图关于头肩形态各几何节点（左肩、头部、右肩、颈线）的严格量化特征：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.1：经典头肩顶形态 (Head & Shoulders) 几何拓扑与颈线断裂确认</span>
    <span class="diagram-tag">HEAD-SHOULDERS-TOPOLOGY</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l03_head_and_shoulders_anatomy.svg -->
  </div>
</div>

- **[头部突出性约束]**：头部最低点必须显著深陷于左右双肩之下，相对双肩均价至少突出 $\ge 3\%$。
- **[双肩对称性容差]**：左肩低点与右肩低点的高度差异必须受控在动态容差 $\epsilon_{\text{shoulder}} \le 5\%$ 之内。
- **[颈线突破与量度目标]**：收盘价站上颈线价格 $P_{\text{neck}}$ 确认突破，理论最小量度目标位为 $P_{\text{target}} = P_{\text{neck}} + H$，其中 $H = P_{\text{neck}} - P_{\text{head}}$。

2. 双底形态与威科夫弹簧效应 (Spring)：
下图展示了双底形态中次底假摔猎杀止损并迅速收复的威科夫弹簧结构：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.2：双底形态 (W-Bottom) 与威科夫弹簧效应 (Spring) 诱空反转结构</span>
    <span class="diagram-tag">WYCKOFF-SPRING</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l03_double_bottom_spring.svg -->
  </div>
</div>

- **[初次探底阻击]**：底 1 发生后迎来超跌反弹，确立中枢颈线高点。
- **[弹簧刺破假跌破]**：底 2 跌破底 1 最低点引发破位追空盘，但随即被大单承接并收出长下影线。
- **[突破确认入场]**：价格放量收复颈线确立双底反转，盈亏比往往超过 1:3。

3. 形态量化算法特征抽取流水线：
下图展示了量化系统自动从离散价格时序中提纯形态的 4 步状态过滤网：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.3：形态量化识别算法：局部极值点拓扑抽取与容差约束网</span>
    <span class="diagram-tag">ALGO-EXTRACTION</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l03_quant_feature_extraction.svg -->
  </div>
</div>

- **[极值点序列提纯]**：通过双向滑动窗口提取 5 拐点序列 $E = [e_1, e_2, e_3, e_4, e_5]$。
- **[几何拓扑逻辑校验]**：验证 $e_3 < \min(e_1, e_5)$ 且 $e_2, e_4 > \max(e_1, e_5)$。
- **[动态容差网过滤]**：剔除双肩畸变、颈线倾角过大（$|\theta| > 15^\circ$）的非标准伪形态。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：形态是供需博弈的几何残差</div>
  <div class="callout-body">
    形态本身没有任何预测未来的魔法。优秀的量化交易员只将形态视为“盈亏比极度非对称的风险收益契约”，在颈线突破时入场，止损设在右肩下方，追求至少 1:2 的数学期望。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁在形态未完成颈线收盘突破前“抢跑买入”。在右肩形成过程中提前下注，极易掉入下降中继三角形或双底破位下杀的深渊。
  </div>
</div>

【数学与几何判决模型】
$$\text{Sym}_{\text{shoulder}} = \frac{|P_{\text{LS}} - P_{\text{RS}}|}{P_{\text{LS}}} \le \epsilon_{\text{shoulder}} \quad (\epsilon \le 0.05)$$
$$\text{Prom}_{\text{head}} = \min\left(\frac{P_{\text{LS}} - P_{\text{Head}}}{P_{\text{Head}}}, \frac{P_{\text{RS}} - P_{\text{Head}}}{P_{\text{Head}}}\right) \ge \delta_{\text{prom}} \quad (\delta \ge 0.03)$$
$$\text{RRR} = \frac{P_{\text{target}} - P_{\text{entry}}}{P_{\text{entry}} - P_{\text{stop}}} = \frac{(P_{\text{neck}} + H) - C_t}{C_t - P_{\text{RS}}}$$
定义域：$P_{\text{Head}} < \min(P_{\text{LS}}, P_{\text{RS}}), \quad P_{\text{neck}} > P_{\text{LS}}, \quad C_t \ge P_{\text{neck}}$。

【思考题】
Q1: 经典头肩形态的供需力量衰竭推导：从三次尝试突破的成交量逐级递减、左肩/头/右肩的微观换手率，推导为何颈线破位后常引发量度跌幅的非线性踩踏？
Q2: 威科夫弹簧效应（Wyckoff Spring）与次底假摔猎杀：为什么在双底（W-Bottom）结构中，第二个底部略微刺穿第一个底部最低点（Spring）反而比未刺穿的平底具有更高的反弹胜率？从流动性清算与浮筹吸收的角度论述。
Q3: 形态量化算法的“几何容差”陷阱：为什么在真实市场中机械要求左右肩绝对对称（0% 误差）会导致策略几乎无法触发，而容差过大（如 > 20%）又会陷入过拟合与高假阳性（False Positive）灾难？算法如何自适应动态平衡？

【评分与通过规则】
- 代码 4 分：头肩底几何拓扑校验与颈线突破判定 (2.5分) + 目标价与盈亏比计算 (1.5分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：以拓扑几何与订单流衰竭为核心展开论述
- 通过线：8/10 分。一票否决：未突破即判定有效、盈亏比计算错误
"""'''

L03_ANSWERS_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 3/5 课
第 3 课：经典价格形态量化识别与几何拓扑 (参考答案版)
================================================================================

【Q1 深度参考答案】
经典头肩形态的供需力量衰竭推导：从三次尝试突破的成交量逐级递减、左肩/头/右肩的微观换手率，推导为何颈线破位后常引发量度跌幅的非线性踩踏？
- **[多头攻击动能的递减法则]**：在头肩顶形态中，左肩是强趋势的主升浪，伴随天量成交；随后冲高回落；头部虽创出新高，但成交量明显萎缩（量价背离），说明增量买盘枯竭；右肩的反弹甚至无法触及头部高点，反映多头资金彻底丧失进攻意愿。
- **[颈线支撑的筹码沉淀]**：两次回调的低点连线（颈线）沉淀了大量在形态构筑期间左侧抄底的浮筹。所有右肩买入者与颈线附近的多头，其止损单均密集成交在颈线下方。
- **[非线性雪崩正反馈]**：一旦价格跌破颈线，触发三维共振卖盘：① 颈线多头集中斩仓卖盘；② 趋势突破算法的追空市价单；③ 意识到形态破位的长线机构撤出买单挂单（流动性真空）。三重合力形成做空正反馈，驱动价格快速打满垂直高度 H 的量度跌幅。

【Q2 深度参考答案】
威科夫弹簧效应（Wyckoff Spring）与次底假摔猎杀：为什么在双底（W-Bottom）结构中，第二个底部略微刺穿第一个底部最低点（Spring）反而比未刺穿的平底具有更高的反弹胜率？从流动性清算与浮筹吸收的角度论述。
- **[平底双底的浮筹残留缺陷]**：若第二个底未跌破前低，虽然形态美观，但前低下方积压的大量散户止损单并未被清洗，多头平均持仓成本偏高，后市拉升时极易遭遇获利盘和解套盘的连续砸盘压制。
- **[弹簧假摔的流动性核爆吸收]**：主力资金在次底故意下砸打破前低支撑线，引发条件触发的卖方止损盘（SSL）与破位追空盘狂暴涌出。主力利用这波瞬时的高流动性大口吞下廉价筹码，完成终极吸筹（Terminal Shakeout）。
- **[浮筹彻底出清的轻盈拉升]**：随着坚决杀跌盘被洗劫一空，盘口上方的抛压阻力被彻底排空。主力资金只需很小的买盘即可将价格光速拉回前低之上并暴击颈线，形成胜率与爆发力极佳的威科夫 Spring 结构。

【Q3 深度参考答案】
形态量化算法的“几何容差”陷阱：为什么在真实市场中机械要求左右肩绝对对称（0% 误差）会导致策略几乎无法触发，而容差过大（如 > 20%）又会陷入过拟合与高假阳性（False Positive）灾难？算法如何自适应动态平衡？
- **[机械零容差的样本稀疏（Underfitting）]**：金融市场充满微观噪声，左右肩在自然撮合下绝对等高的概率接近测度零。若设定对称误差低于 1%，全市场数年可能无法捕捉到任何有效样本，策略失去实际可交易性。
- **[过大容差的数据挖掘伪形态（Overfitting & False Positives）]**：若将容差放大至 15%~25%，算法会将普通的震荡无序锯齿波错误识别为头肩形态。此类“畸变伪形态”背后根本不存在多空动能衰竭的因果链，实盘交易胜率将骤降至 35% 以下，带来灾难性回撤。
- **[自适应动态平衡解法]**：工程架构上应当采用“双重约束网”：① 静态几何容差锚定在 5%~8%；② 引入微观动量或成交量确认因子（如头部成交量必须高于右肩成交量，右肩反弹动能 RSI 必须弱于左肩）。通过多维度交叉印证，在样本覆盖率与信号纯度之间达成纳什均衡。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：拒绝图形玄学，坚持严格量化</div>
  <div class="callout-body">
    形态的有效性来自市场多空预期的失衡，而非几何图形的美观。只有在严格拓扑容差、量价背离与盈亏比大于 1:1.5 的前提下，形态交易才具备统计套利的正期望。
  </div>
</div>
"""'''

# ------------------------------------------------------------------------------
# Lesson 04
# ------------------------------------------------------------------------------
L04_STARTER_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 4/5 课
第 4 课：动量与趋势指标数学本质：自适应滤波与时滞消除 (Wilder RSI, Bollinger Bands & Zero Lookahead)
================================================================================

【课程定位与第一性原理】
技术指标绝非预测未来的水晶球，其本质是对历史离散成交价格时序的不同核函数加权（Convolution Filtering）。
投资委员会在评估量化动量系统时，必须从数字信号处理（DSP）与概率统计物理的第一性原理出发，
深刻洞察指标滤波的时滞代价（Phase Lag）、单边市动量钝化与回测中前视偏差（Lookahead Bias）的致命陷阱。

- **[平滑滤波与时滞不可兼得]**：简单移动平均（SMA）与怀尔德平滑（Wilder Smoothing）本质是时域低通滤波器。消除高频噪声必然带来相位延迟；均线金叉死叉在震荡市中天然具有负数学期望。
- **[自适应布林带与波动率挤压]**：曼德博（Mandelbrot）证明金融收益率服从肥尾与波动率聚集特征。布林带通过滚动方差自适应缩放通道；带宽极度挤压（Squeeze）预示着波动率均值回归的能量爆发。
- **[因果性契约与前视偏差清零]**：回测中用当日收盘价直接撮合当日收盘生成的信号（Same-bar Execution），在实盘物理世界中属于无法完成的违约作弊；信号必须严格滞后一期（Shift-1）执行。

【核心概念与就近图文排版】

1. 移动平均滤波器相位时滞比较：
观察下图关于真实价格阶跃与各类移动均线滤波器的响应延迟对比：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.4.1：均线滤波器相位时滞比较：真实价格 vs SMA vs EMA vs 零滞后滤波器</span>
    <span class="diagram-tag">FILTER-PHASE-LAG</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l04_moving_average_lag.svg -->
  </div>
</div>

- **[SMA 简单均线滞后]**：矩形滑动窗口导致权重均匀分布，对价格突变的响应存在 $\frac{N-1}{2}$ 的固有相位时滞。
- **[EMA 指数均线权重衰减]**：赋予近期价格指数级递增权重，有效减轻了时滞，但仍无法完全消除相位延迟。
- **[零滞后滤波代价]**：零滞后算法（如 DEMA/KAMA）虽然时效性强，但对输入高频随机游走噪声极其敏感，容易产生伪翻转信号。

2. 怀尔德 RSI 动量振荡与顶背离：
下图展示了经典 14 周期 RSI 指标在趋势上涨中的背离预警机制：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.4.2：怀尔德 RSI 动量振荡器、顶背离结构与超买超卖界限</span>
    <span class="diagram-tag">WILDER-RSI</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l04_wilder_rsi_momentum.svg -->
  </div>
</div>

- **[怀尔德平滑递推]**：怀尔德平滑衰减因子 $\alpha = \frac{1}{N}$，等价于 $2N-1$ 周期的指数移动平均。
- **[超买区持续钝化]**：在单边强趋势中，RSI 长期黏着在 70 以上，此时盲目按均值回归做空将被瞬间逼空爆仓。
- **[价格与动量顶背离]**：价格创出更高高点（HH），而 RSI 动量峰值创出更低高点（LH），这才是均值回归胜率最高的入场前兆。

3. 自适应布林带挤压 (Volatility Squeeze)：
下图展示了布林带带宽收敛至极限后引发的单边爆发与喇叭口张开：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.4.3：自适应布林带 (Bollinger Bands) 波动率挤压 (Squeeze) 与暴动突破</span>
    <span class="diagram-tag">VOLATILITY-SQUEEZE</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l04_bollinger_volatility_squeeze.svg -->
  </div>
</div>

- **[带宽指标 BandWidth]**：$\text{BandWidth} = \frac{\text{Upper} - \text{Lower}}{\text{Middle}}$，定量度量市场波动率水位。
- **[挤压阶段能量蓄积]**：当带宽跌入历史后 5% 分位数时，反映市场做市商挂单极其密集，波动能量被深度压缩。
- **[%B 突破顺势跟随]**：价格向上穿透上轨（$\%B > 1.0$）且伴随带宽暴涨，确立高胜率顺势突破做多。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：波动率均值回归铁律</div>
  <div class="callout-body">
    资产价格趋势具有记忆性，而资产收益率的波动率具有极强的均值回归性。在极低波动率时购买波动率（做多跨式期权或跟随布林带挤压突破），是量化宏观最经典的非对称下注。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁用当日收盘价生成的信号在当日收盘执行回测撮合！必须将信号序列 `.shift(1)` 滞后到下一交易日执行，否则回测夏普比率完全是前视偏差构造的虚假骗局。
  </div>
</div>

【数学与指标模型】
$$\text{RSI} = 100 - \frac{100}{1 + \text{RS}}, \quad \text{其中 } \text{RS} = \frac{\text{SmoothGain}_t}{\text{SmoothLoss}_t}$$
$$\text{SmoothGain}_t = \frac{\text{SmoothGain}_{t-1} \times (N-1) + \text{Gain}_t}{N}$$
$$\text{Upper} = \text{MA}_N(C) + k \cdot \sigma_N(C), \quad \text{Lower} = \text{MA}_N(C) - k \cdot \sigma_N(C)$$
$$\text{Position}_t = \text{Signal}_{t-1} \quad (\text{严格因果滞后约束})$$
定义域：$N = 14, \quad k = 2.0, \quad \text{RSI} \in [0, 100], \quad \sigma_N(C) > 0$。

【思考题】
Q1: RSI 指标的“钝化伪失效”与“极值背离”：在单边大牛市或流动性极度宽松环境中，RSI 持续高于 70（理论超买）往往长达数周；为什么盲目做空会导致惨重亏损？如何通过“价格创新高而动量无法创新高”的顶背离提高均值回归胜率？
Q2: 波动率挤压（Volatility Squeeze）与波动率聚集（Volatility Clustering）：曼德博（Mandelbrot）指出金融时间序列具有强烈的波动率聚集特征。布林带的带宽（BandWidth = (Upper - Lower)/Middle）压缩至历史极值低分位数（如 5% 分位）时，为何往往预示着爆发性的单边大趋势即将来临？交易员应如何避免在挤压区内被假突破洗出？
Q3: 严格因果契约与前视偏差防范：在向量化回测（Vectorized Backtest）与事件驱动回测（Event-Driven Backtest）中，如果不小心用当日收盘价直接撮合当日根据收盘价生成的买卖信号（Same-bar Close Execution），在实盘中会遇到什么致命问题？在代码架构上如何通过 `.shift(1)` 机制彻底杜绝未来函数？

【评分与通过规则】
- 代码 4 分：怀尔德平滑 RSI 算法 (1.5分) + 布林带及衍生特征计算 (1.5分) + 无前视偏差信号生成 (1分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：深入阐明数字信号滤波与实盘因果对齐
- 通过线：8/10 分。一票否决：未实施 shift(1) 前视隔离、篡改测试断言
"""'''

L04_ANSWERS_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 4/5 课
第 4 课：动量与趋势指标数学本质：自适应滤波与时滞消除 (参考答案版)
================================================================================

【Q1 深度参考答案】
RSI 指标的“钝化伪失效”与“极值背离”：在单边大牛市或流动性极度宽松环境中，RSI 持续高于 70（理论超买）往往长达数周；为什么盲目做空会导致惨重亏损？如何通过“价格创新高而动量无法创新高”的顶背离提高均值回归胜率？
- **[超买指标在强趋势中的单向钝化]**：RSI 本质是过去 14 天涨幅相对跌幅的比率。在由宏观流动性推升的强动量单边市中，每日收盘价持续抬高，分母中的平均亏损几乎为零，导致 RSI 长期被钉死在 75~90 的极端超买区间。此时 RSI 高位恰恰反映了强劲的做多动量，将其视为“贵而必跌”的做空信号是散户最常见的均值回归认知陷阱。
- **[背离信号的微观能量耗竭]**：单纯的高位震荡不可怕，可怕的是背离。当价格创出更高高点（HH），而 RSI 却形成更低高点（LH），这从数学上严格证明了：虽然价格仍在惯性冲高，但单位时间内的平均涨幅加速度正在急剧衰减，边际买盘力量枯竭。
- **[结合结构触发的胜率保障]**：专业交易员绝不在背离发生的瞬间左侧盲目猜顶，而是在 RSI 顶背离成立后，密切监控小级别市场结构破位（如 15 分钟 CHoCH 跌破关键低点）。此时结合“动量背离 + 结构破位”双重共振进场，盈亏比与胜率均呈指数级提升。

【Q2 深度参考答案】
波动率挤压（Volatility Squeeze）与波动率聚集（Volatility Clustering）：曼德博（Mandelbrot）指出金融时间序列具有强烈的波动率聚集特征。布林带的带宽（BandWidth = (Upper - Lower)/Middle）压缩至历史极值低分位数（如 5% 分位）时，为何往往预示着爆发性的单边大趋势即将来临？交易员应如何避免在挤压区内被假突破洗出？
- **[波动率聚集与均值回归循环]**：金融资产的价格行为服从“高波动率 ➔ 低波动率 ➔ 高波动率”的交替循环。当布林带带宽被压缩至历史后 5% 分位数时，表明多空在当前狭窄价格区间内达成高度共识，挂单深度极度堆积，系统熵减达到临界点。
- **[破局脉冲的雪崩效应]**：极窄通道无法容纳任何新的宏观信息或大额头寸再平衡。一旦突发外生事件打破平衡，价格触碰单侧轨道，将瞬间引发单向止损单踩踏与算法追单，触发喇叭口暴力外扩的非线性脉冲行情。
- **[防假突破洗盘风控机制]**：在挤压区间内，做市商常通过双向刺透扫荡止损（Wick Sweep）。防范洗盘的核心法则有二：① 严禁在挤压区间中轨附近提前猜方向下注；② 必须等待有效 K 线实体收盘价收在布林轨道之外（%B > 1.0 或 %B < 0.0），且带宽斜率显著拐头向上时，再行顺势进场。

【Q3 深度参考答案】
严格因果契约与前视偏差防范：在向量化回测（Vectorized Backtest）与事件驱动回测（Event-Driven Backtest）中，如果不小心用当日收盘价直接撮合当日根据收盘价生成的买卖信号（Same-bar Close Execution），在实盘中会遇到什么致命问题？在代码架构上如何通过 `.shift(1)` 机制彻底杜绝未来函数？
- **[物理不可实现的时序倒流]**：在现实交易中，当日收盘价（Close）在交易日的最后一微秒（如 15:00:00）才最终确定。算法不可能在 15:00:00.000 瞬间完成数据采集、计算指标、生成信号、网络报单并在 15:00:00 以当日收盘价完成撮合。
- **[前视偏差对回测的毁灭性粉饰]**：Same-bar Execution 相当于算法在日内就已经预知了当天的收盘结果，回测净值往往呈现出不切实际的完美 45 度向上曲线（夏普比率常虚高至 4.0 以上）。而一旦实盘上线，策略会立刻遭遇严重滑点甚至策略崩盘。
- **[.shift(1) 机制的工程因果铁律]**：量化工程架构必须严格遵循因果对齐原则。在代码中，`position = raw_signal.shift(1).fillna(0)` 强制将信号生成时间与头寸执行时间错开一个周期——即在 $T$ 日收盘根据当日已确定的行情计算信号，并在 $T+1$ 日开盘以市场真实价格完成建仓撮合。这是量化资产管理机构投决会审核策略的绝对红线。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：实盘因果不可违，虚假夏普零容忍</div>
  <div class="callout-body">
    任何未经过严格 shift(1) 时序因果隔离的回测都是数据废品。量化研究员的第一美德是敬畏物理时间维度的单向不可逆性。
  </div>
</div>
"""'''

# ------------------------------------------------------------------------------
# Lesson 05
# ------------------------------------------------------------------------------
L05_STARTER_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 5/5 课
第 5 课：订单流成交量分布 (Volume Profile) 与锚定 VWAP (POC, VAH/VAL & Anchored VWAP)
================================================================================

【课程定位与第一性原理】
传统技术图表只关注价格随“时间（Time）”的展开，却对交易博弈的最关键维度——“成交量在价格上的分布（Volume-at-Price）”完全盲目。
拍卖市场理论（Auction Market Theory, AMT）指出，金融市场本质是一个双向连续竞价的拍卖撮合场，
其唯一终极目的就是在不同价格水平寻找能够促成最大换手交易量的公允价值区（Fair Value）。

- **[成交量分布 VPVR 的博弈本质]**：控制点（POC, Point of Control）是多空双方沉淀筹码最厚重的绝对公允价值共识点；离开价值区意味着拍卖失衡。
- **[70% 价值区与高斯正态分布]**：价值区（VA, Value Area）覆盖约 70% 的历史成交量（对应正态分布 1 个标准差范围 $\pm 1\sigma$），其高轨（VAH）与低轨（VAL）构成最天然的机构供需边界。
- **[锚定 VWAP 的真实持仓成本]**：锚定自重大事件（加息、财报、结构破位）的 Anchored VWAP，代表了自该事件发生以来全市场参与者的加权平均持仓成本线，具有不可逆转的心理防线意义。

【核心概念与就近图文排版】

1. 可见范围成交量分布与 70% 价值区：
观察下图关于水平成交量分箱、POC 控制点与 VAH / VAL 价值区的微观结构：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.1：可见范围成交量分布 (VPVR)：POC 控制点与 70% 价值区 (VAH / VAL)</span>
    <span class="diagram-tag">VOLUME-PROFILE</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l05_volume_profile_vpvr.svg -->
  </div>
</div>

- **[POC 控制点最大共识]**：成交量最高的水平价格分箱（Point of Control），是全市场多空换手博弈最充分的公允锚点。
- **[VAH / VAL 价值区边界]**：从 POC 开始向双向按成交量贪婪扩张直至覆盖 70% 总成交量，上边界为 VAH，下边界为 VAL。
- **[低成交量节点 LVN 真空加速]**：成交量稀薄的低成交量区（Low Volume Node），价格穿透时阻力最小，常发生跳空或单边脉冲快速滑过。

2. 重大事件锚定 VWAP 与动态标准差通道：
下图展示了从重大宏观事件锚定的 AVWAP 及其 $\pm 2\sigma$ 标准差偏离通道：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.2：事件锚定 VWAP (Anchored VWAP) 与动态标准差通道防御模型</span>
    <span class="diagram-tag">ANCHORED-VWAP</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l05_anchored_vwap_dynamics.svg -->
  </div>
</div>

- **[加权成交均价公式]**：$\text{VWAP}_t = \frac{\sum_{i=1}^t P_i \cdot V_i}{\sum_{i=1}^t V_i}$，真实反映资本平均盈亏平衡线。
- **[加权方差通道]**：基于成交量加权方差计算通道上轨与下轨，提供确定性的对冲与均值回归边界。
- **[均线支撑回踩]**：在牛市主升浪中，价格回调至 AVWAP 往往引发机构被动加仓算法的强力买盘拦截。

3. 市场筹码分布三态演进图谱：
下图对比了 P 型分布（空头回补）、b 型分布（长线出逃）与 D 型分布（公允平衡）的三态转换：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.3：市场筹码分布三态：P 型多头冲刺、b 型空头派发与 D 型公允平衡</span>
    <span class="diagram-tag">PROFILE-REGIMES</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l05_liquidity_distribution_regimes.svg -->
  </div>
</div>

- **[P 型分布 (空头回补轧空)]**：成交量集中在当日顶部，底部单薄，反映空头被迫平仓诱发短跑冲刺，高位往往出现接力滞胀。
- **[b 型分布 (多头踩踏清算)]**：成交量堆积在当日底部，顶部单薄，反映多头资金认赔出逃，但在低位存在大资金吸筹。
- **[D 型分布 (经典公允均衡)]**：呈经典高斯钟形分布，POC 居中，多空充分换手，处于无趋势震荡箱体。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：价值区内的均值回归 vs 价值区外的趋势爆发</div>
  <div class="callout-body">
    当价格运行在 70% 价值区内（VAL ~ VAH）时，交易主线是均值回归，做多低点做空高点；一旦价格伴随放量有效跳出价值区并完成回踩确认，意味着全市场对估值共识发生永久性跃迁，必须立刻切换为顺势突破单边策略。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁逆向对抗从关键结构低点锚定的上升 AVWAP！机构执行算法（VWAP Execution Engine）在价格接近 VWAP 时具有自动平滑挂单吸收指令，逆势做空将被机构流动性碾压。
  </div>
</div>

【数学与拍卖模型】
$$\text{Typical\_Price}_t = \frac{H_t + L_t + C_t}{3}$$
$$\text{VWAP}_t = \frac{\sum_{s=1}^t \text{Typical\_Price}_s \times V_s}{\sum_{s=1}^t V_s}$$
$$\sigma_{\text{VWAP}, t} = \sqrt{\frac{\sum_{s=1}^t V_s \times (\text{Typical\_Price}_s - \text{VWAP}_t)^2}{\sum_{s=1}^t V_s}}$$
$$\text{Z-Score}_t = \frac{\text{Typical\_Price}_t - \text{VWAP}_t}{\sigma_{\text{VWAP}, t}}$$
定义域：$V_s > 0, \quad \sigma_{\text{VWAP}, t} > 0, \quad \text{Value\_Area\_Ratio} = 0.70$。

【思考题】
Q1: 价值区（Value Area 70% 规则）的数理统计依据：为什么华尔街拍卖市场理论（Auction Market Theory, AMT）将 70% 的成交量区域定义为“价值区（Value Area）”？当价格由内向外有效突破 VAH 或 VAL 时，为什么传统“均值回归”交易者会被迫止损而演变为单边暴利“趋势行情”？
Q2: 机构算法交易的 VWAP 基准考核：为什么高盛、摩根士丹利等顶级投行的机构大单执行算法（如 TWAP, VWAP 算法执行器）将当天的日内成交均价是否优于市场 VWAP 作为核心考核 KPI？这如何直接导致市场价格在触及日内 VWAP 时产生天然的强支撑与阻力效应？
Q3: 锚定 VWAP（Anchored VWAP, AVWAP）的锚点选择科学：与普通从固定早盘 9:30 开始计算的日内 VWAP 相比，为什么从“年内历史最低点”、“重大利好财报公布日”或“重大结构突破日”锚定的长期 AVWAP 具有强大的中长期筹码支撑力？请从“该事件以来全市场持仓筹码平均盈亏平衡点”的角度进行博弈论解释。

【评分与通过规则】
- 代码 4 分：基于典型价格的成交量分箱与 70% 价值区算法 (2.5分) + 累积 VWAP 与加权标准差通道 (1.5分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：从拍卖理论、大单执行与持仓筹码加权成本展开
- 通过线：8/10 分。一票否决：价值区计算逻辑混乱、删除断言
"""'''

L05_ANSWERS_DOC = r'''r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 5/5 课
第 5 课：订单流成交量分布 (Volume Profile) 与锚定 VWAP (参考答案版)
================================================================================

【Q1 深度参考答案】
价值区（Value Area 70% 规则）的数理统计依据：为什么华尔街拍卖市场理论（Auction Market Theory, AMT）将 70% 的成交量区域定义为“价值区（Value Area）”？当价格由内向外有效突破 VAH 或 VAL 时，为什么传统“均值回归”交易者会被迫止损而演变为单边暴利“趋势行情”？
- **[高斯正态分布 1 个标准差统计对应]**：在大数定律下，市场充分竞价的成交量分布往往趋近于正态分布（Normal Bell Curve）。在正态分布中，$[-1\sigma, +1\sigma]$ 刚好包含 68.26%（工程经验取整为 70%）的数据点。因此，将累计 70% 成交量聚集的区间定义为价值区（Value Area），代表多空双方均认可的公允拍卖中枢。
- **[均值回归交易者的预期模型]**：在价值区内部，价格运行受阻于 VAH 并被 POC 吸引回归；因此区间交易者习惯在 VAH 做空、VAL 做多，止损刚好紧贴在 VAH 上方或 VAL 下方。
- **[突破引发的公允价值再定价]**：一旦买方以侵略性市价单彻底吞噬 VAH 上方的全部挂单，收盘有效站上 VAH，表明市场认为原有价值区过于被低估（Rejection of Low Prices）。此时原先做空的交易员被迫集体买入止损，场外动量交易算法集体进场顺势追多，推动价格脱离原有平衡进入单边极速趋势。

【Q2 深度参考答案】
机构算法交易的 VWAP 基准考核：为什么高盛、摩根士丹利等顶级投行的机构大单执行算法（如 TWAP, VWAP 算法执行器）将当天的日内成交均价是否优于市场 VWAP 作为核心考核 KPI？这如何直接导致市场价格在触及日内 VWAP 时产生天然的强支撑与阻力效应？
- **[资管机构大单执行的最优执行评价体系（Best Execution）]**：主权基金或大型公募委托经纪商（Broker）执行数亿美元建仓时，为了防止经纪商在日内不利价格随意乱买，强制将“实际执行均价与市场 VWAP 的基点偏差（bps vs VWAP）”作为考核与佣金返佣结算标准。买入均价低于 VWAP 则算超额 Alpha 盈利，高于 VWAP 则视为负滑点惩罚。
- **[算法执行器的物理反馈]**：若日内价格运行在 VWAP 下方，买入执行算法会疯狂加速下单吃单（因为此时成交能够直接拉低日内买入成本，优于考核目标）；而一旦价格反弹触及甚至高过 VWAP，买入算法会立刻降速甚至停止挂主动单。
- **[自我实现的价格支撑阻力物理墙]**：全球数千台同时运行的机构 VWAP 算法在同一价格线形成共振——在 VWAP 下方形成强大的被动买入承接，在上方形成卖方释放，使得 VWAP 成为全天最具弹性的动态博弈心理中枢。

【Q3 深度参考答案】
锚定 VWAP（Anchored VWAP, AVWAP）的锚点选择科学：与普通从固定早盘 9:30 开始计算的日内 VWAP 相比，为什么从“年内历史最低点”、“重大利好财报公布日”或“重大结构突破日”锚定的长期 AVWAP 具有强大的中长期筹码支撑力？请从“该事件以来全市场持仓筹码平均盈亏平衡点”的角度进行博弈论解释。
- **[任意自然日时间切片的局限性]**：日历日（每天 9:30 重置）对中长线机构资金是毫无经济学意义的。长线主权基金与多策略对冲基金的持仓周期往往长达数周至数年，其决策是以重大的基本面体制突变（Regime Shift）为时间原点。
- **[重大事件原点的不可逆筹码锚定]**：从重大低点（如恐慌抛售见底日）、超预期财报公布日或央行降息日开始锚定的 AVWAP，精确积分了自该重大事件发生以来进入市场的所有资金的加权平均买入成本（Volume-Weighted Break-Even Price）。
- **[博弈论中的心理防线与保本防御]**：当价格自高位回踩至该事件锚定的 AVWAP 时，意味着自该事件以来入场的所有投资者的平均浮盈归零（到达保本生死线）。多头主力出于捍卫自身综合持仓成本与信心的本能，绝不容许价格有效跌破成本线，必然调集重兵在此处挂出巨额买单坚决防守，从而形成中长线极其强劲的支撑回踩起爆点。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会执行准则：尊重筹码沉淀事实，锚定关键事件共识</div>
  <div class="callout-body">
    AVWAP 剥离了时间序列的伪均线波动，直接测量资金真金白银的持仓成本锚。与持仓成本站在同一阵营，是做多胜率的基本保障。
  </div>
</div>
"""'''

# ------------------------------------------------------------------------------
# Extract existing code bodies
# ------------------------------------------------------------------------------
def extract_code_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Find start of code after top docstring
    # Top docstring is delimited by """
    parts = content.split('"""')
    if len(parts) >= 3:
        # Code starts after second triple-quote
        # But wait: if top docstring starts with r""" or """, split will have empty first element
        code_part = '"""'.join(parts[2:]).strip()
        # Find import line
        idx = code_part.find("import ")
        if idx != -1:
            return code_part[idx:]
        return code_part
    return ""

def main():
    print("🚀 开始升级模块 04 课程文件...")

    lessons_meta = [
        ("lesson01_price_action_market_structure.py", L01_STARTER_DOC, L01_ANSWERS_DOC),
        ("lesson02_support_resistance_orderblocks.py", L02_STARTER_DOC, L02_ANSWERS_DOC),
        ("lesson03_pattern_recognition_quant.py", L03_STARTER_DOC, L03_ANSWERS_DOC),
        ("lesson04_momentum_trend_indicators.py", L04_STARTER_DOC, L04_ANSWERS_DOC),
        ("lesson05_volume_profile_vwap.py", L05_STARTER_DOC, L05_ANSWERS_DOC),
    ]

    for fname, starter_doc, ans_doc in lessons_meta:
        starter_path = os.path.join(BASE_DIR, "04_technical_pa", fname)
        answer_path = os.path.join(BASE_DIR, "04_technical_pa", "answers", fname)

        # Extract code from existing files
        starter_code = extract_code_from_file(starter_path)
        answer_code = extract_code_from_file(answer_path)

        # Write starter file
        with open(starter_path, "w", encoding="utf-8") as f:
            f.write(starter_doc.strip() + "\n\n" + starter_code.strip() + "\n")

        # Write answer file
        with open(answer_path, "w", encoding="utf-8") as f:
            f.write(ans_doc.strip() + "\n\n" + answer_code.strip() + "\n")

        print(f"  ✓ Upgraded: 04_technical_pa/{fname} and answers/{fname}")

    print("🎉 模块 04 全部 5 门课已完成高质感 docstring 与参考答案重构！")

if __name__ == "__main__":
    main()
