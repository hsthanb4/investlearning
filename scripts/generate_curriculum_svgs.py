#!/usr/bin/env python3
"""
InvestLearning SVG Generator
Generates 45 institution-grade, Anthropic minimalist aesthetic SVG diagrams for Modules 01, 02, and 03.
Palette:
  - Background: #FAF9F5, #F5F2EB, #FFFFFF
  - Borders: #D8D3C8, #E2DDD4
  - Primary Ink: #1F1E1B
  - Secondary Ink: #4D4B46, #7D786F
  - Accents:
    * Terracotta: #CC5A36 (warnings, outflows, deductions, down limits)
    * Sage / Fir Green: #5F7355 (liquidity injection, bid, value creation, safe regimes)
    * Grey Cobalt Blue: #486A7D (fed assets, math bounds, mechanisms, normal states)
    * Warm Sand: #EFECE6
"""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SVGS = {}

# ==============================================================================
# MODULE 01: MACRO CYCLE & LIQUIDITY (15 SVGs)
# ==============================================================================

# Lesson 01
SVGS["m01_l01_net_liquidity_flow"] = """<svg viewBox="0 0 780 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="240" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <rect x="25" y="45" width="200" height="85" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="125" y="75" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="600" fill="#1F1E1B" text-anchor="middle">美联储总资产 (Fed Assets)</text>
  <text x="125" y="98" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D" text-anchor="middle">国债/MBS持有量 [+]</text>
  <text x="125" y="116" font-family="Inter, sans-serif" font-size="10" fill="#7D786F" text-anchor="middle">扩表注入 / 缩表回收</text>

  <text x="250" y="92" font-family="Inter, sans-serif" font-size="24" font-weight="bold" fill="#7D786F" text-anchor="middle">-</text>

  <rect x="275" y="45" width="220" height="85" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="385" y="75" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="600" fill="#1F1E1B" text-anchor="middle">法定流动性抽水项</text>
  <text x="385" y="98" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36" text-anchor="middle">TGA 账户 + ON RRP [-]</text>
  <text x="385" y="116" font-family="Inter, sans-serif" font-size="10" fill="#7D786F" text-anchor="middle">财政国库留存与非银闲置资金</text>

  <text x="520" y="92" font-family="Inter, sans-serif" font-size="24" font-weight="bold" fill="#7D786F" text-anchor="middle">=</text>

  <rect x="545" y="45" width="210" height="85" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="650" y="75" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="600" fill="#1F1E1B" text-anchor="middle">美联储实际净流动性</text>
  <text x="650" y="98" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355" text-anchor="middle">Net Liquidity (准备金池)</text>
  <text x="650" y="116" font-family="Inter, sans-serif" font-size="10" fill="#7D786F" text-anchor="middle">驱动一级交易商杠杆与风险偏好</text>

  <path d="M 650 135 L 650 170" stroke="#5F7355" stroke-width="2" marker-end="url(#arrow-green)" fill="none"/>
  <rect x="535" y="175" width="230" height="48" rx="5" fill="#EFECE6" stroke="#D8D3C8" stroke-width="1"/>
  <text x="650" y="195" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#1F1E1B" text-anchor="middle">标普500 / 纳斯达克 估值乘数传导</text>
  <text x="650" y="212" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">Δ P/E ∝ Δ Net Liquidity (t-4周)</text>

  <defs>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#5F7355"/>
    </marker>
  </defs>
</svg>"""

SVGS["m01_l01_pboc_liquidity_corridor"] = """<svg viewBox="0 0 780 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="240" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- PBOC Rate Corridor -->
  <line x1="60" y1="50" x2="720" y2="50" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="725" y="54" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">SLF 利率上限 (常备借贷便利)</text>

  <line x1="60" y1="110" x2="720" y2="110" stroke="#486A7D" stroke-width="2"/>
  <text x="725" y="114" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#486A7D">OMO 7天逆回购基准利率 (政策锚)</text>

  <line x1="60" y1="180" x2="720" y2="180" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="725" y="184" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">超额准备金利率下限 (IOER)</text>

  <!-- Market rate trajectory -->
  <path d="M 80 140 Q 180 80 280 120 T 480 100 T 680 130" fill="none" stroke="#1F1E1B" stroke-width="2.5"/>
  <text x="290" y="85" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#1F1E1B">DR007 银行间真实质押回购利率</text>
  
  <rect x="75" y="195" width="280" height="32" rx="4" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="215" y="215" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46" text-anchor="middle">DR007 &lt; OMO: 银行间流动性充裕淤积</text>

  <rect x="420" y="195" width="280" height="32" rx="4" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="560" y="215" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36" text-anchor="middle">R007 - DR007 剪刀差走阔: 非银流动性枯竭</text>
</svg>"""

SVGS["m01_l01_liquidity_transmission_chain"] = """<svg viewBox="0 0 780 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="220" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <!-- Step 1 -->
  <rect x="30" y="60" width="150" height="80" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="105" y="85" font-family="Newsreader, serif" font-size="13" font-weight="600" fill="#1F1E1B" text-anchor="middle">1. 基础货币释放</text>
  <text x="105" y="105" font-family="JetBrains Mono, monospace" font-size="10" fill="#486A7D" text-anchor="middle">降准 / 买债扩表</text>
  <text x="105" y="123" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">商业银行超储率上升</text>

  <line x1="185" y1="100" x2="220" y2="100" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Step 2 -->
  <rect x="225" y="60" width="150" height="80" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="300" y="85" font-family="Newsreader, serif" font-size="13" font-weight="600" fill="#1F1E1B" text-anchor="middle">2. 银行间资金外溢</text>
  <text x="300" y="105" font-family="JetBrains Mono, monospace" font-size="10" fill="#486A7D" text-anchor="middle">SOFR / DR007 走低</text>
  <text x="300" y="123" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">非银拆借与两融成本下降</text>

  <line x1="380" y1="100" x2="415" y2="100" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Step 3 -->
  <rect x="420" y="60" width="150" height="80" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
  <text x="495" y="85" font-family="Newsreader, serif" font-size="13" font-weight="600" fill="#1F1E1B" text-anchor="middle">3. 风险溢价压缩</text>
  <text x="495" y="105" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355" text-anchor="middle">ERP 快速收敛</text>
  <text x="495" y="123" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">无风险资产收益率受限</text>

  <line x1="575" y1="100" x2="610" y2="100" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Step 4 -->
  <rect x="615" y="60" width="140" height="80" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="685" y="85" font-family="Newsreader, serif" font-size="13" font-weight="600" fill="#1F1E1B" text-anchor="middle">4. 估值乘数扩张</text>
  <text x="685" y="105" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="middle">DCF 分母贴现率下降</text>
  <text x="685" y="123" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">PE/PB 驱动系统性牛市</text>

  <defs>
    <marker id="arrow-generic" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#7D786F"/>
    </marker>
  </defs>
</svg>"""

# Lesson 02
SVGS["m01_l02_yield_curve_regimes"] = """<svg viewBox="0 0 780 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="240" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- Axis -->
  <line x1="60" y1="190" x2="720" y2="190" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="60" y1="40" x2="60" y2="190" stroke="#7D786F" stroke-width="1.5"/>
  <text x="50" y="45" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">收益率 %</text>
  <text x="720" y="208" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">到期期限 (3M, 2Y, 5Y, 10Y, 30Y)</text>

  <!-- Curve 1: Normal (Green) -->
  <path d="M 70 160 Q 250 140 450 90 T 700 65" fill="none" stroke="#5F7355" stroke-width="2.5"/>
  <text x="705" y="65" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#5F7355">常态正斜率 (Term Premium 正常)</text>

  <!-- Curve 2: Flat (Blue) -->
  <line x1="70" y1="110" x2="700" y2="110" stroke="#486A7D" stroke-width="2" stroke-dasharray="5 5"/>
  <text x="705" y="113" font-family="Inter, sans-serif" font-size="11" fill="#486A7D">平坦化曲线 (经济周期见顶放缓)</text>

  <!-- Curve 3: Inverted (Terracotta) -->
  <path d="M 70 70 Q 220 80 440 130 T 700 155" fill="none" stroke="#CC5A36" stroke-width="2.5"/>
  <text x="705" y="158" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#CC5A36">利差倒挂 (加息抗通胀 ➔ 衰退预警)</text>
</svg>"""

SVGS["m01_l02_bank_nim_credit_crunch"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <rect x="40" y="35" width="200" height="75" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="140" y="62" font-family="Newsreader, serif" font-size="13" font-weight="600" fill="#1F1E1B" text-anchor="middle">长短端倒挂 10Y-2Y &lt; 0</text>
  <text x="140" y="82" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36" text-anchor="middle">短端借贷成本 &gt; 长期资产收益</text>
  <text x="140" y="98" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">NIM (净息差) 遭受严重挤压</text>

  <line x1="245" y1="72" x2="285" y2="72" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <rect x="290" y="35" width="200" height="75" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="390" y="62" font-family="Newsreader, serif" font-size="13" font-weight="600" fill="#1F1E1B" text-anchor="middle">商业银行信贷供给骤缩</text>
  <text x="390" y="82" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46" text-anchor="middle">SLOOS 贷款审查标准大幅收紧</text>
  <text x="390" y="98" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">中小企业信用授信额度冻结</text>

  <line x1="495" y1="72" x2="535" y2="72" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <rect x="540" y="35" width="200" height="75" rx="6" fill="#FFFFFF" stroke="#1F1E1B" stroke-width="1.5"/>
  <text x="640" y="62" font-family="Newsreader, serif" font-size="13" font-weight="600" fill="#1F1E1B" text-anchor="middle">实体违约与盈利衰退</text>
  <text x="640" y="82" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36" text-anchor="middle">企业现金流断裂 / 裁员潮</text>
  <text x="640" y="98" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">EPS 断崖式下修 ➔ 股市戴维斯双杀</text>

  <!-- Bottom Un-inversion Alert -->
  <rect x="40" y="145" width="700" height="60" rx="6" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1"/>
  <text x="60" y="170" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36">⚠️ 关键转折陷阱：牛市陡峭化（Bull Steepening）踩踏</text>
  <text x="60" y="190" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46">利差从负转正并非买入信号，而是央行因实体经济暴雷被迫紧急降息确诊衰退，股市真正的大底往往在此刻后 6~12 个月方才到来。</text>
</svg>"""

SVGS["m01_l02_estrella_mishkin_curve"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- Axis -->
  <line x1="80" y1="180" x2="720" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="400" y1="30" x2="400" y2="180" stroke="#D8D3C8" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="80" y1="30" x2="80" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  
  <text x="400" y="198" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="middle">0 bps (利差倒挂分水岭)</text>
  <text x="140" y="198" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="middle">-150 bps</text>
  <text x="660" y="198" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355" text-anchor="middle">+150 bps</text>
  <text x="70" y="35" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">P(Recession)%</text>

  <!-- Logistic S-Curve -->
  <path d="M 100 45 C 250 50, 350 120, 680 175" fill="none" stroke="#CC5A36" stroke-width="3"/>
  <circle cx="280" cy="80" r="5" fill="#CC5A36"/>
  <text x="290" y="75" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36">倒挂 -100 bps: 衰退概率 &gt; 65%</text>

  <rect x="440" y="55" width="260" height="70" rx="5" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="455" y="78" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D">P = 1 / (1 + exp(-(α + β*Spread)))</text>
  <text x="455" y="98" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46">美联储 Estrella-Mishkin 模型</text>
  <text x="455" y="114" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">当利差深度倒挂时，远期 12 个月衰退确定性极高</text>
</svg>"""

# Lesson 03
SVGS["m01_l03_merrill_clock_quadrants"] = """<svg viewBox="0 0 780 260" width="100%" height="260" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="260" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- Cross Axis -->
  <line x1="390" y1="20" x2="390" y2="240" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="40" y1="130" x2="740" y2="130" stroke="#7D786F" stroke-width="1.5"/>
  
  <text x="745" y="134" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#7D786F">经济增长 Growth ↑</text>
  <text x="35" y="134" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#7D786F" text-anchor="end">经济增长 Growth ↓</text>
  <text x="390" y="15" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#7D786F" text-anchor="middle">通胀膨胀 Inflation ↑</text>
  <text x="390" y="255" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#7D786F" text-anchor="middle">通胀下行 Inflation ↓</text>

  <!-- Q1 Overheat (Top Right) -->
  <rect x="410" y="30" width="310" height="90" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="425" y="55" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#CC5A36">2. 过热期 (Overheat: G↑, I↑)</text>
  <text x="425" y="75" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">首选资产：大宗商品 Commodities &gt; 股票</text>
  <text x="425" y="95" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F">工业金属 / 原油暴涨，央行加息紧缩防通胀</text>

  <!-- Q2 Stagflation (Top Left) -->
  <rect x="60" y="30" width="310" height="90" rx="6" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="75" y="55" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#CC5A36">3. 滞胀期 (Stagflation: G↓, I↑)</text>
  <text x="75" y="75" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">首选资产：现金 Cash &gt; 大宗商品 &gt; 股债双杀</text>
  <text x="75" y="95" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">资产配置百慕大，生产成本高企吞噬利润</text>

  <!-- Q3 Recession (Bottom Left) -->
  <rect x="60" y="145" width="310" height="90" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="75" y="170" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#486A7D">4. 衰退期 (Recession: G↓, I↓)</text>
  <text x="75" y="190" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">首选资产：长久期债券 Bonds &gt; 现金</text>
  <text x="75" y="210" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F">央行流动性大放水，无风险利率下行牛市</text>

  <!-- Q4 Recovery (Bottom Right) -->
  <rect x="410" y="145" width="310" height="90" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
  <text x="425" y="170" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#5F7355">1. 复苏期 (Recovery: G↑, I↓)</text>
  <text x="425" y="190" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">首选资产：股票 Equities &gt; 债券</text>
  <text x="425" y="210" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">盈利回升叠加充裕流动性，夏普比率最高窗口</text>
</svg>"""

SVGS["m01_l03_kitchin_inventory_cycle"] = """<svg viewBox="0 0 780 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="240" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- 4 inventory phase boxes in a circular loop -->
  <rect x="40" y="30" width="160" height="80" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="120" y="55" font-family="Newsreader, serif" font-size="13" font-weight="bold" fill="#5F7355" text-anchor="middle">1. 被动去库存</text>
  <text x="120" y="75" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">需求↑, 存货↓</text>
  <text x="120" y="95" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355" text-anchor="middle">★ 权益资产黄金买点</text>

  <line x1="205" y1="70" x2="245" y2="70" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <rect x="250" y="30" width="160" height="80" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="330" y="55" font-family="Newsreader, serif" font-size="13" font-weight="bold" fill="#CC5A36" text-anchor="middle">2. 主动补库存</text>
  <text x="330" y="75" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">需求↑, 存货↑</text>
  <text x="330" y="95" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36" text-anchor="middle">开足马力 / 周期股繁荣</text>

  <line x1="415" y1="70" x2="455" y2="70" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <rect x="460" y="30" width="160" height="80" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="540" y="55" font-family="Newsreader, serif" font-size="13" font-weight="bold" fill="#486A7D" text-anchor="middle">3. 被动补库存</text>
  <text x="540" y="75" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">需求↓, 存货↑</text>
  <text x="540" y="95" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">终端滞销 / 现金防御</text>

  <path d="M 625 70 Q 700 70 700 130 T 625 180" fill="none" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <rect x="460" y="140" width="160" height="80" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="540" y="165" font-family="Newsreader, serif" font-size="13" font-weight="bold" fill="#1F1E1B" text-anchor="middle">4. 主动去库存</text>
  <text x="540" y="185" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">需求↓, 存货↓</text>
  <text x="540" y="205" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D" text-anchor="middle">减产降价 / 债券牛市</text>

  <path d="M 455 180 Q 200 220 120 120" fill="none" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>
</svg>"""

SVGS["m01_l03_asset_rotation_regime"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- Table-like layout of asset weights by regime -->
  <text x="40" y="38" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">宏观体制驱动的资产权重最优配比 (Sharpe 驱动)</text>
  
  <g transform="translate(40, 55)">
    <!-- Header -->
    <rect x="0" y="0" width="700" height="30" fill="#EFECE6" rx="4"/>
    <text x="20" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">宏观阶段</text>
    <text x="200" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">权益股票 (Stocks)</text>
    <text x="360" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">利率债券 (Bonds)</text>
    <text x="500" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">大宗商品 (Commodity)</text>
    <text x="640" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">现金 (Cash)</text>

    <!-- Row 1 Recovery -->
    <line x1="0" y1="60" x2="700" y2="60" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="50" font-family="Inter, sans-serif" font-size="11" fill="#5F7355" font-weight="600">复苏 (Recovery)</text>
    <text x="200" y="50" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#5F7355">60% (主选)</text>
    <text x="360" y="50" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">20%</text>
    <text x="500" y="50" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">10%</text>
    <text x="640" y="50" font-family="JetBrains Mono, monospace" font-size="11" fill="#7D786F">10%</text>

    <!-- Row 2 Overheat -->
    <line x1="0" y1="90" x2="700" y2="90" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="80" font-family="Inter, sans-serif" font-size="11" fill="#CC5A36" font-weight="600">过热 (Overheat)</text>
    <text x="200" y="80" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">30%</text>
    <text x="360" y="80" font-family="JetBrains Mono, monospace" font-size="11" fill="#7D786F">0% (规避加息)</text>
    <text x="500" y="80" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#CC5A36">50% (主选)</text>
    <text x="640" y="80" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">20%</text>

    <!-- Row 3 Stagflation -->
    <line x1="0" y1="120" x2="700" y2="120" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="110" font-family="Inter, sans-serif" font-size="11" fill="#CC5A36" font-weight="600">滞胀 (Stagflation)</text>
    <text x="200" y="110" font-family="JetBrains Mono, monospace" font-size="11" fill="#7D786F">0% (规避双杀)</text>
    <text x="360" y="110" font-family="JetBrains Mono, monospace" font-size="11" fill="#7D786F">10%</text>
    <text x="500" y="110" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">30% (通胀对冲)</text>
    <text x="640" y="110" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#CC5A36">60% (主选)</text>

    <!-- Row 4 Recession -->
    <line x1="0" y1="150" x2="700" y2="150" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="140" font-family="Inter, sans-serif" font-size="11" fill="#486A7D" font-weight="600">衰退 (Recession)</text>
    <text x="200" y="140" font-family="JetBrains Mono, monospace" font-size="11" fill="#7D786F">10%</text>
    <text x="360" y="140" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#486A7D">60% (主选)</text>
    <text x="500" y="140" font-family="JetBrains Mono, monospace" font-size="11" fill="#7D786F">0%</text>
    <text x="640" y="140" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">30%</text>
  </g>
</svg>"""

# Lesson 04
SVGS["m01_l04_dollar_tide_mechanism"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <rect x="40" y="40" width="210" height="150" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="145" y="68" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#486A7D" text-anchor="middle">美联储收水 / 强势美元</text>
  <text x="145" y="92" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">1. 美债收益率高企 (4.5%+)</text>
  <text x="145" y="112" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">2. 美元指数 DXY 走强</text>
  <text x="145" y="132" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">3. 跨国套息 Carry 交易逆转</text>
  <rect x="55" y="150" width="180" height="26" rx="4" fill="#EFECE6"/>
  <text x="145" y="167" font-family="JetBrains Mono, monospace" font-size="9" fill="#4D4B46" text-anchor="middle">全球资本回流美国无风险资产</text>

  <!-- Flow Arrow -->
  <path d="M 260 115 L 340 115" stroke="#CC5A36" stroke-width="3" marker-end="url(#arrow-red)" fill="none"/>
  <text x="300" y="105" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">跨境虹吸</text>

  <rect x="350" y="40" width="390" height="150" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="545" y="68" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#CC5A36" text-anchor="middle">新兴市场与 A 股传导链条</text>
  
  <text x="375" y="95" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 中美利差倒挂加深: US 10Y - CN 10Y &gt; 150 bps</text>
  <text x="375" y="118" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 离岸人民币汇率承压: USD/CNH 向上突破贬值关键关口</text>
  <text x="375" y="141" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 北向资金 (陆股通) 触发外币计价 VaR 止损阈值并系统性净流出</text>
  <text x="375" y="164" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36">• 茅台/宁德等白马核心资产面临跨期折现估值压缩</text>

  <defs>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#CC5A36"/>
    </marker>
  </defs>
</svg>"""

SVGS["m01_l04_us_cn_spread_fx"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- Dual axis chart illustration -->
  <line x1="70" y1="180" x2="710" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="70" y1="30" x2="70" y2="180" stroke="#CC5A36" stroke-width="1.5"/>
  <line x1="710" y1="30" x2="710" y2="180" stroke="#486A7D" stroke-width="1.5"/>

  <text x="60" y="35" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="end">USD/CNH 汇率</text>
  <text x="720" y="35" font-family="JetBrains Mono, monospace" font-size="10" fill="#486A7D">中美利差 (US-CN 10Y bps)</text>

  <!-- Spread Line (Blue) -->
  <path d="M 80 160 Q 250 120 400 90 T 700 45" fill="none" stroke="#486A7D" stroke-width="2.5"/>
  <!-- CNH Line (Terracotta) -->
  <path d="M 80 150 Q 250 110 400 85 T 700 55" fill="none" stroke="#CC5A36" stroke-width="2.5" stroke-dasharray="4 2"/>

  <rect x="180" y="45" width="340" height="40" rx="4" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="350" y="68" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#1F1E1B" text-anchor="middle">利差倒挂幅度与离岸汇率贬值呈现高度协变正相关</text>
</svg>"""

SVGS["m01_l04_capital_flow_shock_index"] = """<svg viewBox="0 0 780 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="220" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="38" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">资本流动冲击指数 (CFSI) 三档状态量化监控</text>

  <!-- Zone 1 Normal -->
  <rect x="40" y="60" width="220" height="130" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <rect x="40" y="60" width="220" height="28" fill="#5F7355" rx="6 6 0 0"/>
  <text x="150" y="79" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CFSI ≤ 1.0 : 常态顺差</text>
  <text x="55" y="110" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 跨境资金处于温和流入/双向平衡</text>
  <text x="55" y="130" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 北向资金保持平稳净申购</text>
  <text x="55" y="150" font-family="Inter, sans-serif" font-size="10" fill="#5F7355" font-weight="600">• 策略行动：核心白马正常超配</text>

  <!-- Zone 2 Warning -->
  <rect x="280" y="60" width="220" height="130" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <rect x="280" y="60" width="220" height="28" fill="#486A7D" rx="6 6 0 0"/>
  <text x="390" y="79" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">1.0 &lt; CFSI ≤ 2.0 : 预警状态</text>
  <text x="295" y="110" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 美元指数飙升或离岸贬值加速</text>
  <text x="295" y="130" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 外资风险偏好收缩，出现流出苗头</text>
  <text x="295" y="150" font-family="Inter, sans-serif" font-size="10" fill="#486A7D" font-weight="600">• 策略行动：暂停加仓，收窄外资重仓股</text>

  <!-- Zone 3 Extreme Shock -->
  <rect x="520" y="60" width="220" height="130" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <rect x="520" y="60" width="220" height="28" fill="#CC5A36" rx="6 6 0 0"/>
  <text x="630" y="79" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CFSI &gt; 2.0 : 极度冲击</text>
  <text x="535" y="110" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 汇率快速破位，北向单日流出超百亿</text>
  <text x="535" y="130" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 估值折现杀跌引发两融被动平仓</text>
  <text x="535" y="150" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36" font-weight="600">• 策略行动：启动外汇断路器对冲防御</text>
</svg>"""

# Lesson 05
SVGS["m01_l05_all_weather_framework"] = """<svg viewBox="0 0 780 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="240" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <text x="390" y="28" font-family="Newsreader, serif" font-size="15" font-weight="bold" fill="#1F1E1B" text-anchor="middle">桥水全天候 (All Weather) 风险正交平价配置矩阵</text>
  
  <rect x="60" y="45" width="310" height="85" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
  <text x="80" y="70" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355">增长超预期 (Growth ↑) 25% 风险</text>
  <text x="80" y="92" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 股票权益 (Equities)</text>
  <text x="80" y="110" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 大宗商品 (Commodities) / 企业信用债</text>

  <rect x="410" y="45" width="310" height="85" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="430" y="70" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36">通胀超预期 (Inflation ↑) 25% 风险</text>
  <text x="430" y="92" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 通胀保值国债 (TIPS)</text>
  <text x="430" y="110" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 原油 / 黄金 / 工业品</text>

  <rect x="60" y="140" width="310" height="85" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="80" y="165" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D">增长低于预期 (Growth ↓) 25% 风险</text>
  <text x="80" y="187" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 名义长期国债 (Nominal Treasury)</text>
  <text x="80" y="205" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 现金等价物 (Cash Equivalents)</text>

  <rect x="410" y="140" width="310" height="85" rx="6" fill="#FFFFFF" stroke="#7D786F" stroke-width="1.5"/>
  <text x="430" y="165" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#1F1E1B">通胀低于预期 (Inflation ↓) 25% 风险</text>
  <text x="430" y="187" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 股票权益 (估值折现降低利好)</text>
  <text x="430" y="205" font-family="Inter, sans-serif" font-size="11" fill="#1F1E1B">• 投资级长期国债</text>
</svg>"""

SVGS["m01_l05_regime_state_machine"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <!-- State 1 Expansion -->
  <circle cx="140" cy="115" r="65" fill="#FFFFFF" stroke="#5F7355" stroke-width="2.5"/>
  <text x="140" y="100" font-family="Newsreader, serif" font-size="13" font-weight="bold" fill="#5F7355" text-anchor="middle">1. 扩张期</text>
  <text x="140" y="118" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">Liq &gt; 0 &amp; VIX ≤ 30</text>
  <text x="140" y="136" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#5F7355" text-anchor="middle">股票敞口 90%</text>

  <!-- Arrow 1 to 2 -->
  <path d="M 210 95 Q 295 70 380 95" fill="none" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>
  <text x="295" y="70" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">流动性边际收缩</text>

  <!-- State 2 Neutral -->
  <circle cx="450" cy="115" r="65" fill="#FFFFFF" stroke="#486A7D" stroke-width="2.5"/>
  <text x="450" y="100" font-family="Newsreader, serif" font-size="13" font-weight="bold" fill="#486A7D" text-anchor="middle">2. 中性防御</text>
  <text x="450" y="118" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">Liq ≤ 0 &amp; VIX ≤ 30</text>
  <text x="450" y="136" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#486A7D" text-anchor="middle">股票敞口 50%</text>

  <!-- Arrow 2 to 3 -->
  <path d="M 520 95 Q 605 70 650 95" fill="none" stroke="#CC5A36" stroke-width="2" marker-end="url(#arrow-red)"/>
  <text x="590" y="70" font-family="Inter, sans-serif" font-size="9" font-weight="bold" fill="#CC5A36" text-anchor="middle">恐慌爆发 VIX &gt; 30</text>

  <!-- State 3 Crisis -->
  <circle cx="690" cy="115" r="55" fill="#FAF0ED" stroke="#CC5A36" stroke-width="2.5"/>
  <text x="690" y="100" font-family="Newsreader, serif" font-size="13" font-weight="bold" fill="#CC5A36" text-anchor="middle">3. 危机风暴</text>
  <text x="690" y="118" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36" text-anchor="middle">VIX &gt; 30 恐慌</text>
  <text x="690" y="136" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">硬降仓至 20%</text>

  <!-- Return paths -->
  <path d="M 640 145 Q 560 175 480 155" fill="none" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>
  <path d="M 390 145 Q 295 175 200 145" fill="none" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>
</svg>"""

SVGS["m01_l05_dynamic_hedging_payoff"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  <!-- Axis -->
  <line x1="70" y1="180" x2="720" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="70" y1="30" x2="70" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <text x="60" y="35" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">累计净值</text>

  <!-- Benchmark Drawdown (Terracotta) -->
  <path d="M 80 150 Q 200 60 300 120 T 450 170 T 580 130 T 700 110" fill="none" stroke="#CC5A36" stroke-width="2" stroke-dasharray="3 3"/>
  <text x="705" y="112" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36">纯多头基准 (最大回撤 -35%)</text>

  <!-- Hedged Strategy (Green) -->
  <path d="M 80 150 Q 200 70 300 100 T 450 115 T 580 80 T 700 50" fill="none" stroke="#5F7355" stroke-width="2.5"/>
  <text x="705" y="52" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#5F7355">全天候自适应对冲 (最大回撤 &lt; 12%)</text>

  <rect x="360" y="125" width="160" height="35" rx="4" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1"/>
  <text x="440" y="146" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36" text-anchor="middle">危机期间自动压缩敞口避险</text>
</svg>"""

# ==============================================================================
# MODULE 02: MICROSTRUCTURE & ORDER FLOW (15 SVGs)
# ==============================================================================

# Lesson 01
SVGS["m02_l01_lob_structure"] = """<svg viewBox="0 0 780 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="250" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <!-- Mid Price Center -->
  <line x1="390" y1="20" x2="390" y2="230" stroke="#7D786F" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="390" y="16" font-family="Newsreader, serif" font-size="12" font-style="italic" fill="#7D786F" text-anchor="middle">中间价 Mid Price = $100.00</text>

  <!-- Ask Side (Right, Terracotta) -->
  <g transform="translate(410, 40)">
    <rect x="0" y="0" width="100" height="24" rx="4" fill="rgba(204, 90, 54, 0.2)" stroke="#CC5A36" stroke-width="1"/>
    <text x="110" y="16" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">Ask 1: $100.05 (200手)</text>

    <rect x="0" y="32" width="160" height="24" rx="4" fill="rgba(204, 90, 54, 0.35)" stroke="#CC5A36" stroke-width="1"/>
    <text x="170" y="48" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">Ask 2: $100.10 (450手)</text>

    <rect x="0" y="64" width="230" height="24" rx="4" fill="rgba(204, 90, 54, 0.5)" stroke="#CC5A36" stroke-width="1"/>
    <text x="240" y="80" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">Ask 3: $100.15 (800手)</text>
    
    <rect x="0" y="96" width="280" height="24" rx="4" fill="rgba(204, 90, 54, 0.65)" stroke="#CC5A36" stroke-width="1"/>
    <text x="290" y="112" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">Ask 4: $100.20 (1200手)</text>
  </g>

  <!-- Bid Side (Left, Fir Green) -->
  <g transform="translate(370, 40)">
    <rect x="-120" y="0" width="120" height="24" rx="4" fill="rgba(95, 115, 85, 0.2)" stroke="#5F7355" stroke-width="1"/>
    <text x="-130" y="16" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355" text-anchor="end">Bid 1: $99.95 (300手)</text>

    <rect x="-190" y="32" width="190" height="24" rx="4" fill="rgba(95, 115, 85, 0.35)" stroke="#5F7355" stroke-width="1"/>
    <text x="-200" y="48" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355" text-anchor="end">Bid 2: $99.90 (600手)</text>

    <rect x="-250" y="64" width="250" height="24" rx="4" fill="rgba(95, 115, 85, 0.5)" stroke="#5F7355" stroke-width="1"/>
    <text x="-260" y="80" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355" text-anchor="end">Bid 3: $99.85 (950手)</text>

    <rect x="-300" y="96" width="300" height="24" rx="4" fill="rgba(95, 115, 85, 0.65)" stroke="#5F7355" stroke-width="1"/>
    <text x="-310" y="112" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355" text-anchor="end">Bid 4: $99.80 (1400手)</text>
  </g>

  <!-- Spread Bracket -->
  <rect x="250" y="190" width="280" height="40" rx="5" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="390" y="215" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B" text-anchor="middle">买卖价差 Spread = $100.05 - $99.95 = $0.10 (10 bps)</text>
</svg>"""

SVGS["m02_l01_matching_engine_flow"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <rect x="30" y="45" width="140" height="75" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="100" y="72" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#1F1E1B" text-anchor="middle">新进委托订单</text>
  <text x="100" y="92" font-family="JetBrains Mono, monospace" font-size="10" fill="#486A7D" text-anchor="middle">Side / Price / Vol</text>
  <text x="100" y="108" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">纳秒时间戳 t0</text>

  <line x1="170" y1="82" x2="210" y2="82" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Decision -->
  <polygon points="270,45 330,82 270,120 210,82" fill="#FFFFFF" stroke="#1F1E1B" stroke-width="1.5"/>
  <text x="270" y="86" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1F1E1B" text-anchor="middle">可交叉撮合?</text>

  <!-- Yes branch -->
  <line x1="330" y1="82" x2="390" y2="82" stroke="#5F7355" stroke-width="2" marker-end="url(#arrow-green)"/>
  <text x="360" y="75" font-family="Inter, sans-serif" font-size="9" font-weight="bold" fill="#5F7355" text-anchor="middle">是</text>

  <rect x="395" y="45" width="165" height="75" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="477" y="70" font-family="Newsreader, serif" font-size="12" font-weight="bold" fill="#5F7355" text-anchor="middle">立即撮合成交</text>
  <text x="477" y="90" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">按对手盘最优价成交</text>
  <text x="477" y="108" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">生成 Trade 记录扣减深度</text>

  <!-- No branch -->
  <line x1="270" y1="120" x2="270" y2="160" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>
  <text x="280" y="145" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">否</text>

  <rect x="180" y="165" width="180" height="50" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="270" y="185" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#486A7D" text-anchor="middle">挂入本方订单簿队列</text>
  <text x="270" y="202" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">按价格优先、时间优先排队</text>

  <!-- Remainder -->
  <path d="M 560 82 Q 650 82 650 145" fill="none" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>
  <rect x="570" y="150" width="180" height="55" rx="6" fill="#EFECE6" stroke="#D8D3C8" stroke-width="1"/>
  <text x="660" y="172" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1F1E1B" text-anchor="middle">未完全成交剩余份额</text>
  <text x="660" y="190" font-family="Inter, sans-serif" font-size="9" fill="#4D4B46" text-anchor="middle">进入挂单队列等待后继撮合</text>
</svg>"""

SVGS["m02_l01_market_sweep_slippage"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="35" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">大额市价买单深度扫盘 (Book Sweep) 与非线性滑点形成</text>

  <!-- Visualizing Order eating through Asks -->
  <g transform="translate(60, 55)">
    <!-- Ask 1 eaten -->
    <rect x="0" y="0" width="180" height="32" rx="4" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="15" y="21" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">Ask 1: $10.00 (200手)</text>
    <text x="170" y="21" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="end">全部吃穿 ✔</text>

    <!-- Ask 2 eaten -->
    <rect x="0" y="42" width="260" height="32" rx="4" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="15" y="63" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">Ask 2: $10.05 (400手)</text>
    <text x="250" y="63" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="end">全部吃穿 ✔</text>

    <!-- Ask 3 partially eaten -->
    <rect x="0" y="84" width="340" height="32" rx="4" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
    <rect x="0" y="84" width="170" height="32" rx="4" fill="rgba(72, 106, 125, 0.2)"/>
    <text x="15" y="105" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B">Ask 3: $10.12 (800手)</text>
    <text x="330" y="105" font-family="Inter, sans-serif" font-size="10" fill="#486A7D" text-anchor="end">部分吃单 400手</text>
  </g>

  <rect x="440" y="55" width="280" height="120" rx="6" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="460" y="82" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">滑点代价 (Execution Shortfall)</text>
  <text x="460" y="104" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F">无冲击基准价 P0 = $10.00</text>
  <text x="460" y="124" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">实际撮合 VWAP = $10.068</text>
  <text x="460" y="146" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36">穿仓滑点: +68 bps (直接抹杀 Alpha)</text>
</svg>"""

# Lesson 02
SVGS["m02_l02_limit_lock_liquidity_freeze"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">A 股一字跌停盘口流动性完全锁死（Liquidity Freeze）物理黑洞</text>

  <!-- Left: Bids = 0 -->
  <rect x="50" y="55" width="280" height="140" rx="6" fill="#FAF0ED" stroke="#CC5A36" stroke-width="2"/>
  <text x="190" y="85" font-family="Inter, sans-serif" font-size="14" font-weight="bold" fill="#CC5A36" text-anchor="middle">买一队列：买量 = 0 股</text>
  <text x="190" y="115" font-family="Inter, sans-serif" font-size="11" fill="#4D4B46" text-anchor="middle">流动性完全蒸发</text>
  <text x="190" y="140" font-family="Inter, sans-serif" font-size="10" fill="#7D786F" text-anchor="middle">即使以跌停价折价甩卖，亦无撮合对手盘</text>
  <text x="190" y="165" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">日内流动性选择权 = 0</text>

  <!-- Right: Asks piled up -->
  <rect x="390" y="55" width="340" height="140" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="560" y="85" font-family="Inter, sans-serif" font-size="14" font-weight="bold" fill="#1F1E1B" text-anchor="middle">卖一封单：巨额压单 (如 800,000 手)</text>
  <text x="420" y="115" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 场内恐慌踩踏，所有持有者挂单抢跑</text>
  <text x="420" y="135" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 交易所撮合队列遵循 FIFO，散户排在队尾绝无可能成交</text>
  <text x="420" y="155" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 真实公允价值已在 -30%，现货遭遇关门打狗连环跌停</text>
</svg>"""

SVGS["m02_l02_t1_vs_t0_execution_risk"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">交易制度微观摩擦：A 股 T+1 制度 vs 美/港股 T+0 风险敞口对比</text>

  <!-- T+1 Flow -->
  <rect x="40" y="55" width="330" height="145" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="60" y="82" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36">A 股 T+1 制度（日内止损受限）</text>
  <text x="60" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">09:35 买入后遭遇闪崩重大利空</text>
  <text x="60" y="125" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36">❌ 当日物理禁止卖出平仓</text>
  <text x="60" y="145" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46">被迫承担 4 小时日内暴跌 + 15 小时隔夜风险</text>
  <text x="60" y="165" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">次日开盘若低开甚至一字跌停，陷入亏损深渊</text>

  <!-- T+0 Flow -->
  <rect x="410" y="55" width="330" height="145" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
  <text x="430" y="82" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355">美港股 T+0 制度（连续回转止损）</text>
  <text x="430" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">买入后若价格向不利方向波动触发阈值</text>
  <text x="430" y="125" font-family="Inter, sans-serif" font-size="10" fill="#5F7355">✔ 毫秒级市价或限价单反向平仓出局</text>
  <text x="430" y="145" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46">风险敞口立即收敛为零，锁死单笔最大损失</text>
  <text x="430" y="165" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">资金可同日循环利用于高夏普无套利机会</text>
</svg>"""

SVGS["m02_l02_cross_market_hedge_ic"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">现货跌停被困下的跨市场衍生品做空对冲隔离架构</text>

  <!-- Blocked Stock -->
  <rect x="50" y="55" width="220" height="90" rx="6" fill="#FAF0ED" stroke="#CC5A36" stroke-width="2"/>
  <text x="160" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">重仓现货标的跌停</text>
  <text x="160" y="100" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">市值 $1,000 万，Beta = 1.2</text>
  <text x="160" y="120" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="middle">现货卖出通路被锁死</text>

  <!-- Cross Arrow -->
  <path d="M 280 100 L 360 100" stroke="#486A7D" stroke-width="2" marker-end="url(#arrow-generic)" fill="none"/>
  <text x="320" y="92" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#486A7D" text-anchor="middle">对冲传导</text>

  <!-- Futures Hedge -->
  <rect x="370" y="55" width="360" height="90" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="550" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D" text-anchor="middle">中证1000股指期货 (IM) / 股指期权做空</text>
  <text x="550" y="100" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="middle">做空手数 N = round((Notional * Beta) / (Price * 200))</text>
  <text x="550" y="120" font-family="Inter, sans-serif" font-size="10" fill="#5F7355" text-anchor="middle">期货端空头盈利对冲现货次日补跌敞口</text>

  <!-- Bottom Warning -->
  <rect x="50" y="160" width="680" height="50" rx="5" fill="#EFECE6" stroke="#D8D3C8" stroke-width="1"/>
  <text x="70" y="180" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36">⚠️ 基差风险防范（Basis Risk）：</text>
  <text x="70" y="198" font-family="Inter, sans-serif" font-size="9" fill="#4D4B46">股指期货可能存在大幅深幅贴现（Discount），对冲持有存在年化 8%~15% 的滚仓负基差摩擦成本。</text>
</svg>"""

# Lesson 03
SVGS["m02_l03_ofi_flux_calculation"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">Cont-Kukanov-Stoikov (2014) 订单流不平衡 (OFI) 三态物理判别</text>

  <!-- Bid side flux -->
  <rect x="40" y="50" width="330" height="155" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
  <text x="60" y="75" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355">买方订单流净驱动力 I_b(t)</text>
  <text x="60" y="100" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">• Pb(t) &gt; Pb(t-1) ➔ I_b = +qb(t)</text>
  <text x="75" y="118" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">(买一价上跳，激进买单建立新档位)</text>
  <text x="60" y="138" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">• Pb(t) == Pb(t-1) ➔ I_b = qb(t) - qb(t-1)</text>
  <text x="75" y="156" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">(价位未变，净挂单增加或撤单减少)</text>
  <text x="60" y="176" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">• Pb(t) &lt; Pb(t-1) ➔ I_b = -qb(t-1)</text>
  <text x="75" y="194" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">(买一价下破，原买档被卖单全部吃穿)</text>

  <!-- Ask side flux -->
  <rect x="410" y="50" width="330" height="155" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="430" y="75" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36">卖方订单流净驱动力 I_a(t)</text>
  <text x="430" y="100" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">• Pa(t) &lt; Pa(t-1) ➔ I_a = +qa(t)</text>
  <text x="445" y="118" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">(卖一价下跳，激进卖单下压建立新档位)</text>
  <text x="430" y="138" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">• Pa(t) == Pa(t-1) ➔ I_a = qa(t) - qa(t-1)</text>
  <text x="445" y="156" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">(价位未变，卖方净挂单增加)</text>
  <text x="430" y="176" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">• Pa(t) &gt; Pa(t-1) ➔ I_a = -qa(t-1)</text>
  <text x="445" y="194" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">(卖一价抬升，原卖档被买单全部吃空)</text>
</svg>"""

SVGS["m02_l03_kyle_lambda_impact"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <!-- Axis -->
  <line x1="70" y1="120" x2="710" y2="120" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="390" y1="30" x2="390" y2="210" stroke="#7D786F" stroke-width="1.5"/>
  
  <text x="715" y="124" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F">OFI (订单流净买入额)</text>
  <text x="390" y="22" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="middle">Δ P_mid (中间价跳跃)</text>

  <!-- Linear Regression Line -->
  <line x1="120" y1="190" x2="660" y2="50" stroke="#486A7D" stroke-width="3"/>

  <!-- Scatter points -->
  <circle cx="200" cy="165" r="3" fill="#486A7D"/>
  <circle cx="280" cy="140" r="3" fill="#486A7D"/>
  <circle cx="450" cy="105" r="3" fill="#486A7D"/>
  <circle cx="530" cy="80" r="3" fill="#486A7D"/>
  <circle cx="610" cy="60" r="3" fill="#486A7D"/>

  <rect x="470" y="140" width="250" height="60" rx="5" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="485" y="162" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#486A7D">ΔP = β · OFI + ε</text>
  <text x="485" y="182" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">斜率 β 即为微观 Kyle's Lambda</text>
</svg>"""

SVGS["m02_l03_multilevel_ofi_decay"] = """<svg viewBox="0 0 780 220" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="220" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">多档挂单簿加权 OFI 权重指数衰减与虚假诱骗过滤模型</text>

  <!-- Bars for L1 to L5 weight -->
  <g transform="translate(60, 50)">
    <!-- L1 -->
    <rect x="0" y="20" width="100" height="110" rx="4" fill="#486A7D"/>
    <text x="50" y="15" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#486A7D" text-anchor="middle">L1 (1.00)</text>
    <text x="50" y="75" font-family="Inter, sans-serif" font-size="10" fill="#FFFFFF" text-anchor="middle">最高信息量</text>
    <text x="50" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">买卖一档</text>

    <!-- L2 -->
    <rect x="130" y="45" width="100" height="85" rx="4" fill="rgba(72, 106, 125, 0.75)"/>
    <text x="180" y="40" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D" text-anchor="middle">L2 (0.60)</text>
    <text x="180" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">买卖二档</text>

    <!-- L3 -->
    <rect x="260" y="70" width="100" height="60" rx="4" fill="rgba(72, 106, 125, 0.5)"/>
    <text x="310" y="65" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D" text-anchor="middle">L3 (0.36)</text>
    <text x="310" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">买卖三档</text>

    <!-- L4 -->
    <rect x="390" y="90" width="100" height="40" rx="4" fill="rgba(72, 106, 125, 0.35)"/>
    <text x="440" y="85" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D" text-anchor="middle">L4 (0.21)</text>
    <text x="440" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">买卖四档</text>

    <!-- L5 -->
    <rect x="520" y="105" width="100" height="25" rx="4" fill="rgba(72, 106, 125, 0.2)"/>
    <text x="570" y="100" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D" text-anchor="middle">L5 (0.13)</text>
    <text x="570" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">买卖五档</text>
  </g>

  <rect x="60" y="175" width="660" height="32" rx="4" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="390" y="195" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46" text-anchor="middle">权重公式: w_k = exp(-α * (k-1))。深度盘口充斥着大量虚假挂单撤单（Spoofing），必须予以快速衰减过滤。</text>
</svg>"""

# Lesson 04
SVGS["m02_l04_impact_decomposition"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">市场冲击成本正交物理分解：永久冲击 vs 临时冲击</text>

  <!-- Left: Permanent -->
  <rect x="40" y="50" width="330" height="155" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="60" y="78" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#CC5A36">永久市场冲击 (Permanent Impact)</text>
  <text x="60" y="102" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">g(v) = γ · v</text>
  <text x="60" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 成因：母单向全市场透露了知情交易者的信息</text>
  <text x="60" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 性质：不可逆，价格中枢被永久性推高</text>
  <text x="60" y="165" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 影响：全周期拆单的所有后续子单均承受该沉没成本</text>

  <!-- Right: Temporary -->
  <rect x="410" y="50" width="330" height="155" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="430" y="78" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#486A7D">临时市场冲击 (Temporary Impact)</text>
  <text x="430" y="102" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">h(v) = η · v  (或平方根法则 η √v)</text>
  <text x="430" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 成因：子单在瞬时消耗了 LOB 盘口局部流动性深度</text>
  <text x="430" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 性质：可逆，做市商回补挂单后价格迅速均值回归</text>
  <text x="430" y="165" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 影响：仅惩罚当期单笔成交价，均匀 TWAP 可使其极小化</text>
</svg>"""

SVGS["m02_l04_almgren_chriss_curves"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <!-- Axis -->
  <line x1="70" y1="180" x2="710" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="70" y1="30" x2="70" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <text x="60" y="35" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">未执行持仓 x(t)</text>
  <text x="710" y="198" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">时间 t (0 ➔ T)</text>

  <!-- Curve 1: Risk Neutral TWAP (Blue, Linear) -->
  <line x1="70" y1="40" x2="700" y2="180" stroke="#486A7D" stroke-width="2" stroke-dasharray="4 4"/>
  <text x="400" y="100" font-family="Inter, sans-serif" font-size="11" fill="#486A7D">λ = 0 (风险中性: 线性 TWAP，临时冲击最小)</text>

  <!-- Curve 2: Moderate Risk Aversion (Green) -->
  <path d="M 70 40 Q 200 120 700 180" fill="none" stroke="#5F7355" stroke-width="2.5"/>
  <text x="320" y="135" font-family="Inter, sans-serif" font-size="11" fill="#5F7355">λ = 1e-6 (中度风险厌恶: 双曲正弦前置)</text>

  <!-- Curve 3: High Risk Aversion (Terracotta) -->
  <path d="M 70 40 Q 120 160 700 180" fill="none" stroke="#CC5A36" stroke-width="2.5"/>
  <text x="220" y="170" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36">λ = 1e-4 (极度规避价格方差: 激进前置快速甩卖)</text>
</svg>"""

SVGS["m02_l04_vwap_intraday_smile"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">日内成交量 U 型微笑曲线（Volume Smile）与 VWAP 执行配比</text>

  <!-- U Curve -->
  <path d="M 80 60 Q 250 160 390 160 T 700 60" fill="none" stroke="#486A7D" stroke-width="3"/>

  <!-- Volume Bars representing bins -->
  <rect x="80" y="60" width="40" height="110" rx="3" fill="rgba(72, 106, 125, 0.4)"/>
  <text x="100" y="185" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">09:30</text>
  <text x="100" y="50" font-family="Inter, sans-serif" font-size="9" font-weight="bold" fill="#486A7D" text-anchor="middle">开盘高峰</text>

  <rect x="370" y="145" width="40" height="25" rx="3" fill="rgba(72, 106, 125, 0.2)"/>
  <text x="390" y="185" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">13:30</text>
  <text x="390" y="135" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">午盘清淡</text>

  <rect x="660" y="60" width="40" height="110" rx="3" fill="rgba(72, 106, 125, 0.4)"/>
  <text x="680" y="185" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">14:55</text>
  <text x="680" y="50" font-family="Inter, sans-serif" font-size="9" font-weight="bold" fill="#486A7D" text-anchor="middle">尾盘博弈</text>

  <rect x="180" y="200" width="420" height="24" rx="4" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="390" y="216" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">VWAP 算法要求将子单规模严格按历史成交量画像比例加权分配</text>
</svg>"""

# Lesson 05
SVGS["m02_l05_capital_taxonomy"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">A 股市场多源资金生态与持仓久期拓扑图</text>

  <!-- Node 1: Foreign Long Only -->
  <rect x="40" y="55" width="210" height="70" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="145" y="78" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355" text-anchor="middle">北向外资长线 (Long-only)</text>
  <text x="145" y="98" font-family="JetBrains Mono, monospace" font-size="9" fill="#4D4B46" text-anchor="middle">托管于花旗/汇丰/摩根大通</text>
  <text x="145" y="114" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">久期 3~5年 / 重仓高ROIC白马</text>

  <!-- Node 2: Domestic Inst -->
  <rect x="285" y="55" width="210" height="70" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="390" y="78" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D" text-anchor="middle">机构席位 (公募/险资/社保)</text>
  <text x="390" y="98" font-family="JetBrains Mono, monospace" font-size="9" fill="#4D4B46" text-anchor="middle">交易所席位明细显示为“机构专用”</text>
  <text x="390" y="114" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">基本面驱动 / 溢价具备持续性</text>

  <!-- Node 3: Hot Money -->
  <rect x="530" y="55" width="210" height="70" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="635" y="78" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">知名顶级游资 (Hot Money)</text>
  <text x="635" y="98" font-family="JetBrains Mono, monospace" font-size="9" fill="#4D4B46" text-anchor="middle">溧阳路 / 江苏路 / 陆家嘴等</text>
  <text x="635" y="114" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">极限 T+1 隔夜博弈 / 点火涨停</text>

  <!-- Bottom: Retail cluster -->
  <rect x="160" y="145" width="460" height="65" rx="6" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="390" y="170" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">散户大本营集群（拉萨天团 / 东财各营业部）</text>
  <text x="390" y="190" font-family="Inter, sans-serif" font-size="10" fill="#4D4B46" text-anchor="middle">由于软件默认开户，拉萨席位霸榜买入往往意味着主力筹码出逃、散户被动高位接盘</text>
</svg>"""

SVGS["m02_l05_seat_game_matrix"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">龙虎榜席位买卖结构与次日/次周超额胜率博弈矩阵</text>

  <g transform="translate(40, 50)">
    <rect x="0" y="0" width="700" height="30" fill="#EFECE6" rx="4"/>
    <text x="20" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">席位组合形态</text>
    <text x="230" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">资金本质属性</text>
    <text x="450" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">次日开盘溢价</text>
    <text x="590" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B">T+5 胜率判定</text>

    <!-- Row 1 -->
    <line x1="0" y1="60" x2="700" y2="60" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="50" font-family="Inter, sans-serif" font-size="11" fill="#5F7355" font-weight="600">3 家以上机构席位大买</text>
    <text x="230" y="50" font-family="Inter, sans-serif" font-size="11" fill="#4D4B46">公募基本面集体建仓</text>
    <text x="450" y="50" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355">高开率 78%</text>
    <text x="590" y="50" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#5F7355">68% (持续主升)</text>

    <!-- Row 2 -->
    <line x1="0" y1="95" x2="700" y2="95" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="85" font-family="Inter, sans-serif" font-size="11" fill="#486A7D" font-weight="600">顶级游资买一 + 无散户</text>
    <text x="230" y="85" font-family="Inter, sans-serif" font-size="11" fill="#4D4B46">超短热点情绪点火</text>
    <text x="450" y="85" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D">冲高率 85%</text>
    <text x="590" y="85" font-family="JetBrains Mono, monospace" font-size="11" fill="#4D4B46">45% (高波动做T)</text>

    <!-- Row 3 -->
    <line x1="0" y1="130" x2="700" y2="130" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="120" font-family="Inter, sans-serif" font-size="11" fill="#CC5A36" font-weight="600">拉萨席位霸榜买入前四</text>
    <text x="230" y="120" font-family="Inter, sans-serif" font-size="11" fill="#CC5A36">主力出逃 / 散户接盘</text>
    <text x="450" y="120" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">低开核按钮 72%</text>
    <text x="590" y="120" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#CC5A36">18% (筹码崩塌)</text>
  </g>
</svg>"""

SVGS["m02_l05_sentiment_gauge_score"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">多维资金情绪综合打分仪 (0 ~ 100 分) 阈值决策区间</text>

  <!-- Gauge Gradient Bar -->
  <rect x="60" y="60" width="660" height="24" rx="12" fill="#EFECE6"/>
  <rect x="60" y="60" width="220" height="24" rx="12 0 0 12" fill="#CC5A36"/>
  <rect x="280" y="60" width="220" height="24" fill="#486A7D"/>
  <rect x="500" y="60" width="220" height="24" rx="0 12 12 0" fill="#5F7355"/>

  <!-- Markers -->
  <text x="60" y="105" font-family="JetBrains Mono, monospace" font-size="11" fill="#CC5A36">0 分</text>
  <text x="280" y="105" font-family="JetBrains Mono, monospace" font-size="11" fill="#486A7D" text-anchor="middle">45 分 (风险线)</text>
  <text x="500" y="105" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355" text-anchor="middle">75 分 (主升线)</text>
  <text x="720" y="105" font-family="JetBrains Mono, monospace" font-size="11" fill="#5F7355" text-anchor="end">100 分</text>

  <!-- Card 1 -->
  <rect x="60" y="125" width="200" height="80" rx="5" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1"/>
  <text x="160" y="148" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36" text-anchor="middle">Score &lt; 45 分: 高危派发</text>
  <text x="75" y="170" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 两融退潮 / 外资撤离</text>
  <text x="75" y="188" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 散户接盘，坚决清仓规避</text>

  <!-- Card 2 -->
  <rect x="290" y="125" width="200" height="80" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1"/>
  <text x="390" y="148" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#486A7D" text-anchor="middle">45 ~ 75 分: 震荡博弈</text>
  <text x="305" y="170" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 资金多空拉锯 / 轮动较快</text>
  <text x="305" y="188" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 控制杠杆，等待明确共振</text>

  <!-- Card 3 -->
  <rect x="520" y="125" width="200" height="80" rx="5" fill="#FFFFFF" stroke="#5F7355" stroke-width="1"/>
  <text x="620" y="148" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#5F7355" text-anchor="middle">Score &gt; 75 分: 强力多头</text>
  <text x="535" y="170" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 机构加仓 + 融资积极买入</text>
  <text x="535" y="188" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 筹码高度集中，顺势做多</text>
</svg>"""

# ==============================================================================
# MODULE 03: FUNDAMENTAL & VALUATION (15 SVGs)
# ==============================================================================

# Lesson 01
SVGS["m03_l01_three_statements_articulation"] = """<svg viewBox="0 0 780 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="250" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="15" font-weight="bold" fill="#1F1E1B">企业三张财务报表底层跨期动态勾稽平衡闭环图</text>

  <!-- Balance Sheet -->
  <rect x="40" y="55" width="210" height="170" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="145" y="80" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#486A7D" text-anchor="middle">资产负债表 (Balance Sheet)</text>
  <text x="55" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 资产 = 负债 + 所有者权益</text>
  <text x="55" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 货币资金余额 (Cash)</text>
  <text x="55" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 留存收益 (Retained Earnings)</text>
  <text x="55" y="165" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 营运资本 (NWC = CA - CL)</text>
  <text x="55" y="195" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F">静态资产价值底册</text>

  <!-- Connect 1 -->
  <path d="M 250 145 L 290 145" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Income Statement -->
  <rect x="295" y="55" width="200" height="170" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="395" y="80" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#CC5A36" text-anchor="middle">利润表 (Income Statement)</text>
  <text x="310" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 营业收入 Revenue</text>
  <text x="310" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 营业利润 EBIT</text>
  <text x="310" y="145" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36">• 净利润 Net Income</text>
  <rect x="305" y="160" width="180" height="45" rx="4" fill="#FAF0ED"/>
  <text x="395" y="178" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36" text-anchor="middle">ΔRE = 净利润 - 现金分红</text>
  <text x="395" y="195" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">权益增量勾稽纽带</text>

  <!-- Connect 2 -->
  <path d="M 495 145 L 535 145" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Cash Flow -->
  <rect x="540" y="55" width="200" height="170" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="640" y="80" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#5F7355" text-anchor="middle">现金流量表 (Cash Flow)</text>
  <text x="555" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 经营现金流 CFO</text>
  <text x="555" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 投资现金流 CFI</text>
  <text x="555" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 筹资现金流 CFF</text>
  <rect x="550" y="160" width="180" height="45" rx="4" fill="#EFECE6"/>
  <text x="640" y="178" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355" text-anchor="middle">ΔCash = CFO + CFI + CFF</text>
  <text x="640" y="195" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">直接配平资产负债表现金项</text>
</svg>"""

SVGS["m03_l01_dupont_five_factor_tree"] = """<svg viewBox="0 0 780 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="250" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">现代杜邦五因子 (DuPont 5-Factor) 分解树与驱动力映射</text>

  <!-- Top ROE -->
  <rect x="290" y="45" width="200" height="40" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="390" y="70" font-family="Newsreader, serif" font-size="15" font-weight="bold" fill="#1F1E1B" text-anchor="middle">ROE 净资产收益率</text>

  <!-- 5 Branch Lines -->
  <line x1="390" y1="85" x2="390" y2="110" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="100" y1="110" x2="680" y2="110" stroke="#7D786F" stroke-width="1.5"/>
  
  <line x1="100" y1="110" x2="100" y2="135" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="245" y1="110" x2="245" y2="135" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="390" y1="110" x2="390" y2="135" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="535" y1="110" x2="535" y2="135" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="680" y1="110" x2="680" y2="135" stroke="#7D786F" stroke-width="1.5"/>

  <!-- Box 1 -->
  <rect x="40" y="135" width="120" height="85" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="100" y="155" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B" text-anchor="middle">1. 税收负担</text>
  <text x="100" y="172" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D" text-anchor="middle">NI / EBT</text>
  <text x="100" y="195" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">税收优惠与壁垒</text>

  <!-- Box 2 -->
  <rect x="185" y="135" width="120" height="85" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
  <text x="245" y="155" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B" text-anchor="middle">2. 利息负担</text>
  <text x="245" y="172" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D" text-anchor="middle">EBT / EBIT</text>
  <text x="245" y="195" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">有息债务利息侵蚀</text>

  <!-- Box 3 -->
  <rect x="330" y="135" width="120" height="85" rx="5" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="390" y="155" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#5F7355" text-anchor="middle">3. 营业利润率</text>
  <text x="390" y="172" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355" text-anchor="middle">EBIT / Rev</text>
  <text x="390" y="195" font-family="Inter, sans-serif" font-size="9" font-weight="bold" fill="#5F7355" text-anchor="middle">核心护城河定价权</text>

  <!-- Box 4 -->
  <rect x="475" y="135" width="120" height="85" rx="5" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="535" y="155" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#5F7355" text-anchor="middle">4. 资产周转率</text>
  <text x="535" y="172" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355" text-anchor="middle">Rev / Assets</text>
  <text x="535" y="195" font-family="Inter, sans-serif" font-size="9" font-weight="bold" fill="#5F7355" text-anchor="middle">运营与供应链效率</text>

  <!-- Box 5 -->
  <rect x="620" y="135" width="120" height="85" rx="5" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="680" y="155" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36" text-anchor="middle">5. 权益乘数</text>
  <text x="680" y="172" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36" text-anchor="middle">Assets / Equity</text>
  <text x="680" y="195" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36" text-anchor="middle">财务杠杆双刃剑</text>
</svg>"""

SVGS["m03_l01_accrual_vs_cash_gap"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">应计盈余 vs 经营现金流剪刀差：间接法 CFO 拆解红线</text>

  <rect x="50" y="55" width="200" height="140" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="150" y="80" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#CC5A36" text-anchor="middle">净利润 Net Income</text>
  <text x="70" y="110" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 权责发生制核算</text>
  <text x="70" y="130" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 允许赊销确认收入</text>
  <text x="70" y="150" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36">• 极易人为提前透支</text>

  <!-- Adjustments in middle -->
  <g transform="translate(270, 60)">
    <rect x="0" y="0" width="240" height="32" rx="4" fill="#EFECE6"/>
    <text x="120" y="20" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">+ 折旧与摊销 (非现金支出)</text>

    <rect x="0" y="42" width="240" height="40" rx="4" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1"/>
    <text x="120" y="58" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">- 营运资本增加 (ΔNWC &gt; 0)</text>
    <text x="120" y="74" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">应收账款暴增 + 存货积压抽血</text>

    <rect x="0" y="92" width="240" height="32" rx="4" fill="#EFECE6"/>
    <text x="120" y="112" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">= 经营活动现金流量净额 CFO</text>
  </g>

  <!-- Right: Warning -->
  <rect x="530" y="55" width="200" height="140" rx="6" fill="#FAF0ED" stroke="#CC5A36" stroke-width="2"/>
  <text x="630" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">暴雷红线预警</text>
  <text x="545" y="110" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">若连续多年：</text>
  <text x="545" y="130" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#CC5A36">CFO &lt; 净利润</text>
  <text x="545" y="155" font-family="Inter, sans-serif" font-size="9" fill="#4D4B46">利润充斥账面纸面财富，真实购买力竭尽，极易陷入庞氏融资。</text>
</svg>"""

# Lesson 02
SVGS["m03_l02_beneish_eight_pillars"] = """<svg viewBox="0 0 780 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="250" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">Beneish M-Score 财务舞弊排雷预警 8 维指标雷达矩阵</text>

  <g transform="translate(40, 50)">
    <!-- Row 1 -->
    <rect x="0" y="0" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="80" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36" text-anchor="middle">DSRI 应收账款指数</text>
    <text x="80" y="44" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">权重: +0.920</text>
    <text x="80" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">激进确认收入 / 塞货</text>

    <rect x="180" y="0" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="260" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36" text-anchor="middle">GMI 毛利率恶化指数</text>
    <text x="260" y="44" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">权重: +0.528</text>
    <text x="260" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">基本面承压造假动机</text>

    <rect x="360" y="0" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
    <text x="440" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#486A7D" text-anchor="middle">AQI 资产质量恶化</text>
    <text x="440" y="44" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">权重: +0.404</text>
    <text x="440" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">非硬资产/研发资本化</text>

    <rect x="540" y="0" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
    <text x="620" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#486A7D" text-anchor="middle">SGI 营收高速增长</text>
    <text x="620" y="44" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">权重: +0.892</text>
    <text x="620" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">增长失速时造假高发</text>

    <!-- Row 2 -->
    <rect x="0" y="90" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#7D786F" stroke-width="1.5"/>
    <text x="80" y="114" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B" text-anchor="middle">DEPI 折旧率放缓</text>
    <text x="80" y="134" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">权重: +0.115</text>
    <text x="80" y="152" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">拉长折旧年限虚增利润</text>

    <rect x="180" y="90" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#7D786F" stroke-width="1.5"/>
    <text x="260" y="114" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B" text-anchor="middle">SGAI 期间费用失调</text>
    <text x="260" y="134" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">权重: -0.172</text>
    <text x="260" y="152" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">费控效率边际走弱</text>

    <rect x="360" y="90" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
    <text x="440" y="114" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36" text-anchor="middle">TATA 核心应计比率</text>
    <text x="440" y="134" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">权重: +4.037 (最关键)</text>
    <text x="440" y="152" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36" text-anchor="middle">(NI - CFO) / Assets</text>

    <rect x="540" y="90" width="160" height="75" rx="5" fill="#FFFFFF" stroke="#7D786F" stroke-width="1.5"/>
    <text x="620" y="114" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1F1E1B" text-anchor="middle">LVGI 财务杠杆跳升</text>
    <text x="620" y="134" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46" text-anchor="middle">权重: +0.0327</text>
    <text x="620" y="152" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">违反债务契约风险</text>
  </g>

  <!-- Threshold note -->
  <text x="40" y="235" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#CC5A36">判别界限：M-Score &gt; -1.78 即触发高舞弊概率预警（如安然暴雷前为 -1.49）</text>
</svg>"""

SVGS["m03_l02_deposit_loan_paradox"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">A 股典型财务造假形态：“存贷双高”（大存大贷）资金体外循环拓扑</text>

  <rect x="50" y="55" width="220" height="90" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="160" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">账面资产：巨额货币资金</text>
  <text x="160" y="100" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B" text-anchor="middle">账面躺着 100 亿元现金</text>
  <text x="160" y="120" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">年化利息收入却极低 (&lt; 0.5%)</text>

  <rect x="510" y="55" width="220" height="90" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="620" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">账面负债：巨额短期借款</text>
  <text x="620" y="100" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B" text-anchor="middle">同时借入 80 亿元高息短贷</text>
  <text x="620" y="120" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36" text-anchor="middle">每年刚性支出数亿元利息费用</text>

  <!-- Paradox Box -->
  <rect x="290" y="70" width="200" height="60" rx="5" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="390" y="94" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36" text-anchor="middle">反常逻辑悖论！</text>
  <text x="390" y="112" font-family="Inter, sans-serif" font-size="9" fill="#4D4B46" text-anchor="middle">有钱不用却借高息贷款？</text>

  <rect x="50" y="165" width="680" height="48" rx="4" fill="#FFFFFF" stroke="#D8D3C8" stroke-width="1"/>
  <text x="70" y="185" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1F1E1B">微观真实真相（康美/康得新案）：</text>
  <text x="70" y="202" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">所谓“百亿存款”属于伪造虚假对账单，或早已被大股东私自质押担保受限，属于严重欺诈。</text>
</svg>"""

SVGS["m03_l02_inventory_margin_divergence"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">经典造假形态：“存货周转天数逆势飙升 + 毛利率反常走高”背离排雷</text>

  <!-- Dual Divergence Lines -->
  <line x1="80" y1="180" x2="700" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="80" y1="40" x2="80" y2="180" stroke="#7D786F" stroke-width="1.5"/>

  <!-- Inventory Days Up (Terracotta) -->
  <path d="M 90 150 Q 250 130 420 90 T 680 45" fill="none" stroke="#CC5A36" stroke-width="2.5"/>
  <text x="685" y="48" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#CC5A36">存货周转天数狂飙 (滞销堆积)</text>

  <!-- Gross Margin Up (Blue, Abnormal) -->
  <path d="M 90 140 Q 250 110 420 70 T 680 30" fill="none" stroke="#486A7D" stroke-width="2.5" stroke-dasharray="4 2"/>
  <text x="685" y="30" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#486A7D">虚增毛利率 (反常飙升)</text>

  <rect x="180" y="110" width="380" height="50" rx="5" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1"/>
  <text x="370" y="130" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">商业逻辑违背：产品卖不动，毛利率怎可能暴涨？</text>
  <text x="370" y="148" font-family="Inter, sans-serif" font-size="9" fill="#4D4B46" text-anchor="middle">操纵手段：少结转当期营业成本，将生产成本蓄意囤积在存货资产中虚增当期毛利。</text>
</svg>"""

# Lesson 03
SVGS["m03_l03_roic_wacc_spread_eva"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">商业护城河量化第一性原理：ROIC - WACC 超额利差与 EVA 财富创造</text>

  <g transform="translate(60, 55)">
    <!-- Wide Moat Company -->
    <rect x="0" y="0" width="280" height="135" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
    <text x="140" y="25" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355" text-anchor="middle">宽护城河企业 (Wide Moat)</text>
    <rect x="20" y="40" width="240" height="24" rx="4" fill="#EFECE6"/>
    <text x="140" y="56" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355" text-anchor="middle">ROIC = 24.5% &gt;&gt; WACC = 8.5%</text>
    <text x="30" y="85" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 超额利差 Spread = +16.0%</text>
    <text x="30" y="105" font-family="Inter, sans-serif" font-size="10" fill="#5F7355" font-weight="bold">• 经济增加值 EVA &gt; 0 : 真实复利增值</text>
    <text x="30" y="125" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">扩产追加投资 = 放大股东财富！</text>

    <!-- Value Destroying Company -->
    <rect x="360" y="0" width="280" height="135" rx="6" fill="#FAF0ED" stroke="#CC5A36" stroke-width="2"/>
    <text x="500" y="25" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">价值毁灭企业 (No Moat / 陷阱)</text>
    <rect x="380" y="40" width="240" height="24" rx="4" fill="#FFFFFF"/>
    <text x="500" y="56" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="middle">ROIC = 5.2% &lt; WACC = 8.5%</text>
    <text x="390" y="85" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 负利差 Spread = -3.3%</text>
    <text x="390" y="105" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36" font-weight="bold">• 经济增加值 EVA &lt; 0 : 账面有利润实亏</text>
    <text x="390" y="125" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36">盲目扩产投资 = 加速毁灭股东财富！</text>
  </g>
</svg>"""

SVGS["m03_l03_moat_decay_curves"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <!-- Axis -->
  <line x1="70" y1="180" x2="710" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <line x1="70" y1="30" x2="70" y2="180" stroke="#7D786F" stroke-width="1.5"/>
  <text x="60" y="35" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">ROIC %</text>
  <text x="710" y="198" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">时间 (年: 1 ➔ 20)</text>

  <!-- WACC line -->
  <line x1="70" y1="140" x2="710" y2="140" stroke="#7D786F" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="715" y="144" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F">WACC 资本成本底线 (8%)</text>

  <!-- Curve 1: Wide Moat (Green) -->
  <path d="M 80 40 Q 300 45 700 80" fill="none" stroke="#5F7355" stroke-width="3"/>
  <text x="450" y="65" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#5F7355">宽护城河 (λ=0.03): 20年持久超额收益</text>

  <!-- Curve 2: Narrow Moat (Blue) -->
  <path d="M 80 50 Q 250 90 700 135" fill="none" stroke="#486A7D" stroke-width="2"/>
  <text x="350" y="105" font-family="Inter, sans-serif" font-size="11" fill="#486A7D">窄护城河 (λ=0.10): 8~10年回归均值</text>

  <!-- Curve 3: No Moat (Terracotta) -->
  <path d="M 80 60 Q 150 135 700 140" fill="none" stroke="#CC5A36" stroke-width="2"/>
  <text x="210" y="155" font-family="Inter, sans-serif" font-size="11" fill="#CC5A36">无壁垒代工 (λ=0.30): 3年抹平利润</text>
</svg>"""

SVGS["m03_l03_invested_capital_balance"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">投入资本 (Invested Capital) 资产端与融资端会计守恒天平</text>

  <!-- Asset Side -->
  <rect x="50" y="55" width="310" height="140" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="205" y="80" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#486A7D" text-anchor="middle">资产端透视 (Operating Perspective)</text>
  <text x="70" y="108" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B">IC = 净营运资本(NWC) + 固定资产(PP&amp;E)</text>
  <text x="95" y="126" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B">+ 无形资产 - 超额闲置现金</text>
  <text x="70" y="155" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 衡量实际投入企业日常运营的真金白银</text>
  <text x="70" y="175" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 剔除理财金融资产与无息应付款</text>

  <text x="390" y="130" font-family="Inter, sans-serif" font-size="24" font-weight="bold" fill="#7D786F" text-anchor="middle">≡</text>

  <!-- Financing Side -->
  <rect x="420" y="55" width="310" height="140" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="575" y="80" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#5F7355" text-anchor="middle">融资端透视 (Financing Perspective)</text>
  <text x="440" y="108" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B">IC = 股东权益总额 (Equity)</text>
  <text x="465" y="126" font-family="JetBrains Mono, monospace" font-size="11" fill="#1F1E1B">+ 有息负债 (Total Debt) - 现金</text>
  <text x="440" y="155" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 衡量债权人与股东投入的总资本金</text>
  <text x="440" y="175" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 与资产端严格恒等守恒！</text>
</svg>"""

# Lesson 04
SVGS["m03_l04_two_stage_dcf_timeline"] = """<svg viewBox="0 0 780 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="240" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">两阶段现金流折现 (DCF) 估值模型时间轴架构</text>

  <!-- Stage 1 Explicit Forecast -->
  <rect x="50" y="50" width="380" height="120" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="240" y="75" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D" text-anchor="middle">阶段 1: 显性预测期 (年 1 ~ 5)</text>
  <text x="70" y="100" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">PV_Forecast = ∑ [ FCFF_t / (1 + WACC)^t ]</text>
  <text x="70" y="125" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 逐年精细测算：营收、毛利、EBIT、CapEx与NWC</text>
  <text x="70" y="145" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 占企业价值比重通常仅为 20%~35%</text>

  <!-- Stage 2 Terminal Value -->
  <rect x="460" y="50" width="270" height="120" rx="6" fill="#FFFFFF" stroke="#CC5A36" stroke-width="2"/>
  <text x="595" y="75" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#CC5A36" text-anchor="middle">阶段 2: 永续终值期 (TV)</text>
  <text x="475" y="100" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">TV = FCFF_5 * (1+g) / (WACC - g)</text>
  <text x="475" y="125" font-family="Inter, sans-serif" font-size="10" fill="#7D786F">• 戈登增长模型 (g &lt; WACC)</text>
  <text x="475" y="145" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36">• 占估值比重高达 65%~80%！</text>

  <!-- Bottom Equities Bridge -->
  <rect x="50" y="185" width="680" height="40" rx="5" fill="#EFECE6" stroke="#D8D3C8" stroke-width="1"/>
  <text x="390" y="210" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#1F1E1B" text-anchor="middle">股权内在价值 Equity Value = 企业价值 EV (PV_Forecast + PV_TV) - 净有息负债 Net Debt</text>
</svg>"""

SVGS["m03_l04_wacc_sensitivity_matrix"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">估值敏感性热力矩阵：WACC 与永续增长率 g 双变量网格</text>

  <g transform="translate(60, 48)">
    <rect x="0" y="0" width="660" height="30" fill="#EFECE6" rx="4"/>
    <text x="40" y="20" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#1F1E1B">每股内在价值(元)</text>
    <text x="180" y="20" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46">g = 1.5%</text>
    <text x="300" y="20" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46">g = 2.0%</text>
    <text x="420" y="20" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#486A7D">g = 2.5% (基准)</text>
    <text x="540" y="20" font-family="JetBrains Mono, monospace" font-size="10" fill="#4D4B46">g = 3.0%</text>

    <!-- Row 1 WACC 8.0% -->
    <line x1="0" y1="60" x2="660" y2="60" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="52" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">WACC 8.0%</text>
    <text x="180" y="52" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">52.4 元</text>
    <text x="300" y="52" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">58.1 元</text>
    <text x="420" y="52" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">65.2 元</text>
    <text x="540" y="52" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">74.6 元</text>

    <!-- Row 2 WACC 9.0% Base -->
    <line x1="0" y1="95" x2="660" y2="95" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="87" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#486A7D">WACC 9.0% (基准)</text>
    <text x="180" y="87" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">44.8 元</text>
    <text x="300" y="87" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">49.0 元</text>
    <text x="420" y="87" font-family="JetBrains Mono, monospace" font-size="11" font-weight="bold" fill="#486A7D">54.2 元 ★中枢</text>
    <text x="540" y="87" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">60.6 元</text>

    <!-- Row 3 WACC 10.0% -->
    <line x1="0" y1="130" x2="660" y2="130" stroke="#D8D3C8" stroke-width="1"/>
    <text x="20" y="122" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">WACC 10.0%</text>
    <text x="180" y="122" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">38.9 元</text>
    <text x="300" y="122" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">42.1 元</text>
    <text x="420" y="122" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">46.0 元</text>
    <text x="540" y="122" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">50.7 元</text>
  </g>

  <text x="60" y="210" font-family="Inter, sans-serif" font-size="10" fill="#CC5A36">投决会结论：贴现率变动 ±1% 将引起每股内在价值 ±20% 的巨幅摇摆，必须进行概率区间定价。</text>
</svg>"""

SVGS["m03_l04_monte_carlo_valuation_dist"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">蒙特卡洛 10,000 次模拟内在价值概率密度分布与安全边际置信带</text>

  <!-- Bell Curve -->
  <path d="M 80 180 Q 250 180 340 90 T 400 45 T 460 90 Q 550 180 720 180" fill="none" stroke="#486A7D" stroke-width="2.5"/>

  <!-- Shaded 90% confidence -->
  <line x1="260" y1="50" x2="260" y2="180" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="260" y="195" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="middle">5%分位数: 39.5元</text>

  <line x1="400" y1="45" x2="400" y2="180" stroke="#5F7355" stroke-width="2"/>
  <text x="400" y="195" font-family="JetBrains Mono, monospace" font-size="10" font-weight="bold" fill="#5F7355" text-anchor="middle">50%中位数: 53.8元</text>

  <line x1="540" y1="50" x2="540" y2="180" stroke="#486A7D" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="540" y="195" font-family="JetBrains Mono, monospace" font-size="10" fill="#486A7D" text-anchor="middle">95%分位数: 69.2元</text>

  <rect x="80" y="60" width="160" height="40" rx="4" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1"/>
  <text x="160" y="84" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">买入安全边际 P &lt; 39.5元</text>
</svg>"""

# Lesson 05
SVGS["m03_l05_multiples_decision_tree"] = """<svg viewBox="0 0 780 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="240" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">相对估值乘数家族 (PE / PB / PS / EV-EBITDA / PEG) 行业适用性决策树</text>

  <!-- 5 Cards -->
  <g transform="translate(40, 50)">
    <!-- PE -->
    <rect x="0" y="0" width="130" height="160" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
    <text x="65" y="25" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D" text-anchor="middle">P/E 市盈率</text>
    <text x="15" y="50" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 适用：消费/蓝筹</text>
    <text x="15" y="70" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 盈利平稳持续</text>
    <text x="15" y="90" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 资本结构相似</text>
    <text x="15" y="125" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36">⚠️ 禁忌：周期股顶峰</text>

    <!-- PB -->
    <rect x="145" y="0" width="130" height="160" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
    <text x="210" y="25" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D" text-anchor="middle">P/B 市净率</text>
    <text x="160" y="50" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 适用：银行/重工业</text>
    <text x="160" y="70" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• PB-ROE 联动框架</text>
    <text x="160" y="90" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 强周期品破净</text>
    <text x="160" y="125" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36">⚠️ 禁忌：轻资产SaaS</text>

    <!-- PS -->
    <rect x="290" y="0" width="130" height="160" rx="5" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
    <text x="355" y="25" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355" text-anchor="middle">P/S 市销率</text>
    <text x="305" y="50" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 适用：SaaS/创新药</text>
    <text x="305" y="70" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 高增长未盈利</text>
    <text x="305" y="90" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 抢占市场份额期</text>
    <text x="305" y="125" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36">⚠️ 禁忌：毛利过薄行业</text>

    <!-- EV/EBITDA -->
    <rect x="435" y="0" width="130" height="160" rx="5" fill="#FFFFFF" stroke="#486A7D" stroke-width="1.5"/>
    <text x="500" y="25" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D" text-anchor="middle">EV/EBITDA</text>
    <text x="450" y="50" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 适用：跨国并购/基建</text>
    <text x="450" y="70" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 剔除折旧与利息</text>
    <text x="450" y="90" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 资本结构中性</text>
    <text x="450" y="125" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">高杠杆重资产利器</text>

    <!-- PEG -->
    <rect x="580" y="0" width="120" height="160" rx="5" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
    <text x="640" y="25" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355" text-anchor="middle">PEG</text>
    <text x="595" y="50" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• GARP 策略</text>
    <text x="595" y="70" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• PEG &lt; 1.0 低估</text>
    <text x="595" y="90" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• PEG &gt; 2.0 透支</text>
    <text x="595" y="125" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">彼得林奇经典准则</text>
  </g>
</svg>"""

SVGS["m03_l05_cyclical_pe_inversion"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">强周期股“估值反转之谜”：景气顶峰低 PE 陷阱 vs 景气冰点高/负 PE 黄金坑</text>

  <!-- Cycle Sine Curve -->
  <path d="M 80 140 Q 230 20 380 140 T 680 140" fill="none" stroke="#486A7D" stroke-width="2.5"/>

  <!-- Peak (Low PE Trap) -->
  <circle cx="230" cy="80" r="6" fill="#CC5A36"/>
  <rect x="140" y="15" width="180" height="50" rx="4" fill="#FAF0ED" stroke="#CC5A36" stroke-width="1.5"/>
  <text x="230" y="35" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#CC5A36" text-anchor="middle">景气大顶：PE = 2~3 倍 ❌</text>
  <text x="230" y="52" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">利润爆表 / 貌似极度低估实为大顶</text>

  <!-- Trough (High PE Buy) -->
  <circle cx="530" cy="200" r="6" fill="#5F7355"/>
  <rect x="440" y="170" width="180" height="50" rx="4" fill="#FFFFFF" stroke="#5F7355" stroke-width="1.5"/>
  <text x="530" y="190" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#5F7355" text-anchor="middle">景气冰点：PE 畸高或亏损 ✔</text>
  <text x="530" y="207" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">全行业巨亏出清 / PB 见底黄金买点</text>
</svg>"""

SVGS["m03_l05_value_trap_defense"] = """<svg viewBox="0 0 780 230" width="100%" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect width="780" height="230" fill="#FAF9F5" rx="8" stroke="#D8D3C8" stroke-width="1"/>
  
  <text x="40" y="32" font-family="Newsreader, serif" font-size="14" font-weight="bold" fill="#1F1E1B">量化相对估值横截面“价值陷阱（Value Trap）”防御与质量过滤架构</text>

  <!-- Step 1 Raw Multiples -->
  <rect x="40" y="55" width="180" height="120" rx="6" fill="#FFFFFF" stroke="#7D786F" stroke-width="1.5"/>
  <text x="130" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#1F1E1B" text-anchor="middle">1. 行业横截面 Z-Score</text>
  <text x="55" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 行业细分 PE / PB 偏离度</text>
  <text x="55" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 寻找低估值低分位数标的</text>
  <text x="55" y="150" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36">⚠️ 风险：便宜往往因质次</text>

  <line x1="225" y1="115" x2="265" y2="115" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Step 2 Quality Gate -->
  <rect x="270" y="55" width="220" height="120" rx="6" fill="#FFFFFF" stroke="#5F7355" stroke-width="2"/>
  <text x="380" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#5F7355" text-anchor="middle">2. 基本面质量过滤器 (Gate)</text>
  <text x="285" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">✔ ROIC &gt; 10% (具有资本回报门槛)</text>
  <text x="285" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">✔ 利息保障倍数 &gt; 3.0x (无偿债危机)</text>
  <text x="285" y="145" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">✔ 盈利预测下修动量无断崖恶化</text>

  <line x1="495" y1="115" x2="535" y2="115" stroke="#7D786F" stroke-width="1.5" marker-end="url(#arrow-generic)"/>

  <!-- Step 3 Final Alpha Portfolio -->
  <rect x="540" y="55" width="200" height="120" rx="6" fill="#FFFFFF" stroke="#486A7D" stroke-width="2"/>
  <text x="640" y="80" font-family="Inter, sans-serif" font-size="12" font-weight="bold" fill="#486A7D" text-anchor="middle">3. 均值回归阿尔法组合</text>
  <text x="555" y="105" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 剔除价值陷阱僵尸企业</text>
  <text x="555" y="125" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">• 保留真正被错杀的优质龙头</text>
  <text x="555" y="150" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#5F7355">• 夏普比率显著提升</text>
</svg>"""

def main():
    print(f"Generating {len(SVGS)} high-texture SVGs...")
    
    # Target folders
    folders = {
        "m01": (os.path.join(BASE_DIR, "01_macro_cycle", "assets"), os.path.join(BASE_DIR, "web", "assets", "01_macro_cycle")),
        "m02": (os.path.join(BASE_DIR, "02_micro_market", "assets"), os.path.join(BASE_DIR, "web", "assets", "02_micro_market")),
        "m03": (os.path.join(BASE_DIR, "03_fundamental", "assets"), os.path.join(BASE_DIR, "web", "assets", "03_fundamental")),
    }
    
    for mod_key, (local_dir, web_dir) in folders.items():
        os.makedirs(local_dir, exist_ok=True)
        os.makedirs(web_dir, exist_ok=True)

    generated = 0
    for name, content in SVGS.items():
        mod_prefix = name[:3]
        if mod_prefix in folders:
            local_dir, web_dir = folders[mod_prefix]
            file_name = f"{name}.svg"
            local_path = os.path.join(local_dir, file_name)
            web_path = os.path.join(web_dir, file_name)
            
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")
            with open(web_path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")
            generated += 1

    print(f"✅ Successfully generated and synced {generated} SVG diagrams across local and web directories!")

if __name__ == "__main__":
    main()
