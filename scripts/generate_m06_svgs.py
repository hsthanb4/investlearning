#!/usr/bin/env python3
"""
生成模块 06 (现代投资组合与仓位风控) 配套高质感 Anthropic 风格 SVG 矢量图
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
SVGS["m06_l01_efficient_frontier_cml"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.1.1：马科维茨有效前沿 (Efficient Frontier) 与资本市场线 (CML) 切点模型</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">MARKOWITZ MVO</text>

  <!-- Axes -->
  <line x1="80" y1="210" x2="700" y2="210" stroke="#1F1E1B" stroke-width="1.5"/>
  <line x1="80" y1="40" x2="80" y2="210" stroke="#1F1E1B" stroke-width="1.5"/>
  <text x="70" y="45" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">预期回报 E[R]</text>
  <text x="700" y="225" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">组合波动率 σ_p</text>

  <!-- Risk Free Rate Point -->
  <circle cx="80" cy="180" r="4" fill="#486A7D"/>
  <text x="70" y="184" font-family="JetBrains Mono, monospace" font-size="10" fill="#486A7D" text-anchor="end">R_f = 2%</text>

  <!-- Efficient Frontier Hyperbola Curve -->
  <!-- GMV point: (220, 130) -->
  <path d="M 450 200 Q 220 180 220 130 Q 220 70 480 50" fill="none" stroke="#CC5A36" stroke-width="2.5"/>

  <!-- Inefficient Lower Part -->
  <path d="M 450 200 Q 220 180 220 130" fill="none" stroke="#7D786F" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="360" y="195" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">无效前沿下半支</text>

  <!-- Efficient Upper Part -->
  <text x="490" y="52" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#CC5A36">马科维茨有效前沿</text>

  <!-- Global Minimum Variance (GMV) Point -->
  <circle cx="220" cy="130" r="5" fill="#C08535"/>
  <text x="210" y="134" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535" text-anchor="end">GMV (全局最小方差)</text>

  <!-- Tangency Portfolio (Max Sharpe) -->
  <!-- Tangency point: (350, 85) -->
  <circle cx="350" cy="85" r="6" fill="#5F7355"/>
  <text x="350" y="72" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">切点组合 (Max Sharpe)</text>

  <!-- Capital Market Line (CML) from Rf through Tangency -->
  <line x1="80" y1="180" x2="650" y2="40" stroke="#5F7355" stroke-width="2"/>
  <text x="655" y="44" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#5F7355">资本市场线 CML</text>

  <!-- Scatter points inside frontier (Feasible set) -->
  <circle cx="320" cy="140" r="2.5" fill="rgba(72,106,125,0.4)"/>
  <circle cx="380" cy="120" r="2.5" fill="rgba(72,106,125,0.4)"/>
  <circle cx="420" cy="150" r="2.5" fill="rgba(72,106,125,0.4)"/>
  <circle cx="300" cy="160" r="2.5" fill="rgba(72,106,125,0.4)"/>
  <circle cx="480" cy="130" r="2.5" fill="rgba(72,106,125,0.4)"/>
  <text x="390" y="145" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">可行投资组合集 (Feasible Set)</text>

  <text x="380" y="238" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">托宾两基金分离定理：理性投资者只需配置无风险资产与切点切线组合，通过杠杆调节风险偏好</text>
</svg>"""

SVGS["m06_l01_quadratic_programming_geometry"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.1.2：二次规划 (QP) 求解几何拓扑：凸优化等高椭圆与单纯形约束面</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">CONVEX OPTIMIZATION</text>

  <!-- Optimization Formulation on Left -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#486A7D" text-anchor="middle">二次规划数学标准型 (Standard QP)</text>
    
    <text x="140" y="55" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#1F1E1B" text-anchor="middle">
      \min_{w} \frac{1}{2} w^T \Sigma w - q \cdot \mu^T w
    </text>

    <text x="20" y="85" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B">受限于线性约束 (Linear Constraints):</text>
    <text x="20" y="105" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#5F7355">• \sum w_i = 1.0 (全仓预算约束)</text>
    <text x="20" y="125" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#CC5A36">• 0 \le w_i \le w_{max} (严禁做空与单票上限)</text>
    <text x="20" y="140" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">目标函数 Hessian 矩阵 Σ 必须半正定</text>
  </g>

  <!-- Geometric Visualization on Right -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    <text x="140" y="20" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#1F1E1B" text-anchor="middle">等风险方差椭圆等高线</text>

    <!-- Concentric Ellipses (Variance Contours) -->
    <ellipse cx="140" cy="85" rx="100" ry="45" fill="none" stroke="rgba(72,106,125,0.3)" stroke-width="1"/>
    <ellipse cx="140" cy="85" rx="70" ry="32" fill="none" stroke="rgba(72,106,125,0.5)" stroke-width="1.5"/>
    <ellipse cx="140" cy="85" rx="40" ry="18" fill="none" stroke="#486A7D" stroke-width="2"/>
    <circle cx="140" cy="85" r="4" fill="#486A7D"/>
    <text x="140" y="80" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D" text-anchor="middle">GMV Center</text>

    <!-- Simplex Linear Constraint Line -->
    <line x1="40" y1="125" x2="240" y2="45" stroke="#5F7355" stroke-width="2"/>
    <text x="245" y="48" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#5F7355">Σw=1</text>

    <!-- Tangency Optimum Point -->
    <circle cx="170" cy="73" r="5" fill="#CC5A36"/>
    <text x="175" y="65" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#CC5A36">KKT 最优解 w*</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">二次规划的全局凸性保证了数值求解的绝对收敛，但若约束过少极易落入非物理角点极端权重</text>
</svg>"""

SVGS["m06_l01_error_maximization_instability"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.1.3：马科维茨“误差放大器”(Error Maximizer) 效应与病态权重翻转</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">NUMERICAL INSTABILITY</text>

  <!-- Left: True Inputs vs Perturbed Inputs -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">输入微小扰动 Δμ = 0.5%</text>

    <!-- Asset Expected Return Bars -->
    <text x="20" y="55" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">Asset A: μ = 10.0% ➔ 10.5%</text>
    <rect x="20" y="60" width="210" height="12" fill="#486A7D"/>
    
    <text x="20" y="90" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B">Asset B: μ = 10.0% (不变)</text>
    <rect x="20" y="95" width="200" height="12" fill="#7D786F"/>

    <text x="140" y="130" font-family="Inter, sans-serif" font-size="9.5" fill="#CC5A36" text-anchor="middle">输入仅发生不可察觉的微小估计残差</text>
  </g>

  <!-- Arrow -->
  <path d="M 360 120 L 395 120" stroke="#CC5A36" stroke-width="2.5"/>
  <text x="377" y="110" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36" text-anchor="middle">Σ^-1</text>

  <!-- Right: Catastrophic Output Weight Flip -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">输出最优权重灾难性翻转！</text>

    <text x="20" y="55" font-family="JetBrains Mono, monospace" font-size="10" fill="#5F7355">Weight A: 50% ➔ 92% (疯狂满仓)</text>
    <rect x="20" y="60" width="230" height="14" fill="#5F7355"/>

    <text x="20" y="95" font-family="JetBrains Mono, monospace" font-size="10" fill="#CC5A36">Weight B: 50% ➔ 8% (几乎清空)</text>
    <rect x="20" y="100" width="20" height="14" fill="#CC5A36"/>

    <text x="140" y="132" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#CC5A36" text-anchor="middle">协方差求逆放大了最大的估计噪音</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">理查德·米肖（Michaud）名言：均值-方差优化本质是“误差放大器”，必须使用收缩估计或黑石-利特曼模型</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 02
# -----------------------------------------------------------------------------
SVGS["m06_l02_capital_vs_risk_allocation"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.2.1：经典 60/40 股债组合的名义资本配置 vs 真实风险贡献假象</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">CAPITAL VS RISK TRAP</text>

  <!-- Left: Nominal Capital Weights (60 / 40) -->
  <g transform="translate(100, 55)">
    <rect x="0" y="0" width="240" height="140" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
    <text x="120" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#486A7D" text-anchor="middle">名义资本分配 (看似平衡)</text>

    <!-- Nominal Pie Bar -->
    <rect x="25" y="45" width="190" height="30" rx="4" fill="#CC5A36"/>
    <text x="80" y="65" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#FFFFFF">股票 60%</text>

    <rect x="140" y="45" width="75" height="30" rx="4" fill="#5F7355"/>
    <text x="175" y="65" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#FFFFFF">债券 40%</text>

    <text x="120" y="100" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B" text-anchor="middle">股票年化波幅 σ_e = 18%</text>
    <text x="120" y="118" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B" text-anchor="middle">债券年化波幅 σ_b = 4%</text>
  </g>

  <!-- Right: True Risk Contribution (93% / 7%) -->
  <g transform="translate(420, 55)">
    <rect x="0" y="0" width="240" height="140" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="120" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">真实方差风险贡献 (严重裸露)</text>

    <!-- Risk Contribution Bar -->
    <rect x="25" y="45" width="190" height="30" rx="4" fill="#CC5A36"/>
    <text x="100" y="65" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#FFFFFF">股票风险贡献 92.8%</text>

    <rect x="185" y="45" width="30" height="30" rx="4" fill="#5F7355"/>
    <text x="200" y="65" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#FFFFFF">债7%</text>

    <text x="120" y="100" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#CC5A36" text-anchor="middle">90% 以上净值波动完全由股票决定</text>
    <text x="120" y="118" font-family="Inter, sans-serif" font-size="9" fill="#7D786F" text-anchor="middle">所谓 60/40 分散化只是脆弱的会计安慰剂</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">因为股票波动率是债券的 4~5 倍，风险平价的核心洞见在于：必须按风险配资，而非按资金记账</text>
</svg>"""

SVGS["m06_l02_equal_risk_contribution_pie"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.2.2：风险平价等风险贡献 (Equal Risk Contribution, ERC) 平衡矩阵</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">ERC MECHANICS</text>

  <!-- Formula Box Left -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">边际风险贡献 (MRC) 等式</text>
    
    <text x="140" y="55" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#1F1E1B" text-anchor="middle">
      \text{MRC}_i = \frac{(\Sigma w)_i}{\sigma_p}
    </text>

    <text x="140" y="85" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">
      \text{TRC}_i = w_i \times \text{MRC}_i = \frac{\sigma_p}{N}
    </text>

    <text x="20" y="115" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 每个资产对组合总方差的边际贡献严格相等</text>
    <text x="20" y="135" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 低波资产 (国债) 获得更高权重或适度杠杆</text>
  </g>

  <!-- 4 Asset Equal Risk Contribution Equal Balance on Right -->
  <g transform="translate(380, 50)">
    <rect x="0" y="0" width="320" height="145" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    <text x="160" y="22" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#1F1E1B" text-anchor="middle">4 大类资产总风险等额切分 (各 25%)</text>

    <!-- 4 Balanced Slices -->
    <rect x="25" y="45" width="60" height="50" rx="4" fill="#CC5A36"/>
    <text x="55" y="70" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">股票</text>
    <text x="55" y="86" font-family="JetBrains Mono, monospace" font-size="9" fill="#FFFFFF" text-anchor="middle">25% RC</text>

    <rect x="95" y="45" width="60" height="50" rx="4" fill="#5F7355"/>
    <text x="125" y="70" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">长期国债</text>
    <text x="125" y="86" font-family="JetBrains Mono, monospace" font-size="9" fill="#FFFFFF" text-anchor="middle">25% RC</text>

    <rect x="165" y="45" width="60" height="50" rx="4" fill="#C08535"/>
    <text x="195" y="70" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">大宗商品</text>
    <text x="195" y="86" font-family="JetBrains Mono, monospace" font-size="9" fill="#FFFFFF" text-anchor="middle">25% RC</text>

    <rect x="235" y="45" width="60" height="50" rx="4" fill="#486A7D"/>
    <text x="265" y="70" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">抗通胀债</text>
    <text x="265" y="86" font-family="JetBrains Mono, monospace" font-size="9" fill="#FFFFFF" text-anchor="middle">25% RC</text>

    <text x="160" y="125" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">彻底消除任何单一大类资产的系统性绑架</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">风险平价不依赖极不可靠的预期收益率预测 μ，仅依赖结构相对稳定的协方差矩阵 Σ</text>
</svg>"""

SVGS["m06_l02_all_weather_economic_matrix"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.2.3：桥水全天候 (All Weather) 宏观经济环境四象限对冲架构</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">DALIO ALL WEATHER</text>

  <!-- Quadrants Grid -->
  <g transform="translate(100, 50)">
    <!-- Dividing Cross Lines -->
    <line x1="280" y1="10" x2="280" y2="150" stroke="#1F1E1B" stroke-width="1.5"/>
    <line x1="20" y1="80" x2="540" y2="80" stroke="#1F1E1B" stroke-width="1.5"/>

    <!-- Axis Labels -->
    <text x="280" y="5" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#CC5A36" text-anchor="middle">通胀高于预期 Inflation ↑</text>
    <text x="280" y="165" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">通胀低于预期 Inflation ↓</text>
    <text x="10" y="84" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#486A7D" text-anchor="end">增长衰退 Growth ↓</text>
    <text x="550" y="84" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#5F7355">增长扩张 Growth ↑</text>

    <!-- Quadrant 1: Growth UP + Inflation UP (Top Right) -->
    <rect x="290" y="15" width="240" height="60" rx="4" fill="rgba(192, 133, 53, 0.12)"/>
    <text x="410" y="35" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#C08535" text-anchor="middle">过热期 (Growth ↑ / Inf ↑)</text>
    <text x="410" y="55" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#1F1E1B" text-anchor="middle">优势资产: 大宗商品、黄金、TIPS</text>

    <!-- Quadrant 2: Growth UP + Inflation DOWN (Bottom Right) -->
    <rect x="290" y="85" width="240" height="60" rx="4" fill="rgba(95, 115, 85, 0.12)"/>
    <text x="410" y="105" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">金发姑娘期 (Growth ↑ / Inf ↓)</text>
    <text x="410" y="125" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#1F1E1B" text-anchor="middle">优势资产: 股票、高收益信用债</text>

    <!-- Quadrant 3: Growth DOWN + Inflation DOWN (Bottom Left) -->
    <rect x="30" y="85" width="240" height="60" rx="4" fill="rgba(72, 106, 125, 0.12)"/>
    <text x="150" y="105" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#486A7D" text-anchor="middle">衰退期 (Growth ↓ / Inf ↓)</text>
    <text x="150" y="125" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#1F1E1B" text-anchor="middle">优势资产: 长期名义国债、现金</text>

    <!-- Quadrant 4: Growth DOWN + Inflation UP (Top Left) -->
    <rect x="30" y="15" width="240" height="60" rx="4" fill="rgba(204, 90, 54, 0.12)"/>
    <text x="150" y="35" font-family="Newsreader, serif" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">滞胀期 (Growth ↓ / Inf ↑)</text>
    <text x="150" y="55" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#1F1E1B" text-anchor="middle">优势资产: 原油、黄金、抗通胀债</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">任何一种经济环境下都有两组资产在产生正现金流，全天候的核心是让四大象限风险暴露完全中性化</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 03
# -----------------------------------------------------------------------------
SVGS["m06_l03_log_utility_growth_curve"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.3.1：对数效用几何财富增长率曲线：全凯利 (Full Kelly) 峰值与半凯利安全边际</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">KELLY LOG-UTILITY</text>

  <!-- Axes -->
  <line x1="80" y1="180" x2="680" y2="180" stroke="#1F1E1B" stroke-width="1.5"/>
  <line x1="80" y1="40" x2="80" y2="210" stroke="#1F1E1B" stroke-width="1.5"/>
  <text x="70" y="45" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">复合增长 g(f)</text>
  <text x="680" y="195" font-family="JetBrains Mono, monospace" font-size="10" fill="#1F1E1B" text-anchor="end">下注比例 / 杠杆 f</text>

  <!-- Parabolic Kelly Growth Curve g(f) = r + f*(mu-r) - 0.5*f^2*sigma^2 -->
  <path d="M 80 160 Q 240 60 380 60 Q 520 60 620 210" fill="none" stroke="#CC5A36" stroke-width="3"/>

  <!-- Zero Return Line -->
  <line x1="80" y1="160" x2="650" y2="160" stroke="#7D786F" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="655" y="164" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F">g=0</text>

  <!-- Half Kelly Point -->
  <circle cx="230" cy="85" r="5" fill="#5F7355"/>
  <line x1="230" y1="85" x2="230" y2="180" stroke="#5F7355" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="230" y="70" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355" text-anchor="middle">Half Kelly (0.5 f*)</text>
  <text x="230" y="195" font-family="Inter, sans-serif" font-size="9" fill="#5F7355" text-anchor="middle">获得 75% 增长，波动骤降 50%</text>

  <!-- Full Kelly Peak -->
  <circle cx="380" cy="60" r="6" fill="#CC5A36"/>
  <line x1="380" y1="60" x2="380" y2="180" stroke="#CC5A36" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="380" y="45" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">Full Kelly (f* 最优极值)</text>
  <text x="380" y="195" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36" text-anchor="middle">f* = (p*b - q) / b</text>

  <!-- Overbetting Danger Zone (f > 2f*) -->
  <circle cx="580" cy="160" r="5" fill="#1F1E1B"/>
  <line x1="580" y1="160" x2="580" y2="210" stroke="#1F1E1B" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="580" y="150" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36" text-anchor="middle">f &gt; 2f* 必然破产区</text>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">凯利公式最大警示：当下注比例超过 2 倍最佳值时，期望几何增长率直接转为负数，长期持有 100% 破产</text>
</svg>"""

SVGS["m06_l03_risk_of_ruin_simulation"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.3.2：过度杠杆下几何平均增长率崩塌与破产概率 (Risk of Ruin) 爆炸</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">RUIN PROBABILITY</text>

  <!-- Left: Equity Trajectories Monte Carlo -->
  <g transform="translate(60, 50)">
    <line x1="30" y1="140" x2="320" y2="140" stroke="#1F1E1B" stroke-width="1.5"/>
    <line x1="30" y1="20" x2="30" y2="140" stroke="#1F1E1B" stroke-width="1.5"/>
    <text x="325" y="144" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">时间步 (交易次数 N)</text>
    <text x="25" y="15" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="end">Log Wealth</text>

    <!-- Half Kelly Path (Smooth compounder in Fir Green) -->
    <path d="M 30 110 Q 100 95 180 70 T 310 25" fill="none" stroke="#5F7355" stroke-width="2.5"/>
    <text x="315" y="28" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#5F7355">半凯利稳健复利</text>

    <!-- Full Kelly Path (Wild fluctuations in Ochre) -->
    <path d="M 30 110 Q 70 50 120 90 T 200 40 T 310 35" fill="none" stroke="#C08535" stroke-width="1.5"/>
    <text x="315" y="45" font-family="JetBrains Mono, monospace" font-size="9" fill="#C08535">全凯利 (高波动回撤)</text>

    <!-- Overbetting 2.5x Kelly Path (Crash into Ruin in Terracotta) -->
    <path d="M 30 110 Q 60 30 110 50 T 170 138 L 310 139" fill="none" stroke="#CC5A36" stroke-width="2.5"/>
    <circle cx="170" cy="138" r="5" fill="#CC5A36"/>
    <text x="240" y="130" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#CC5A36">2.5x 杠杆: 破产归零</text>
  </g>

  <!-- Right: Ruin Formula Card -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#CC5A36"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">破产概率解析解 (Risk of Ruin)</text>

    <text x="140" y="55" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#1F1E1B" text-anchor="middle">
      P(\text{Ruin}) = \left(\frac{1 - \text{Edge}}{1 + \text{Edge}}\right)^{\text{Capital} / \text{Bet}}
    </text>

    <text x="20" y="85" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 只要存在 1 次爆仓可能，长期大数定律必然兑现</text>
    <text x="20" y="105" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 几何平均收益远低于算术平均收益</text>
    <text x="20" y="125" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#5F7355">• 资深对冲基金只采用 0.3x ~ 0.5x 凯利下注</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">算术平均是无知的幻觉，几何平均才是财富积累的铁律：亏损 50% 需要盈利 100% 才能回本</text>
</svg>"""

SVGS["m06_l03_multi_asset_continuous_kelly"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.3.3：连续时间多资产凯利最优杠杆向量 f* = Σ^-1 (μ - r) 拓扑结构</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">CONTINUOUS KELLY</text>

  <!-- Center Formula Box -->
  <rect x="80" y="50" width="600" height="45" rx="6" fill="#FAF8F5" stroke="#486A7D" stroke-width="1.5"/>
  <text x="380" y="78" font-family="JetBrains Mono, monospace" font-size="13" font-weight="700" fill="#1F1E1B" text-anchor="middle">
    f^* = \Sigma^{-1} (\mu - r \mathbf{1}), \quad g(f^*) = r + \frac{1}{2} (\mu - r \mathbf{1})^T \Sigma^{-1} (\mu - r \mathbf{1})
  </text>

  <!-- 3 Dimensional Vector Decomposition Below -->
  <g transform="translate(80, 110)">
    <!-- Component 1: Excess Return Driver -->
    <rect x="0" y="0" width="180" height="75" rx="4" fill="#FAF8F5" stroke="#5F7355"/>
    <text x="90" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">超额收益驱动项 (μ - r)</text>
    <text x="15" y="45" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 确定性 Alpha / 风险溢价</text>
    <text x="15" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 收益越高，最优杠杆线性放大</text>

    <!-- Component 2: Covariance Inversion -->
    <rect x="210" y="0" width="180" height="75" rx="4" fill="#FAF8F5" stroke="#CC5A36"/>
    <text x="300" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#CC5A36" text-anchor="middle">协方差惩罚矩阵 Σ^-1</text>
    <text x="225" y="45" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 资产波动率平方惩罚</text>
    <text x="225" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 跨资产关联度对冲降噪</text>

    <!-- Component 3: Gross Leverage Constraint -->
    <rect x="420" y="0" width="180" height="75" rx="4" fill="#FAF8F5" stroke="#C08535"/>
    <text x="510" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#C08535" text-anchor="middle">总杠杆物理硬约束</text>
    <text x="435" y="45" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• ||f*||_1 &le; Max_Leverage</text>
    <text x="435" y="62" font-family="Inter, sans-serif" font-size="9" fill="#7D786F">• 防范黑天鹅隔夜跳空挤兑</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">多资产连续凯利在数学形式上等价于风险厌恶系数 λ=1 的均值-方差优化，是量化配置的最高统领式</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 04
# -----------------------------------------------------------------------------
SVGS["m06_l04_var_vs_cvar_tail_distribution"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.4.1：正态分布 vs 真实厚尾分布：VaR 阈值盲区与 CVaR 条件期望尾部损失</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">VAR VS CVAR TAILS</text>

  <!-- Left Density Plot -->
  <g transform="translate(60, 45)">
    <!-- Base Axis -->
    <line x1="20" y1="150" x2="380" y2="150" stroke="#1F1E1B" stroke-width="1.5"/>
    <text x="200" y="170" font-family="Inter, sans-serif" font-size="10" fill="#1F1E1B" text-anchor="middle">投资组合收益率 R</text>
    <text x="200" y="15" font-family="JetBrains Mono, monospace" font-size="9" fill="#7D786F" text-anchor="middle">μ = 0</text>

    <!-- Normal Distribution (Dotted Blue) -->
    <path d="M 50 148 Q 120 145 160 90 T 200 30 T 240 90 T 350 148" fill="none" stroke="#486A7D" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="310" y="100" font-family="JetBrains Mono, monospace" font-size="9" fill="#486A7D">正态高斯假设</text>

    <!-- Student-t / Fat-tailed Distribution (Solid Terracotta with huge tails) -->
    <path d="M 30 140 Q 80 135 150 90 T 200 15 T 250 90 T 370 140" fill="none" stroke="#CC5A36" stroke-width="2.5"/>
    <text x="330" y="60" font-family="Newsreader, serif" font-size="10" font-weight="700" fill="#CC5A36">真实肥尾分布 (Kurt &gt; 10)</text>

    <!-- VaR cutoff line at alpha=5% -->
    <line x1="90" y1="40" x2="90" y2="150" stroke="#C08535" stroke-width="2"/>
    <text x="90" y="32" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535" text-anchor="middle">95% VaR</text>

    <!-- CVaR Shaded Tail Area to the left of VaR -->
    <rect x="30" y="115" width="60" height="35" fill="rgba(204, 90, 54, 0.25)"/>
    
    <!-- CVaR Expected Shortfall Center Marker -->
    <circle cx="60" cy="135" r="4" fill="#CC5A36"/>
    <line x1="60" y1="135" x2="60" y2="150" stroke="#CC5A36" stroke-width="2"/>
    <text x="60" y="125" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36" text-anchor="middle">CVaR</text>
  </g>

  <!-- Right: Comparison Metrics Card -->
  <g transform="translate(480, 50)">
    <rect x="0" y="0" width="220" height="145" rx="6" fill="#FAF8F5" stroke="#E5DFD5"/>
    <text x="16" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#1F1E1B">巴塞尔协议 III 核心定论：</text>
    
    <text x="16" y="50" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B"><tspan font-weight="700">VaR 致命缺陷：</tspan> 仅给出 95% 门槛，对门槛外的灾难深浅完全失明，非凸且多次可加性失效。</text>
    
    <text x="16" y="95" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B"><tspan font-weight="700" fill="#5F7355">CVaR 绝对优势：</tspan> 严格度量击穿 VaR 后的条件期望损失，满足次可加性公理，是一致性风险度量底座。</text>

    <text x="16" y="135" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#CC5A36">厚尾真实损失: CVaR &gt;&gt; VaR</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">在流动性挤兑与崩盘日，正态 VaR 预测的“万年一遇”事件频频发生，唯有 CVaR 能守住偿付安全边际</text>
</svg>"""

SVGS["m06_l04_drawdown_high_water_mark"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.4.2：动态历史最高水位线 (HWM) 与水下回撤 (Underwater Chart) 深度刻画</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">HIGH-WATER MARK</text>

  <!-- Top Panel: Cumulative Wealth & HWM -->
  <g transform="translate(60, 45)">
    <text x="0" y="12" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#1F1E1B">累计净值与历史最高峰值 (HWM)</text>
    
    <!-- HWM Staircase (Firm Sage line) -->
    <path d="M 20 60 L 120 60 L 160 35 L 340 35 L 420 20 L 640 20" fill="none" stroke="#5F7355" stroke-width="2" stroke-dasharray="4 2"/>
    <text x="645" y="24" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">HWM 水平线</text>

    <!-- Actual Wealth Path (Graphite line dropping below HWM) -->
    <polyline points="20,60 80,75 120,60 160,35 220,95 280,110 340,35 380,65 420,20 480,85 540,55 600,30" 
              fill="none" stroke="#1F1E1B" stroke-width="2"/>

    <!-- Drawdown Shaded Area between HWM and Wealth -->
    <polygon points="160,35 220,95 280,110 340,35 160,35" fill="rgba(204, 90, 54, 0.15)"/>
    <text x="250" y="80" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#CC5A36" text-anchor="middle">深幅回撤期 MaxDD = -22.5%</text>
  </g>

  <!-- Separator Line -->
  <line x1="60" y1="140" x2="700" y2="140" stroke="#E5DFD5" stroke-width="1"/>

  <!-- Bottom Panel: Underwater Drawdown % (0 to -30%) -->
  <g transform="translate(60, 150)">
    <line x1="20" y1="10" x2="640" y2="10" stroke="#1F1E1B" stroke-width="1"/>
    <text x="10" y="14" font-family="JetBrains Mono, monospace" font-size="9" fill="#1F1E1B" text-anchor="end">0%</text>
    
    <line x1="20" y1="40" x2="640" y2="40" stroke="#CC5A36" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="10" y="44" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36" text-anchor="end">-15%</text>

    <!-- Underwater Polygon filled with Terracotta -->
    <polygon points="20,10 80,25 120,10 160,10 220,55 280,65 340,10 380,30 420,10 480,50 540,30 600,10" 
             fill="rgba(204, 90, 54, 0.25)" stroke="#CC5A36" stroke-width="1.5"/>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">水下时间（Time Underwater）比最大回撤幅度更折磨LP心理：一年不创新高往往引发机构赎回潮</text>
</svg>"""

SVGS["m06_l04_circuit_breaker_sentinel_states"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.4.3：阶梯式动态回撤风控哨兵状态转移模型 (Drawdown Sentinel State Machine)</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">SENTINEL CIRCUITS</text>

  <!-- State 1: Normal (Green) -->
  <g transform="translate(60, 60)">
    <rect x="0" y="0" width="180" height="130" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="2"/>
    <rect x="0" y="0" width="180" height="28" rx="6" fill="#5F7355"/>
    <text x="90" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">正常运行状态 (Normal)</text>

    <text x="15" y="55" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#5F7355">DD &gt; -5%</text>
    <text x="15" y="75" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 仓位乘数 Pos = 1.0</text>
    <text x="15" y="95" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 策略全功率运转</text>
    <text x="15" y="115" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">高水位附近顺风期</text>
  </g>

  <!-- Transition 1 -->
  <path d="M 245 110 L 285 110" stroke="#C08535" stroke-width="2"/>
  <text x="265" y="100" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#C08535" text-anchor="middle">DD &le; -5%</text>

  <!-- State 2: Warning (Ochre) -->
  <g transform="translate(290, 60)">
    <rect x="0" y="0" width="180" height="130" rx="6" fill="#FAF8F5" stroke="#C08535" stroke-width="2"/>
    <rect x="0" y="0" width="180" height="28" rx="6" fill="#C08535"/>
    <text x="90" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">一级预警状态 (Warning)</text>

    <text x="15" y="55" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#C08535">-10% &lt; DD &le; -5%</text>
    <text x="15" y="75" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 仓位强制缩半 Pos = 0.5</text>
    <text x="15" y="95" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 主动缩减组合方差</text>
    <text x="15" y="115" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F">净值修复后自动解锁</text>
  </g>

  <!-- Transition 2 -->
  <path d="M 475 110 L 515 110" stroke="#CC5A36" stroke-width="2"/>
  <text x="495" y="100" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#CC5A36" text-anchor="middle">DD &le; -10%</text>

  <!-- State 3: Halted (Terracotta) -->
  <g transform="translate(520, 60)">
    <rect x="0" y="0" width="180" height="130" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="2"/>
    <rect x="0" y="0" width="180" height="28" rx="6" fill="#CC5A36"/>
    <text x="90" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">二级熔断状态 (Halted)</text>

    <text x="15" y="55" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#CC5A36">DD &le; -10%</text>
    <text x="15" y="75" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 仓位清零 Pos = 0.0 (全现金)</text>
    <text x="15" y="95" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B">• 交易强制硬断路器熔断</text>
    <text x="15" y="115" font-family="Inter, sans-serif" font-size="8.5" fill="#CC5A36">人工投决会介入审查</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">决策必须严格滞后 1 期执行（T-1 信号决定 T 日仓位），彻底杜绝日内未来函数前视作弊</text>
</svg>"""

# -----------------------------------------------------------------------------
# Lesson 05
# -----------------------------------------------------------------------------
SVGS["m06_l05_barbell_allocation_architecture"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.5.1：塔勒布反脆弱杠铃 (Antifragile Barbell) 顶层资产配置架构</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">TALEB BARBELL</text>

  <!-- Left Side: Ultra-Conservative Extreme (85% - 90%) -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="260" height="145" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="2"/>
    <rect x="0" y="0" width="260" height="30" rx="6" fill="#5F7355"/>
    <text x="130" y="20" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">极端保守底座 (85% ~ 90%)</text>

    <text x="20" y="55" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#1F1E1B">超短期国债 (T-Bills) 与无风险现金</text>
    <text x="20" y="80" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 零违约风险、零久期利率风险</text>
    <text x="20" y="100" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 锁定绝对流动性，确保绝不破产</text>
    <text x="20" y="120" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 享有危机时刻扫货便宜资产的特许权</text>
    <text x="130" y="138" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#5F7355" text-anchor="middle">最大潜在亏损: 0.0%</text>
  </g>

  <!-- Middle: Barbell Connecting Rod (Middle Fragile is ZERO) -->
  <g transform="translate(325, 110)">
    <line x1="0" y1="15" x2="110" y2="15" stroke="#CC5A36" stroke-width="4"/>
    <circle cx="55" cy="15" r="14" fill="#CC5A36"/>
    <text x="55" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">✕</text>
    <text x="55" y="42" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#CC5A36" text-anchor="middle">中等风险</text>
    <text x="55" y="55" font-family="Inter, sans-serif" font-size="8.5" fill="#7D786F" text-anchor="middle">伪稳健配置 0%</text>
  </g>

  <!-- Right Side: Ultra-Aggressive Convex Extreme (10% - 15%) -->
  <g transform="translate(440, 50)">
    <rect x="0" y="0" width="260" height="145" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="2"/>
    <rect x="0" y="0" width="260" height="30" rx="6" fill="#CC5A36"/>
    <text x="130" y="20" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">极端进取凸性端 (10% ~ 15%)</text>

    <text x="20" y="55" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#1F1E1B">深度虚值期权 / 非对称黑天鹅对冲</text>
    <text x="20" y="80" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 平时承受微小且确定性权利金磨损</text>
    <text x="20" y="100" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 危机时发生 50x ~ 100x 指数级非线性暴涨</text>
    <text x="20" y="120" font-family="Inter, sans-serif" font-size="9.5" fill="#7D786F">• 享受全市场恐慌的凸性收益 (Convexity)</text>
    <text x="130" y="138" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#CC5A36" text-anchor="middle">上行无限潜能: +∞%</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">反脆弱第一性原理：拒绝平庸的中间派伪分散，将下行风险硬性锁死为 0，同时保留对正向黑天鹅的最大敞口</text>
</svg>"""

SVGS["m06_l05_higher_moments_skew_kurt"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.5.2：高阶统计矩：偏度 (Skewness) 与超额峰度 (Excess Kurtosis) 非对称图谱</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">HIGHER MOMENTS</text>

  <!-- Left: Negative Skew (Steamroller & Nickels) -->
  <g transform="translate(60, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#CC5A36" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#CC5A36" text-anchor="middle">负偏度 (Negative Skew: 压路机前捡硬币)</text>
    
    <!-- Left fat tail curve -->
    <path d="M 20 120 Q 80 115 140 100 T 220 30 T 260 120" fill="none" stroke="#CC5A36" stroke-width="2.5"/>
    <circle cx="50" cy="118" r="4" fill="#CC5A36"/>
    <text x="50" y="105" font-family="JetBrains Mono, monospace" font-size="9" fill="#CC5A36">长左厚尾</text>

    <text x="140" y="135" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">卖出深度虚值期权 / 套利资金的典型特征</text>
  </g>

  <!-- Right: Positive Skew (Convex Antifragile) -->
  <g transform="translate(420, 50)">
    <rect x="0" y="0" width="280" height="145" rx="6" fill="#FAF8F5" stroke="#5F7355" stroke-width="1.5"/>
    <text x="140" y="24" font-family="Newsreader, serif" font-size="12" font-weight="700" fill="#5F7355" text-anchor="middle">正偏度 (Positive Skew: 彩票型反脆弱收益)</text>

    <!-- Right fat tail curve -->
    <path d="M 20 120 Q 60 30 140 100 T 200 115 T 260 120" fill="none" stroke="#5F7355" stroke-width="2.5"/>
    <circle cx="230" cy="118" r="4" fill="#5F7355"/>
    <text x="230" y="105" font-family="JetBrains Mono, monospace" font-size="9" fill="#5F7355">长右厚尾</text>

    <text x="140" y="135" font-family="Inter, sans-serif" font-size="9" fill="#1F1E1B" text-anchor="middle">买入虚值期权 / 早期创投 / 趋势跟踪的特征</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">高额算术夏普往往由严重的负偏度与肥尾峰度（Kurtosis &gt; 15）粉饰而成，暴雷只是时间问题</text>
</svg>"""

SVGS["m06_l05_convexity_payoff_asymmetry"] = """<svg viewBox="0 0 760 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="250" fill="#FAF8F5" rx="8" stroke="#E5DFD5" stroke-width="1"/>
  <text x="30" y="32" font-family="Newsreader, Georgia, serif" font-size="14" font-weight="700" fill="#1F1E1B">图 6.5.3：非对称凸性回报剖面：常态 Theta 磨损 vs 极端危机 Gamma / Vega 暴击</text>
  <text x="730" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#7D786F" text-anchor="end">CONVEXITY PAYOFF</text>

  <!-- Payoff Chart -->
  <g transform="translate(100, 45)">
    <!-- Axes -->
    <line x1="40" y1="130" x2="520" y2="130" stroke="#1F1E1B" stroke-width="1.5"/>
    <line x1="280" y1="20" x2="280" y2="170" stroke="#1F1E1B" stroke-width="1.5"/>
    <text x="525" y="134" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B">市场价格变动 ΔS</text>
    <text x="275" y="20" font-family="Inter, sans-serif" font-size="9.5" fill="#1F1E1B" text-anchor="end">策略损益 PnL</text>

    <!-- Normal Market Flat Theta Loss -->
    <line x1="240" y1="140" x2="320" y2="140" stroke="#CC5A36" stroke-width="3"/>
    <text x="280" y="156" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#CC5A36" text-anchor="middle">常态下有限权利金耗损 -Theta</text>

    <!-- Extreme Crash Left Upward Spike (Deep OTM Put Convex Explosion) -->
    <path d="M 240 140 Q 140 135 60 30" fill="none" stroke="#5F7355" stroke-width="3.5"/>
    <circle cx="60" cy="30" r="5" fill="#5F7355"/>
    <text x="60" y="20" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">崩盘时 +5000% 暴赚</text>

    <!-- Extreme Rally Right Upward Spike (Deep OTM Call Convex Explosion) -->
    <path d="M 320 140 Q 420 135 500 30" fill="none" stroke="#5F7355" stroke-width="3.5"/>
    <circle cx="500" cy="30" r="5" fill="#5F7355"/>
    <text x="500" y="20" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#5F7355" text-anchor="middle">狂热时 +5000% 暴赚</text>
  </g>

  <text x="380" y="235" font-family="Inter, sans-serif" font-size="11" fill="#7D786F" text-anchor="middle">凸性（Jensen 不等式）是投资者在不确定性世界中的唯一免费午餐：波动越大，对持有人越有利</text>
</svg>"""

def main():
    target_dirs = [
        os.path.join(BASE_DIR, "06_risk_portfolio", "assets"),
        os.path.join(BASE_DIR, "06_risk_portfolio", "images"),
        os.path.join(BASE_DIR, "web", "assets", "06_risk_portfolio"),
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

    print(f"✅ 成功生成并同步模块 06 共 {count} 个纯 SVG 文件到所有对应资产目录！")

if __name__ == "__main__":
    main()
