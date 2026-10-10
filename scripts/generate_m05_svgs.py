#!/usr/bin/env python3
"""
生成模块 05 (量化多因子与统计套利) 配套高质感 Anthropic 风格 SVG 矢量图
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
SVGS["m05_l01_factor_evaluation_pipeline"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.1.1：生产级单因子数据清洗与正交预处理流水线 (Factor Pipeline)</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">FACTOR PREPROCESSING</text>

  <!-- Step 1: Raw Factor -->
  <g transform="translate(35, 60)">
    <rect x="0" y="0" width="150" height="135" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <rect x="0" y="0" width="150" height="28" rx="6" fill="#486A7D"/>
    <text x="75" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">1. 原始因子抽取</text>
    <text x="12" y="52" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#1F1E1B">Raw Score X_i</text>
    <text x="12" y="74" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 财务/价量/分析师</text>
    <text x="12" y="94" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 包含极值与缺失</text>
    <text x="12" y="114" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D">N ≈ 5000 股票</text>
  </g>

  <path d="M 195 127 L 220 127" stroke="#7D786F" stroke-width="2"/>

  <!-- Step 2: Winsorization MAD -->
  <g transform="translate(230, 60)">
    <rect x="0" y="0" width="150" height="135" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <rect x="0" y="0" width="150" height="28" rx="6" fill="#CC5A36"/>
    <text x="75" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">2. MAD 去极值</text>
    <text x="12" y="52" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#1F1E1B">Median Absolute Dev</text>
    <text x="12" y="74" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 阈值: med ± 3*1.4826*MAD</text>
    <text x="12" y="94" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 压制极端异常值</text>
    <text x="12" y="114" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">Non-Gaussian Clip</text>
  </g>

  <path d="M 390 127 L 415 127" stroke="#7D786F" stroke-width="2"/>

  <!-- Step 3: Standardization -->
  <g transform="translate(425, 60)">
    <rect x="0" y="0" width="150" height="135" rx="6" fill="#FAF8F5" stroke="#C08535" stroke-width="1.5"/>
    <rect x="0" y="0" width="150" height="28" rx="6" fill="#C08535"/>
    <text x="75" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">3. 截面标准化</text>
    <text x="12" y="52" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#1F1E1B">Z-Score Transform</text>
    <text x="12" y="74" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• (X - mean) / std</text>
    <text x="12" y="94" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 消除不同维度量纲</text>
    <text x="12" y="114" font-family="JetBrains Mono, monospace" font-size="9" fill="#C08535">μ = 0, σ = 1</text>
  </g>

  <path d="M 585 127 L 610 127" stroke="#7D786F" stroke-width="2"/>

  <!-- Step 4: Neutralization -->
  <g transform="translate(620, 60)">
    <rect x="0" y="0" width="115" height="135" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <rect x="0" y="0" width="115" height="28" rx="6" fill="#5F7355"/>
    <text x="57" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">4. 行业市值中性化</text>
    <text x="8" y="52" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B">OLS 残差剥离</text>
    <text x="8" y="74" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">X = β*Ind + γ*Size + ε</text>
    <text x="8" y="94" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">纯净纯 Alpha 残差</text>
    <text x="8" y="114" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#5F7355">Pure Factor ε_i</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">未经过行业与市值中性化的因子，绝大多数只是在被动裸露大盘蓝筹或行业贝塔风险</text>
</svg>"""

SVGS["m05_l01_rank_ic_distribution"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.1.2：截面 Rank IC 时序分布与 IR (信息比率) 稳定性检验</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">RANK IC &amp; IR STATS</text>

  <!-- Left: Time Series Bar Chart -->
  <g transform="translate(60, 50)">
    <line x1="0" y1="80" x2="380" y2="80" stroke="#1F1E1B" stroke-width="1.5"/>
    <text x="-10" y="84" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">0.0</text>
    <text x="-10" y="30" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355" text-anchor="end">+0.10</text>
    <text x="-10" y="130" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="end">-0.10</text>

    <!-- Monthly IC Bars -->
    <!-- Positive bars -->
    <rect x="15" y="45" width="12" height="35" fill="#5F7355"/>
    <rect x="35" y="35" width="12" height="45" fill="#5F7355"/>
    <rect x="55" y="50" width="12" height="30" fill="#5F7355"/>
    <rect x="75" y="25" width="12" height="55" fill="#5F7355"/>
    <!-- Negative bar -->
    <rect x="95" y="80" width="12" height="20" fill="#CC5A36"/>
    <rect x="115" y="40" width="12" height="40" fill="#5F7355"/>
    <rect x="135" y="30" width="12" height="50" fill="#5F7355"/>
    <rect x="155" y="55" width="12" height="25" fill="#5F7355"/>
    <rect x="175" y="80" width="12" height="15" fill="#CC5A36"/>
    <rect x="195" y="38" width="12" height="42" fill="#5F7355"/>
    <rect x="215" y="48" width="12" height="32" fill="#5F7355"/>
    <rect x="235" y="28" width="12" height="52" fill="#5F7355"/>
    <rect x="255" y="35" width="12" height="45" fill="#5F7355"/>
    <rect x="275" y="80" width="12" height="25" fill="#CC5A36"/>
    <rect x="295" y="42" width="12" height="38" fill="#5F7355"/>
    <rect x="315" y="30" width="12" height="50" fill="#5F7355"/>
    <rect x="335" y="45" width="12" height="35" fill="#5F7355"/>
    <rect x="355" y="50" width="12" height="30" fill="#5F7355"/>

    <!-- Mean IC Line -->
    <line x1="0" y1="48" x2="380" y2="48" stroke="#C08535" stroke-width="2" stroke-dasharray="4 3"/>
    <text x="390" y="52" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535">Mean Rank IC = 0.052</text>
  </g>

  <!-- Right: Metrics Scoreboard -->
  <g transform="translate(520, 50)">
    <rect x="0" y="0" width="200" height="145" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    <text x="16" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#1F1E1B">投决会核心评价硬指标：</text>
    
    <text x="16" y="50" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">IC Mean: <tspan font-weight="700" fill="#5F7355">+0.052 (&gt;0.03及格)</tspan></text>
    <text x="16" y="72" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">IC Std:  <tspan font-weight="700">0.078</tspan></text>
    <text x="16" y="94" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">IR (IC/Std): <tspan font-weight="700" fill="#CC5A36">0.67 (&gt;0.5优质)</tspan></text>
    <text x="16" y="116" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">IC &gt; 0 胜率: <tspan font-weight="700" fill="#5F7355">83.3%</tspan></text>
    <text x="16" y="136" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">半衰期: 约 18 个交易日</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">Rank IC 采用斯皮尔曼秩相关，完全克服了正态分布假设与非线性单调离群点扭曲</text>
</svg>"""

SVGS["m05_l01_quantile_monotonicity"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.1.3：因子五分位数 (Quantiles) 分层回测单调性与多空净值对决</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">QUANTILE BACKTEST</text>

  <!-- Left: Quantile 1-5 Bar Chart -->
  <g transform="translate(80, 55)">
    <line x1="0" y1="130" x2="260" y2="130" stroke="#1F1E1B" stroke-width="1.5"/>
    <text x="130" y="152" font-family="Inter, sans-serif" font-size="10" fill="#7D786F" text-anchor="middle">因子得分升序 5 等分 (Q1=空头, Q5=多头)</text>

    <!-- Q1 (Worst) -->
    <rect x="20" y="100" width="35" height="30" fill="rgba(204, 90, 54, 0.6)"/>
    <text x="37" y="90" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#CC5A36" text-anchor="middle">-4.2%</text>
    <text x="37" y="145" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="middle">Q1</text>

    <!-- Q2 -->
    <rect x="70" y="80" width="35" height="50" fill="rgba(204, 90, 54, 0.3)"/>
    <text x="87" y="72" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#CC5A36" text-anchor="middle">+1.8%</text>
    <text x="87" y="145" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="middle">Q2</text>

    <!-- Q3 (Benchmark) -->
    <rect x="120" y="65" width="35" height="65" fill="#486A7D"/>
    <text x="137" y="57" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#486A7D" text-anchor="middle">+6.5%</text>
    <text x="137" y="145" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="middle">Q3</text>

    <!-- Q4 -->
    <rect x="170" y="45" width="35" height="85" fill="rgba(95, 115, 85, 0.6)"/>
    <text x="187" y="37" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#5F7355" text-anchor="middle">+11.2%</text>
    <text x="187" y="145" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="middle">Q4</text>

    <!-- Q5 (Best) -->
    <rect x="220" y="20" width="35" height="110" fill="#5F7355"/>
    <text x="237" y="12" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">+18.6%</text>
    <text x="237" y="145" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">Q5</text>
  </g>

  <!-- Right: Cumulative Long-Short Equity Curve -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="280" height="150" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    <text x="16" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#1F1E1B">多空对冲净值 (Long Q5 - Short Q1)</text>

    <!-- Upward sloping smooth equity curve -->
    <path d="M 25 125 Q 90 110 140 80 T 210 50 T 260 25" fill="none" stroke="#5F7355" stroke-width="2.5"/>
    <circle cx="260" cy="25" r="4" fill="#5F7355"/>
    <text x="260" y="15" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355" text-anchor="end">年化多空夏普 = 2.45</text>

    <!-- Benchmark horizontal line -->
    <line x1="25" y1="125" x2="260" y2="125" stroke="#7D786F" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="25" y="142" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">严格单调递增 = 具备稳健选股预测能力</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">若分层回测中 Q2 &gt; Q3 或 Q4 跌破基准，说明因子存在严重非线性凹凸性，不可直接用于线性打分</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 02
# -----------------------------------------------------------------------------
SVGS["m05_l02_fama_french_factor_zoo"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.2.1：Fama-French 五因子资产定价模型正交分解与 Alpha 剥离</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">FAMA-FRENCH 5 FACTOR</text>

  <!-- Formula Box -->
  <rect x="50" y="50" width="660" height="45" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
  <text x="380" y="78" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#1F1E1B" text-anchor="middle">
    R_i - R_f = α_i + β_mkt(MKT) + β_smb(SMB) + β_hml(HML) + β_rmw(RMW) + β_cma(CMA) + ε_i
  </text>

  <!-- 5 Factors Grid -->
  <g transform="translate(50, 110)">
    <!-- Factor 1: MKT -->
    <rect x="0" y="0" width="120" height="75" rx="4" fill="#FAF8F5" stroke="#486A7D"/>
    <text x="60" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#486A7D" text-anchor="middle">MKT (市场溢价)</text>
    <text x="60" y="42" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">R_m - R_f</text>
    <text x="60" y="60" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F" text-anchor="middle">系统性宏观Beta</text>

    <!-- Factor 2: SMB -->
    <rect x="135" y="0" width="120" height="75" rx="4" fill="#FAF8F5" stroke="#5F7355"/>
    <text x="195" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">SMB (规模溢价)</text>
    <text x="195" y="42" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">Small Minus Big</text>
    <text x="195" y="60" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F" text-anchor="middle">小市值非流动性溢价</text>

    <!-- Factor 3: HML -->
    <rect x="270" y="0" width="120" height="75" rx="4" fill="#FAF8F5" stroke="#C08535"/>
    <text x="330" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#C08535" text-anchor="middle">HML (价值溢价)</text>
    <text x="330" y="42" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">High Minus Low</text>
    <text x="330" y="60" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F" text-anchor="middle">高账面市值比 (PB)</text>

    <!-- Factor 4: RMW -->
    <rect x="405" y="0" width="120" height="75" rx="4" fill="#FAF8F5" stroke="#5F7355"/>
    <text x="465" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">RMW (盈利溢价)</text>
    <text x="465" y="42" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">Robust Minus Weak</text>
    <text x="465" y="60" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F" text-anchor="middle">高 ROE / ROIC 质量</text>

    <!-- Factor 5: CMA -->
    <rect x="540" y="0" width="120" height="75" rx="4" fill="#FAF8F5" stroke="#CC5A36"/>
    <text x="600" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">CMA (投资风格)</text>
    <text x="600" y="42" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="middle">Conservative - Aggressive</text>
    <text x="600" y="60" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F" text-anchor="middle">低资本开支再投资</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">若基金在扣除 5 因子后截距项 α 的 t 统计量未通过显著性检验，其超额收益纯属风格暴露运气</text>
</svg>"""

SVGS["m05_l02_barra_risk_model_matrix"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.2.2：Barra 多因子结构化风险模型矩阵：风格因子与行业暴露拓扑</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">BARRA RISK MATRIX</text>

  <!-- Left: Exposure Matrix X (N x K) -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="180" height="140" rx="4" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <text x="90" y="22" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#486A7D" text-anchor="middle">暴露矩阵 X (N × K)</text>
    <line x1="10" y1="32" x2="170" y2="32" stroke="#E5DFD5"/>
    <text x="15" y="52" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 行业因子哑变量 (0/1)</text>
    <text x="15" y="72" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 规模 Size (Log Market Cap)</text>
    <text x="15" y="92" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 动量 Momentum (12-1M)</text>
    <text x="15" y="112" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 波动率 Volatility / 价值</text>
    <text x="15" y="130" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F">N只股票 × K个风险因子</text>
  </g>

  <!-- Multiplication Symbol -->
  <text x="270" y="125" font-family="Inter, sans-serif" font-size="20" font-weight="bold" fill="#7D786F" text-anchor="middle">×</text>

  <!-- Middle: Factor Covariance Matrix F (K x K) -->
  <g transform="translate(300, 50)">
    <rect x="0" y="0" width="170" height="140" rx="4" fill="#FAF8F5" stroke="#C08535" stroke-width="1.5"/>
    <text x="85" y="22" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#C08535" text-anchor="middle">因子协方差 F (K × K)</text>
    <line x1="10" y1="32" x2="160" y2="32" stroke="#E5DFD5"/>
    <text x="15" y="55" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 因子时序收益协方差</text>
    <text x="15" y="75" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 指数半衰期加权 (Half-life)</text>
    <text x="15" y="95" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• Newey-West 滞后自相关调整</text>
    <text x="15" y="125" font-family="JetBrains Mono, monospace" font-size="9" fill="#C08535">正定矩阵保证</text>
  </g>

  <!-- Plus Symbol -->
  <text x="500" y="125" font-family="Inter, sans-serif" font-size="20" font-weight="bold" fill="#7D786F" text-anchor="middle">+</text>

  <!-- Right: Specific Risk Matrix Delta (N x N Diagonal) -->
  <g transform="translate(530, 50)">
    <rect x="0" y="0" width="170" height="140" rx="4" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="85" y="22" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">特异风险 Δ (对角阵)</text>
    <line x1="10" y1="32" x2="160" y2="32" stroke="#E5DFD5"/>
    <text x="15" y="55" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 单股不可解释特异方差</text>
    <text x="15" y="75" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 假定股票间残差不相关</text>
    <text x="15" y="95" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 维数灾难缩减: O(N^2) ➔ O(K^2)</text>
    <text x="15" y="125" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">Diag(σ_ε1^2, ..., σ_εN^2)</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">总协方差矩阵分解公式: Σ = X F X^T + Δ，彻底化解 5000 维资产全协方差估计的病态奇异性</text>
</svg>"""

SVGS["m05_l02_specific_risk_decomposition"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.2.3：投资组合总风险方差分解：风格系统性风险 vs 股票特异风险</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">RISK ATTRIBUTION</text>

  <!-- Left: Concentrated Portfolio (High Specific Risk) -->
  <g transform="translate(80, 50)">
    <rect x="0" y="0" width="260" height="145" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="130" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">集中持仓组合 (持股 N = 10)</text>
    
    <!-- Stacked Bar -->
    <rect x="30" y="45" width="200" height="35" fill="#486A7D"/>
    <text x="130" y="67" font-family="JetBrains Mono, monospace" font-size="10" fill="#FFFFFF" text-anchor="middle">系统性因子风险 35%</text>

    <rect x="30" y="80" width="200" height="45" fill="#CC5A36"/>
    <text x="130" y="107" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">股票特异风险 65% (未分散)</text>

    <text x="130" y="140" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">承受巨大黑天鹅暴雷脆弱性</text>
  </g>

  <!-- Right: Diversified Quant Portfolio (Pure Factor Alpha) -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="260" height="145" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="130" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">量化全市场分散组合 (持股 N = 300)</text>

    <!-- Stacked Bar -->
    <rect x="30" y="45" width="200" height="65" fill="#486A7D"/>
    <text x="130" y="82" font-family="JetBrains Mono, monospace" font-size="10" fill="#FFFFFF" text-anchor="middle">系统性因子风险 88%</text>

    <rect x="30" y="110" width="200" height="15" fill="#5F7355"/>
    <text x="130" y="122" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">特异风险 12% (大数定律分散)</text>

    <text x="130" y="140" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">组合收益纯由因子选股 Alpha 决定</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">现代资产组合核心原则：市场绝不对单只股票的特异风险给予超额定价，必须通过多因子分散化消除</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 03
# -----------------------------------------------------------------------------
SVGS["m05_l03_cointegration_vs_correlation"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.3.1：伪相关性 (Spurious Correlation) vs 长期协整 (Cointegration) 本质对立</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">ENGLE-GRANGER TEST</text>

  <!-- Left: High Correlation but No Cointegration (Drifting Apart) -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">高相关性但不协整 (伪套利陷阱)</text>
    
    <path d="M 20 120 Q 90 90 160 70 T 260 20" fill="none" stroke="#1F1E1B" stroke-width="2"/>
    <text x="265" y="24" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B">Asset A</text>

    <path d="M 20 130 Q 90 105 160 95 T 260 65" fill="none" stroke="#CC5A36" stroke-width="2"/>
    <text x="265" y="69" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">Asset B</text>

    <line x1="240" y1="20" x2="240" y2="65" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="140" y="115" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">Pearson r = 0.95 (同向上涨)</text>
    <text x="140" y="132" font-family="Inter, sans-serif" font-size="9" fill="#CC5A36" text-anchor="middle">价差持续发散漂移，死扛套利必然爆仓</text>
  </g>

  <!-- Right: Cointegrated (Drunkard and his dog) -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">严格协整 (长期经济/商业均衡绑定)</text>

    <path d="M 20 100 Q 80 60 140 80 T 200 40 T 260 50" fill="none" stroke="#1F1E1B" stroke-width="2"/>
    <text x="265" y="54" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B">Asset A</text>

    <!-- Asset B entangled with A -->
    <path d="M 20 110 Q 80 75 140 65 T 200 55 T 260 40" fill="none" stroke="#5F7355" stroke-width="2" stroke-dasharray="4 2"/>
    <text x="265" y="38" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">Asset B</text>

    <!-- Spread stationary around 0 -->
    <line x1="20" y1="120" x2="260" y2="120" stroke="#E5DFD5"/>
    <text x="140" y="115" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">残差序列 ε_t = P_A - β P_B 服从 I(0) 平稳</text>
    <text x="140" y="132" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#5F7355" text-anchor="middle">ADF p-value &lt; 0.01 拒绝随机游走</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">配对交易第一性原理：只做存在产业链上下游或完全替代品协整关系的对子，严禁做统计虚假相关</text>
</svg>"""

SVGS["m05_l03_ornstein_uhlenbeck_spread"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.3.2：Ornstein-Uhlenbeck (OU) 价差连续均值回归过程与半衰期 (Half-Life)</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">OU PROCESS</text>

  <!-- Left: SDE Formula Card -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="220" height="145" rx="6" fill="#FAF8F5" stroke="#486A7D"/>
    <text x="110" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#486A7D" text-anchor="middle">OU 随机微分方程 (SDE)</text>
    
    <text x="110" y="54" font-family="JetBrains Mono, monospace" font-size="10.5" fill="#1F1E1B" text-anchor="middle">dx_t = θ(μ - x_t)dt + σ dW_t</text>
    
    <text x="15" y="80" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• θ: 均值回归速率 (Mean Reversion Speed)</text>
    <text x="15" y="98" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• μ: 长期均衡价差均值 (Long-term Mean)</text>
    <text x="15" y="116" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• σ: 价差扩散波动率 (Volatility)</text>
    <text x="15" y="134" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#5F7355">半衰期 T_half = ln(2) / θ</text>
  </g>

  <!-- Right: Simulated Mean Reversion Path -->
  <g transform="translate(320, 50)">
    <rect x="0" y="0" width="380" height="145" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    
    <!-- Long-term Mean Line (y=70) -->
    <line x1="20" y1="70" x2="360" y2="70" stroke="#1F1E1B" stroke-width="1.5" stroke-dasharray="4 3"/>
    <text x="365" y="74" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">μ (均值)</text>

    <!-- +2 Sigma Band -->
    <line x1="20" y1="25" x2="360" y2="25" stroke="#CC5A36" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="365" y="29" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">+2σ 开仓做空</text>

    <!-- -2 Sigma Band -->
    <line x1="20" y1="115" x2="360" y2="115" stroke="#5F7355" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="365" y="119" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">-2σ 开仓做多</text>

    <!-- Reverting Path -->
    <polyline points="30,70 60,40 90,20 120,45 150,65 180,85 210,120 240,95 270,72 300,50 340,68" 
              fill="none" stroke="#486A7D" stroke-width="2.5"/>

    <!-- Half-life Bracket -->
    <line x1="90" y1="15" x2="150" y2="15" stroke="#C08535" stroke-width="2"/>
    <text x="120" y="12" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#C08535" text-anchor="middle">半衰期 T_half</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">半衰期决定最佳持仓周期：若 T_half &gt; 90 天，资金占用成本与模型漂移风险将急剧压垮策略夏普</text>
</svg>"""

SVGS["m05_l03_pairs_trading_bands"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.3.3：配对交易标准化 Z-Score 动态通道与硬止损熔断风控架构</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">TRADING BANDS</text>

  <!-- Bands Display Area -->
  <g transform="translate(60, 45)">
    <!-- Stop Loss High (+3.0) -->
    <line x1="20" y1="15" x2="640" y2="15" stroke="#CC5A36" stroke-width="2" stroke-dasharray="3 3"/>
    <text x="645" y="19" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36">+3.0σ (硬止损)</text>

    <!-- Short Entry (+2.0) -->
    <line x1="20" y1="45" x2="640" y2="45" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="645" y="49" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">+2.0σ (做空价差)</text>

    <!-- Take Profit (0.0 Mean) -->
    <line x1="20" y1="85" x2="640" y2="85" stroke="#1F1E1B" stroke-width="1.5"/>
    <text x="645" y="89" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#1F1E1B">0.0 (平仓均值)</text>

    <!-- Long Entry (-2.0) -->
    <line x1="20" y1="125" x2="640" y2="125" stroke="#5F7355" stroke-width="1.5"/>
    <text x="645" y="129" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">-2.0σ (做多价差)</text>

    <!-- Stop Loss Low (-3.0) -->
    <line x1="20" y1="155" x2="640" y2="155" stroke="#CC5A36" stroke-width="2" stroke-dasharray="3 3"/>
    <text x="645" y="159" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36">-3.0σ (硬止损)</text>

    <!-- Z-score trajectory -->
    <polyline points="40,85 100,55 140,40 180,50 220,85 280,110 320,130 360,115 410,85 470,35 510,12" 
              fill="none" stroke="#486A7D" stroke-width="2.5"/>

    <!-- Event 1: Normal Profit Trade -->
    <circle cx="140" cy="40" r="5" fill="#CC5A36"/>
    <text x="140" y="32" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#CC5A36" text-anchor="middle">卖A买B</text>
    <circle cx="220" cy="85" r="4" fill="#5F7355"/>
    <text x="220" y="100" font-family="Inter, sans-serif" font-size="9" fill="#5F7355" text-anchor="middle">止盈出场</text>

    <!-- Event 2: Stop Loss Triggered -->
    <circle cx="510" cy="12" r="5" fill="#CC5A36"/>
    <text x="510" y="4" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#CC5A36" text-anchor="middle">突破+3σ 协整断裂止损</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">价差突破 3 倍标准差往往意味着基本面发生了不可逆重组（如并购/破产），坚决止损不可死扛</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 04
# -----------------------------------------------------------------------------
SVGS["m05_l04_purged_walk_forward_cv"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.4.1：金融机器学习 Purged &amp; Embargoed 滚动步进时序交叉验证</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">DE PRADO PURGED CV</text>

  <!-- Fold 1 -->
  <g transform="translate(60, 50)">
    <text x="0" y="18" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#1F1E1B">Fold 1</text>
    <!-- Train Window (Fir Green) -->
    <rect x="60" y="5" width="280" height="20" rx="3" fill="#5F7355"/>
    <text x="200" y="19" font-family="Inter, sans-serif" font-size="9.5" fill="#FFFFFF" text-anchor="middle">训练集 Train (3 年)</text>

    <!-- Purged Gap (Terracotta hatched) -->
    <rect x="340" y="5" width="20" height="20" rx="2" fill="#CC5A36"/>
    <text x="350" y="19" font-family="Inter, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">P</text>

    <!-- Test Window (Cobalt Blue) -->
    <rect x="360" y="5" width="120" height="20" rx="3" fill="#486A7D"/>
    <text x="420" y="19" font-family="Inter, sans-serif" font-size="9.5" fill="#FFFFFF" text-anchor="middle">测试集 Test (6 个月)</text>

    <!-- Embargo Window (Ochre) -->
    <rect x="480" y="5" width="25" height="20" rx="2" fill="#C08535"/>
    <text x="492" y="19" font-family="Inter, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">E</text>
  </g>

  <!-- Fold 2 -->
  <g transform="translate(60, 85)">
    <text x="0" y="18" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#1F1E1B">Fold 2</text>
    <rect x="140" y="5" width="280" height="20" rx="3" fill="#5F7355"/>
    <text x="280" y="19" font-family="Inter, sans-serif" font-size="9.5" fill="#FFFFFF" text-anchor="middle">训练集 Train (滚动前移)</text>

    <rect x="420" y="5" width="20" height="20" rx="2" fill="#CC5A36"/>
    <text x="430" y="19" font-family="Inter, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">P</text>

    <rect x="440" y="5" width="120" height="20" rx="3" fill="#486A7D"/>
    <text x="500" y="19" font-family="Inter, sans-serif" font-size="9.5" fill="#FFFFFF" text-anchor="middle">测试集 Test</text>

    <rect x="560" y="5" width="25" height="20" rx="2" fill="#C08535"/>
    <text x="572" y="19" font-family="Inter, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">E</text>
  </g>

  <!-- Fold 3 -->
  <g transform="translate(60, 120)">
    <text x="0" y="18" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#1F1E1B">Fold 3</text>
    <rect x="220" y="5" width="280" height="20" rx="3" fill="#5F7355"/>
    <text x="360" y="19" font-family="Inter, sans-serif" font-size="9.5" fill="#FFFFFF" text-anchor="middle">训练集 Train</text>

    <rect x="500" y="5" width="20" height="20" rx="2" fill="#CC5A36"/>
    <text x="510" y="19" font-family="Inter, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">P</text>

    <rect x="520" y="5" width="120" height="20" rx="3" fill="#486A7D"/>
    <text x="580" y="19" font-family="Inter, sans-serif" font-size="9.5" fill="#FFFFFF" text-anchor="middle">测试集 Test</text>
  </g>

  <!-- Legend -->
  <g transform="translate(100, 165)">
    <rect x="0" y="5" width="12" height="12" fill="#CC5A36"/>
    <text x="18" y="15" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">Purging (样本重叠清洗): 剔除因未来回报持有期跨界而泄露的训练观测</text>
    
    <rect x="0" y="25" width="12" height="12" fill="#C08535"/>
    <text x="18" y="35" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">Embargo (隔离期缓冲): 隔离自回归时序记忆泄露，彻底根绝过拟合</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">普通 K-Fold 随机打乱切分在时序数据中是完全失效的，会由于标签重叠导致惊人的虚高假象</text>
</svg>"""

SVGS["m05_l04_tree_ensemble_feature_importance"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.4.2：梯度提升树 (GBDT / LightGBM) 因子非线性交互与 SHAP 重要度分解</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">FEATURE IMPORTANCE</text>

  <!-- Feature Importance Horizontal Bar Chart -->
  <g transform="translate(80, 50)">
    <!-- Feature 1: ROIC Spread -->
    <text x="120" y="22" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">ROIC - WACC</text>
    <rect x="130" y="10" width="320" height="16" rx="3" fill="#5F7355"/>
    <text x="460" y="22" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355">28.4% (核心基本面)</text>

    <!-- Feature 2: Momentum 12M -->
    <text x="120" y="47" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">Momentum_12M</text>
    <rect x="130" y="35" width="240" height="16" rx="3" fill="#486A7D"/>
    <text x="380" y="47" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#486A7D">21.2% (中期动量)</text>

    <!-- Feature 3: Volatility Squeeze -->
    <text x="120" y="72" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">Vol_Squeeze_20D</text>
    <rect x="130" y="60" width="180" height="16" rx="3" fill="#C08535"/>
    <text x="320" y="72" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535">16.5% (波动压缩)</text>

    <!-- Feature 4: OFI Imbalance -->
    <text x="120" y="97" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">OFI_Flux_1D</text>
    <rect x="130" y="85" width="140" height="16" rx="3" fill="#486A7D"/>
    <text x="280" y="97" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#486A7D">12.8% (订单流不平衡)</text>

    <!-- Feature 5: Beneish M-Score -->
    <text x="120" y="122" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">Beneish_MScore</text>
    <rect x="130" y="110" width="110" height="16" rx="3" fill="#CC5A36"/>
    <text x="250" y="122" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36">9.7% (舞弊排雷门槛)</text>

    <!-- Feature 6: EP Ratio -->
    <text x="120" y="147" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">EP_Ratio_TTM</text>
    <rect x="130" y="135" width="85" height="16" rx="3" fill="#7D786F"/>
    <text x="225" y="147" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F">7.6% (估值基底)</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">树模型能够自动捕获“当高 ROIC 遇上低估值与动量共振”的强非线性交互协同收益</text>
</svg>"""

SVGS["m05_l04_overfitting_backtest_trap"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.4.3：量化回测多重检验陷阱与伪发现率 (False Discovery Rate) 衰减律</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">P-HACKING DEFENSE</text>

  <!-- Curve: Max In-Sample Sharpe vs Trials N -->
  <g transform="translate(80, 50)">
    <line x1="40" y1="140" x2="380" y2="140" stroke="#1F1E1B" stroke-width="1.5"/>
    <line x1="40" y1="20" x2="40" y2="140" stroke="#1F1E1B" stroke-width="1.5"/>
    <text x="390" y="144" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B">尝试因子/策略试验次数 N</text>
    <text x="35" y="15" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">In-Sample 夏普</text>

    <!-- Asymptotic False Sharpe growth curve -->
    <path d="M 40 120 Q 120 70 220 40 T 360 25" fill="none" stroke="#CC5A36" stroke-width="2.5"/>
    <circle cx="360" cy="25" r="4" fill="#CC5A36"/>
    <text x="365" y="28" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36">样本内假夏普 &gt; 3.0</text>

    <!-- True Out-of-Sample Flat Line -->
    <line x1="40" y1="110" x2="360" y2="110" stroke="#5F7355" stroke-width="2" stroke-dasharray="4 3"/>
    <text x="365" y="114" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355">样本外真实夏普 ≈ 0.4</text>

    <text x="180" y="80" font-family="Inter, sans-serif" font-size="9.5" fill="#CC5A36">数据挖掘过拟合必然筛选出随机噪声</text>
  </g>

  <!-- Right: Deflated Sharpe Ratio Card -->
  <g transform="translate(480, 50)">
    <rect x="0" y="0" width="220" height="145" rx="6" fill="#FAF8F5" stroke="#C08535"/>
    <text x="110" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#C08535" text-anchor="middle">Bailey &amp; López de Prado</text>
    <text x="110" y="44" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#1F1E1B" text-anchor="middle">折损夏普比率 (DSR)</text>
    
    <text x="12" y="70" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 显式惩罚试验次数 N</text>
    <text x="12" y="88" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 惩罚非正态偏度与超额峰度</text>
    <text x="12" y="106" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 计算 DSR &gt; 0.95 置信概率</text>
    <text x="12" y="132" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#CC5A36">严禁未经多次试验折损的回测</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">测试 1000 次随机时序必然能找到一条年化 50% 的“神级曲线”——这是数理统计常识，而非投资能力</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 05
# -----------------------------------------------------------------------------
SVGS["m05_l05_csmom_vs_tsmom_matrix"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.5.1：截面动量 (CSMOM) 与时间序列动量 (TSMOM) 机制拓扑对比</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">MOMENTUM DUALITY</text>

  <!-- Left: Cross-Sectional Momentum (Relative) -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#486A7D" text-anchor="middle">截面动量 CSMOM (相对强弱)</text>

    <!-- Comparison across assets at fixed t -->
    <rect x="25" y="45" width="230" height="25" rx="3" fill="#5F7355"/>
    <text x="140" y="62" font-family="JetBrains Mono, monospace" font-size="10" fill="#FFFFFF" text-anchor="middle">做多: 表现最优前 20% (相对赢家)</text>

    <rect x="25" y="75" width="230" height="25" rx="3" fill="#FAF8F5" stroke="#7D786F"/>
    <text x="140" y="92" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="middle">中间 60%: 不开仓 / 现金观望</text>

    <rect x="25" y="105" width="230" height="25" rx="3" fill="#CC5A36"/>
    <text x="140" y="122" font-family="JetBrains Mono, monospace" font-size="10" fill="#FFFFFF" text-anchor="middle">做空: 表现最差后 20% (相对输家)</text>

    <text x="140" y="142" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">严格零净头寸 (Dollar Neutral)</text>
  </g>

  <!-- Right: Time-Series Momentum (Absolute Trend) -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">时间序列动量 TSMOM (绝对趋势)</text>

    <!-- Trend filter rule -->
    <rect x="25" y="45" width="230" height="35" rx="3" fill="#FAF8F5" stroke="#5F7355"/>
    <text x="140" y="62" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355" text-anchor="middle">P_t &gt; P_{t-12M} (自身绝对上涨)</text>
    <text x="140" y="76" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#5F7355" text-anchor="middle">➜ 100% 多头满仓</text>

    <rect x="25" y="85" width="230" height="35" rx="3" fill="#FAF8F5" stroke="#CC5A36"/>
    <text x="140" y="102" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36" text-anchor="middle">P_t &lt; P_{t-12M} (自身绝对下跌)</text>
    <text x="140" y="116" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#CC5A36" text-anchor="middle">➜ 做空或清仓避险至现金</text>

    <text x="140" y="142" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">头寸方向仅由资产自身历史时序决定</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">CSMOM 赚取截面异质选股溢价，TSMOM 赚取全市场长波趋势红利与危机 Alpha</text>
</svg>"""

SVGS["m05_l05_momentum_crash_volatility"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.5.2：动量崩盘 (Momentum Crash) 物理机理：熊市触底剧烈反弹期的空头反噬</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">MOMENTUM CRASH</text>

  <!-- Market V-shape Reversal Chart -->
  <g transform="translate(60, 45)">
    <!-- Market Bottom (Panic End) -->
    <polyline points="20,40 100,110 180,160 240,110 320,50 400,20" fill="none" stroke="#1F1E1B" stroke-width="2"/>
    <text x="180" y="180" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#CC5A36" text-anchor="middle">熊市底部暴跌出清点</text>

    <!-- Losers Basket (Short leg explodes up!) -->
    <path d="M 180 160 Q 240 70 320 20 T 400 5" fill="none" stroke="#CC5A36" stroke-width="3" stroke-dasharray="4 3"/>
    <text x="405" y="10" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36">空头组合 (高Beta垃圾股) 暴涨 +150% 轧空</text>

    <!-- Winners Basket (Long leg lags behind) -->
    <path d="M 180 160 Q 240 130 320 80 T 400 45" fill="none" stroke="#5F7355" stroke-width="2"/>
    <text x="405" y="50" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">多头组合 (前期防御避险股) 滞涨 +20%</text>

    <line x1="320" y1="20" x2="320" y2="80" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="325" y="55" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#CC5A36">动量净值断崖式崩盘 -60%</text>
  </g>

  <!-- Right: Option Payoff Analogy -->
  <g transform="translate(500, 75)">
    <rect x="0" y="0" width="200" height="120" rx="6" fill="#FAF8F5" stroke="#CC5A36"/>
    <text x="100" y="22" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">隐含空头看涨期权结构</text>
    <text x="12" y="44" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">• 平时稳定赚取小额正收益</text>
    <text x="12" y="62" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">• 熊市反转期呈现严重负偏度</text>
    <text x="12" y="80" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">• 高杠杆垃圾股反弹弹性巨大</text>
    <text x="12" y="102" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36">必须配备波动率过滤器</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">历史上惨烈的动量崩盘（如 1932、2009）均发生在恐慌见底后的暴力反弹阶段，空头腿亏损击穿本金</text>
</svg>"""

SVGS["m05_l05_macro_regime_trend_filter"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 5.5.3：宏观市场体制过滤器与动量策略动态波动率自适应杠杆控制</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">VOL TARGETING</text>

  <!-- Left: Regime Switch Flowchart -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="300" height="145" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <text x="150" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#486A7D" text-anchor="middle">市场宏观体制与波动率状态机</text>

    <!-- State 1: Low Vol Bull -->
    <rect x="20" y="35" width="260" height="28" rx="4" fill="rgba(95, 115, 85, 0.15)" stroke="#5F7355"/>
    <text x="30" y="52" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B">低波上行区 (VIX &lt; 20 且 P &gt; MA200):</text>
    <text x="270" y="52" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#5F7355" text-anchor="end">Leverage = 1.0 (全速)</text>

    <!-- State 2: High Vol Choppy -->
    <rect x="20" y="70" width="260" height="28" rx="4" fill="rgba(192, 133, 53, 0.15)" stroke="#C08535"/>
    <text x="30" y="87" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B">高波震荡区 (20 &le; VIX &le; 30):</text>
    <text x="270" y="87" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#C08535" text-anchor="end">Leverage = 0.5 (半仓)</text>

    <!-- State 3: Panic Regime -->
    <rect x="20" y="105" width="260" height="28" rx="4" fill="rgba(204, 90, 54, 0.15)" stroke="#CC5A36"/>
    <text x="30" y="122" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B">恐慌危机区 (VIX &gt; 30 或 崩盘后反弹):</text>
    <text x="270" y="122" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#CC5A36" text-anchor="end">Leverage = 0.0 (空仓防崩)</text>
  </g>

  <!-- Right: Volatility Targeting Formula -->
  <g transform="translate(400, 50)">
    <rect x="0" y="0" width="300" height="145" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="150" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">目标波动率缩放 (Volatility Targeting)</text>

    <text x="150" y="55" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#1F1E1B" text-anchor="middle">
      w_t = \min\left(1.5, \frac{\sigma_{\text{target}}}{\hat{\sigma}_t}\right)
    </text>

    <text x="15" y="85" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 波动率上升时系统自动降低名义仓位敞口</text>
    <text x="15" y="105" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 波动率平稳时放大仓位保持恒定风险预算</text>
    <text x="15" y="125" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#5F7355">• 彻底消除动量因子的肥尾下行巨震</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">优秀的量化动量基金并非拥有更好的选股公式，而是拥有顶级的自适应波动率与崩盘避险断路器</text>
</svg>"""

def main():
    target_dirs = [
        os.path.join(BASE_DIR, "05_quant_trading", "assets"),
        os.path.join(BASE_DIR, "05_quant_trading", "images"),
        os.path.join(BASE_DIR, "web", "assets", "05_quant_trading"),
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

    print(f"✅ 成功生成并同步模块 05 共 {count} 个纯 SVG 文件到所有对应资产目录！")

if __name__ == "__main__":
    main()
