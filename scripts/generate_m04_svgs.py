#!/usr/bin/env python3
"""
生成模块 04 配套高质感 Anthropic 风格 SVG 矢量图
低饱和度配色：
- 背景: #FAF8F5, 边框: #E5DFD5
- 主色墨黑: #1F1E1B, 次色: #7D786F
- 陶土褐: #CC5A36, 冷杉绿: #5F7355, 灰钴蓝: #486A7D, 赭石金: #C08535
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SVGS = {}

# -----------------------------------------------------------------------------
# Lesson 01
# -----------------------------------------------------------------------------
SVGS["m04_l01_swing_points"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.1.1：局部摆动极值点 (Swing High / Swing Low) 双向邻域识别几何结构</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">WINDOW k=2</text>
  
  <line x1="50" y1="210" x2="710" y2="210" stroke="#E5DFD5" stroke-width="1"/>
  <line x1="50" y1="130" x2="710" y2="130" stroke="#E5DFD5" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="50" y1="60" x2="710" y2="60" stroke="#E5DFD5" stroke-width="1" stroke-dasharray="3 3"/>
  
  <!-- Swing Low Point (Valley) Left -->
  <g transform="translate(130, 95)">
    <line x1="20" y1="15" x2="20" y2="75" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="14" y="25" width="12" height="40" fill="#CC5A36" stroke="#CC5A36"/>
    <text x="20" y="90" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t-2</text>

    <line x1="60" y1="30" x2="60" y2="90" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="54" y="40" width="12" height="40" fill="#CC5A36" stroke="#CC5A36"/>
    <text x="60" y="105" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t-1</text>

    <!-- Swing Low Center -->
    <line x1="100" y1="45" x2="100" y2="110" stroke="#1F1E1B" stroke-width="2"/>
    <rect x="94" y="55" width="12" height="40" fill="#FAF8F5" stroke="#5F7355" stroke-width="2"/>
    <circle cx="100" cy="110" r="4" fill="#5F7355"/>
    <text x="100" y="128" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">Swing Low [t]</text>
    <text x="100" y="142" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">Low[t] &lt; Low[t±1, t±2]</text>

    <line x1="140" y1="25" x2="140" y2="85" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="134" y="30" width="12" height="40" fill="#5F7355" stroke="#5F7355"/>
    <text x="140" y="100" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t+1</text>

    <line x1="180" y1="10" x2="180" y2="70" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="174" y="15" width="12" height="40" fill="#5F7355" stroke="#5F7355"/>
    <text x="180" y="85" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t+2</text>
  </g>

  <!-- Swing High Point (Peak) Right -->
  <g transform="translate(420, 35)">
    <line x1="20" y1="60" x2="20" y2="120" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="14" y="70" width="12" height="40" fill="#5F7355" stroke="#5F7355"/>
    <text x="20" y="135" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t-2</text>

    <line x1="60" y1="45" x2="60" y2="105" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="54" y="55" width="12" height="40" fill="#5F7355" stroke="#5F7355"/>
    <text x="60" y="120" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t-1</text>

    <!-- Swing High Center -->
    <line x1="100" y1="20" x2="100" y2="85" stroke="#1F1E1B" stroke-width="2"/>
    <rect x="94" y="30" width="12" height="40" fill="#FAF8F5" stroke="#CC5A36" stroke-width="2"/>
    <circle cx="100" cy="20" r="4" fill="#CC5A36"/>
    <text x="100" y="12" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">Swing High [t]</text>
    <text x="100" y="105" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">High[t] &gt; High[t±1, t±2]</text>

    <line x1="140" y1="50" x2="140" y2="110" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="134" y="60" width="12" height="40" fill="#CC5A36" stroke="#CC5A36"/>
    <text x="140" y="125" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t+1</text>

    <line x1="180" y1="65" x2="180" y2="125" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="174" y="75" width="12" height="40" fill="#CC5A36" stroke="#CC5A36"/>
    <text x="180" y="140" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">t+2</text>
  </g>
  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">必须在 t+k 柱收盘后方可零前视确认极值，严格杜绝 Lookahead Bias</text>
</svg>"""

SVGS["m04_l01_bos_choch_state_machine"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.1.2：市场结构推进状态机：BOS 顺势延续与 CHoCH 趋势反转先兆</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">SMC STATE MACHINE</text>

  <!-- Trend Polyline -->
  <polyline points="50,180 120,100 170,140 250,70 310,120 390,50 470,150 530,120 610,210 680,180" 
            fill="none" stroke="#486A7D" stroke-width="2.5" stroke-linejoin="round"/>
  
  <!-- Bullish BOS 1 -->
  <line x1="120" y1="100" x2="260" y2="100" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="4 3"/>
  <circle cx="120" cy="100" r="4" fill="#5F7355"/>
  <text x="120" y="90" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355" text-anchor="middle">HH1</text>
  <rect x="180" y="88" width="65" height="18" rx="3" fill="#FAF8F5" stroke="#5F7355"/>
  <text x="212" y="101" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#5F7355" text-anchor="middle">BOS [+]</text>

  <!-- Bullish BOS 2 -->
  <line x1="250" y1="70" x2="400" y2="70" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="4 3"/>
  <circle cx="250" cy="70" r="4" fill="#5F7355"/>
  <text x="250" y="60" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355" text-anchor="middle">HH2</text>
  <rect x="320" y="58" width="65" height="18" rx="3" fill="#FAF8F5" stroke="#5F7355"/>
  <text x="352" y="71" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#5F7355" text-anchor="middle">BOS [+]</text>

  <!-- Peak -->
  <circle cx="390" cy="50" r="5" fill="#CC5A36"/>
  <text x="390" y="40" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">Peak HH3</text>

  <!-- Higher Low (Critical HL) -->
  <circle cx="310" cy="120" r="5" fill="#C08535"/>
  <text x="310" y="140" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535" text-anchor="middle">关键 HL2 (防线)</text>
  <line x1="310" y1="120" x2="500" y2="120" stroke="#CC5A36" stroke-width="2" stroke-dasharray="4 3"/>

  <!-- CHoCH Break Point -->
  <rect x="420" y="110" width="85" height="20" rx="3" fill="#CC5A36"/>
  <text x="462" y="124" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">CHoCH [Bear]</text>
  <text x="462" y="145" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36" text-anchor="middle">实体跌穿前HL反转</text>

  <!-- Bearish BOS -->
  <line x1="470" y1="150" x2="620" y2="150" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="4 3"/>
  <rect x="535" y="140" width="70" height="18" rx="3" fill="#FAF8F5" stroke="#CC5A36"/>
  <text x="570" y="153" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36" text-anchor="middle">BOS [-]</text>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">BOS 确认同向趋势延续，CHoCH 标志结构破位，必须等待回调确认而非盲目反手</text>
</svg>"""

SVGS["m04_l01_liquidity_sweep_vs_breakout"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.1.3：实体收盘突破 (Valid Breakout) 与影线流动性掠夺 (Liquidity Sweep) 对比</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">ORDER FLOW PROOF</text>

  <line x1="50" y1="100" x2="710" y2="100" stroke="#C08535" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="60" y="93" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535">前高阻力位 (Swing High: $100.00)</text>

  <g transform="translate(100, 40)">
    <rect x="10" y="0" width="240" height="180" rx="6" fill="rgba(95, 115, 85, 0.08)" stroke="#5F7355" stroke-width="1"/>
    <text x="130" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">有效实体收盘突破 (Valid BOS)</text>
    
    <line x1="70" y1="75" x2="70" y2="135" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="64" y="85" width="12" height="35" fill="#5F7355"/>

    <line x1="120" y1="40" x2="120" y2="120" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="112" y="48" width="16" height="55" fill="#5F7355"/>
    
    <line x1="170" y1="30" x2="170" y2="90" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="162" y="35" width="16" height="40" fill="#5F7355"/>

    <text x="130" y="150" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">Close &gt; $100.00 形成坚实实体</text>
    <text x="130" y="166" font-family="Inter, sans-serif" font-size="9" fill="#5F7355" text-anchor="middle">买方完全吸收上方挂单，顺势做多</text>
  </g>

  <g transform="translate(420, 40)">
    <rect x="10" y="0" width="240" height="180" rx="6" fill="rgba(204, 90, 54, 0.08)" stroke="#CC5A36" stroke-width="1"/>
    <text x="130" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">影线流动性掠夺 (Liquidity Sweep)</text>
    
    <line x1="70" y1="75" x2="70" y2="135" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="64" y="85" width="12" height="35" fill="#5F7355"/>

    <line x1="120" y1="30" x2="120" y2="130" stroke="#CC5A36" stroke-width="2"/>
    <rect x="112" y="65" width="16" height="50" fill="#CC5A36"/>
    <circle cx="120" cy="30" r="4" fill="#CC5A36"/>
    
    <line x1="170" y1="80" x2="170" y2="155" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="162" y="90" width="16" height="50" fill="#CC5A36"/>

    <text x="130" y="150" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">High &gt; $100 但 Close &lt; $100</text>
    <text x="130" y="166" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36" text-anchor="middle">机构诱多吃散户止损买单，随后反手下杀</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">量化算法必须以收盘价（Close）确认结构，严防影线假突破诱多屠杀</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 02
# -----------------------------------------------------------------------------
SVGS["m04_l02_order_block_formation"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.2.1：看涨机构订单块 (Bullish Order Block) 形成与未成交流动性回踩吸收</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">ORDER BLOCK (OB)</text>

  <g transform="translate(70, 50)">
    <line x1="40" y1="70" x2="40" y2="150" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="30" y="80" width="20" height="55" fill="#FAF8F5" stroke="#CC5A36" stroke-width="2"/>
    <text x="40" y="170" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36" text-anchor="middle">主升浪前最后阴线</text>
    
    <rect x="30" y="80" width="460" height="55" fill="rgba(95, 115, 85, 0.12)" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="4 4"/>
    <text x="260" y="112" font-family="Newsreader, Georgia, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">机构未成交买单残留区 (Bullish OB Zone: $94.00 ~ $97.50)</text>

    <line x1="90" y1="40" x2="90" y2="110" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="82" y="45" width="16" height="55" fill="#5F7355"/>
    
    <line x1="140" y1="10" x2="140" y2="75" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="132" y="15" width="16" height="50" fill="#5F7355"/>
    <text x="140" y="0" font-family="Inter, sans-serif" font-size="9" font-weight="600" fill="#5F7355" text-anchor="middle">暴力拉升 BOS</text>

    <line x1="220" y1="20" x2="220" y2="70" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="214" y="25" width="12" height="35" fill="#CC5A36"/>

    <line x1="260" y1="40" x2="260" y2="90" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="254" y="45" width="12" height="35" fill="#CC5A36"/>

    <line x1="300" y1="65" x2="300" y2="115" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="294" y="70" width="12" height="35" fill="#CC5A36"/>

    <line x1="350" y1="70" x2="350" y2="125" stroke="#5F7355" stroke-width="2"/>
    <rect x="342" y="75" width="16" height="30" fill="#5F7355"/>
    <circle cx="350" cy="125" r="4" fill="#5F7355"/>
    <text x="350" y="145" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">精准回踩测试 (Mitigation)</text>

    <line x1="410" y1="35" x2="410" y2="95" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="402" y="40" width="16" height="45" fill="#5F7355"/>

    <line x1="470" y1="0" x2="470" y2="60" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="462" y="5" width="16" height="45" fill="#5F7355"/>
  </g>

  <g transform="translate(580, 60)">
    <rect x="0" y="0" width="150" height="130" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    <text x="12" y="22" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#1F1E1B">订单块本质法则：</text>
    <text x="12" y="42" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">1. 必须引发结构BOS</text>
    <text x="12" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">2. 伴随失衡缺口FVG</text>
    <text x="12" y="82" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">3. 回踩为机构补单</text>
    <text x="12" y="102" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">4. 止损设于阴线最低点</text>
    <text x="12" y="120" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#5F7355">盈亏比 &gt; 1:3</text>
  </g>
  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">订单块是机构吸收对手盘流动性的真实留存凭证，而非普通技术指标的数学平滑</text>
</svg>"""

SVGS["m04_l02_liquidity_pools_bsl_ssl"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.2.2：买方流动性池 (BSL) 与卖方流动性池 (SSL) 机构跨周期猎杀路径</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">LIQUIDITY POOLS</text>

  <rect x="100" y="55" width="560" height="28" rx="4" fill="rgba(204, 90, 54, 0.12)" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="380" y="73" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">买方流动性池 BSL (Buy-Side Liquidity: 散户追多挂单 + 空头止损单集中区)</text>

  <rect x="100" y="165" width="560" height="28" rx="4" fill="rgba(95, 115, 85, 0.12)" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="380" y="183" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">卖方流动性池 SSL (Sell-Side Liquidity: 散户破位止损单 + 突破追空单集中区)</text>

  <path d="M 120 150 Q 200 130 260 90 T 360 45 T 460 140 T 540 205 T 640 120" 
        fill="none" stroke="#1F1E1B" stroke-width="2.5"/>

  <circle cx="360" cy="45" r="5" fill="#CC5A36"/>
  <text x="360" y="38" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#CC5A36" text-anchor="middle">① 冲刺猎杀 BSL 吸收对手盘</text>

  <circle cx="540" cy="205" r="5" fill="#5F7355"/>
  <text x="540" y="222" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">② 砸盘扫荡 SSL 触发恐慌盘并反向吸筹</text>

  <text x="380" y="240" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">价格运动的本质是在 BSL 与 SSL 两大流动性磁铁之间循环穿梭，为机构大单提供对手盘容量</text>
</svg>"""

SVGS["m04_l02_fair_value_gap"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.2.3：公允价值失衡区 (Fair Value Gap, FVG) 几何拓扑与再平衡机制</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">FVG IMBALANCE</text>

  <g transform="translate(140, 45)">
    <line x1="50" y1="120" x2="50" y2="180" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="42" y="130" width="16" height="40" fill="#5F7355"/>
    <line x1="50" y1="120" x2="250" y2="120" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="30" y="115" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">K1 High</text>

    <line x1="120" y1="20" x2="120" y2="150" stroke="#1F1E1B" stroke-width="2"/>
    <rect x="110" y="35" width="20" height="100" fill="#5F7355"/>
    <text x="120" y="170" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">K2: 单边侵略大阳线</text>

    <line x1="190" y1="40" x2="190" y2="90" stroke="#1F1E1B" stroke-width="1.5"/>
    <rect x="182" y="45" width="16" height="35" fill="#5F7355"/>
    <line x1="120" y1="60" x2="250" y2="60" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="210" y="55" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">K3 Low</text>

    <rect x="50" y="60" width="280" height="60" fill="rgba(192, 133, 53, 0.15)" stroke="#C08535" stroke-width="1.5"/>
    <text x="190" y="95" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#C08535" text-anchor="middle">FVG 失衡真空区 (Gap = K3 Low - K1 High)</text>
  </g>

  <g transform="translate(510, 50)">
    <rect x="0" y="0" width="210" height="145" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    <text x="16" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#1F1E1B">微观再平衡物理机制：</text>
    <text x="16" y="46" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 仅有买方侵略吃单，无卖方报价</text>
    <text x="16" y="66" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 盘口存在严重的撮合残缺</text>
    <text x="16" y="86" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 价格具有强烈的回补再平衡引力</text>
    <text x="16" y="106" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 50% 折让位 (Consequent Encroachment)</text>
    <text x="16" y="126" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#5F7355">回踩 FVG 是第二买点</text>
  </g>
  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">失衡区代表单向流动性挤压，价格大概率回踩回补该真空区以达成双边公允撮合</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 03
# -----------------------------------------------------------------------------
SVGS["m04_l03_head_and_shoulders_anatomy"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.3.1：经典头肩顶形态 (Head &amp; Shoulders) 几何拓扑与颈线断裂确认</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">PATTERN TOPOLOGY</text>

  <polyline points="80,180 150,100 210,140 310,50 410,140 480,95 540,165 590,140 660,220" 
            fill="none" stroke="#1F1E1B" stroke-width="2.5" stroke-linejoin="round"/>

  <circle cx="150" cy="100" r="5" fill="#486A7D"/>
  <text x="150" y="85" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#486A7D" text-anchor="middle">左肩 (Left Shoulder)</text>
  <text x="150" y="70" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">初次冲高放量</text>

  <circle cx="310" cy="50" r="6" fill="#CC5A36"/>
  <text x="310" y="35" font-family="Newsreader, serif" font-size="13" font-weight="700" fill="#CC5A36" text-anchor="middle">头部 (Head: 极值点)</text>
  <text x="310" y="20" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36" text-anchor="middle">量能背离见顶</text>

  <circle cx="480" cy="95" r="5" fill="#486A7D"/>
  <text x="480" y="80" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#486A7D" text-anchor="middle">右肩 (Right Shoulder)</text>
  <text x="480" y="65" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">无法创新高，动能枯竭</text>

  <line x1="160" y1="140" x2="600" y2="140" stroke="#C08535" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="210" y="158" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535">颈线支撑 (Neckline: $100.00)</text>

  <circle cx="540" cy="165" r="5" fill="#CC5A36"/>
  <text x="540" y="185" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#CC5A36" text-anchor="middle">有效击穿颈线</text>

  <circle cx="590" cy="140" r="4" fill="#C08535"/>
  <text x="615" y="130" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">弱势回踩确认</text>
  <text x="660" y="235" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36">量度目标跌幅 H</text>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">头肩顶是供需天平衰竭的经典具象化：多头三次尝试上攻，成交量逐级递减，直至颈线溃败</text>
</svg>"""

SVGS["m04_l03_double_bottom_spring"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.3.2：双底形态 (W-Bottom) 与威科夫弹簧效应 (Spring) 诱空反转结构</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">WYCKOFF SPRING</text>

  <line x1="80" y1="160" x2="680" y2="160" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="90" y="152" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">第一底支撑基线 (Bottom 1: $80.00)</text>

  <polyline points="100,60 180,160 270,100 370,185 410,140 480,95 560,95 650,40" 
            fill="none" stroke="#1F1E1B" stroke-width="2.5" stroke-linejoin="round"/>

  <circle cx="180" cy="160" r="5" fill="#486A7D"/>
  <text x="180" y="180" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#486A7D" text-anchor="middle">初次探底 (Bottom 1)</text>

  <circle cx="270" cy="100" r="5" fill="#C08535"/>
  <line x1="270" y1="100" x2="580" y2="100" stroke="#C08535" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="340" y="92" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535">颈线位 (Neckline: $92.00)</text>

  <circle cx="370" cy="185" r="6" fill="#CC5A36"/>
  <text x="370" y="210" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">威科夫弹簧效应 (Spring)</text>
  <text x="370" y="224" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">故意刺破前低触发止损后光速拉回</text>

  <circle cx="480" cy="95" r="5" fill="#5F7355"/>
  <text x="495" y="85" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#5F7355">放量突破颈线</text>
  
  <text x="380" y="242" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">真假双底的分水岭：次底若带长下影假摔并迅速收复，是主力洗盘完成的最强信号</text>
</svg>"""

SVGS["m04_l03_quant_feature_extraction"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.3.3：形态量化识别算法：局部极值点拓扑抽取与容差约束网</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">ALGO EXTRACTION</text>

  <g transform="translate(40, 60)">
    <rect x="0" y="0" width="150" height="130" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <rect x="0" y="0" width="150" height="26" rx="6" fill="#486A7D"/>
    <text x="75" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">1. 时序极值滤波</text>
    <text x="12" y="48" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B">find_peaks(P)</text>
    <text x="12" y="68" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 滚动窗口 k 邻域</text>
    <text x="12" y="88" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 极值点序列提纯</text>
    <text x="12" y="108" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D">E = [e1, e2, e3, e4, e5]</text>
  </g>

  <path d="M 200 125 L 225 125" stroke="#7D786F" stroke-width="2"/>

  <g transform="translate(235, 60)">
    <rect x="0" y="0" width="150" height="130" rx="6" fill="#FAF8F5" stroke="#C08535" stroke-width="1.5"/>
    <rect x="0" y="0" width="150" height="26" rx="6" fill="#C08535"/>
    <text x="75" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">2. 几何拓扑校验</text>
    <text x="12" y="48" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B">topology_check()</text>
    <text x="12" y="68" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• e1, e5 为肩峰</text>
    <text x="12" y="88" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• e3 为极值头峰</text>
    <text x="12" y="108" font-family="JetBrains Mono, monospace" font-size="9" fill="#C08535">e3.h &gt; max(e1.h, e5.h)</text>
  </g>

  <path d="M 395 125 L 420 125" stroke="#7D786F" stroke-width="2"/>

  <g transform="translate(430, 60)">
    <rect x="0" y="0" width="150" height="130" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <rect x="0" y="0" width="150" height="26" rx="6" fill="#5F7355"/>
    <text x="75" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">3. 动态容差约束</text>
    <text x="12" y="48" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B">tolerance_filter()</text>
    <text x="12" y="68" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 双肩高度对称比</text>
    <text x="12" y="88" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 颈线倾角 |θ| &lt; 15°</text>
    <text x="12" y="108" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">|e1.h - e5.h| / e1.h &lt; ε</text>
  </g>

  <path d="M 590 125 L 615 125" stroke="#7D786F" stroke-width="2"/>

  <g transform="translate(625, 60)">
    <rect x="0" y="0" width="110" height="130" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <rect x="0" y="0" width="110" height="26" rx="6" fill="#CC5A36"/>
    <text x="55" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">4. 信号触发</text>
    <text x="10" y="55" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B">Breakout?</text>
    <text x="10" y="85" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">放量穿透颈线</text>
    <text x="10" y="115" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36">Signal = ±1</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">通过严格数学拓扑定义形态，消灭主观“看图说话”，实现 100% 确定性回测检验</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 04
# -----------------------------------------------------------------------------
SVGS["m04_l04_moving_average_lag"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.4.1：均线滤波器相位时滞比较：真实价格 vs SMA vs EMA vs 零滞后滤波器</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">FILTER PHASE LAG</text>

  <line x1="60" y1="200" x2="700" y2="200" stroke="#E5DFD5" stroke-width="1"/>
  
  <path d="M 70 170 L 220 170 L 250 80 L 480 80 L 510 170 L 680 170" fill="none" stroke="#1F1E1B" stroke-width="2.5"/>
  <text x="120" y="160" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#1F1E1B">真实资产价格 (Raw Price)</text>

  <path d="M 70 170 L 220 170 Q 280 165 340 85 L 480 85 Q 540 90 600 170 L 680 170" fill="none" stroke="#CC5A36" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="360" y="105" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36">SMA(20): 显著相位滞后</text>

  <path d="M 70 170 L 220 170 Q 255 140 290 82 L 480 82 Q 515 110 550 170 L 680 170" fill="none" stroke="#486A7D" stroke-width="2"/>
  <text x="260" y="65" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#486A7D">EMA(20): 响应加快</text>

  <path d="M 70 170 L 220 170 L 252 81 L 480 81 L 512 170 L 680 170" fill="none" stroke="#5F7355" stroke-width="2" stroke-dasharray="2 2"/>
  <text x="490" y="65" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355">Zero-Lag DEMA/KAMA</text>

  <line x1="250" y1="125" x2="330" y2="125" stroke="#C08535" stroke-width="2"/>
  <text x="290" y="142" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#C08535" text-anchor="middle">Δt 相位延迟损耗</text>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">低通滤波器的物理铁律：平滑度与时效性不可兼得，消除滞后必然引入伪高频噪声</text>
</svg>"""

SVGS["m04_l04_wilder_rsi_momentum"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.4.2：怀尔德 RSI 动量振荡器、顶背离结构与超买超卖界限</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">WILDER RSI(14)</text>

  <g transform="translate(60, 45)">
    <text x="0" y="10" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#1F1E1B">价格时序 P_t (创新高 HH)</text>
    <polyline points="20,50 120,40 180,60 280,30 350,55 450,15 520,45 600,75" fill="none" stroke="#1F1E1B" stroke-width="2"/>
    <circle cx="280" cy="30" r="4" fill="#1F1E1B"/>
    <circle cx="450" cy="15" r="4" fill="#CC5A36"/>
    <line x1="280" y1="30" x2="450" y2="15" stroke="#CC5A36" stroke-width="2"/>
    <text x="365" y="16" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36">价格不断创出更高高点</text>
  </g>

  <line x1="60" y1="130" x2="700" y2="130" stroke="#E5DFD5" stroke-width="1"/>

  <g transform="translate(60, 140)">
    <line x1="0" y1="20" x2="640" y2="20" stroke="#CC5A36" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="645" y="24" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">70 (超买)</text>
    
    <line x1="0" y1="65" x2="640" y2="65" stroke="#5F7355" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="645" y="69" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">30 (超卖)</text>

    <polyline points="20,45 120,35 180,55 280,15 350,45 450,30 520,50 600,70" fill="none" stroke="#486A7D" stroke-width="2"/>
    <circle cx="280" cy="15" r="4" fill="#CC5A36"/>
    <circle cx="450" cy="30" r="4" fill="#CC5A36"/>
    <line x1="280" y1="15" x2="450" y2="30" stroke="#CC5A36" stroke-width="2"/>
    <text x="365" y="38" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36">RSI 顶背离 (动量衰减 Lower High)</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">单边强趋势中超买指标会长期钝化，唯有“价格创新高而动量无法创新高”的背离才具备胜率优势</text>
</svg>"""

SVGS["m04_l04_bollinger_volatility_squeeze"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.4.3：自适应布林带 (Bollinger Bands) 波动率挤压 (Squeeze) 与暴动突破</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">VOLATILITY SQUEEZE</text>

  <path d="M 70 70 Q 200 80 340 110 Q 420 120 480 50 L 680 30 
           L 680 210 L 480 190 Q 420 135 340 145 Q 200 170 70 180 Z" 
        fill="rgba(72, 106, 125, 0.08)"/>

  <path d="M 70 70 Q 200 80 340 110 Q 420 120 480 50 L 680 30" fill="none" stroke="#CC5A36" stroke-width="2"/>
  <text x="685" y="35" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">Upper (+2σ)</text>

  <path d="M 70 125 Q 200 125 340 127 Q 420 128 480 120 L 680 120" fill="none" stroke="#C08535" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="685" y="123" font-family="JetBrains Mono, monospace" font-size="9" fill="#C08535">Mid (SMA20)</text>

  <path d="M 70 180 Q 200 170 340 145 Q 420 135 480 190 L 680 210" fill="none" stroke="#5F7355" stroke-width="2"/>
  <text x="685" y="213" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">Lower (-2σ)</text>

  <polyline points="70,120 130,130 190,120 250,135 310,125 360,128 410,123 450,90 500,45 560,35 640,25" 
            fill="none" stroke="#1F1E1B" stroke-width="2.5"/>

  <rect x="330" y="85" width="80" height="85" rx="4" fill="none" stroke="#C08535" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="370" y="78" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#C08535" text-anchor="middle">极度收敛 (Squeeze)</text>
  <text x="370" y="185" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">带宽 Bandwidth &lt; 5%</text>

  <text x="520" y="25" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#CC5A36">通道喇叭口暴力张开</text>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">波动率具有剧烈的均值回归特性：低波动期压缩得越紧，爆发后的顺势脉冲越具爆发力</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 05
# -----------------------------------------------------------------------------
SVGS["m04_l05_volume_profile_vpvr"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.5.1：可见范围成交量分布 (VPVR)：POC 控制点与 70% 价值区 (VAH / VAL)</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">VOLUME PROFILE</text>

  <g transform="translate(60, 50)">
    <polyline points="20,130 60,110 100,140 140,80 180,95 220,50 260,70 300,40" fill="none" stroke="#1F1E1B" stroke-width="2"/>
    <text x="140" y="170" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">K线价格时序轨迹</text>
  </g>

  <g transform="translate(400, 45)">
    <line x1="-60" y1="35" x2="300" y2="35" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="310" y="39" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36">VAH ($105.00)</text>

    <line x1="-60" y1="85" x2="300" y2="85" stroke="#CC5A36" stroke-width="2.5"/>
    <text x="310" y="89" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#CC5A36">POC 控制点 ($98.00)</text>

    <line x1="-60" y1="135" x2="300" y2="135" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="310" y="139" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355">VAL ($91.00)</text>

    <rect x="0" y="15" width="60" height="15" fill="rgba(72, 106, 125, 0.4)"/>
    <rect x="0" y="35" width="130" height="15" fill="rgba(95, 115, 85, 0.6)"/>
    <rect x="0" y="55" width="180" height="15" fill="rgba(95, 115, 85, 0.7)"/>
    <rect x="0" y="75" width="260" height="18" fill="#CC5A36"/>
    <text x="245" y="88" font-family="JetBrains Mono, monospace" font-size="9" fill="#FFFFFF" text-anchor="end">MAX VOL</text>
    <rect x="0" y="98" width="190" height="15" fill="rgba(95, 115, 85, 0.7)"/>
    <rect x="0" y="118" width="140" height="15" fill="rgba(95, 115, 85, 0.6)"/>
    <rect x="0" y="138" width="50" height="15" fill="rgba(72, 106, 125, 0.4)"/>
    <rect x="0" y="158" width="20" height="15" fill="rgba(72, 106, 125, 0.2)"/>

    <line x1="-20" y1="35" x2="-20" y2="135" stroke="#486A7D" stroke-width="2"/>
    <text x="-25" y="90" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#486A7D" text-anchor="end">70% 价值区 (Value Area)</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">POC 是多空博弈的最核心筹码共识锚点，脱离价值区后将面临强力均值回归或真空加速</text>
</svg>"""

SVGS["m04_l05_anchored_vwap_dynamics"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.5.2：事件锚定 VWAP (Anchored VWAP) 与动态标准差通道防御模型</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">ANCHORED VWAP</text>

  <line x1="160" y1="45" x2="160" y2="210" stroke="#CC5A36" stroke-width="2" stroke-dasharray="4 3"/>
  <circle cx="160" cy="150" r="5" fill="#CC5A36"/>
  <text x="160" y="40" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">重大事件锚点 (如财报发布/加息落地)</text>

  <path d="M 160 150 Q 260 135 380 120 T 540 100 T 680 85" fill="none" stroke="#5F7355" stroke-width="3"/>
  <text x="690" y="89" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355">Anchored VWAP</text>

  <path d="M 160 150 Q 260 115 380 95 T 540 70 T 680 50" fill="none" stroke="#486A7D" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="690" y="54" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D">+1 StdDev</text>

  <path d="M 160 150 Q 260 155 380 145 T 540 130 T 680 120" fill="none" stroke="#486A7D" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="690" y="124" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D">-1 StdDev</text>

  <polyline points="160,150 210,110 260,95 310,80 370,120 430,118 490,75 560,98 630,60" 
            fill="none" stroke="#1F1E1B" stroke-width="2"/>
  <circle cx="430" cy="118" r="4" fill="#5F7355"/>
  <text x="430" y="140" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#5F7355" text-anchor="middle">机构持仓成本均线强支撑回踩</text>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">AVWAP 反映该重大事件发生后全市场资金的真实加权持仓成本，具有不可逆的心理防线意义</text>
</svg>"""

SVGS["m04_l05_liquidity_distribution_regimes"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 4.5.3：市场筹码分布三态：P 型多头冲刺、b 型空头派发与 D 型公允平衡</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">PROFILE PROFILES</text>

  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="190" height="150" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="95" y="24" font-family="Newsreader, serif" font-size="13" font-weight="700" fill="#5F7355" text-anchor="middle">P 型分布 (空头回补)</text>
    <rect x="30" y="35" width="100" height="12" fill="#5F7355"/>
    <rect x="30" y="50" width="120" height="12" fill="#5F7355"/>
    <rect x="30" y="65" width="90" height="12" fill="#5F7355"/>
    <rect x="30" y="80" width="20" height="12" fill="rgba(95,115,85,0.4)"/>
    <rect x="30" y="95" width="15" height="12" fill="rgba(95,115,85,0.4)"/>
    <rect x="30" y="110" width="15" height="12" fill="rgba(95,115,85,0.4)"/>
    <text x="95" y="140" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F" text-anchor="middle">空头止损踩踏，高位滞胀</text>
  </g>

  <g transform="translate(285, 50)">
    <rect x="0" y="0" width="190" height="150" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <text x="95" y="24" font-family="Newsreader, serif" font-size="13" font-weight="700" fill="#486A7D" text-anchor="middle">D 型分布 (均衡公允)</text>
    <rect x="30" y="35" width="25" height="12" fill="rgba(72,106,125,0.4)"/>
    <rect x="30" y="50" width="70" height="12" fill="rgba(72,106,125,0.6)"/>
    <rect x="30" y="65" width="125" height="12" fill="#486A7D"/>
    <rect x="30" y="80" width="70" height="12" fill="rgba(72,106,125,0.6)"/>
    <rect x="30" y="95" width="25" height="12" fill="rgba(72,106,125,0.4)"/>
    <text x="95" y="140" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F" text-anchor="middle">多空充分换手，箱体震荡</text>
  </g>

  <g transform="translate(510, 50)">
    <rect x="0" y="0" width="190" height="150" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="95" y="24" font-family="Newsreader, serif" font-size="13" font-weight="700" fill="#CC5A36" text-anchor="middle">b 型分布 (多头踩踏)</text>
    <rect x="30" y="35" width="15" height="12" fill="rgba(204,90,54,0.4)"/>
    <rect x="30" y="50" width="15" height="12" fill="rgba(204,90,54,0.4)"/>
    <rect x="30" y="65" width="30" height="12" fill="rgba(204,90,54,0.4)"/>
    <rect x="30" y="80" width="90" height="12" fill="#CC5A36"/>
    <rect x="30" y="95" width="120" height="12" fill="#CC5A36"/>
    <rect x="30" y="110" width="100" height="12" fill="#CC5A36"/>
    <text x="95" y="140" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F" text-anchor="middle">长线资金出逃，低位吸筹</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">筹码形态直观反映主控资金的筹码搬运意图：P型谨防见顶回落，b型静待震荡筑底</text>
</svg>"""

def main():
    target_dirs = [
        os.path.join(BASE_DIR, "04_technical_pa", "assets"),
        os.path.join(BASE_DIR, "04_technical_pa", "images"),
        os.path.join(BASE_DIR, "web", "assets", "04_technical_pa"),
        os.path.join(BASE_DIR, "web", "images"),
    ]
    for d in target_dirs:
        os.makedirs(d, exist_ok=True)

    count = 0
    for name, content in SVGS.items():
        fname = f"{name}.svg"
        for d in target_dirs:
            with open(os.path.join(d, fname), "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")
        count += 1

    print(f"✅ 成功生成并同步模块 04 共 {count} 个纯 SVG 文件到所有对应资产目录！")

if __name__ == "__main__":
    main()
