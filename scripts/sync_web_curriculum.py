#!/usr/bin/env python3
"""
同步更新 web/js/data-curriculum.js 中的模块 04、05、06 全量数据
生成 15 门高质量课程配置：
- m04_l01 ~ m04_l05 (价格行为学)
- m05_l01 ~ m05_l05 (多因子与统计套利)
- m06_l01 ~ m06_l05 (现代投资组合与仓位风控)
"""

import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_svg(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return f"<!-- Missing SVG: {rel_path} -->"

def load_code(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        parts = content.strip().split('"""', 2)
        if len(parts) >= 3:
            return parts[2].strip()
        return content.strip()
    return ""

# ==============================================================================
# MODULE 04 LESSONS
# ==============================================================================
def get_m04_lessons():
    lessons = []
    
    # --- L01 ---
    svg1 = load_svg("04_technical_pa/images/m04_l01_swing_points.svg")
    svg2 = load_svg("04_technical_pa/images/m04_l01_bos_choch_state_machine.svg")
    svg3 = load_svg("04_technical_pa/images/m04_l01_liquidity_sweep_vs_breakout.svg")
    code1 = load_code("04_technical_pa/answers/lesson01_price_action_market_structure.py")
    starter1 = load_code("04_technical_pa/lesson01_price_action_market_structure.py")

    t1 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：价格行为学与流动性守恒</div>
  <div class="callout-body">
    K 线不是随机漫步的连续函数，而是多空在特定流动性池（Liquidity Pools）博弈的离散能量投影。摆动极值点（Swing Points）是买卖双方力量达到极限的物理转折点，凝结了做市商库存成本与散户止损单。
  </div>
</div>

<p>在识别微观市场结构时，必须首先通过滑动窗口确定局部高低点。下图展示了局部摆动极值点在窗口 $k=2$ 约束下的微观判定几何：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.1.1：局部摆动极值点 (Swing High / Swing Low) 双向邻域识别几何结构</span>
    <span class="diagram-tag">SWING-POINTS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[波峰判定规则]</strong>：若 $\text{High}_t > \text{High}_{t \pm j}$ 对所有 $1 \le j \le k$ 均严格成立，则 $t$ 确认为局部波峰 Swing High。</li>
  <li><strong>[波谷判定规则]</strong>：若 $\text{Low}_t < \text{Low}_{t \pm j}$ 对所有 $1 \le j \le k$ 均严格成立，则 $t$ 确认为局部波谷 Swing Low。</li>
  <li><strong>[零前视确权时滞]</strong>：算法必须在 $t+k$ 柱收盘后方可零前视确权 $t$ 时刻的极值，严格杜绝 Lookahead Bias。</li>
</ul>

<p>确认摆动点后，市场结构推进表现为顺势延续 (BOS) 与趋势反转 (CHoCH) 的离散状态转移：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.1.2：市场结构推进状态机：BOS 顺势延续与 CHoCH 趋势反转先兆</span>
    <span class="diagram-tag">BOS-CHOCH-STATE</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[顺势结构突破 BOS]</strong>：多头趋势中收盘价向上有效击穿前关键 Swing High，确认买方侵略性吃单清空了挂单流动性。</li>
  <li><strong>[角色转变先兆 CHoCH]</strong>：多头趋势中收盘价向下跌破前关键 Higher Low，宣告多头结构破裂，状态机转移为潜在熊市。</li>
  <li><strong>[回调二次确认规则]</strong>：CHoCH 发生后严禁市价追单，必须等待价格回踩未成交流动性区并企稳后再行开仓。</li>
</ul>

<p>在判定有效突破时，必须严格区分实体收盘与影线假突破：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.1.3：实体收盘突破 (Valid Breakout) 与影线流动性掠夺 (Liquidity Sweep) 对比</span>
    <span class="diagram-tag">SWEEP-VS-BOS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[有效突破的收盘价锚]</strong>：仅当 K 线实体收盘价稳定越过关键高低点时，才确认挂单供给被彻底吸收。</li>
  <li><strong>[影线扫荡的屠杀本质]</strong>：最高价刺破前高但收盘跌回（Wick Sweep），属于主力利用突破追涨盘完成高位空头派发。</li>
  <li><strong>[风控伪信号过滤网]</strong>：算法必须强制过滤影线假突破，避免将机构诱多诱空误判为趋势突破。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁使用滞后均线金叉死叉作为交易指令！均线在震荡市中带来连续高频的假信号与负期望磨损，微观摆动结构突破能第一时间穿透主力资金意图。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{State}_t = \mathbb{I}(C_t > \text{Last\_SH}) \to \text{BULLISH}, \quad \mathbb{I}(C_t < \text{Last\_HL}) \to \text{BEAR\_CHOCH}</div>
  <div class="math-domain">定义域：C_t > 0, \quad \text{window } k \ge 2, \quad t \ge 2k+1</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m04_l01", "num": "01", "title": "价格行为学与市场结构识别状态机",
        "difficulty": "进阶", "time": "30 分钟", "status": "completed",
        "objectives": [
            "掌握局部摆动极值点 (Swing High/Low) 在无前视时序中的双向邻域数学判别",
            "建立基于 BOS (结构突破) 与 CHoCH (角色转变) 的多状态推进有限状态机",
            "辨析实体收盘有效突破与影线流动性掠夺 (Liquidity Sweep) 的微观订单流机制"
        ],
        "theory": t1.strip(), "code": code1,
        "qa": [
            {"q": "Q1: 滞后均线 vs 实时价格行为：为什么 MA 金叉死叉在震荡市中会导致灾难性连续回撤？",
             "hint": "从低通滤波器的相位延迟与摆动极值点订单流锚定展开分析。",
             "ans": "均线本质是价格的时域低通滤波，存在固有相位时滞。震荡市中均线反复缠绕，金叉常买在波段顶点、死叉常割在波段底，左右挨打；而微观摆动点反映买卖力量耗尽的物理锚点，BOS 突破反映盘口深度真实被击穿，不含任何平滑滤波滞后。"},
            {"q": "Q2: 为什么机构算法严格要求收盘价有效突破，而将影线刺破视为流动性扫荡？",
             "hint": "从收盘价公允均衡权重与主力诱多诱空对手盘机制分析。",
             "ans": "日内极值往往由偶发薄流动性扫单造成，实体收盘价才反映博弈结束时机构资金接受的公允均衡价。若最高价刺破前高但收盘跌回，反映主力利用散户追涨买单和空头止损单作为流动性对手盘趁机派发空单，随后顺势下杀。"},
            {"q": "Q3: 日线处于空头结构而 15 分钟级别出现向上 CHoCH 时，交易员应如何设计交易计划？",
             "hint": "从多时间周期共振与顺大势逆小势分析。",
             "ans": "大周期日线决定战略偏向（Short Only）。将 15 分钟的反弹 CHoCH 视为高价值回调，监控其触及日线关键供需区或 0.618 斐波那契位，等待 15 分钟重新出现向下 Bearish CHoCH 确认反转时进场做空，止损紧贴小级别高点，止盈瞄准日线前低，斩获 1:4 以上盈亏比。"}
        ],
        "exercise": {"starter": starter1}
    })

    # --- L02 ---
    svg1 = load_svg("04_technical_pa/images/m04_l02_order_block_formation.svg")
    svg2 = load_svg("04_technical_pa/images/m04_l02_liquidity_pools_bsl_ssl.svg")
    svg3 = load_svg("04_technical_pa/images/m04_l02_fair_value_gap.svg")
    code2 = load_code("04_technical_pa/answers/lesson02_support_resistance_orderblocks.py")
    starter2 = load_code("04_technical_pa/lesson02_support_resistance_orderblocks.py")

    t2 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：散户止损即机构流动性对手盘</div>
  <div class="callout-body">
    百亿美元级机构建仓的最大瓶颈是市场冲击滑点。机构主力必须在拉升前主动制造破位恐慌或诱多突破，从而在散户集中的止损流动性池中完成大额头寸的无滑点交割。
  </div>
</div>

<p>在爆发性单边位移（Displacement）发生之前，机构逆向吸筹留下的最后相反K线构成订单块。下图展示了看涨订单块的形成与回踩缓解过程：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.2.1：看涨机构订单块 (Bullish Order Block) 形成与未成交流动性回踩吸收</span>
    <span class="diagram-tag">ORDER-BLOCK-OB</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[脉冲位移确认]</strong>：OB 后的单边 K 线必须满足实体扩张 $\text{body}_{t+1} \ge 1.8 \times \text{body}_t$ 且创出新高，确认机构大额主动买盘介入。</li>
  <li><strong>[未成交买单残留]</strong>：OB 阴线区间包含机构未全部成交的限价多单，在价格回调时形成强大引力。</li>
  <li><strong>[缓解与失效状态]</strong>：价格探入 [Bottom, Top] 区间触发缓解（Mitigation）；若收盘价跌破 Bottom，则宣告订单块失效（Invalidation）。</li>
</ul>

<p>市场价格的宏观轨迹是在买方流动性池与卖方流动性池之间循环穿梭：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.2.2：买方流动性池 (BSL) 与卖方流动性池 (SSL) 机构跨周期猎杀路径</span>
    <span class="diagram-tag">LIQUIDITY-POOLS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[BSL 买方流动性聚集]</strong>：前高上方汇集散户突破追多买单与前期空头止损买单。</li>
  <li><strong>[SSL 卖方流动性聚集]</strong>：前低下方汇集散户破位追空卖单与前期多头止损卖单。</li>
  <li><strong>[跨周期钟摆拍卖]</strong>：价格扫荡外部流动性池兑现利润 ➔ 折返内部失衡区补单 ➔ 蓄势发起下一轮单边主推。</li>
</ul>

<p>单边侵略行情中三根 K 线之间的未撮合真空区构成公允价值失衡区：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.2.3：公允价值失衡区 (Fair Value Gap, FVG) 几何拓扑与再平衡机制</span>
    <span class="diagram-tag">FVG-IMBALANCE</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[失衡真空定义]</strong>：K1 高点与 K3 低点之间未发生交叠的空白区间，即 $\text{FVG} = \text{Low}_3 - \text{High}_1 > 0$。</li>
  <li><strong>[双边公允撮合引力]</strong>：失衡区内缺乏双边撮合，价格大概率折返补全该真空区。</li>
  <li><strong>[50% 轴心折让位]</strong>：回踩 FVG 50% 轴心（Consequent Encroachment）是第二高胜率狙击买点。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    跌破订单块最低点（Invalidation）意味着主控机构已撤出防守，原有多头假设被彻底证伪。必须严格执行 1R 止损离场，严禁越跌越买盲目扛单。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{Displacement} = \frac{|C_{t+1} - O_{t+1}|}{|C_t - O_t|} \ge 1.8, \quad \text{FVG} = L_{t+2} - H_t > 0</div>
  <div class="math-domain">定义域：H_t > L_t > 0, \quad \text{Displacement} \in [1.8, +\infty)</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m04_l02", "num": "02", "title": "供需区 (Order Blocks) 与流动性扫荡检测",
        "difficulty": "进阶", "time": "35 分钟", "status": "completed",
        "objectives": [
            "掌握机构订单块 (Bullish/Bearish Order Block) 形成的微观记账原理与位移倍数条件",
            "理解 BSL (买方流动性) 与 SSL (卖方流动性) 作为大额头寸撮合燃料池的循环导航",
            "量化检测公允价值失衡区 (FVG) 及订单块缓解 (Mitigation) 与失效 (Invalidation) 状态"
        ],
        "theory": t2.strip(), "code": code2,
        "qa": [
            {"q": "Q1: 为什么主升浪前最后的一根阴线会留存海量机构未成交买单？",
             "hint": "从大资金建仓冲击成本与回踩平仓解套对冲单角度推导。",
             "ans": "百亿级大资金建仓若直接市价买入会产生巨大自伤滑点，因此必须在拉升前主动下砸制造恐慌以吸收对手盘。该阴线中留有机构自身的做空对冲底仓，主升浪爆发后对冲单浮亏。机构引导价格回踩该区域平掉空头解套，并激活剩余未成交限价多单，引发第二波暴涨。"},
            {"q": "Q2: 为什么价格总是从外在流动性池扫荡至内在失衡区，再发起下一轮主推？",
             "hint": "从做市商商业模式与内外流动性再平衡拍卖分析。",
             "ans": "前高前低的外在流动性（BSL/SSL）汇聚了全市场最密集的被动止损单，扫荡 BSL/SSL 能为机构大单提供最大容量的对手盘完成套现或初次吸筹。掠夺后盘口短期流动性真空，价格在均值回归引力下折返内部 FVG 或未缓解 OB 进行补单再平衡，完成能量蓄积。"},
            {"q": "Q3: 跌破看涨订单块最低点（Invalidation）从微观资金结构看意味着什么？",
             "hint": "从多头底线成本击穿与供给完全主导分析。",
             "ans": "订单块最低点是机构最后入场吸收流动性的绝对底线成本。收盘价跌破该位置，证明主控机构已彻底放弃防守，甚至已在高位出逃。原有多头供给吸收假说完全证伪，卖方流动性将被真空加速穿透，必须无条件执行止损斩仓。"}
        ],
        "exercise": {"starter": starter2}
    })

    # --- L03 ---
    svg1 = load_svg("04_technical_pa/images/m04_l03_head_and_shoulders_anatomy.svg")
    svg2 = load_svg("04_technical_pa/images/m04_l03_double_bottom_spring.svg")
    svg3 = load_svg("04_technical_pa/images/m04_l03_quant_feature_extraction.svg")
    code3 = load_code("04_technical_pa/answers/lesson03_pattern_recognition_quant.py")
    starter3 = load_code("04_technical_pa/lesson03_pattern_recognition_quant.py")

    t3 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：形态是供求天平衰竭的几何投影</div>
  <div class="callout-body">
    形态本身没有预测未来的魔法。优秀的量化交易员将形态解构为严格的极值点拓扑空间（Topological Extremum Space），在颈线突破时入场，止损紧贴右肩，追求非对称的数学正期望。
  </div>
</div>

<p>经典头肩顶/底反映多空三次冲击力量的逐级衰竭。下图展示了头肩形态量化几何拓扑与量度目标位：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.1：经典头肩顶形态 (Head &amp; Shoulders) 几何拓扑与颈线断裂确认</span>
    <span class="diagram-tag">HEAD-SHOULDERS-TOPOLOGY</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[头部深陷度约束]</strong>：头部极值点必须相对双肩均价突出 $\ge 3\%$，确保形态具备清晰的极值中枢。</li>
  <li><strong>[双肩对称性容差]</strong>：左肩与右肩价格差异受控在 $\le 5\%$ 容差内，保障形态几何均衡。</li>
  <li><strong>[量度跌幅目标]</strong>：颈线破位后理论量度目标位为 $P_{\text{target}} = P_{\text{neck}} \pm H$，其中 $H$ 为头至颈线的垂直高度。</li>
</ul>

<p>在双底结构中，次底故意刺破前低（Spring）随后快速收复，展现极强的威科夫弹簧效应：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.2：双底形态 (W-Bottom) 与威科夫弹簧效应 (Spring) 诱空反转结构</span>
    <span class="diagram-tag">WYCKOFF-SPRING</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[初次探底确立基线]</strong>：底 1 形成后反弹确立中枢颈线高点。</li>
  <li><strong>[弹簧刺破假摔]</strong>：底 2 刺破底 1 最低点触发破位止损盘，随即被大单强力承接并收出长下影线。</li>
  <li><strong>[浮筹出清拉升]</strong>：上方抛压被彻底清洗，放量突破颈线时往往走出极具爆发力的单边行情。</li>
</ul>

<p>量化系统必须通过严格的多层容差网实现形态算法的自动提取：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.3.3：形态量化识别算法：局部极值点拓扑抽取与容差约束网</span>
    <span class="diagram-tag">ALGO-EXTRACTION</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[时序极值滤波]</strong>：滑动窗口提取 5 拐点序列 $E = [e_1, e_2, e_3, e_4, e_5]$。</li>
  <li><strong>[几何拓扑校验]</strong>：验证 $e_3$ 为全局极值点，且 $e_2, e_4$ 构成颈线高点。</li>
  <li><strong>[动态容差网过滤]</strong>：过滤颈线倾角过大或双肩严重畸变的无效样本。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁在形态未完成颈线收盘突破前抢跑买入！在右肩形成阶段提前下注，极易掉入下降中继三角形或双底破位下杀的深渊。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{RRR} = \frac{P_{\text{target}} - C_t}{C_t - P_{\text{RS}}} = \frac{(P_{\text{neck}} + H) - C_t}{C_t - P_{\text{RS}}} \ge 1.5</div>
  <div class="math-domain">定义域：P_{\text{Head}} < \min(P_{\text{LS}}, P_{\text{RS}}), \quad C_t \ge P_{\text{neck}}, \quad H = P_{\text{neck}} - P_{\text{Head}}</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m04_l03", "num": "03", "title": "经典价格形态量化识别与几何拓扑",
        "difficulty": "核心", "time": "40 分钟", "status": "completed",
        "objectives": [
            "掌握头肩底 (IHS) 几何拓扑空间中 5 关键拐点的参数化容差约束定义",
            "理解威科夫弹簧效应 (Wyckoff Spring) 诱空假跌破与次底筹码出清机制",
            "实现自动化形态特征提取器并严密计算量度目标位与突破入场盈亏比 (RRR)"
        ],
        "theory": t3.strip(), "code": code3,
        "qa": [
            {"q": "Q1: 头肩形态颈线破位后为什么常引发量度跌幅的非线性雪崩？",
             "hint": "从三次上攻动能递减与颈线密集止损触发分析。",
             "ans": "左肩为强趋势放量；头部虽创微幅新高但量能萎缩（量价背离）；右肩反弹无力创新高，多头彻底力竭。颈线聚集了形态构筑期抄底盘与追多盘的密集止损。一旦跌破，触发三维共振卖盘：多头斩仓市价单、追空算法单、机构撤买单，流动性瞬间失衡引发非线性暴跌。"},
            {"q": "Q2: 为什么双底中次底略微刺穿前低（Spring）反而比未刺穿平底胜率更高？",
             "hint": "从浮筹出清与主力终极吸筹角度展开。",
             "ans": "平底双底未跌破前低，前低下方的散户止损单未被清洗，拉升时易遭遇解套抛压；而次底故意砸破前低，触发卖方止损盘（SSL）涌出，主力利用高流动性瞬间吞下廉价筹码完成终极吸筹（Spring）。浮筹被洗劫一空后，盘口阻力被排空，随后拉升轻盈迅猛。"},
            {"q": "Q3: 为什么机械要求左右肩 0% 误差会导致策略失效，而容差过大又会掉入伪形态陷阱？",
             "hint": "从统计过拟合与假阳性率平衡角度剖析。",
             "ans": "零容差在充满微观噪声的真实市场中样本稀疏（Underfitting），全市场数年可能无一符合；容差放大至 15%~25% 则会将随机锯齿波误判为头肩形态（Overfitting），假阳性率飙升导致胜率暴跌至 35% 以下。工程上应锚定 5%~8% 容差，并结合成交量与动能指标交叉确认。"}
        ],
        "exercise": {"starter": starter3}
    })

    # --- L04 ---
    svg1 = load_svg("04_technical_pa/images/m04_l04_moving_average_lag.svg")
    svg2 = load_svg("04_technical_pa/images/m04_l04_wilder_rsi_momentum.svg")
    svg3 = load_svg("04_technical_pa/images/m04_l04_bollinger_volatility_squeeze.svg")
    code4 = load_code("04_technical_pa/answers/lesson04_momentum_trend_indicators.py")
    starter4 = load_code("04_technical_pa/lesson04_momentum_trend_indicators.py")

    t4 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：低通滤波的时滞代价与波动率聚集</div>
  <div class="callout-body">
    技术指标是历史价格卷积滤波的滞后统计摘要。消除高频噪声必然引入相位延迟（Phase Lag）；而资产收益率的波动率具有强烈的均值回归聚集性，波动率极度压缩预示着单边暴利突破。
  </div>
</div>

<p>均线滤波器本质是时域低通滤波器。下图对比了真实价格突变与 SMA、EMA、零滞后均线的响应时滞：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.4.1：均线滤波器相位时滞比较：真实价格 vs SMA vs EMA vs 零滞后滤波器</span>
    <span class="diagram-tag">FILTER-PHASE-LAG</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[SMA 矩形窗滞后]</strong>：权重均匀分布，对价格阶跃响应存在 $\frac{N-1}{2}$ 周期的物理相位延迟。</li>
  <li><strong>[EMA 指数加权加速]</strong>：近期价格赋予更高权重，有效改善了时滞，但仍无法彻底消除延迟。</li>
  <li><strong>[零滞后滤波代价]</strong>：零滞后算法对高频噪声极度敏感，在震荡市极易发生频繁伪翻转磨损。</li>
</ul>

<p>经典怀尔德 RSI 动量指标在强趋势中会发生高位钝化，顶背离才是最核心的均值回归信号：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.4.2：怀尔德 RSI 动量振荡器、顶背离结构与超买超卖界限</span>
    <span class="diagram-tag">WILDER-RSI</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[怀尔德平滑递推]</strong>：衰减因子 $\alpha = 1/N$，等价于 $2N-1$ 周期的指数移动平均。</li>
  <li><strong>[单边市持续钝化]</strong>：单边暴涨中 RSI 长期钉在 75~90 之间，此时盲目做空必然被逼空打爆。</li>
  <li><strong>[价格与动量顶背离]</strong>：价格创出更高高点而 RSI 创出更低高点，严格证明边际做多动量加速度耗尽。</li>
</ul>

<p>自适应布林带通过滚动方差度量市场熵值，带宽极度挤压预示着大级别行情启动：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.4.3：自适应布林带 (Bollinger Bands) 波动率挤压 (Squeeze) 与暴动突破</span>
    <span class="diagram-tag">VOLATILITY-SQUEEZE</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[带宽指标 BandWidth]</strong>：$\text{BandWidth} = (\text{Upper} - \text{Lower}) / \text{Middle}$，度量相对波动率水平。</li>
  <li><strong>[极度收敛 Squeeze]</strong>：带宽跌入历史后 5% 分位数，表明挂单密集堆积，能量高度压缩。</li>
  <li><strong>[%B 突破顺势跟随]</strong>：价格向上穿透上轨（$\%B > 1.0$）且伴随带宽暴涨，确立高胜率顺势做多。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁使用当日收盘价生成的信号在当日收盘执行撮合！必须强制施加 `.shift(1)` 滞后因果约束，将交易顺延至次日开盘执行，彻底根绝未来函数前视偏差。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{BandWidth} = \frac{4k \sigma_N(C)}{\text{SMA}_N(C)}, \quad \text{Position}_t = \text{Signal}_{t-1}</div>
  <div class="math-domain">定义域：N = 20, \quad k = 2.0, \quad \sigma_N(C) > 0, \quad \text{Position} \in \{-1, 0, 1\}</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m04_l04", "num": "04", "title": "动量指标、自适应布林带与时滞消除",
        "difficulty": "核心", "time": "35 分钟", "status": "completed",
        "objectives": [
            "从时域数字信号滤波角度理解均线相位时滞 (Phase Lag) 的数学守恒",
            "掌握怀尔德平滑 (Wilder Smoothing) RSI 算法、高位钝化机制与动量背离判定",
            "构建基于自适应布林带挤压 (Volatility Squeeze) 与零前视 (Shift-1) 交易信号引擎"
        ],
        "theory": t4.strip(), "code": code4,
        "qa": [
            {"q": "Q1: 为什么在强趋势中 RSI 持续高于 70 做空会导致惨重亏损？背离的物理机制是什么？",
             "hint": "从单边市收盘价单向抬高与动量加速度衰减分析。",
             "ans": "单边大牛市中每日收盘持续抬高，平均亏损趋于零，RSI 长期被钉在 75~90 之间，此时高 RSI 反映强做多动量而非见顶。顶背离（价格破新高而 RSI 见顶回落）从数学上证明虽然价格在冲高，但单位时间内的涨幅加速度正在急剧衰减，结合小级别 CHoCH 破位才是均值回归胜率最高点。"},
            {"q": "Q2: 布林带带宽挤压至极低水平为何预示着单边爆发？如何防范挤压区假突破？",
             "hint": "从波动率聚集与均值回归、实体收盘确认防扫荡分析。",
             "ans": "金融时间序列波动率具有强烈聚集性与均值回归性。带宽压缩至后 5% 分位表明多空高度共识、深度堆积，系统熵减达到临界点，无法容纳新信息，一旦打破平衡必引发单向止损踩踏。防范洗盘法则：严禁在挤压中轨猜方向，必须等待实体收盘确立站上轨外且带宽斜率显著向上时顺势进场。"},
            {"q": "Q3: 为什么当日收盘价生成信号不能在当日收盘撮合？如何用 .shift(1) 彻底杜绝未来函数？",
             "hint": "从物理时间不可逆与因果执行契约推导。",
             "ans": "当日收盘价在交易最后一毫秒才确定，实盘无法在瞬间完成计算、决策与撮合。Same-bar Execution 相当于提前预知未来，回测夏普常虚高至 4.0 以上，实盘上线必然崩盘。`position = signal.shift(1)` 强制将信号滞后到次日执行，保证回测严格服从现实物理因果契约。"}
        ],
        "exercise": {"starter": starter4}
    })

    # --- L05 ---
    svg1 = load_svg("04_technical_pa/images/m04_l05_volume_profile_vpvr.svg")
    svg2 = load_svg("04_technical_pa/images/m04_l05_anchored_vwap_dynamics.svg")
    svg3 = load_svg("04_technical_pa/images/m04_l05_liquidity_distribution_regimes.svg")
    code5 = load_code("04_technical_pa/answers/lesson05_volume_profile_vwap.py")
    starter5 = load_code("04_technical_pa/lesson05_volume_profile_vwap.py")

    t5 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：拍卖市场理论 (AMT) 与真实持仓成本</div>
  <div class="callout-body">
    金融市场是一个双向连续竞价的拍卖场，终极目的在于寻找能够达成最大成交换手的公允价值区（Fair Value Area）。锚定 VWAP 反映自重大事件以来全市场真金白银的加权平均买入成本线。
  </div>
</div>

<p>成交量在价格上的垂直分布刻画了筹码共识中枢。下图展示了 VPVR 直方图、POC 控制点与 70% 价值区：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.1：可见范围成交量分布 (VPVR)：POC 控制点与 70% 价值区 (VAH / VAL)</span>
    <span class="diagram-tag">VOLUME-PROFILE</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[POC 控制点最大共识]</strong>：成交量最高的分箱价位，代表多空博弈最充分的绝对公允锚点。</li>
  <li><strong>[VAH / VAL 70% 价值区]</strong>：从 POC 双向贪婪扩张覆盖 70% 总成交量的上下边界，构成天然供求屏障。</li>
  <li><strong>[LVN 低成交量真空]</strong>：低成交量节点缺乏挂单防御，价格穿透时阻力最小，常发生跳空加速。</li>
</ul>

<p>从重大历史事件锚定的 VWAP 及其动态标准差通道提供不可逆的持仓成本防线：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.2：事件锚定 VWAP (Anchored VWAP) 与动态标准差通道防御模型</span>
    <span class="diagram-tag">ANCHORED-VWAP</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[AVWAP 持仓成本线]</strong>：从财报发布、央行降息或结构突破日锚定，真实度量该事件以来的市场保本线。</li>
  <li><strong>[加权标准差偏离通道]</strong>：基于成交量加权方差计算 $\pm 2\sigma$ 通道，提供均值回归与对冲边界。</li>
  <li><strong>[机构算法被动承接]</strong>：回调至 AVWAP 时，机构被动买入执行算法自动激活，形成极强支撑。</li>
</ul>

<p>筹码形态直观映射主控资金的筹码搬运意图：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.3：市场筹码分布三态：P 型多头冲刺、b 型空头派发与 D 型公允平衡</span>
    <span class="diagram-tag">PROFILE-REGIMES</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[P 型分布 (空头回补)]</strong>：量堆积在高位，底部单薄，空头止损踩踏冲刺，谨防高位接力滞胀。</li>
  <li><strong>[b 型分布 (长线抛售)]</strong>：量堆积在低位，顶部单薄，长线多头出逃但低位有大资金吸筹，静待筑底。</li>
  <li><strong>[D 型分布 (公允均衡)]</strong>：经典高斯对称钟形，POC 居中，多空充分换手，处于箱体震荡。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    当价格有效放量突破价值区（VAH/VAL）时，必须立刻停止震荡市的“高抛低吸均值回归”，顺势切换为突破大单边趋势策略，严防在价值区外逆势扛单爆仓。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{VWAP}_t = \frac{\sum_{s=1}^t P_s V_s}{\sum_{s=1}^t V_s}, \quad \sigma_{\text{vwap}, t} = \sqrt{\frac{\sum V_s (P_s - \text{VWAP}_t)^2}{\sum V_s}}</div>
  <div class="math-domain">定义域：V_s > 0, \quad \text{Value\_Area\_Pct} = 0.70, \quad Z = \frac{P_t - \text{VWAP}_t}{\sigma_{\text{vwap}, t}}</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m04_l05", "num": "05", "title": "成交量分布 (Volume Profile) 与锚定 VWAP",
        "difficulty": "专家", "time": "45 分钟", "status": "completed",
        "objectives": [
            "掌握拍卖市场理论 (AMT) 下基于价格垂直分箱的 70% 价值区 (VAH/VAL) 与 POC 计算",
            "理解机构算法交易对 VWAP 执行基准的被动绑定及其自实现强支撑阻力效应",
            "实现重大事件锚定 VWAP (Anchored VWAP) 与成交量加权动态方差偏离通道策略"
        ],
        "theory": t5.strip(), "code": code5,
        "qa": [
            {"q": "Q1: 为什么拍卖市场理论将 70% 成交量定义为价值区？突破 VAH 为什么会引发暴烈单边？",
             "hint": "从正态分布 1 个标准差统计对应与公允价值再定价展开。",
             "ans": "正态分布中 $[-1\sigma, +1\sigma]$ 包含 68.26%（工程取整 70%）的数据点，代表多空充分竞价认可的公允拍卖中枢。在价值区内交易者习惯高抛低吸；一旦有效突破 VAH，表明市场彻底拒绝低价并发生价值跃迁，原有做空资金集体止损买入，场外趋势资金狂暴追多，形成单边趋势。"},
            {"q": "Q2: 顶级投行机构大单执行算法为何将 VWAP 作为核心考核？如何导致触及 VWAP 的支撑阻力？",
             "hint": "从最佳执行（Best Execution）评价机制与算法执行器的物理反馈分析。",
             "ans": "资管机构委托券商大单建仓时，将成交均价相对 VWAP 的基点偏差作为考核与返佣标准（买价低于 VWAP 算超额，高于则受罚）。若价格低于 VWAP，买入算法加速抢单吃单拉低成本；触及或超过 VWAP 则立刻降速甚至停止挂单。全球数千台算法共振，在 VWAP 形成极具弹性的天然承接墙。"},
            {"q": "Q3: 相比固定 9:30 开始的日内 VWAP，为什么从历史低点或重大财报日锚定的 AVWAP 支撑力极强？",
             "hint": "从该事件以来全市场持仓筹码平均保本线博弈分析。",
             "ans": "日历日切片对长线资金毫无经济学意义。从重大低点或财报公布日锚定的 AVWAP，精确积分了自该重大事件以来进入市场的所有资金的加权平均买入成本（Break-Even Price）。回踩 AVWAP 意味着入场资金平均浮盈归零到达保本生死线，多头主力出于捍卫自身综合成本与信心的本能必调集重兵挂单坚决防守。"}
        ],
        "exercise": {"starter": starter5}
    })

    return lessons

# ==============================================================================
# MODULE 05 LESSONS
# ==============================================================================
def get_m05_lessons():
    lessons = []
    
    # --- L01 ---
    svg1 = load_svg("05_quant_trading/images/m05_l01_factor_evaluation_pipeline.svg")
    svg2 = load_svg("05_quant_trading/images/m05_l01_rank_ic_distribution.svg")
    svg3 = load_svg("05_quant_trading/images/m05_l01_quantile_monotonicity.svg")
    code1 = load_code("05_quant_trading/answers/lesson01_single_factor_testing.py")
    starter1 = load_code("05_quant_trading/lesson01_single_factor_testing.py")

    t1 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：格林诺德基本定律 (Fundamental Law of Active Management)</div>
  <div class="callout-body">
    主动投资的信息比率决定于因子技能与广度的乘积：$\text{IR} \approx \text{IC} \times \sqrt{\text{Breadth}}$。单因子检验是验证特征是否具备独立预测能力的绝对科学基石。
  </div>
</div>

<p>生产级因子预处理必须经过严格去极值、标准化与行业市值中性化：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.1.1：生产级单因子数据清洗与正交预处理流水线 (Factor Pipeline)</span>
    <span class="diagram-tag">FACTOR-PREPROCESSING</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[MAD 稳健去极值]</strong>：基于中位数绝对偏差截断厚尾异常值，破损点高达 50%。</li>
  <li><strong>[截面 Z-Score 标准化]</strong>：消除不同因子之间的量纲差异，保证横截面均值为 0、方差为 1。</li>
  <li><strong>[行业市值中性化 OLS]</strong>：剥离宏观行业与市值 Beta 暴露，提取纯净的选股 Alpha 残差。</li>
</ul>

<p>Rank IC 度量因子预测排名的单调相关度，ICIR 度量稳定性：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.1.2：截面 Rank IC 时序分布与 IR (信息比率) 稳定性检验</span>
    <span class="diagram-tag">RANK-IC-STATS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[Rank IC 秩相关]</strong>：斯皮尔曼秩相关对非线性单调映射与离群点具有极佳鲁棒性。</li>
  <li><strong>[ICIR 稳定性比率]</strong>：年化 $\text{ICIR} > 0.5$ 视为优质因子，t 统计量检验统计显著性。</li>
  <li><strong>[因子半衰期衰减]</strong>：度量预测信号随时间的衰减速度，决定策略调仓换手周期。</li>
</ul>

<p>五分位数分层回测检验收益单调性与多空净值对决：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.1.3：因子五分位数 (Quantiles) 分层回测单调性与多空净值对决</span>
    <span class="diagram-tag">QUANTILE-BACKTEST</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[多空组合收益]</strong>：买入 Q5 卖出 Q1 剥离市场 Beta，检验纯超额收益能力。</li>
  <li><strong>[单调性检验得分]</strong>：收益必须沿 Q1 ➔ Q5 严格单调递增，单调性得分 $> 0.70$。</li>
  <li><strong>[换手磨损控制]</strong>：评估换手率与交易成本冲击，防止纸面富贵。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁使用未经行业与市值中性化的原始因子！未经中性化的因子其收益往往来自被动暴露周期行业或小盘股 Beta，风格反转时将遭遇致命回撤。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{Rank IC} = 1 - \frac{6 \sum d_i^2}{N(N^2 - 1)}, \quad \text{ICIR} = \frac{\bar{\text{IC}}}{\sigma_{\text{IC}}} \sqrt{12}</div>
  <div class="math-domain">定义域：N \ge 30, \quad \text{Rank IC} \in [-1, 1], \quad \sigma_{\text{IC}} > 0</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m05_l01", "num": "01", "title": "单因子检验评价框架与 IC / Rank IC / 分层回测",
        "difficulty": "进阶", "time": "35 分钟", "status": "completed",
        "objectives": [
            "掌握基于中位数绝对偏差 (MAD) 去极值与截面 Z-Score 标准化的稳健数据预处理",
            "理解 Rank IC、IC 均值、IC 标准差与年化 ICIR (信息比率) 的统计假设与评价标准",
            "实现五分位数 (Quantile) 分层回测引擎并计算多空年化超额与单调性得分"
        ],
        "theory": t1.strip(), "code": code1,
        "qa": [
            {"q": "Q1: 为什么机构量化多因子体系几乎只考核 Rank IC 而非 Pearson IC？",
             "hint": "从收益率肥尾分布、离群值扰动与排序单调映射分析。",
             "ans": "Pearson IC 假设正态分布与线性因果，极易被 1~2 只极端异常值个股扭曲；Rank IC 使用次序排名，完全消除离群点干扰，能精准捕获非线性单调关系。多因子选股本质是根据相对强弱排序构建组合，Rank IC 在数学上与实际投资行为完全同构。"},
            {"q": "Q2: 一个估值因子中性化后夏普从 2.5 降至 0.3，说明它原来赚的是什么钱？",
             "hint": "从被动风格暴露与纯 Alpha 提纯视角剖析。",
             "ans": "说明该因子未中性化时高收益 90% 来自周期重资产行业与小盘股的被动 Beta 溢价，而非真正的个股 Alpha。成长股牛市时该因子会遭遇崩盘；中性化剔除外生风格后留下的 0.3 夏普才是纯净、低相关、可全天候复制的真 Alpha。"},
            {"q": "Q3: 分层回测中 Q2 > Q3 收益倒挂意味着什么？能否直接用于线性打分？",
             "hint": "从非线性特征与模型破裂分析。",
             "ans": "说明因子对中间梯队的区分度失效，呈现 U 型或倒 U 型非线性特征。严禁直接代入线性模型加权，否则会导致优化器病态配置。工程上应改用哑变量分段离散化、样条函数转换或 GBDT 树模型非线性学习。"}
        ],
        "exercise": {"starter": starter1}
    })

    # --- L02 ---
    svg1 = load_svg("05_quant_trading/images/m05_l02_fama_french_factor_zoo.svg")
    svg2 = load_svg("05_quant_trading/images/m05_l02_barra_risk_model_matrix.svg")
    svg3 = load_svg("05_quant_trading/images/m05_l02_specific_risk_decomposition.svg")
    code2 = load_code("05_quant_trading/answers/lesson02_fama_french_barra.py")
    starter2 = load_code("05_quant_trading/lesson02_fama_french_barra.py")

    t2 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：APT 无套利定价与多因子风险预算</div>
  <div class="callout-body">
    单因子 CAPM 假定市场只有一个单一 Beta。真实世界的风险是多维的。多因子风险模型的价值在于：让你清楚知道组合赚的每一分钱究竟是在承担哪种具体的风险补偿。
  </div>
</div>

<p>Fama-French 五因子模型将股票收益正交分解为市场、规模、价值、盈利与投资风格溢价：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.2.1：Fama-French 五因子资产定价模型正交分解与 Alpha 剥离</span>
    <span class="diagram-tag">FAMA-FRENCH-5F</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[MKT 市场基准溢价]</strong>：全市场超额回报 $R_m - R_f$，度量系统性市场贝塔。</li>
  <li><strong>[SMB 规模溢价]</strong>：小市值相对大市值的流动性风险补偿。</li>
  <li><strong>[HML 价值溢价]</strong>：高账面市值比相对低账面市值比的困境反转估值补偿。</li>
  <li><strong>[RMW 盈利质量溢价]</strong>：高 ROE/ROIC 健壮组合相对弱质组合的质量溢价。</li>
  <li><strong>[CMA 投资风格溢价]</strong>：保守低资本扩张组合相对激进扩张组合的风格溢价。</li>
</ul>

<p>Barra 结构化风险模型将 5000 维股票协方差降维投影至风格与行业因子：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.2.2：Barra 多因子结构化风险模型矩阵：风格因子与行业暴露拓扑</span>
    <span class="diagram-tag">BARRA-RISK-MATRIX</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[因子暴露矩阵 X]</strong>：$N \times K$ 阶矩阵，包含行业虚拟变量与风格因子标准化暴露。</li>
  <li><strong>[因子协方差 F]</strong>：$K \times K$ 阶紧凑正定矩阵，通过时序加权与自相关调整估计。</li>
  <li><strong>[特异风险对角阵 Δ]</strong>：$N \times N$ 对角阵，极大降低自由度，彻底消除协方差奇异性。</li>
</ul>

<p>投资组合总方差必须精准切分为系统性风险与特异风险：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.2.3：投资组合总风险方差分解：风格系统性风险 vs 股票特异风险</span>
    <span class="diagram-tag">RISK-ATTRIBUTION</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[集中持仓的特异风险裸露]</strong>：仅持股 10 只的组合特异风险 $> 65\%$，高度受制于个股黑天鹅。</li>
  <li><strong>[量化分散组合的系统性纯度]</strong>：持股数百只组合特异风险 $< 15\%$，收益纯由因子 Alpha 驱动。</li>
  <li><strong>[方差分解等式]</strong>：$\sigma_p^2 = w^T X F X^T w + w^T \Delta w$。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    若某基金经理超额收益的 80% 来自小市值（SMB）敞口，投决会应将其定性为伪 Alpha 风格对赌，强制在组合优化器中将风格敞口锁定在 $\pm 0.1\sigma$ 以内。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\Sigma = X_{N \times K} F_{K \times K} X^T_{K \times N} + \Delta_{N \times N}</div>
  <div class="math-domain">定义域：N \gg K \ge 5, \quad \text{Factor\_Risk\_Pct} + \text{Specific\_Risk\_Pct} \equiv 100\%</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m05_l02", "num": "02", "title": "经典 Fama-French 模型与 Barra 结构化风险分解",
        "difficulty": "核心", "time": "40 分钟", "status": "completed",
        "objectives": [
            "掌握 Fama-French 多因子 OLS 正交回归与主动阿尔法 (Alpha) 剥离技术",
            "理解 Barra 结构化模型将高维股票协方差分解为因子协方差与特异风险的降维代数",
            "实现投资组合风格暴露归因与因子系统性风险/特异风险方差完全分解"
        ],
        "theory": t2.strip(), "code": code2,
        "qa": [
            {"q": "Q1: 为什么多因子模型中的系统性因子收益本质是风险补偿而非免费午餐？",
             "hint": "从经济周期恶化时的系统性亏损与套利拥挤度分析。",
             "ans": "小市值股票在流动性危机中面临再融资断裂风险，低估值价值股往往处于困境重组边缘。投资者持有这些资产的超额收益本质是对承担暴雷破产风险的必要风险溢价。套利资金大规模涌入后，因子拥挤度升高，传统溢价会发生长期衰减。"},
            {"q": "Q2: Barra 模型如何将 5000 维协方差从 1250 万个参数压缩至不到 7000 个？",
             "hint": "从因子线性生成元模型与特异风险对角假设推导。",
             "ans": "直接估计样本协方差需要 $N(N+1)/2 \approx 1250$ 万个参数，在长样本不足时严重欠秩且病态。Barra 假设收益由 $K$ 个公共因子驱动，将协方差分解为 $\Sigma = X F X^T + \Delta$。只需估计 $K(K+1)/2$ 个因子协方差与 $N$ 个特异对角方差，总参数量减少 99.94%，保证数值稳定。"},
            {"q": "Q3: 为什么顶级量化对冲基金对 Barra 风格因子敞口施加极窄阈值（< 0.1σ）？",
             "hint": "从 LP 契约、管理费合法性与防范踩踏分析。",
             "ans": "对冲基金收取 2/20 管理费必须提供零 Beta 的纯粹选股 Alpha。若收益来自小盘股敞口，LP 可以直接买低费率小盘 ETF。此外，风格因子在去杠杆时极易发生流动性踩踏。严格约束风格敞口能倒逼经理专注于特异选股能力。"}
        ],
        "exercise": {"starter": starter2}
    })

    # --- L03 ---
    svg1 = load_svg("05_quant_trading/images/m05_l03_cointegration_vs_correlation.svg")
    svg2 = load_svg("05_quant_trading/images/m05_l03_ornstein_uhlenbeck_spread.svg")
    svg3 = load_svg("05_quant_trading/images/m05_l03_pairs_trading_bands.svg")
    code3 = load_code("05_quant_trading/answers/lesson03_statistical_arbitrage_pairs.py")
    starter3 = load_code("05_quant_trading/lesson03_statistical_arbitrage_pairs.py")

    t3 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：统计套利基于产业链协整而非表面相关</div>
  <div class="callout-body">
    统计套利不相信数字巧合。唯有当资产对子之间存在不可分割的产业链勾稽与商业替代关系时，价差的均值回归才具备坚如磐石的物理驱动力。
  </div>
</div>

<p>时间序列必须通过协整检验以剔除伪相关陷阱：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.3.1：伪相关性 (Spurious Correlation) vs 长期协整 (Cointegration) 本质对立</span>
    <span class="diagram-tag">ENGLE-GRANGER-TEST</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[伪相关发散陷阱]</strong>：高相关性资产价差方差随时间线性发散，盲目套利必然穿仓。</li>
  <li><strong>[长期协整平稳]</strong>：线性组合残差 $\epsilon_t = P_A - \beta P_B$ 服从 $I(0)$ 均值平稳过程。</li>
  <li><strong>[Engle-Granger 检验]</strong>：OLS 拟合对冲比率 $\beta$，残差 ADF 检验必须满足 $p < 0.05$。</li>
</ul>

<p>价差随机动态服从 Ornstein-Uhlenbeck (OU) 均值回归连续随机过程：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.3.2：Ornstein-Uhlenbeck (OU) 价差连续均值回归过程与半衰期 (Half-Life)</span>
    <span class="diagram-tag">OU-PROCESS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[OU 微分方程]</strong>：$dx_t = \theta (\mu - x_t) dt + \sigma dW_t$，$\theta$ 为回归速率。</li>
  <li><strong>[半衰期公式]</strong>：$T_{\text{half}} = \ln(2) / \theta$，决定最佳持仓周期。</li>
  <li><strong>[可交易性边界]</strong>：半衰期在 5~20 个交易日为黄金区间；超过 90 天则资金周转效率崩塌。</li>
</ul>

<p>标准化 Z-Score 动态通道与硬止损断路器风控架构：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.3.3：配对交易标准化 Z-Score 动态通道与硬止损熔断风控架构</span>
    <span class="diagram-tag">TRADING-BANDS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[开仓阈值]</strong>：$|Z| \ge 2.0$ 处于统计极端离群区，入场套利。</li>
  <li><strong>[均值止盈]</strong>：$|Z| \le 0.5$ 顺利回归中枢，平仓兑现利润。</li>
  <li><strong>[硬止损断路器]</strong>：$|Z| \ge 3.0$ 触发结构破裂硬止损，严防单边发散。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁在价差突破 3.5 倍标准差时加杠杆抄底补仓！极端脱锚大概率反映底层协整基底发生永久性基本面断裂（如私有化要约、破产重组），必须坚决斩仓。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">Z_t = \frac{\epsilon_t - \mu_\epsilon}{\sigma_\epsilon}, \quad T_{\text{half}} = -\frac{\ln(2) \Delta t}{\ln(1 + b)}</div>
  <div class="math-domain">定义域：\beta > 0, \quad \theta > 0, \quad T_{\text{half}} \in (0, 252], \quad Z \in (-\infty, +\infty)</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m05_l03", "num": "03", "title": "统计套利与配对交易：协整检验与 OU 过程",
        "difficulty": "核心", "time": "45 分钟", "status": "completed",
        "objectives": [
            "掌握单位根过程 I(1) 与残差平稳 I(0) 的 Engle-Granger 两步法协整检验",
            "利用连续时间 Ornstein-Uhlenbeck (OU) 随机微分方程与 AR(1) 估计价差半衰期",
            "构建基于动态滚动 Z-Score 通道与 3-Sigma 结构性断裂硬止损的配对交易系统"
        ],
        "theory": t3.strip(), "code": code3,
        "qa": [
            {"q": "Q1: 为什么相关系数 0.98 的资产在配对套利中依然可能导致严重穿仓？",
             "hint": "从非平稳单位根序列与残差平稳协整检验展开推导。",
             "ans": "两个含时间趋势的非平稳 I(1) 随机游走序列，即便完全无关，直接算皮尔逊相关系数也会呈现 0.9 以上的虚假相关；但其价差残差不平稳，方差随时间线性发散。协整检验要求线性组合残差严格消除单位根服从 I(0) 平稳过程，才有回归均值的向心力。"},
            {"q": "Q2: 为什么价差半衰期高达 120 天的对子对于量化基金而言是不可交易的？",
             "hint": "从资金时间成本与宏观体制漂移分析。",
             "ans": "半衰期 120 天意味着单笔套利建仓到平仓需要 6~12 个月，资金周转率极低，扣除融券利息后年化收益几乎归零；更致命的是在漫长周期中易遭遇宏观体制突变（加息、产业政策转向），历史对冲比率发生漂移导致模型崩溃。"},
            {"q": "Q3: 当价差突破 3.5 倍标准差时，风控手册为何强制要求在此处坚决截断止损？",
             "hint": "从结构性断裂（Structural Break）与微观黑天鹅分析。",
             "ans": "正态分布下突破 3.5 倍标准差概率不足 0.05%，一旦发生大概率说明底层协整基底发生永久性断裂（如标的公司获现金私有化要约、债务违约重组或核心专利被废）。此时已无均值回归可言，加杠杆死扛必招致灭顶之灾，唯有止损能锁定最大损失。"}
        ],
        "exercise": {"starter": starter3}
    })

    # --- L04 ---
    svg1 = load_svg("05_quant_trading/images/m05_l04_purged_walk_forward_cv.svg")
    svg2 = load_svg("05_quant_trading/images/m05_l04_tree_ensemble_feature_importance.svg")
    svg3 = load_svg("05_quant_trading/images/m05_l04_overfitting_backtest_trap.svg")
    code4 = load_code("05_quant_trading/answers/lesson04_ml_factor_combination.py")
    starter4 = load_code("05_quant_trading/lesson04_ml_factor_combination.py")

    t4 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：金融数据与通用机器学习的本质差异</div>
  <div class="callout-body">
    通用机器学习假定样本独立同分布且信噪比极高；而金融数据具有极强非平稳性与低信噪比（< 5%）。盲目套用复杂模型 99% 的概率是在精确拟合历史随机噪声。
  </div>
</div>

<p>金融时序交叉验证必须实施严格的样本重叠清洗与隔离缓冲：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.4.1：金融机器学习 Purged &amp; Embargoed 滚动步进时序交叉验证</span>
    <span class="diagram-tag">PURGED-CV</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[Purging 重叠清洗]</strong>：剔除训练集末尾与测试集前向持有期重叠的样本，根绝未来信息泄露。</li>
  <li><strong>[Embargo 隔离缓冲]</strong>：在测试集后设置冷却期，防范自回归时序记忆渗透。</li>
  <li><strong>[Walk-Forward 步进推进]</strong>：滚动窗口向前演进，严格模拟样本外真实预测。</li>
</ul>

<p>集成树模型能够自动捕获基本面与动量因子的深层非线性交互：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.4.2：梯度提升树 (GBDT / LightGBM) 因子非线性交互与 SHAP 重要度分解</span>
    <span class="diagram-tag">FEATURE-IMPORTANCE</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[条件决策分叉]</strong>：优先以高 ROIC 划分优质子集，再在子集内细分动量与估值。</li>
  <li><strong>[特征增益归一]</strong>：特征重要度严格归一化为 100%，反映边际贡献权重。</li>
  <li><strong>[浅树正则化]</strong>：树深度控制在 3~5 层以内，防止过拟合市场噪声。</li>
</ul>

<p>多重假设检验陷阱与折损夏普比率（DSR）数学防御：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.4.3：量化回测多重检验陷阱与伪发现率 (False Discovery Rate) 衰减律</span>
    <span class="diagram-tag">P-HACKING-DEFENSE</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[虚假夏普膨胀]</strong>：测试 10,000 次随机时序必然能筛选出样本内夏普 $> 3.0$ 的假特征。</li>
  <li><strong>[DSR 惩罚算法]</strong>：显式对试验次数 $N$、收益偏度与超额峰度施加数学惩罚。</li>
  <li><strong>[严刑拷打准入]</strong>：只有通过 DSR > 0.95 且商业逻辑闭环的策略才允许实盘上线。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁使用传统随机 K-Fold 交叉验证！由于标签时间跨度重叠，传统 K-Fold 回测夏普纯属前视泄露制造的废纸，实盘必然遭遇严重滑铁卢。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{DSR} = \Phi\left(\frac{(\text{SR} - \text{SR}^*)\sqrt{T-1}}{\sqrt{1 - \gamma_3 \text{SR} + \frac{\gamma_4 - 1}{4}\text{SR}^2}}\right)</div>
  <div class="math-domain">定义域：N \ge 1, \quad \text{DSR} \in [0, 1], \quad \text{SR}^* = \sqrt{2 \ln N}</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m05_l04", "num": "04", "title": "机器学习多因子组合与非线性特征挖掘",
        "difficulty": "核心", "time": "45 分钟", "status": "completed",
        "objectives": [
            "理解重叠收益标签导致的信息泄漏与 Purged & Embargoed Walk-Forward 交叉验证原理",
            "掌握利用集成树模型 (Random Forest / GBDT) 提取因子非线性交互与特征重要性",
            "学习多重假设检验陷阱、伪发现率 (FDR) 与折损夏普比率 (Deflated Sharpe) 审计"
        ],
        "theory": t4.strip(), "code": code4,
        "qa": [
            {"q": "Q1: 为什么传统随机 K-Fold 在金融时序预测中彻底失效？Purging 机制如何解决？",
             "hint": "从前向持有期标签重叠与时序信息倒流分析。",
             "ans": "金融预测标签是未来多期收益，若随机抽样，时刻 t 被划入测试集而 t+1 划入训练集，训练集包含了未来价格，直接向测试集泄露未来答案。Purging 强制剔除训练集中与测试集时间产生交叠的样本，Embargo 隔离自相关记忆，彻底斩断泄漏。"},
            {"q": "Q2: 相比线性多因子加权，集成树模型在挖掘 Alpha 时的核心优势是什么？",
             "hint": "从递归分叉与条件非线性交互分析。",
             "ans": "线性模型假定因子效用独立且边际恒定；树模型通过递归分叉天然能捕获高阶非线性交互（例如：高研发支出只有在低负债科技龙头身上才是护城河，在亏损垃圾股身上是催命符），且对离群值具有天然鲁棒性。"},
            {"q": "Q3: 为什么尝试 10000 次回测筛选出的夏普 3.0 因子必须经过 DSR 折损惩罚？",
             "hint": "从极值理论期望与多重测试伪发现推导。",
             "ans": "在纯随机高斯噪声中抽样 10000 次，根据极值理论最大夏普期望也会达到 $\sqrt{2\ln(10000)} \approx 4.29$。研究员无脑尝试万次必然能碰出假神级因子。DSR 显式对试验次数 N 与高阶矩施加严厉惩罚，唯有 DSR > 0.95 才能确认具备真实预测力。"}
        ],
        "exercise": {"starter": starter4}
    })

    # --- L05 ---
    svg1 = load_svg("05_quant_trading/images/m05_l05_csmom_vs_tsmom_matrix.svg")
    svg2 = load_svg("05_quant_trading/images/m05_l05_momentum_crash_volatility.svg")
    svg3 = load_svg("05_quant_trading/images/m05_l05_macro_regime_trend_filter.svg")
    code5 = load_code("05_quant_trading/answers/lesson05_momentum_cross_sectional_ts.py")
    starter5 = load_code("05_quant_trading/lesson05_momentum_cross_sectional_ts.py")

    t5 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：动量崩盘的做空期权本质与波动率自适应</div>
  <div class="callout-body">
    动量效应跨百年顽健存在，但伴随着毁灭性的负偏度动量崩盘（Momentum Crash）风险。做空深度跌幅的垃圾股相当于卖出虚值看涨期权；唯有引入大盘体制滤网与目标波动率倒数加权，动量策略才能跨越牛熊。
  </div>
</div>

<p>截面动量（CSMOM）与时间序列动量（TSMOM）在构造与敞口上截然不同：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.5.1：截面动量 (CSMOM) 与时间序列动量 (TSMOM) 机制拓扑对比</span>
    <span class="diagram-tag">MOMENTUM-DUALITY</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[CSMOM 截面相对强弱]</strong>：做多前 20% 赢家、做空后 20% 输家，净敞口美元中性。</li>
  <li><strong>[TSMOM 时序绝对趋势]</strong>：依据资产自身过去 12 个月超额回报决定多空，享有危机 Alpha。</li>
  <li><strong>[危机对冲互补性]</strong>：CSMOM 在慢牛中选股超额显著，TSMOM 在暴跌主跌浪中迅速翻空提供保护。</li>
</ul>

<p>熊市触底反弹期，前期输家组合暴涨轧空引发惨烈的动量崩盘：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.5.2：动量崩盘 (Momentum Crash) 物理机理：熊市触底剧烈反弹期的空头反噬</span>
    <span class="diagram-tag">MOMENTUM-CRASH</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[垃圾股的 Gamma 核爆]</strong>：深跌垃圾股股权实质是深度虚值期权，反弹时涨幅高达 150%~300%。</li>
  <li><strong>[防御赢家股滞涨]</strong>：多头持仓的防御股在反弹初期滞涨，多头微利无法弥补空头翻倍暴亏。</li>
  <li><strong>[空头腿轧空踩踏]</strong>：纯动量组合短时间内净值暴跌 50%~70%，发生惨烈的动量崩盘。</li>
</ul>

<p>宏观大盘均线过滤与目标波动率倒数缩放架构：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 5.5.3：宏观市场体制过滤器与动量策略动态波动率自适应杠杆控制</span>
    <span class="diagram-tag">VOL-TARGETING</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[大盘 200 日线滤网]</strong>：指数位于 200 日线下方时关闭空头腿或直接清仓避险。</li>
  <li><strong>[波动率倒数缩放]</strong>：仓位乘数 $w_t = \min(1.5, \sigma_{\text{target}} / \hat{\sigma}_t)$，波动率上升时主动退防。</li>
  <li><strong>[几何复利修复]</strong>：回撤收窄 30% 以上，夏普比率倍增，彻底消除左尾黑天鹅。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁在高波动熊市底部满杠杆做空输家组合！必须将 12-1M（剔除最近 1 个月反转）与目标波动率缩放作为强制执行的底层风控断路器。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">w_t = \text{Filter}_t \times \min\left(1.5, \frac{\sigma_{\text{target}}}{\hat{\sigma}_{\text{roll}, t}}\right), \quad R_{\text{comp}, t} = w_t \times R_{\text{CSMOM}, t}</div>
  <div class="math-domain">定义域：N \ge 20, \quad \sigma_{\text{target}} = 0.12, \quad \hat{\sigma}_{\text{roll}} > 0</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m05_l05", "num": "05", "title": "截面动量与时间序列动量：崩盘机制与波动率过滤",
        "difficulty": "专家", "time": "50 分钟", "status": "completed",
        "objectives": [
            "掌握截面动量 (CSMOM) 与时间序列动量 (TSMOM) 在构造与风险敞口上的本质对立",
            "剖析动量崩盘 (Momentum Crash) 中做空困境股的隐含虚值看涨期权物理机制",
            "实现结合大盘 200 日线宏观体制滤网与目标波动率倒数缩放 (Vol Targeting) 复合动量引擎"
        ],
        "theory": t5.strip(), "code": code5,
        "qa": [
            {"q": "Q1: 为什么 TSMOM 在历次宏观金融危机中能展现强大的非线性正向对冲收益？",
             "hint": "从绝对趋势跟踪与净敞口灵活翻空分析。",
             "ans": "CSMOM 强制保持美元中性，熊市中多头腿同样遭受暴跌；而 TSMOM 依据资产自身时序绝对趋势决定方向，在系统性熊市初期能够全面翻空大盘、做多避险国债黄金，在漫长主跌浪中空头产生巨额现金流，表现类似长久期免费看跌期权。"},
            {"q": "Q2: 为什么在熊市触底强力反弹阶段，纯动量头寸会遭遇高达 50%~70% 的毁灭性崩盘？",
             "hint": "从困境垃圾股的默顿期权结构与空头轧空推导。",
             "ans": "高负债深跌垃圾股的股权实质是深度虚值看涨期权，在熊市底部 Delta 极小但 Gamma 极高。当央行大放水救市时，垃圾股破产概率骤降，股价瞬间暴涨 200% 以上。动量基金做空该组合承担无上限的负 Gamma 亏损，多头防御股滞涨无法抵消空头轧空，引发动量崩盘。"},
            {"q": "Q3: 为什么目标波动率倒数缩放不仅没有降低长期收益，反而将回撤削减了 40% 以上？",
             "hint": "从波动率聚集提前预警与几何复利方差惩罚推导。",
             "ans": "动量崩盘必然发生在波动率飙升数周之后，波动率聚集提供了提前退防窗口。倒数加权在暴风雨来临时自动把杠杆从 1.0 砍至 0.2，规避了本金腰斩。根据几何复利公式 $g \approx \mu - \frac{1}{2}\sigma^2$，将下行方差压减一半带来的复利增益远超微小机会成本，实现完美的非对称优化。"}
        ],
        "exercise": {"starter": starter5}
    })

    return lessons

# ==============================================================================
# MODULE 06 LESSONS
# ==============================================================================
def get_m06_lessons():
    lessons = []
    
    # --- L01 ---
    svg1 = load_svg("06_risk_portfolio/images/m06_l01_efficient_frontier_cml.svg")
    svg2 = load_svg("06_risk_portfolio/images/m06_l01_quadratic_programming_geometry.svg")
    svg3 = load_svg("06_risk_portfolio/images/m06_l01_error_maximization_instability.svg")
    code1 = load_code("06_risk_portfolio/answers/lesson01_markowitz_mvo.py")
    starter1 = load_code("06_risk_portfolio/lesson01_markowitz_mvo.py")

    t1 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：分散化是全金融市场唯一的免费午餐</div>
  <div class="callout-body">
    只要资产间相关系数 $\rho < 1$，组合方差就必然严格小于单项加权方差之和。通过将低相关或负相关的优质资产有机组合，投资组合能在完全不牺牲预期收益的前提下削减 30%~50% 波动率。
  </div>
</div>

<p>在引入无风险利率后，有效前沿坍缩为资本市场线（CML），切点即为最大夏普组合：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.1.1：马科维茨有效前沿 (Efficient Frontier) 与资本市场线 (CML) 切点模型</span>
    <span class="diagram-tag">MARKOWITZ-MVO</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[可行集双曲线外缘]</strong>：所有合法组合构成的紧凑凸集，最左端顶点为全局最小方差组合（GMV）。</li>
  <li><strong>[有效前沿上支]</strong>：GMV 以上边界，相同波动率下提供严格最高的预期收益率。</li>
  <li><strong>[两基金分离定理]</strong>：所有理性投资者只需配置无风险国债与切点组合 $w^*$，通过借贷杠杆调节风险偏好。</li>
</ul>

<p>在禁止做空约束下，均值-方差优化是严格凸二次规划问题：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.1.2：二次规划 (QP) 求解几何拓扑：凸优化等高椭圆与单纯形约束面</span>
    <span class="diagram-tag">CONVEX-OPTIMIZATION</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[等方差椭圆轮廓线]</strong>：目标函数 $\frac{1}{2} w^T \Sigma w$ 形成以极值点为中心的同心同轴椭球等高线。</li>
  <li><strong>[单纯形约束多胞体]</strong>：$\sum w_i = 1$ 与 $w_i \ge 0$ 构成紧凑有界可行域。</li>
  <li><strong>[KKT 切点条件收敛]</strong>：椭球等高线与单纯形边界相切点即为全局唯一最优数值解。</li>
</ul>

<p>未加约束的 MVO 优化器实质是“误差放大器”，必须防范权重病态翻转：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.1.3：马科维茨“误差放大器”(Error Maximizer) 效应与病态权重翻转</span>
    <span class="diagram-tag">NUMERICAL-INSTABILITY</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[协方差求逆噪声放大]</strong>：解析解 $w^* \propto \Sigma^{-1}(\mu - R_f \mathbf{1})$ 对预期收益输入极其敏感。</li>
  <li><strong>[病态角点极端配置]</strong>：收益率 $0.5\%$ 微小扰动即可引发权重从 50% 暴增至 90% 以上。</li>
  <li><strong>[工程治理解决方案]</strong>：引入 Ledoit-Wolf 协方差收缩或 Black-Litterman 贝叶斯反向均衡收益。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁直接将未经正则化的历史样本平均收益输入 MVO！历史均值充满采样噪声，过度拟合历史赢家资产会在风格切换时遭受毁灭性亏损。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\min_w \frac{1}{2} w^T \Sigma w - q \cdot \mu^T w \quad \text{s.t.} \quad \mathbf{1}^T w = 1, \quad w_i \ge 0</div>
  <div class="math-domain">定义域：\Sigma \succ 0, \quad w \in [0, 1]^N, \quad q \ge 0</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m06_l01", "num": "01", "title": "马科维茨均值-方差理论 (MVO) 与有效前沿求解",
        "difficulty": "进阶", "time": "40 分钟", "status": "completed",
        "objectives": [
            "掌握马科维茨均值-方差凸优化二次规划 (QP) 标准型与两基金分离定理",
            "理解全局最小方差组合 (GMV) 与最大夏普切线组合的解析与数值求解",
            "剖析协方差求逆的误差放大器 (Error Maximizer) 效应与权重病态集中治理"
        ],
        "theory": t1.strip(), "code": code1,
        "qa": [
            {"q": "Q1: 为什么在引入无风险利率后，所有理性投资者的风险资产配置都会收敛到唯一的切点组合？",
             "hint": "从夏普比率几何切线斜率与托宾两基金分离定理推导。",
             "ans": "从无风险利率点向有效前沿引射线，切点处夏普比率达到全局极大，形成资本市场线（CML）。两基金分离定理将决策解耦为客观工程计算（全市场唯一的切点组合）与主观效用匹配（无风险资产与切点组合间的资金分配），CML 上各点夏普均优于单纯风险资产前沿，实现投资者福利最大化。"},
            {"q": "Q2: 为什么理查德·米肖称 MVO 为“误差放大器”？如何通过收缩估计或 BL 模型解耦？",
             "hint": "从协方差求逆对最小特征值的放大与极端权重翻转推导。",
             "ans": "解析解包含 $\Sigma^{-1}$ 运算，本质是对协方差特征值倒数加权，将最小特征值的随机采样噪声放大数百倍；优化器会疯狂满仓收益微幅虚高的资产并做空优质资产。工程上采用 Ledoit-Wolf 向结构化目标收缩抬高特征值下界，或用 Black-Litterman 从市值均衡反向推导超额收益，消除病态翻转。"},
            {"q": "Q3: 施加禁止做空约束（w >= 0）是如何影响有效前沿与理论最大夏普的？",
             "hint": "从单纯形多胞体约束与 KKT 条件分析。",
             "ans": "无约束时仅有单一方程可用拉格朗日求解析解；加入 $w_i \ge 0$ 后变成 N 个不等式约束，必须满足 KKT 互补松弛性，需用二次规划数值求解。卖空限制缩小了解法可行域，剥离了做空垃圾股提供杠杆的能力，使有效前沿向右下方推移，理论最大夏普下降 15%~30%，但杜绝了穿仓风险。"}
        ],
        "exercise": {"starter": starter1}
    })

    # --- L02 ---
    svg1 = load_svg("06_risk_portfolio/images/m06_l02_capital_vs_risk_allocation.svg")
    svg2 = load_svg("06_risk_portfolio/images/m06_l02_equal_risk_contribution_pie.svg")
    svg3 = load_svg("06_risk_portfolio/images/m06_l02_all_weather_economic_matrix.svg")
    code2 = load_code("06_risk_portfolio/answers/lesson02_risk_parity_all_weather.py")
    starter2 = load_code("06_risk_portfolio/lesson02_risk_parity_all_weather.py")

    t2 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：用风险计价资产，而非按资金记账</div>
  <div class="callout-body">
    资本的计价货币会贬值，但真实的风险贡献守恒不变。风险平价打破了名义资金分配的安慰剂假象，将各大类资产的方差边际贡献严格均等化，实现真正的全天候对冲。
  </div>
</div>

<p>传统 60/40 股债配比存在巨大的风险集中陷阱：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.2.1：经典 60/40 股债组合的名义资本配置 vs 真实风险贡献假象</span>
    <span class="diagram-tag">CAPITAL-VS-RISK-TRAP</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[资金名义伪分散]</strong>：表面上配置 60% 股票、40% 国债，看似平衡。</li>
  <li><strong>[风险贡献超 90%]</strong>：由于股票波动率是债券 4.5 倍，股票实际贡献了组合逾 92% 的总方差。</li>
  <li><strong>[危机防守真空]</strong>：股市大跌时债券微薄收益被彻底淹没，组合实质是高波股票多头。</li>
</ul>

<p>等风险贡献（ERC）通过欧拉方差分解强制四大资产绝对风险均等切分：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.2.2：风险平价等风险贡献 (Equal Risk Contribution, ERC) 平衡矩阵</span>
    <span class="diagram-tag">ERC-MECHANICS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[边际风险贡献 MRC]</strong>：$\text{MRC}_i = (\Sigma w)_i / \sigma_p$，度量单位权重微调对总波动的偏导数。</li>
  <li><strong>[绝对风险贡献 TRC]</strong>：$\text{TRC}_i = w_i \times \text{MRC}_i$，总和严格守恒等于组合总波动率。</li>
  <li><strong>[等额风险分配]</strong>：强制约束所有资产 $\text{TRC}_i \equiv \sigma_p / N$，低波债券获更高权重。</li>
</ul>

<p>桥水全天候宏观四象限对冲架构：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.2.3：桥水全天候 (All Weather) 宏观经济环境四象限对冲架构</span>
    <span class="diagram-tag">DALIO-ALL-WEATHER</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[增长超预期]</strong>：股票、大宗商品、高收益信用债繁荣。</li>
  <li><strong>[增长低预期]</strong>：长期名义国债提供降息资本利得缓冲。</li>
  <li><strong>[通胀超预期]</strong>：大宗商品、黄金、通胀保值国债（TIPS）抗通胀对冲。</li>
  <li><strong>[通胀低预期]</strong>：长久期优质债券与成长资产估值修复。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    风险平价高度依赖低波债券端加杠杆。当突发暴力加息且股债相关性由负转正（$\rho > 0$）时，杠杆债券端会发生严重亏损，必须配置动态止损与相关性自适应过滤器。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{TRC}_i = w_i \frac{(\Sigma w)_i}{\sigma_p} = \frac{\sigma_p}{N}, \quad \sum_{i=1}^N \text{TRC}_i \equiv \sigma_p</div>
  <div class="math-domain">定义域：\Sigma \succ 0, \quad w_i > 0, \quad \sum w_i = 1</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m06_l02", "num": "02", "title": "风险平价 (Risk Parity) 模型与全天候资产配置",
        "difficulty": "核心", "time": "45 分钟", "status": "completed",
        "objectives": [
            "掌握欧拉齐次函数定理在投资组合方差分解中的边际风险贡献 (MRC) 推导",
            "理解传统 60/40 组合中 90% 风险由股票独占的资本伪分散陷阱",
            "实现等风险贡献 (ERC) 非线性规划求解器并构建全天候宏观四象限对冲矩阵"
        ],
        "theory": t2.strip(), "code": code2,
        "qa": [
            {"q": "Q1: 为什么 60/40 组合中 40% 资金在债券上，而 90% 以上方差风险被股票独占？",
             "hint": "根据欧拉方差分解定理与方差平方效应推导。",
             "ans": "组合总方差是一阶齐次函数，欧拉展开为 $\sum w_i \text{MRC}_i$。股票波动率约 18%，债券约 4%，因方差平方效应，股票方差贡献达 $(0.6)^2 (0.18)^2 \approx 0.01166$，债券仅 $(0.4)^2 (0.04)^2 \approx 0.000256$。股票占总方差近 98%，债券防守在数量级上被彻底淹没。"},
            {"q": "Q2: 为什么 2022 年全球央行暴力加息导致风险平价基金遭遇惨烈回撤？",
             "hint": "从低波债券加杠杆与股债负相关性假说破灭分析。",
             "ans": "未加杠杆的风险平价债券比重大收益过低，必须对债券端加 2~3 倍杠杆。过去 30 年策略依赖股债天然负相关；2022 年 40 年未遇的通胀迫使美联储连续加息 75bps，股债相关性逆转为强正相关（+0.6），重仓且加了杠杆的债券端发生雪崩，未能对冲反而放大亏损。"},
            {"q": "Q3: 为什么商品、黄金与 TIPS 是传统股债组合抵御“滞胀”不可或缺的对冲基石？",
             "hint": "从宏观四象限定价与滞胀期名义股债双杀推导。",
             "ans": "传统 60/40 仅覆盖增长超预期与通胀低于预期，在增长下行且通胀高企的滞胀象限完全裸奔（经济下行杀股票，贴现率上升杀债券）。商品是通胀源头直接涨价产生现金流，TIPS 本金与 CPI 挂钩消除贴现侵蚀，黄金提供主权信用对冲，补全了唯一的防守死角。"}
        ],
        "exercise": {"starter": starter2}
    })

    # --- L03 ---
    svg1 = load_svg("06_risk_portfolio/images/m06_l03_log_utility_growth_curve.svg")
    svg2 = load_svg("06_risk_portfolio/images/m06_l03_risk_of_ruin_simulation.svg")
    svg3 = load_svg("06_risk_portfolio/images/m06_l03_multi_asset_continuous_kelly.svg")
    code3 = load_code("06_risk_portfolio/answers/lesson03_kelly_criterion_ruin.py")
    starter3 = load_code("06_risk_portfolio/lesson03_kelly_criterion_ruin.py")

    t3 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：几何平均复利才是财富积累的唯一真理</div>
  <div class="callout-body">
    单次博弈算术平均收益只是无知的统计幻觉，连续投资的复利本质是几何平均乘积：$W_T = W_0 \prod (1 + R_t)$。只要中途遭遇一次 $-100\%$ 穿仓，后续乘上多大数字最终也是 0。
  </div>
</div>

<p>香农对数效用下的复合几何增长率曲线呈现倒 U 型抛物线：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.3.1：对数效用几何财富增长率曲线：全凯利 (Full Kelly) 峰值与半凯利安全边际</span>
    <span class="diagram-tag">KELLY-LOG-UTILITY</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[Full Kelly 全凯利峰值]</strong>：最佳下注比例 $f^* = (pb - q)/b$，最大化长期复利增长率。</li>
  <li><strong>[Half Kelly 黄金法则]</strong>：采用 $0.5 f^*$ 仓位下注，收获 $75\%$ 全凯利增长，同时方差暴跌 $50\%$。</li>
  <li><strong>[必然破产区 ($f > 2f^*$)]</strong>：当下注超过 2 倍最佳比例，期望几何增长率转为负数，长期持有 100% 破产。</li>
</ul>

<p>过度杠杆在蒙特卡洛模拟中引发财富崩塌与破产概率指数级爆炸：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.3.2：过度杠杆下几何平均增长率崩塌与破产概率 (Risk of Ruin) 爆炸</span>
    <span class="diagram-tag">RUIN-PROBABILITY</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[半凯利平稳复利]</strong>：净值平滑稳健指数上行，破产率严格受控在 $0.0\%$。</li>
  <li><strong>[全凯利巨震承受]</strong>：中位数财富可观，但经常面临回撤 $> 50\%$ 的精神折磨。</li>
  <li><strong>[2.5x 杠杆破产归零]</strong>：负复利惩罚爆发（跌 50% 需涨 100% 回本），破产率骤升 $> 15\%$。</li>
</ul>

<p>连续时间多资产凯利最优杠杆向量拓扑：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.3.3：连续时间多资产凯利最优杠杆向量 f* = Σ^-1 (μ - r) 拓扑结构</span>
    <span class="diagram-tag">CONTINUOUS-KELLY</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[超额收益驱动项]</strong>：$\mu - r$，线性放大最优配置杠杆。</li>
  <li><strong>[协方差矩阵惩罚]</strong>：$\Sigma^{-1}$，进行波动率平方惩罚与跨资产相关性对冲。</li>
  <li><strong>[总名义杠杆物理边界]</strong>：必须施加 $L_1$ 范数硬约束：$\|f^*\|_1 \le \text{Max\_Leverage}$。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁使用全凯利杠杆进行实盘配置！由于胜率 $p$ 和盈亏比 $b$ 的估计充满乐观偏差，使用全凯利极易误入 $f > 2f^*$ 破产区。实盘只允许采用 0.3x ~ 0.5x 凯利下注。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">f^* = \frac{p(b+1) - 1}{b}, \quad \mathbf{f}^* = \Sigma^{-1} (\mu - r \mathbf{1}), \quad g(f) = r + f(\mu - r) - \frac{1}{2} f^2 \sigma^2</div>
  <div class="math-domain">定义域：p \in [0, 1], \quad b > 0, \quad \Sigma \succ 0, \quad f \in [0, 2f^*]</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m06_l03", "num": "03", "title": "凯利公式数学推导、破产风险与动态杠杆",
        "difficulty": "核心", "time": "45 分钟", "status": "completed",
        "objectives": [
            "推导伯努利对数效用最大化下的离散凯利公式与连续几何布朗运动增长率曲线",
            "理解过度杠杆导致几何复合增长率崩塌与破产概率 (Risk of Ruin) 指数爆炸机制",
            "求解多资产连续凯利杠杆向量并应用半凯利 (Half Kelly) 工程安全边际"
        ],
        "theory": t3.strip(), "code": code3,
        "qa": [
            {"q": "Q1: 胜率 50%、盈 60%、亏 40% 的单期算术期望达 +10% 博弈，满仓为何必破产？",
             "hint": "从几何平均收益率公式与大数定律连续复利推导。",
             "ans": "单期算术期望虽为 +10%，但每次满仓下注，经历一盈一亏后的财富乘数为 $(1+0.6)(1-0.4) = 0.96$（净亏 4%）。复合单期几何增长率为 $\sqrt{0.96}-1 \approx -2.02\%$。大数定律下 $2N$ 次博弈后财富按 $(0.96)^N$ 指数衰减至零。算术平均忽略了亏损的非对称惩罚，几何平均才是复利真相。"},
            {"q": "Q2: 为什么文艺复兴等顶级对冲基金在实盘中普遍将仓位硬性压缩至半凯利甚至更低？",
             "hint": "从全凯利回撤深度与泰勒展开方差大幅削减推导。",
             "ans": "全凯利在财富翻倍前遭遇回撤超 50% 概率高达 33.3%，没人能承受 80% 回撤不崩溃。泰勒展开表明，半凯利 $0.5f^*$ 能保留 75% 理论增长率，而方差波动直接砍掉 75%！此外，实盘中胜率和盈亏比估计存在向上偏差，全凯利极易踩入 $f > 2f^*$ 破产区，半凯利提供了巨大的安全缓冲区。"},
            {"q": "Q3: 连续时间多资产凯利向量在估计协方差失真时，为何会导致多资产交叉爆仓？",
             "hint": "从协方差求逆对低估相关性的交叉杠杆放大推导。",
             "ans": "多资产凯利公式等价于风险厌恶系数 $\lambda=1$ 的 MVO。若低估了资产间尾部相关性，$\Sigma^{-1}$ 会误以为资产具备极强对冲能力，输出极高的多空对冲杠杆（如多 400%、空 300%）。危机来临时所有资产相关性瞬间收敛为 1，对冲假象破灭，数倍总杠杆瞬间引爆强制平仓踩踏穿仓。"}
        ],
        "exercise": {"starter": starter3}
    })

    # --- L04 ---
    svg1 = load_svg("06_risk_portfolio/images/m06_l04_var_vs_cvar_tail_distribution.svg")
    svg2 = load_svg("06_risk_portfolio/images/m06_l04_drawdown_high_water_mark.svg")
    svg3 = load_svg("06_risk_portfolio/images/m06_l04_circuit_breaker_sentinel_states.svg")
    code4 = load_code("06_risk_portfolio/answers/lesson04_var_cvar_risk_measures.py")
    starter4 = load_code("06_risk_portfolio/lesson04_var_cvar_risk_measures.py")

    t4 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：一致性风险度量与资本保全的绝对性</div>
  <div class="callout-body">
    收益率决定基金飞多高，回撤控制决定基金活多久。波动率无法刻画极端左尾风险。CVaR 满足次可加性公理，而动态回撤熔断哨兵是防穿仓的最后一道自动化物理保险丝。
  </div>
</div>

<p>正态高斯假设在金融肥尾危机面前彻底失效：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.4.1：正态分布 vs 真实厚尾分布：VaR 阈值盲区与 CVaR 条件期望尾部损失</span>
    <span class="diagram-tag">VAR-VS-CVAR-TAILS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[VaR 的黑天鹅盲区]</strong>：仅给出分位数门槛，对击穿门槛后的灾难深浅完全失明。</li>
  <li><strong>[CVaR 条件期望积分]</strong>：严格积分击穿 VaR 后的条件期望损失，保留所有长厚尾冲击。</li>
  <li><strong>[巴塞尔协议 III 变革]</strong>：全面强制以 97.5% CVaR 取代 99% VaR 作为资本准备金计提底座。</li>
</ul>

<p>动态历史最高水位线（HWM）与水下回撤（Underwater）深度图谱：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.4.2：动态历史最高水位线 (HWM) 与水下回撤 (Underwater Chart) 深度刻画</span>
    <span class="diagram-tag">HIGH-WATER-MARK</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[最高水位线 HWM]</strong>：$H_t = \max_{s \le t} W_s$，单调递增阶梯式推进。</li>
  <li><strong>[动态回撤率 DD]</strong>：$\text{DD}_t = (W_t - H_t) / H_t \le 0$，直观反映实际被套深度。</li>
  <li><strong>[水下时间耐受度]</strong>：回撤持续时间长短直接决定机构 LP 的资金赎回压力。</li>
</ul>

<p>阶梯式动态回撤风控哨兵状态转移模型：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.4.3：阶梯式动态回撤风控哨兵状态转移模型 (Drawdown Sentinel State Machine)</span>
    <span class="diagram-tag">SENTINEL-CIRCUITS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[正常运行态 (Normal)]</strong>：$\text{DD} > -5\%$，仓位乘数 $M = 1.0$，策略全速运转。</li>
  <li><strong>[一级预警降仓 (Warning)]</strong>：$-10\% < \text{DD} \le -5\%$，仓位强制压缩至 $M = 0.5$ 削减方差。</li>
  <li><strong>[二级硬熔断冷冻 (Halted)]</strong>：$\text{DD} \le -10\%$，仓位强制清零 $M = 0.0$，全现金等待投决会复盘。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    风控决策必须严格执行 $T-1$ 滞后！严禁用当日包含盘中未结价格的高水位直接作为当日收盘风控判决，彻底杜绝日内前视偏差作弊。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{CVaR}_\alpha = -\frac{1}{\alpha} \int_0^\alpha Q_p(R) dp, \quad \text{DD}_t = \frac{W_t - \max_{s \le t} W_s}{\max_{s \le t} W_s}</div>
  <div class="math-domain">定义域：\alpha = 0.05, \quad \text{Warning\_DD} = -0.05, \quad \text{Circuit\_Breaker\_DD} = -0.10</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m06_l04", "num": "04", "title": "风险价值 (VaR)、CVaR 与动态回撤熔断控制",
        "difficulty": "核心", "time": "45 分钟", "status": "completed",
        "objectives": [
            "掌握高斯正态假定下参数法与经验分布历史模拟法单期 VaR/CVaR 计算",
            "理解 VaR 次可加性 (Sub-additivity) 失效反例与巴塞尔协议 III 强制切换 CVaR 的必然性",
            "实现基于历史最高水位线 (HWM) 与零前视偏差阶梯式动态回撤熔断风控哨兵"
        ],
        "theory": t4.strip(), "code": code4,
        "qa": [
            {"q": "Q1: 为什么 VaR 违反次可加性公理？巴塞尔 III 为什么强制采用 CVaR？",
             "hint": "从巨灾债券期权空头反例与尾部损失条件期望推导。",
             "ans": "VaR 仅度量分位数切片。两个独立违约概率各 4% 的巨灾债券组合，95% VaR 均为 0；合并后组合违约率跃升至 7.84% > 5%，95% VaR 变为 5000 万，出现合并风险大于两项之和的荒谬悖论。CVaR 度量击穿门槛后的条件期望损失，满足凸性与次可加性，全面覆盖黑天鹅灾难。"},
            {"q": "Q2: 参数法正态 VaR 在 2008 和 2020 危机中为什么会出现系统性瞬间穿仓？",
             "hint": "从高斯超指数衰减与真实金融市场幂律帕累托厚尾对比分析。",
             "ans": "正态分布密度超指数极速衰减，偏离 6 个标准差事件理论概率为数百万年一次。而真实金融市场服从长厚尾幂律分布，极端暴跌概率高出数万倍。雷曼等投行依赖正态 VaR 提取准备金，在 2008 年连续遭遇数万年一遇的 6-8 Sigma 暴跌时，准备金瞬间击穿破产。"},
            {"q": "Q3: 为什么阶梯式风控哨兵必须严格滞后 1 期（Shift-1）执行？",
             "hint": "从非线性负复利伤害与实盘物理因果契约推导。",
             "ans": "回撤对复利伤害非线性（跌 50% 需涨 100% 回本）。回撤 -5% 说明模型短期失配，砍半仓位可将方差削减 50% 缓冲；跌破 -10% 则强制全现金冷冻锁定最大亏损。若在 t 日盘中用包含 t 日收盘价的 HWM 计算风控，在实盘不可行；T-1 决策 T 日执行保证了回测因果绝对真实。"}
        ],
        "exercise": {"starter": starter4}
    })

    # --- L05 ---
    svg1 = load_svg("06_risk_portfolio/images/m06_l05_barbell_allocation_architecture.svg")
    svg2 = load_svg("06_risk_portfolio/images/m06_l05_higher_moments_skew_kurt.svg")
    svg3 = load_svg("06_risk_portfolio/images/m06_l05_convexity_payoff_asymmetry.svg")
    code5 = load_code("06_risk_portfolio/answers/lesson05_tail_risk_black_swan.py")
    starter5 = load_code("06_risk_portfolio/lesson05_tail_risk_black_swan.py")

    t5 = """
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：凸性（Convexity）是不确定性世界中的唯一盟友</div>
  <div class="callout-body">
    根据琴生不等式，对于正向凸性收益结构 $\mathbb{E}[f(x)] \ge f(\mathbb{E}[x])$，世界的不确定性与波动率越大，最终期望回报反而越高。反脆弱的核心就是彻底拥抱凸性、成为波动率的朋友。
  </div>
</div>

<p>塔勒布反脆弱杠铃策略彻底否定中间平庸资产，构建双极端配置：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.5.1：塔勒布反脆弱杠铃 (Antifragile Barbell) 顶层资产配置架构</span>
    <span class="diagram-tag">TALEB-BARBELL</span>
  </div>
  <div class="diagram-svg-container">
    __SVG1__
  </div>
</div>

<ul class="label-list">
  <li><strong>[极端保守底座 (85%~90%)]</strong>：配置零违约风险的超短国债与现金，硬性将最大潜在损失锁死在 10% 以内。</li>
  <li><strong>[中间平庸资产 0%]</strong>：抛弃垃圾债等伪稳健资产，消除危机中流动性踩踏假象。</li>
  <li><strong>[极端进取凸性端 (10%~15%)]</strong>：配置深度虚值看跌期权，享有无限上行与正向黑天鹅暴击。</li>
</ul>

<p>收益率分布高阶统计矩：负偏度陷阱 vs 正偏度反脆弱：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.5.2：高阶统计矩：偏度 (Skewness) 与超额峰度 (Excess Kurtosis) 非对称图谱</span>
    <span class="diagram-tag">HIGHER-MOMENTS</span>
  </div>
  <div class="diagram-svg-container">
    __SVG2__
  </div>
</div>

<ul class="label-list">
  <li><strong>[负偏度 (压路机前捡硬币)]</strong>：平时稳定小赚，左侧拖着长厚尾，一旦暴雷瞬间穿仓。</li>
  <li><strong>[正偏度 (反脆弱长右尾)]</strong>：平时微损保费，右侧拥有极高爆发厚尾，享受危机红利。</li>
  <li><strong>[超额峰度 (Excess Kurtosis)]</strong>：金融资产收益率通常呈现高尖峰厚尾（Kurt > 6.0）。</li>
</ul>

<p>非对称凸性回报剖面：常态 Theta 磨损 vs 危机 Gamma 暴击：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.5.3：非对称凸性回报剖面：常态 Theta 磨损 vs 极端危机 Gamma / Vega 暴击</span>
    <span class="diagram-tag">CONVEXITY-PAYOFF</span>
  </div>
  <div class="diagram-svg-container">
    __SVG3__
  </div>
</div>

<ul class="label-list">
  <li><strong>[常态平稳期]</strong>：仅承受确定性微弱权利金耗损（-Theta），国债利息足以完全覆盖。</li>
  <li><strong>[危机爆发期]</strong>：Gamma 爆发叠加 VIX 暴涨（+Vega），期权产生 50~100 倍非线性利润。</li>
  <li><strong>[流动性救赎]</strong>：在全市场地板价兑现期权暴利，从容大肆扫货优质核心资产。</li>
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁被高胜率策略（Win Rate > 95%）蒙蔽！卖出虚值期权维持连续数年不回撤的基金，实质是在借取未来的尾部自杀贷款，投决会必须强制审查其超额峰度与偏度。
  </div>
</div>

<div class="math-block">
  <div class="math-formula">\text{Kurt} = \frac{\frac{1}{N}\sum (R_i - \bar{R})^4}{\sigma^4} - 3.0, \quad \text{Barbell} = 0.90 \times \text{Cash} + 0.10 \times \text{Convex\_OTM}</div>
  <div class="math-domain">定义域：\sigma > 0, \quad \text{Kurt} \in [-3, +\infty), \quad \text{Normal Distribution} \equiv 0.0</div>
</div>
""".replace("__SVG1__", svg1).replace("__SVG2__", svg2).replace("__SVG3__", svg3)

    lessons.append({
        "id": "m06_l05", "num": "05", "title": "尾部风险度量与反脆弱杠铃配置",
        "difficulty": "专家", "time": "45 分钟", "status": "completed",
        "objectives": [
            "掌握收益率高阶统计矩偏度 (Skewness) 与超额峰度 (Excess Kurtosis) 的计算与尾部含义",
            "理解塔勒布反脆弱杠铃策略对中间派伪平庸资产的彻底否定与极端双极构建哲学",
            "剖析尾部对冲基金 (Tail Risk Funds) 承担有限 Theta 磨损以博取危机 50 倍 Gamma 凸性机制"
        ],
        "theory": t5.strip(), "code": code5,
        "qa": [
            {"q": "Q1: 为什么反脆弱杠铃策略的抗脆弱性远高于持有 100% 中等风险资产？",
             "hint": "从中间资产危机时流动性踩踏与杠铃极端保守端生存权锁定推导。",
             "ans": "中间资产（低评级债、混合基金）在平稳期看似稳健，危机时流动性断裂跌幅与股票一致，剥夺生存权；杠铃策略将 90% 锁死在超短国债，物理锁定最大下行损失不超过 10%，永远保有生存权；剩余 10% 凸性衍生品在百年一遇危机中爆发 30-50 倍暴利，赋予在全市场血流成河时从容抄底的特许权。"},
            {"q": "Q2: 为什么单纯看夏普比率高达 3.0 的策略往往是潜伏的巨型炸弹？如何穿透识别？",
             "hint": "从卖出虚值期权负偏度与巨大超额峰度指纹剖析。",
             "ans": "夏普比率仅看均值和方差，默认假定对称分布。卖出深度虚值期权平时每月稳定赚权利金，净值走完美直线（夏普达 3.0-4.0）；但其高阶矩具有极端负偏度（<-2.5）和巨大超额峰度（>20）。一旦发生 1% 黑天鹅，单次 Gamma 亏损直接抹平数年利润并穿仓倒欠。必须将高阶矩作为一票否决指标。"},
            {"q": "Q3: 尾部对冲基金（如 Universa）平时每年亏保费，在危机中如何反哺母基金？",
             "hint": "从深度虚值期权 Gamma 和 Vega 双重暴击与地板价再平衡分析。",
             "ans": "深度虚值 Put 平时耗损有限 Theta（每年 1-2% 保费）；危机闪崩时标的跌破行权价，内涵价值暴增（Gamma 效应）叠加 VIX 飙升（Vega 效应），期权暴涨 30~80 倍。以 3.3% 仓位单月暴赚 3600% 完全对冲母基金股票暴跌，更重要的是在全市场爆仓践踏时提供充沛现金，在地板价扫货优质核心资产。"}
        ],
        "exercise": {"starter": starter5}
    })

    return lessons

def main():
    print("🚀 开始全量同步 web/js/data-curriculum.js...")
    js_path = os.path.join(BASE_DIR, "web", "js", "data-curriculum.js")
    
    m04_lessons = get_m04_lessons()
    m05_lessons = get_m05_lessons()
    m06_lessons = get_m06_lessons()

    print(f"  ✓ 模块 04 生成 {len(m04_lessons)} 门课程")
    print(f"  ✓ 模块 05 生成 {len(m05_lessons)} 门课程")
    print(f"  ✓ 模块 06 生成 {len(m06_lessons)} 门课程")

    temp_data = {
        "m04": m04_lessons,
        "m05": m05_lessons,
        "m06": m06_lessons
    }
    temp_json_path = os.path.join(BASE_DIR, "scripts", "temp_m04_m05_m06.json")
    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(temp_data, f, ensure_ascii=False)

    node_script = """
const fs = require('fs');
const path = require('path');

const jsPath = path.resolve('web/js/data-curriculum.js');
let code = fs.readFileSync(jsPath, 'utf8');
code = code.replace('const CURRICULUM_DATA =', 'global.CURRICULUM_DATA =');
eval(code);

const updateData = JSON.parse(fs.readFileSync('scripts/temp_m04_m05_m06.json', 'utf8'));

// Update m04
const m04 = global.CURRICULUM_DATA.find(m => m.id === 'm04');
if (m04) {
    m04.lessons = updateData.m04;
    m04.lessons_count = 5;
    m04.title = '价格行为学与技术分析';
    console.log('✓ Updated m04 with 5 lessons');
}

// Update m05
const m05 = global.CURRICULUM_DATA.find(m => m.id === 'm05');
if (m05) {
    m05.lessons = updateData.m05;
    m05.lessons_count = 5;
    m05.title = '量化多因子与统计套利';
    console.log('✓ Updated m05 with 5 lessons');
}

// Update m06
const m06 = global.CURRICULUM_DATA.find(m => m.id === 'm06');
if (m06) {
    m06.lessons = updateData.m06;
    m06.lessons_count = 5;
    m06.title = '现代投资组合与仓位风控';
    console.log('✓ Updated m06 with 5 lessons');
}

// Write back
const newCode = `/**
 * StockLearning Curriculum Database
 * 10 Modules, Comprehensive syllabus, institutional formulas, production code, Q&A, and interactive exercises
 */

const CURRICULUM_DATA = ${JSON.stringify(global.CURRICULUM_DATA, null, 2)};
`;

fs.writeFileSync(jsPath, newCode, 'utf8');
console.log('🎉 Successfully saved web/js/data-curriculum.js with all updated lessons!');
"""
    with open(os.path.join(BASE_DIR, "scripts", "apply_update_curriculum.js"), "w", encoding="utf-8") as f:
        f.write(node_script)

    os.system(f"node {os.path.join(BASE_DIR, 'scripts', 'apply_update_curriculum.js')}")

if __name__ == "__main__":
    main()
