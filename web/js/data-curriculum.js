/**
 * InvestLearning Curriculum Database (Anthropic & Quarto Enhanced)
 * 10 Modules, Institutional Grade Syllabus, Cold Tone, KaTeX Math & SVG Topology
 */

const CURRICULUM_DATA = [
  {
    "id": "m01",
    "num": "01",
    "folder": "01_macro_cycle",
    "title": "宏观经济与流动性传导",
    "title_en": "Macroeconomics & Liquidity Cycles",
    "desc": "以第一性原理拆解央行资产负债表扩张收缩、利率期限结构、通胀动力学与美林投资时钟大类资产配置框架。",
    "icon": "🌐",
    "lessons_count": 5,
    "lessons": [
      {
        "id": "m01_l01",
        "num": "01",
        "title": "央行资产负债表与净流动性模型",
        "difficulty": "进阶",
        "time": "30 分钟",
        "status": "completed",
        "objectives": [
          "掌握中央银行负债端准备金、TGA账户与隔夜逆回购（ON RRP）的三方守恒对冲机制",
          "建立宏观净流动性（Net Liquidity）对风险资产估值乘数（PE/PS）分母端的折现压制方程",
          "量化测算流动性脉冲（Liquidity Impulse）与主要宽基指数历史超额收益的弹性系数"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：现代法币体系的负债本质</div>\n                  <div class=\"callout-body\">\n                    在纯信用法币制度下，商业银行体系的流动性不取决于实体黄金存量，而取决于主权中央银行与财政部的资产负债表扩张速度。估值扩张的根本推手在于准备金充裕度，而非单纯的基本面叙事。\n                  </div>\n                </div>\n\n                <p>在评估系统性风险资产折现中枢时，首要锚点是解构美联储负债端结构对基础货币与商业银行准备金的刚性挤出效应。下图揭示了现代央行净流动性的物理流转闭环：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 1.1：美联储资产负债表流转与净流动性传导拓扑</span>\n        <span class=\"diagram-tag\">ARCH-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Fed Assets Box -->\n  <rect x=\"30\" y=\"35\" width=\"190\" height=\"70\" rx=\"6\" fill=\"#FAF8F5\" stroke=\"#486A7D\" stroke-width=\"2\"/>\n  <text x=\"125\" y=\"65\" font-family=\"Newsreader, Georgia, serif\" font-size=\"14\" font-weight=\"600\" fill=\"#1F1E1B\" text-anchor=\"middle\">美联储总资产规模</text>\n  <text x=\"125\" y=\"85\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#486A7D\" text-anchor=\"middle\">SOMA 购债 / 再贷款 (+)</text>\n  <!-- Minus TGA & RRP Box -->\n  <rect x=\"280\" y=\"35\" width=\"200\" height=\"70\" rx=\"6\" fill=\"#FAF8F5\" stroke=\"#CC5A36\" stroke-width=\"2\"/>\n  <text x=\"380\" y=\"65\" font-family=\"Newsreader, Georgia, serif\" font-size=\"14\" font-weight=\"600\" fill=\"#1F1E1B\" text-anchor=\"middle\">系统流动性抽水项</text>\n  <text x=\"380\" y=\"85\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#CC5A36\" text-anchor=\"middle\">TGA 财政部存款 + ON RRP (-)</text>\n  <!-- Equals Net Liquidity Box -->\n  <rect x=\"540\" y=\"35\" width=\"190\" height=\"70\" rx=\"6\" fill=\"#FAF8F5\" stroke=\"#5F7355\" stroke-width=\"2\"/>\n  <text x=\"635\" y=\"65\" font-family=\"Newsreader, Georgia, serif\" font-size=\"14\" font-weight=\"600\" fill=\"#1F1E1B\" text-anchor=\"middle\">银行系统有效准备金</text>\n  <text x=\"635\" y=\"85\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#5F7355\" text-anchor=\"middle\">Net Liquidity 真实估值锚</text>\n  <!-- Arrows -->\n  <line x1=\"220\" y1=\"70\" x2=\"275\" y2=\"70\" stroke=\"#7D786F\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <text x=\"250\" y=\"62\" font-family=\"JetBrains Mono, monospace\" font-size=\"14\" font-weight=\"700\" fill=\"#CC5A36\" text-anchor=\"middle\">-</text>\n  <line x1=\"480\" y1=\"70\" x2=\"535\" y2=\"70\" stroke=\"#7D786F\" stroke-width=\"2\"/>\n  <text x=\"510\" y=\"63\" font-family=\"JetBrains Mono, monospace\" font-size=\"14\" font-weight=\"700\" fill=\"#5F7355\" text-anchor=\"middle\">=</text>\n  <!-- Downward Transmission Curve -->\n  <path d=\"M 635 105 L 635 145 Q 635 165 595 165 L 125 165 Q 85 165 85 185\" fill=\"none\" stroke=\"#CC5A36\" stroke-width=\"2\" stroke-dasharray=\"4 4\"/>\n  <rect x=\"90\" y=\"160\" width=\"580\" height=\"40\" rx=\"6\" fill=\"#FBF0EB\" stroke=\"#F0D0C5\" stroke-width=\"1\"/>\n  <text x=\"380\" y=\"185\" font-family=\"Inter, sans-serif\" font-size=\"12\" font-weight=\"600\" fill=\"#CC5A36\" text-anchor=\"middle\">流动性脉冲通过资本成本 WACC 压低估值分母端，直接决定纳斯达克与大盘风险溢价</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[资产负债表恒等式]</strong>：美联储总资产（SOMA 证券组合 + 贴现窗口贷款）必须精确恒等于负债端法定准备金、财政部存款账户（TGA）与隔夜逆回购（ON RRP）之和。</li>\n                  <li><strong>[TGA 蓄水池虹吸]</strong>：美国财政部发债收缴私人流动性注入 TGA 账户，直接导致银行体系可用准备金直线下降，对成长股估值形成高位抽水。</li>\n                  <li><strong>[ON RRP 缓冲垫衰减]</strong>：当货币市场基金（MMF）在逆回购池中的沉淀资金消耗完毕后，任何新增国债发行都将 100% 消耗商业银行准备金，触发流动性硬着陆风险。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{Net Liquidity}_t = \\text{Fed Total Assets}_t - (\\text{TGA}_t + \\text{ON RRP}_t)</div>\n                  <div class=\"math-domain\">变量定义域：\\text{Assets} \\in [0, 10^{13}] \\text{ USD}, \\quad \\text{TGA}, \\text{RRP} \\ge 0</div>\n                </div>\n\n                <div class=\"callout callout-warning\">\n                  <div class=\"callout-title\">⚠️ 常见认知误区：单纯跟踪 M2 增速指标</div>\n                  <div class=\"callout-body\">\n                    传统商业银行 M2 统计存在严重的季度披露时滞，且包含定期储蓄沉淀。高频机构对冲必须以央行周度资产负债表与隔夜利率走廊为第一基准。\n                  </div>\n                </div>\n                ",
        "code": "import pandas as pd\n\ndef calculate_fed_net_liquidity(fed_total_assets: pd.Series, tga: pd.Series, rrp: pd.Series) -> pd.Series:\n    \"\"\"\n    计算美联储净流动性序列:\n    Net_Liquidity = Total_Assets - (TGA + RRP)\n    \"\"\"\n    df = pd.DataFrame({\"assets\": fed_total_assets, \"tga\": tga, \"rrp\": rrp})\n    return df[\"assets\"] - (df[\"tga\"] + df[\"rrp\"])\n\ndef compute_liquidity_impulse(net_liquidity: pd.Series, window: int = 4) -> pd.Series:\n    \"\"\"计算流动性脉冲 (百分比变化率)\"\"\"\n    return net_liquidity.pct_change(periods=window) * 100.0\n",
        "qa": [
          {
            "q": "Q1: 为什么当财政部大幅发债补充 TGA 账户时，若逆回购池（RRP）枯竭，标普500会承受极端估值折现杀伤？",
            "a": "当 RRP 尚有余量时，货币市场基金可抽回 RRP 认购短债，不冲击银行准备金；而当 RRP 耗尽，发债资金必须 100% 划扣自商业银行准备金账户，迫使一级交易商资产负债表承载力骤降，通过提高风险溢价（ERP）并打压权益资产 DCF 现值。"
          },
          {
            "q": "Q2: 中国人民银行（PBOC）的流动性投放机制与美联储有何本质不同？",
            "a": "美联储主要依赖公开市场二级国债买卖（SOMA）；而 PBOC 依赖结构性货币政策工具（MLF、再贷款、买断式逆回购及降准），具有鲜明的信贷定向引导与超额准备金率窗口指导特征。"
          },
          {
            "q": "Q3: 美联储放缓量化紧缩（QT）缩表节奏，在定价方程中属于何种性质的信号？",
            "a": "属于边际宽松偏鸽信号。放缓缩表意味着从市场抽回国债存量的速度减慢，期限溢价（Term Premium）收敛，直接压低 10Y 美债实际收益率（TIPS），从而降低权益资产的贴现率。"
          }
        ]
      },
      {
        "id": "m01_l02",
        "num": "02",
        "title": "利率期限结构与利差倒挂衰退预警",
        "difficulty": "进阶",
        "time": "35 分钟",
        "status": "completed",
        "objectives": [
          "掌握收益率曲线自然三次样条插值（Cubic Spline）与瞬时远期利率推导",
          "建立 10Y-2Y 与 10Y-3M 利差倒挂预测宏观经济衰退的 Logistic 概率模型",
          "解构利差从倒挂转向‘牛市陡峭化（Bull Steepening）’时的资产杀跌机制"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：无风险利率锚与期限溢价</div>\n                  <div class=\"callout-body\">\n                    利率期限结构是全市场机构交易员对未来实际经济增长、通胀中枢与央行基准利率路径的联合概率预期。收益率曲线形态直接决定商业银行存贷利差与金融机构信用中介意愿。\n                  </div>\n                </div>\n\n                <p>在分析长短端利率走势时，必须观察期限结构的曲率变动。下图展示了收益率曲线从常态向上倾斜到倒挂形态的微观演化：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 1.2：利率期限结构常态与倒挂形态对比</span>\n        <span class=\"diagram-tag\">CHART-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Axis -->\n  <line x1=\"60\" y1=\"180\" x2=\"720\" y2=\"180\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <line x1=\"60\" y1=\"30\" x2=\"60\" y2=\"180\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <text x=\"50\" y=\"40\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">利率%</text>\n  <text x=\"720\" y=\"198\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">到期期限 (3M, 2Y, 5Y, 10Y, 30Y)</text>\n  <!-- Normal Yield Curve (Sage Green) -->\n  <path d=\"M 70 160 Q 250 140 450 90 T 700 60\" fill=\"none\" stroke=\"#5F7355\" stroke-width=\"2.5\"/>\n  <text x=\"705\" y=\"58\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#5F7355\">常态期限溢价曲线</text>\n  <!-- Inverted Yield Curve (Terracotta) -->\n  <path d=\"M 70 70 Q 200 80 400 130 T 700 150\" fill=\"none\" stroke=\"#CC5A36\" stroke-width=\"2.5\"/>\n  <text x=\"705\" y=\"152\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#CC5A36\">倒挂形态 (衰退预警)</text>\n  <!-- 10Y - 2Y Spread Annotation -->\n  <line x1=\"280\" y1=\"95\" x2=\"280\" y2=\"135\" stroke=\"#C08535\" stroke-width=\"1.5\" stroke-dasharray=\"3 3\"/>\n  <text x=\"290\" y=\"118\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" font-weight=\"600\" fill=\"#C08535\">10Y-2Y 倒挂利差 &lt; 0 bps</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[预期假说与期限溢价]</strong>：长期利率等于未来短期利率期望均值加上持有长久期资产的不确定性补偿（Term Premium）。</li>\n                  <li><strong>[倒挂传导机制]</strong>：央行紧缩推升短端利率，但市场对远期经济悲观导致长端利率被动压低，形成利差小于零（10Y-2Y &lt; 0 bps）。</li>\n                  <li><strong>[陡峭化再定价风险]</strong>：历史上最大的股市回撤并不发生在初次倒挂时，而发生在倒挂结束、央行被迫紧急降息确诊衰退的“非意愿牛市陡峭化”区间。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{Spread}_{10Y-2Y} = (y_{10Y} - y_{2Y}) \\times 100 \\quad (\\text{bps})</div>\n                  <div class=\"math-domain\">定义域：y_{10Y}, y_{2Y} \\in [0, 0.20], \\quad \\text{Regime} = \\mathbb{I}(\\text{Spread} &lt; 0)</div>\n                </div>\n                ",
        "code": "import pandas as pd\n\ndef calculate_yield_spread(yield_10y: pd.Series, yield_2y: pd.Series) -> pd.Series:\n    \"\"\"计算 10Y-2Y 利差 (基点 bps)\"\"\"\n    return (yield_10y - yield_2y) * 100.0\n\ndef detect_inversion_regime(spread_bps: pd.Series) -> pd.Series:\n    \"\"\"返回布尔序列: True 表示处于倒挂体制 (spread < 0)\"\"\"\n    return spread_bps < 0.0\n",
        "qa": [
          {
            "q": "Q1: 为什么收益率曲线倒挂重新恢复陡峭时，反而是权益市场历史上最剧烈的杀跌期？",
            "a": "初次倒挂时实体经济与企业盈利尚有惯性；而当利差由负转正，通常伴随失业率飙升与央行启动非意愿紧急降息，衰退与企业盈利暴跌被官方确诊，导致分子端现金流发生断崖式下修。"
          },
          {
            "q": "Q2: 实际利率（TIPS）对高估值科技成长股的折现率压制机制为何？",
            "a": "科技股属于超长久期资产（现金流主要集中在 5~10 年后的远期）。根据现值公式 $PV = CF / (1+r)^T$，实际利率上升会使得高次方分母膨胀，对长久期资产的现值杀伤远大于低久期成熟价值股。"
          },
          {
            "q": "Q3: 中国国债收益率曲线极少出现深幅倒挂的原因是什么？",
            "a": "中国商业银行是国债的绝对配置主体且享受免税政策；同时央行跨周期调节流动性，利率市场化具有双轨制特征，有效抑制了极端期限利差扭曲。"
          }
        ]
      }
    ]
  },
  {
    "id": "m02",
    "num": "02",
    "folder": "02_micro_market",
    "title": "市场微观结构与订单流",
    "title_en": "Market Microstructure & Order Flow",
    "desc": "深入交易所限价订单簿（LOB）撮合物理现实、买卖点差动力学、OFI 订单流不平衡与 Almgren-Chriss 算法拆单。",
    "icon": "⚡",
    "lessons_count": 5,
    "lessons": [
      {
        "id": "m02_l01",
        "num": "01",
        "title": "限价订单簿 (LOB) 撮合与盘口深度",
        "difficulty": "进阶",
        "time": "40 分钟",
        "status": "completed",
        "objectives": [
          "建立双向价格优先、时间优先（FIFO）连续撮合引擎数据结构",
          "推导加权微观价格（Micro-Price）与买卖价差（Spread）的微观形成机制",
          "分析大额市价单连续吃单穿透引发的非线性冲击与流动性黑洞"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：蜡烛图背后的微观物理实体</div>\n                  <div class=\"callout-body\">\n                    技术分析所看到的 K 线只是微观交易完成后的事后统计残差。交易真实发生的物理世界是限价订单簿（Limit Order Book），是挂单流动性供给方与吃单侵略方纳秒级博弈的能量场。\n                  </div>\n                </div>\n\n                <p>下图展示了连续竞价交易所顶层买卖挂单排队与价差（Spread）动力学：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 2.1：限价订单簿买卖深度阶梯与流动性分布</span>\n        <span class=\"diagram-tag\">LOB-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Midline -->\n  <line x1=\"380\" y1=\"20\" x2=\"380\" y2=\"200\" stroke=\"#D7E2D8\" stroke-width=\"1\" stroke-dasharray=\"4 4\"/>\n  <text x=\"380\" y=\"18\" font-family=\"Newsreader, serif\" font-size=\"12\" font-style=\"italic\" fill=\"#7D786F\" text-anchor=\"middle\">公允中间价 Mid Price</text>\n  <!-- Bid side (Green) -->\n  <rect x=\"180\" y=\"45\" width=\"180\" height=\"22\" rx=\"4\" fill=\"rgba(95, 115, 85, 0.25)\" stroke=\"#5F7355\" stroke-width=\"1\"/>\n  <text x=\"190\" y=\"60\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#1F1E1B\">Bid 1: $100.20 (450手)</text>\n  <rect x=\"130\" y=\"75\" width=\"230\" height=\"22\" rx=\"4\" fill=\"rgba(95, 115, 85, 0.35)\" stroke=\"#5F7355\" stroke-width=\"1\"/>\n  <text x=\"140\" y=\"90\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#1F1E1B\">Bid 2: $100.15 (820手)</text>\n  <rect x=\"80\" y=\"105\" width=\"280\" height=\"22\" rx=\"4\" fill=\"rgba(95, 115, 85, 0.5)\" stroke=\"#5F7355\" stroke-width=\"1\"/>\n  <text x=\"90\" y=\"120\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#1F1E1B\">Bid 3: $100.10 (1400手 机构护盘)</text>\n  <!-- Ask side (Terracotta) -->\n  <rect x=\"400\" y=\"45\" width=\"160\" height=\"22\" rx=\"4\" fill=\"rgba(204, 90, 54, 0.25)\" stroke=\"#CC5A36\" stroke-width=\"1\"/>\n  <text x=\"550\" y=\"60\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#1F1E1B\" text-anchor=\"end\">Ask 1: $100.25 (320手)</text>\n  <rect x=\"400\" y=\"75\" width=\"210\" height=\"22\" rx=\"4\" fill=\"rgba(204, 90, 54, 0.35)\" stroke=\"#CC5A36\" stroke-width=\"1\"/>\n  <text x=\"600\" y=\"90\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#1F1E1B\" text-anchor=\"end\">Ask 2: $100.30 (690手)</text>\n  <rect x=\"400\" y=\"105\" width=\"270\" height=\"22\" rx=\"4\" fill=\"rgba(204, 90, 54, 0.5)\" stroke=\"#CC5A36\" stroke-width=\"1\"/>\n  <text x=\"660\" y=\"120\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" fill=\"#1F1E1B\" text-anchor=\"end\">Ask 3: $100.35 (1250手 阻力墙)</text>\n  <!-- Spread Marker -->\n  <line x1=\"360\" y1=\"150\" x2=\"400\" y2=\"150\" stroke=\"#C08535\" stroke-width=\"2\"/>\n  <text x=\"380\" y=\"170\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" font-weight=\"600\" fill=\"#C08535\" text-anchor=\"middle\">Spread = $0.05 (5 bps)</text>\n  <text x=\"380\" y=\"195\" font-family=\"Inter, sans-serif\" font-size=\"11\" fill=\"#7D786F\" text-anchor=\"middle\">流动性吃单穿透时，市价单沿深度曲线向上/向下产生非线性滑点</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[限价单流动性供给]</strong>：做市商与被动资金在盘口挂出限价单提供流动性，承担逆向选择风险并赚取买卖点差（Spread）。</li>\n                  <li><strong>[市价单侵略性消耗]</strong>：主动买单或卖单以市价瞬间扫荡盘口可用深度，直接改变下一时刻的公允中间价（Mid Price）。</li>\n                  <li><strong>[微观公允价格 Micro-Price]</strong>：当买一挂单量远大于卖一挂单量时，下一笔成交向上突破的概率显著升高，传统中间价存在系统性偏见。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">P_{\\text{micro}} = \\frac{V_B \\cdot P_A + V_A \\cdot P_B}{V_B + V_A}, \\quad \\text{Spread} = P_A - P_B</div>\n                  <div class=\"math-domain\">定义域：P_A &gt; P_B &gt; 0, \\quad V_A, V_B \\ge 0</div>\n                </div>\n                ",
        "code": "from typing import Dict, Tuple\n\nclass SimpleLOB:\n    def __init__(self):\n        self.bids: Dict[float, int] = {}\n        self.asks: Dict[float, int] = {}\n\n    def add_limit_order(self, side: str, price: float, volume: int):\n        target = self.bids if side == 'bid' else self.asks\n        target[price] = target.get(price, 0) + volume\n\n    def get_best_bid_ask(self) -> Tuple[float, float]:\n        best_bid = max(self.bids.keys()) if self.bids else 0.0\n        best_ask = min(self.asks.keys()) if self.asks else 0.0\n        return best_bid, best_ask\n\n    def get_spread_and_mid(self) -> Tuple[float, float]:\n        bb, ba = self.get_best_bid_ask()\n        spread = ba - bb\n        mid = (ba + bb) / 2.0\n        return spread, mid\n",
        "qa": [
          {
            "q": "Q1: 为什么在流动性枯竭时，Spread 会瞬间急剧放大？",
            "a": "在剧烈波动或知情交易者进场时，做市商为了规避被毒性订单流（Toxic Flow）逆向选择收割，会本能撤出买卖盘挂单，导致深度真空，价差拉大以补偿库存风险。"
          },
          {
            "q": "Q2: 高频交易商（HFT）为何不惜巨资部署微波基站以争夺纳秒级时间优先权？",
            "a": "限价单队列遵循 FIFO 原则。谁先排在队首，谁就拥有以无风险成本赚取买卖价差的最优成交权，后到的挂单只能充当垫背牺牲品。"
          },
          {
            "q": "Q3: 什么是虚假挂单撤单（Spoofing）？",
            "a": "庄家在盘口深处虚挂数千手巨额买单营造支撑假象，诱导散户市价跟进买入，在自己高位卖单成交的瞬间光速撤单，属于严重的市场操纵行为。"
          }
        ]
      }
    ]
  },
  {
    "id": "m03",
    "num": "03",
    "folder": "03_fundamental",
    "title": "现代基本面财务建模",
    "title_en": "Fundamental Analysis & Valuation",
    "desc": "三表动态勾稽平衡校验、杜邦五因子拆解、Beneish M-Score 8维法务舞弊排雷与两阶段自由现金流折现（DCF）。",
    "icon": "💎",
    "lessons_count": 5,
    "lessons": [
      {
        "id": "m03_l01",
        "num": "01",
        "title": "三张财务报表勾稽与杜邦五因子拆解",
        "difficulty": "核心",
        "time": "45 分钟",
        "status": "completed",
        "objectives": [
          "掌握资产负债表、利润表与现金流量表收付实现制底层勾稽平衡守恒",
          "建立现代五因子杜邦分析模型，拆解净资产收益率的真伪引擎",
          "识别依靠非经常性损益或金融负债单轮驱动推高 ROE 的高脆弱性陷阱"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：商业本质的会计恒等映射</div>\n                  <div class=\"callout-body\">\n                    市值是企业内在价值在二级市场的报价投影。无论市场先生如何狂躁，企业的最终价值必然锚定其创造自由现金流的能力。三张财务报表是透视管理层资本配置效率的绝对事实底册。\n                  </div>\n                </div>\n\n                <p>在解剖一家公司的 ROE 质量时，必须穿透表象。下图展示了现代杜邦五因子分解的层级传导链条：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 3.1：杜邦五因子分解模型与商业驱动力解构</span>\n        <span class=\"diagram-tag\">DUPONT-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Top ROE Box -->\n  <rect x=\"290\" y=\"20\" width=\"180\" height=\"42\" rx=\"6\" fill=\"#FAF8F5\" stroke=\"#CC5A36\" stroke-width=\"2\"/>\n  <text x=\"380\" y=\"46\" font-family=\"Newsreader, Georgia, serif\" font-size=\"16\" font-weight=\"700\" fill=\"#1F1E1B\" text-anchor=\"middle\">ROE 净资产收益率</text>\n  <!-- 5 Factors -->\n  <g transform=\"translate(35, 110)\">\n    <rect x=\"0\" y=\"0\" width=\"125\" height=\"55\" rx=\"5\" fill=\"#FFFFFF\" stroke=\"#486A7D\" stroke-width=\"1.5\"/>\n    <text x=\"62\" y=\"24\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#1F1E1B\" text-anchor=\"middle\">税收负担</text>\n    <text x=\"62\" y=\"42\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#486A7D\" text-anchor=\"middle\">NI / EBT</text>\n    \n    <rect x=\"140\" y=\"0\" width=\"125\" height=\"55\" rx=\"5\" fill=\"#FFFFFF\" stroke=\"#486A7D\" stroke-width=\"1.5\"/>\n    <text x=\"202\" y=\"24\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#1F1E1B\" text-anchor=\"middle\">利息负担</text>\n    <text x=\"202\" y=\"42\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#486A7D\" text-anchor=\"middle\">EBT / EBIT</text>\n\n    <rect x=\"280\" y=\"0\" width=\"130\" height=\"55\" rx=\"5\" fill=\"#FFFFFF\" stroke=\"#5F7355\" stroke-width=\"2\"/>\n    <text x=\"345\" y=\"24\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"700\" fill=\"#5F7355\" text-anchor=\"middle\">经营利润率 (核心)</text>\n    <text x=\"345\" y=\"42\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#5F7355\" text-anchor=\"middle\">EBIT / Revenue</text>\n\n    <rect x=\"425\" y=\"0\" width=\"125\" height=\"55\" rx=\"5\" fill=\"#FFFFFF\" stroke=\"#5F7355\" stroke-width=\"2\"/>\n    <text x=\"487\" y=\"24\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"700\" fill=\"#5F7355\" text-anchor=\"middle\">资产周转率 (效率)</text>\n    <text x=\"487\" y=\"42\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#5F7355\" text-anchor=\"middle\">Revenue / Assets</text>\n\n    <rect x=\"565\" y=\"0\" width=\"125\" height=\"55\" rx=\"5\" fill=\"#FFFFFF\" stroke=\"#C08535\" stroke-width=\"1.5\"/>\n    <text x=\"627\" y=\"24\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#C08535\" text-anchor=\"middle\">权益乘数 (杠杆风险)</text>\n    <text x=\"627\" y=\"42\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#C08535\" text-anchor=\"middle\">Assets / Equity</text>\n  </g>\n  <!-- Connector lines -->\n  <line x1=\"380\" y1=\"62\" x2=\"380\" y2=\"90\" stroke=\"#7D786F\" stroke-width=\"1.5\"/>\n  <path d=\"M 95 110 L 95 90 L 690 90 L 690 110\" fill=\"none\" stroke=\"#7D786F\" stroke-width=\"1.5\"/>\n  <text x=\"380\" y=\"195\" font-family=\"Inter, sans-serif\" font-size=\"11\" fill=\"#7D786F\" text-anchor=\"middle\">真正具备护城河的企业依赖“高经营利润率”与“高周转”，而非过度仰仗“权益乘数”单腿冲刺</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[经营利润率与资产周转率]</strong>：真正优秀的护城河企业（如茅台、苹果、Costco）依靠定价权（高 EBIT 利润率）或极高运营周转（高资产周转率）驱动 ROE。</li>\n                  <li><strong>[利息负担与税收侵蚀]</strong>：息税前利润（EBIT）经财务费用与所得税扣减后才是属于股东的净利润，利息保障倍数过低将放大违约脆弱性。</li>\n                  <li><strong>[权益乘数杠杆双刃剑]</strong>：依靠激进举债推高的 ROE 在宏观去杠杆周期中极易发生流动性挤兑与断崖式归零。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{ROE} = \\frac{\\text{NI}}{\\text{EBT}} \\times \\frac{\\text{EBT}}{\\text{EBIT}} \\times \\frac{\\text{EBIT}}{\\text{Rev}} \\times \\frac{\\text{Rev}}{\\text{Assets}} \\times \\frac{\\text{Assets}}{\\text{Equity}}</div>\n                  <div class=\"math-domain\">定义域：\\text{Rev}, \\text{Assets}, \\text{Equity} &gt; 0, \\quad \\text{ROE} \\in [-\\infty, +\\infty]</div>\n                </div>\n                ",
        "code": "def dupont_5_factor(net_income: float, ebt: float, ebit: float, revenue: float, total_assets: float, equity: float) -> dict:\n    tax_burden = net_income / ebt\n    interest_burden = ebt / ebit\n    operating_margin = ebit / revenue\n    asset_turnover = revenue / total_assets\n    equity_multiplier = total_assets / equity\n    roe = net_income / equity\n    return {\n        \"tax_burden\": tax_burden,\n        \"interest_burden\": interest_burden,\n        \"operating_margin\": operating_margin,\n        \"asset_turnover\": asset_turnover,\n        \"equity_multiplier\": equity_multiplier,\n        \"roe\": roe\n    }\n",
        "qa": [
          {
            "q": "Q1: 为什么经营性现金流净额持续小于净利润是上市公司财报排雷的头号红线？",
            "a": "权责发生制下，企业可通过向渠道激进塞货确认应收账款虚增利润，但收付实现制下的现金流无法伪造。若利润无法转化为银行存款真金白银，往往掩盖着存货滞销或账面造假。"
          },
          {
            "q": "Q2: 区分 Costco 模式与传统高杠杆房企的杜邦驱动本质差异。",
            "a": "Costco 依靠会员特许权和极致供应链实现极高的资产周转率（>3.5次）驱动高质量 ROE；而传统房企利润率微薄，完全依赖高负债（权益乘数 > 8倍）赌资产升值，一旦下行周期来临必然爆雷。"
          },
          {
            "q": "Q3: 为什么商誉减值对当期经营活动现金流毫无影响，却对资产负债表与净利润具有毁灭性打击？",
            "a": "商誉在收购时已完成了现金支付。后续计提商誉减值属于纯账面非现金减值损失，不影响当期经营进出流水，但会永久性摧毁账面股东权益并导致报表净利润巨亏。"
          }
        ]
      }
    ]
  },
  {
    "id": "m04",
    "num": "04",
    "folder": "04_technical_pa",
    "title": "价格行为学与技术分析",
    "title_en": "Price Action & Quantitative Technicals",
    "desc": "剥离滞后玄学指标，以价格行为学（Price Action）、市场结构突破（BOS/CHoCH）、订单块（Order Blocks）与无未来函数信号构建交易逻辑。",
    "icon": "📈",
    "lessons_count": 5,
    "lessons": [
      {
        "id": "m04_l01",
        "num": "01",
        "title": "价格行为学与市场结构识别",
        "difficulty": "进阶",
        "time": "35 分钟",
        "status": "completed",
        "objectives": [
          "建立严格的摆动高点（Swing High）与波谷低点（Swing Low）数学识别算法",
          "量化判定顺势结构突破（BOS）与趋势反转性质转变（CHoCH）状态机",
          "利用多时间周期结构共振过滤 80% 的震荡市假突破噪音"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：道氏理论的价格序列拓扑化</div>\n                  <div class=\"callout-body\">\n                    任何资产的价格趋势本质上是离散时间波峰波谷序列的相对位置转移。牛市的定义是不断产生更高的高点（HH）与更高的低点（HL），熊市则是连续产生更低的高点（LH）与更低的低点（LL）。\n                  </div>\n                </div>\n\n                <p>下图展示了从顺势结构突破（BOS）到趋势终结角色反转（CHoCH）的严格价格拓扑变化：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 4.1：价格行为学市场结构突破 (BOS) 与反转 (CHoCH) 状态机</span>\n        <span class=\"diagram-tag\">SMC-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Bullish Trend Leg -->\n  <polyline points=\"50,170 120,90 170,130 260,50 320,100 420,25\" fill=\"none\" stroke=\"#5F7355\" stroke-width=\"2.5\"/>\n  <!-- Swing High & Low markers -->\n  <circle cx=\"120\" cy=\"90\" r=\"4\" fill=\"#5F7355\"/>\n  <text x=\"120\" y=\"78\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#5F7355\" text-anchor=\"middle\">HH 1</text>\n  <circle cx=\"260\" cy=\"50\" r=\"4\" fill=\"#5F7355\"/>\n  <text x=\"260\" y=\"38\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#5F7355\" text-anchor=\"middle\">HH 2</text>\n  <!-- BOS Breakout Line -->\n  <line x1=\"120\" y1=\"90\" x2=\"260\" y2=\"90\" stroke=\"#486A7D\" stroke-width=\"1.5\" stroke-dasharray=\"4 4\"/>\n  <text x=\"190\" y=\"84\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" font-weight=\"600\" fill=\"#486A7D\">BOS 顺势突破</text>\n  <!-- Higher Low (HL) -->\n  <circle cx=\"320\" cy=\"100\" r=\"4\" fill=\"#5F7355\"/>\n  <text x=\"320\" y=\"118\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#5F7355\" text-anchor=\"middle\">关键防守 HL</text>\n  <!-- Reversal Breakdown (CHoCH) -->\n  <polyline points=\"420,25 480,150 540,110 650,200\" fill=\"none\" stroke=\"#CC5A36\" stroke-width=\"2.5\"/>\n  <line x1=\"320\" y1=\"100\" x2=\"490\" y2=\"100\" stroke=\"#CC5A36\" stroke-width=\"1.5\" stroke-dasharray=\"4 4\"/>\n  <text x=\"410\" y=\"115\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" font-weight=\"700\" fill=\"#CC5A36\">CHoCH 性质转变 (跌穿 HL 转空)</text>\n  <circle cx=\"540\" cy=\"110\" r=\"4\" fill=\"#CC5A36\"/>\n  <text x=\"540\" y=\"98\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#CC5A36\" text-anchor=\"middle\">LH 1 (次高做空点)</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[BOS 顺势突破]</strong>：价格突破前期摆动高点并以实体蜡烛收盘确认，标志着机构主买力量延续趋势。</li>\n                  <li><strong>[HL 防守底线]</strong>：最近一个抬高的低点（HL）是多头阵地的防守生命线，击穿前趋势始终有效。</li>\n                  <li><strong>[CHoCH 反转信号]</strong>：当价格首次跌穿最近的 HL，宣告多头结构破裂，市场进入角色转变转为空头主导。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{Trend}_t = \\begin{cases} \\text{BULL}, & \\text{if } H_t &gt; H_{t-1} \\land L_t &gt; L_{t-1} \\\\ \\text{BEAR}, & \\text{if } H_t &lt; H_{t-1} \\land L_t &lt; L_{t-1} \\\\ \\text{RANGE}, & \\text{otherwise} \\end{cases}</div>\n                  <div class=\"math-domain\">定义域：H_t, L_t \\in \\mathbb{R}^+, \\quad H_t &gt; L_t</div>\n                </div>\n                ",
        "code": "from typing import List\n\ndef identify_market_trend(highs: List[float], lows: List[float]) -> str:\n    if highs[1] > highs[0] and lows[1] > lows[0]:\n        return 'BULL'\n    elif highs[1] < highs[0] and lows[1] < lows[0]:\n        return 'BEAR'\n    else:\n        return 'RANGE'\n",
        "qa": [
          {
            "q": "Q1: 为什么移动平均线交叉在横盘市中频繁产生摩擦损耗，而市场结构突破具有更高的信噪比？",
            "a": "移动平均线属于时域低通滤波器，具有数学上不可消除的固定时间滞后；而结构突破直接对应供需边界的物理破位，能第一时间反映机构订单意图。"
          },
          {
            "q": "Q2: 怎样区分影线刺破流动性扫荡（Wick Sweep）与有效结构突破？",
            "a": "有效突破要求蜡烛实体（Candle Body）稳固收盘在前高阻力线之外；若仅仅影线刺破后收盘快速拉回，属于典型的诱多流动性扫荡。"
          },
          {
            "q": "Q3: 多时间周期共振在交易执行中的具体规则为何？",
            "a": "日线/周线决定大级别主趋势与多空偏向，15分钟/1小时负责定位 CHoCH 入场点位与设置微小止损，严格顺大级别逆小级别。"
          }
        ]
      }
    ]
  },
  {
    "id": "m05",
    "num": "05",
    "folder": "05_quant_trading",
    "title": "量化多因子与统计套利",
    "title_en": "Quantitative Multi-Factor & StatArb",
    "desc": "单因子检验（IC/RankIC/ICIR）、Fama-French 多因子回归、Barra 风险模型与协整配对均值回归。",
    "icon": "🧬",
    "lessons_count": 5,
    "lessons": [
      {
        "id": "m05_l01",
        "num": "01",
        "title": "单因子评价框架与 IC / Rank IC 计算",
        "difficulty": "核心",
        "time": "40 分钟",
        "status": "completed",
        "objectives": [
          "掌握横截面信息系数（IC）与斯皮尔曼秩相关系数（Rank IC）的统计计算",
          "建立多周期因子衰减（Factor Decay）与信息比率（ICIR）稳定性评价体系",
          "实现全市场股票池分位数单调收益回测与多空 Alpha 收益剥离"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：投资基础法则 (Fundamental Law)</div>\n                  <div class=\"callout-body\">\n                    理查德·格林诺德（Richard Grinold）提出的主动管理基本法则：$IR = IC \\times \\sqrt{Breadth}$。量化对冲的核心不在于某一次预测的惊人准确度，而在于拥有微弱正向的预测优势（$IC &gt; 0$）并在大量独立股票（$Breadth$）上成千上万次重复下注。\n                  </div>\n                </div>\n\n                <ul class=\"label-list\">\n                  <li><strong>[Rank IC 鲁棒性优势]</strong>：传统 Pearson IC 受个股极端异常值干扰极大，Rank IC 通过对横截面因子值与收益率分别排序，具备高度的抗噪能力。</li>\n                  <li><strong>[ICIR 稳定性指标]</strong>：$ICIR = \\text{Mean}(IC) / \\text{Std}(IC) \\times \\sqrt{12}$。优秀的因子不仅要求均值显著大于 0，更要求波动率极低。</li>\n                  <li><strong>[分位数单调性检验]</strong>：将全市场股票按因子得分均匀划分为 5 组或 10 组，检验收益率是否呈现严格单调递增，剔除虚假非线性过拟合。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{Rank IC}_t = \\text{Corr}(\\text{rank}(F_{i, t}), \\text{rank}(R_{i, t+1}))</div>\n                  <div class=\"math-domain\">统计显著性检验：t = \\frac{\\text{Mean}(\\text{IC})}{\\text{Std}(\\text{IC})} \\sqrt{T} &gt; 2.0</div>\n                </div>\n                ",
        "code": "import pandas as pd\n\ndef calculate_rank_ic(factor_scores: pd.Series, forward_returns: pd.Series) -> float:\n    \"\"\"计算单个横截面上的 Spearman Rank IC\"\"\"\n    return factor_scores.corr(forward_returns, method='spearman')\n",
        "qa": [
          {
            "q": "Q1: 为什么在因子回测前必须进行行业市值中性化？",
            "a": "许多未中性化的因子实质上只是大盘股或特定周期行业的暴露代号。只有剥离行业与市值影响，才能验证其是否具有真正的选股特质 Alpha。"
          },
          {
            "q": "Q2: 什么是因子拥挤度（Factor Crowding）？",
            "a": "当大量量化基金采用相同开源因子建仓，买入端被过度推高。一旦遭遇宏观冲击或流动性抽离，将引发多只基金同步赎回踩踏，导致因子收益瞬间崩塌。"
          },
          {
            "q": "Q3: 怎样评估因子的生命周期衰减半衰期？",
            "a": "计算当前因子与未来第 $k$ 期收益率的相关性 $IC(k)$，绘制自相关衰减曲线，观察 IC 跌至峰值一半所需的持有期天数。"
          }
        ]
      }
    ]
  },
  {
    "id": "m06",
    "num": "06",
    "folder": "06_risk_portfolio",
    "title": "投资组合与仓位风控",
    "title_en": "Portfolio Theory & Risk Sizing",
    "desc": "马科维茨有效前沿优化、全天候风险平价（Risk Parity）、凯利公式数学推导与破产悬崖风控。",
    "icon": "⚖️",
    "lessons_count": 5,
    "lessons": [
      {
        "id": "m06_l01",
        "num": "01",
        "title": "马科维茨均值-方差与有效前沿",
        "difficulty": "核心",
        "time": "40 分钟",
        "status": "completed",
        "objectives": [
          "建立多资产期望收益率向量与协方差矩阵的二次规划优化模型",
          "推导全局最小方差组合（MVP）与资本配置线（CAL）最大夏普切点组合",
          "理解资产间负相关性在不牺牲组合预期收益前提下压制总波动率的数学证明"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：唯一免费的午餐是资产配置</div>\n                  <div class=\"callout-body\">\n                    马科维茨证明了：只要资产间收益相关系数 $\\rho &lt; 1$，组合的总体方差必然小于单资产方差的加权平均。分散化投资能够在不牺牲预期收益的同时消除非系统性特质风险。\n                  </div>\n                </div>\n\n                <p>下图展示了马科维茨双曲线有效前沿与无风险资产引入后的最大夏普资本配置线（CAL）：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 6.1：马科维茨均值-方差有效前沿与最大夏普切点组合</span>\n        <span class=\"diagram-tag\">MVO-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Axes -->\n  <line x1=\"70\" y1=\"180\" x2=\"710\" y2=\"180\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <line x1=\"70\" y1=\"30\" x2=\"70\" y2=\"180\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <text x=\"60\" y=\"40\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">预期收益 E[R]</text>\n  <text x=\"710\" y=\"198\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">波动率 σ</text>\n  <!-- Efficient Frontier Hyperbola -->\n  <path d=\"M 210 135 Q 200 95 320 60 T 680 35\" fill=\"none\" stroke=\"#486A7D\" stroke-width=\"2.5\"/>\n  <path d=\"M 210 135 Q 260 160 450 175\" fill=\"none\" stroke=\"#A6A095\" stroke-width=\"1.5\" stroke-dasharray=\"3 3\"/>\n  <!-- Tangency Portfolio & CAL -->\n  <line x1=\"70\" y1=\"150\" x2=\"650\" y2=\"30\" stroke=\"#C08535\" stroke-width=\"2\"/>\n  <circle cx=\"360\" cy=\"72\" r=\"5\" fill=\"#C08535\"/>\n  <text x=\"375\" y=\"68\" font-family=\"Newsreader, serif\" font-size=\"13\" font-weight=\"700\" fill=\"#C08535\">最大夏普切点组合 (Tangency)</text>\n  <!-- MVP -->\n  <circle cx=\"210\" cy=\"135\" r=\"4\" fill=\"#5F7355\"/>\n  <text x=\"200\" y=\"152\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#5F7355\" text-anchor=\"middle\">最小方差组合 (MVP)</text>\n  <!-- Risk Free Rate -->\n  <circle cx=\"70\" cy=\"150\" r=\"3\" fill=\"#7D786F\"/>\n  <text x=\"62\" y=\"154\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">Rf</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[有效前沿双曲线]</strong>：在给定波动率约束下能达到的最高收益点轨迹，任何位于曲线下方的组合均为非有效劣势组合。</li>\n                  <li><strong>[切线组合 Tangency Portfolio]</strong>：从无风险利率 $R_f$ 出发做有效前沿的切线，切点拥有全市场最高夏普比率（Sharpe Ratio）。</li>\n                  <li><strong>[协方差矩阵敏感性问题]</strong>：直接对样本协方差矩阵求逆容易导致极端权重配置，工程实践中必须采用 Ledoit-Wolf 收缩估计进行正则化。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\min_w \\frac{1}{2} w^T \\Sigma w \\quad \\text{s.t.} \\quad w^T \\mu = R_p, \\quad \\sum w_i = 1, \\quad w_i \\ge 0</div>\n                  <div class=\"math-domain\">参数定义：w \\in \\mathbb{R}^N, \\quad \\Sigma \\in \\mathbb{R}^{N \\times N} \\text{ 为半正定协方差矩阵}</div>\n                </div>\n                ",
        "code": "import numpy as np\n\ndef calculate_portfolio_performance(weights: np.ndarray, expected_returns: np.ndarray, cov_matrix: np.ndarray) -> tuple:\n    ret = float(np.dot(weights, expected_returns))\n    vol = float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))\n    return ret, vol\n",
        "qa": [
          {
            "q": "Q1: 为什么马科维茨纯数学优化被称为‘误差放大器（Error Maximizer）’？",
            "a": "优化器对微小的期望收益估计误差极度敏感，倾向于给历史收益最高但估计误差最大的资产分配最大仓位，实盘表现极度脆弱。"
          },
          {
            "q": "Q2: 索提诺比率（Sortino Ratio）相较于夏普比率的优势是什么？",
            "a": "夏普比率将向上的暴涨波动也惩罚为风险，而索提诺比率只惩罚跌破目标收益的下行半方差（Downside Deviation），更符合理性的风险厌恶心理。"
          },
          {
            "q": "Q3: 怎样利用风险平价（Risk Parity）解决股票承担 90% 风险敞口的问题？",
            "a": "让每个资产对组合总方差的边际风险贡献（MRC）相等，使低波动债券与高波动股票处于平等的风险预算地位。"
          }
        ]
      },
      {
        "id": "m06_l03",
        "num": "03",
        "title": "凯利公式数学推导与破产概率模型",
        "difficulty": "核心",
        "time": "45 分钟",
        "status": "completed",
        "objectives": [
          "推导长期对数资本几何增长率最大化的凯利解析解",
          "建立高斯连续收益下的连续凯利公式 $f^* = \\mu / \\sigma^2$",
          "量化证明当注码比例超过 $2f^*$ 时的‘破产峭壁’与遍历性坍缩"
        ],
        "theory": "\n                <div class=\"callout callout-warning\">\n                  <div class=\"callout-title\">⚠️ 投决会首要铁律：绝不触碰吸收态壁垒 (Never Blow Up)</div>\n                  <div class=\"callout-body\">\n                    在真实世界的时间序列复利中，资金本金归零属于不可逆的‘吸收态’（Absorbing Barrier）。凯利公式是数学上唯一能够保证几何平均增长率最大的仓位分配解，但过度下注会导致毁灭性灾难。\n                  </div>\n                </div>\n\n                <p>下图展示了复利增长率 $g(f)$ 与下注仓位比例的非对称关系及破产悬崖：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 6.2：凯利公式资本增长率曲线与破产悬崖</span>\n        <span class=\"diagram-tag\">KELLY-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Axes -->\n  <line x1=\"60\" y1=\"160\" x2=\"710\" y2=\"160\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <line x1=\"60\" y1=\"30\" x2=\"60\" y2=\"190\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <text x=\"50\" y=\"40\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">复利增长率 g(f)</text>\n  <text x=\"710\" y=\"150\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">下注比例 f</text>\n  <!-- Kelly Curve -->\n  <path d=\"M 60 160 Q 230 40 340 50 Q 450 60 520 160 Q 560 205 600 215\" fill=\"none\" stroke=\"#486A7D\" stroke-width=\"2.5\"/>\n  <!-- Optimal f* -->\n  <circle cx=\"340\" cy=\"50\" r=\"5\" fill=\"#5F7355\"/>\n  <line x1=\"340\" y1=\"50\" x2=\"340\" y2=\"160\" stroke=\"#5F7355\" stroke-width=\"1.5\" stroke-dasharray=\"3 3\"/>\n  <text x=\"340\" y=\"40\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" font-weight=\"700\" fill=\"#5F7355\" text-anchor=\"middle\">最优全凯利 f* (最大期望增长)</text>\n  <!-- Half Kelly (Terracotta) -->\n  <circle cx=\"200\" cy=\"85\" r=\"4\" fill=\"#CC5A36\"/>\n  <text x=\"200\" y=\"75\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" font-weight=\"600\" fill=\"#CC5A36\" text-anchor=\"middle\">半凯利 0.5f* (机构首选)</text>\n  <!-- 2f* Ruin Cliff -->\n  <circle cx=\"520\" cy=\"160\" r=\"5\" fill=\"#CC5A36\"/>\n  <line x1=\"520\" y1=\"30\" x2=\"520\" y2=\"190\" stroke=\"#CC5A36\" stroke-width=\"1.5\" stroke-dasharray=\"2 2\"/>\n  <text x=\"530\" y=\"145\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"700\" fill=\"#CC5A36\">2f* 破产悬崖 (g &lt; 0 必然归零)</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[最优全凯利点 $f^*$]</strong>：在峰值点资本几何复合增长率达到理论极值，但伴随着极其剧烈的心脏级净值回撤（经常回撤 >50%）。</li>\n                  <li><strong>[半凯利防守首选]</strong>：采用 $0.5 f^*$ 仓位下注，能够保留全凯利 75% 的复合增长速度，同时将回撤方差大幅压缩 50% 以上。</li>\n                  <li><strong>[2倍凯利破产悬崖]</strong>：若贪婪重仓使得下注比例 $f \\ge 2 f^*$，由于波动率拖累，长期几何平均增长率 $g(f) &lt; 0$，财富在大数定律下 100% 必然归零。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">f^* = \\frac{p \\cdot b - (1 - p)}{b} = \\frac{\\mu}{\\sigma^2}</div>\n                  <div class=\"math-domain\">参数定义域：p \\in (0, 1) \\text{ (胜率)}, \\quad b &gt; 0 \\text{ (盈亏比)}, \\quad f^* \\in [0, 1]</div>\n                </div>\n                ",
        "code": "def kelly_fraction(p: float, b: float) -> float:\n    val = (p * b - (1.0 - p)) / b\n    return max(0.0, val)\n",
        "qa": [
          {
            "q": "Q1: 为什么胜率高达 80% 的策略，如果满仓下注在小概率黑天鹅事件中依然必然归零？",
            "a": "因为多次博弈是连乘过程。只要单次遇到跌停穿仓爆仓（$1-100\\%=0$），乘积立刻为零，此前的 100 次翻倍全部被清算。"
          },
          {
            "q": "Q2: 为什么机构基金经理普遍严格执行半凯利（Half-Kelly）？",
            "a": "真实市场的胜率和盈亏比是动态估计值而非确定常量。半凯利提供了极大的估计容错安全垫，避免了估计过高跌入 $2f^*$ 破产悬崖。"
          },
          {
            "q": "Q3: 怎样根据宏观流动性紧缩动态缩放凯利下注系数？",
            "a": "当 VIX 突破 30 或市场流动性收紧时，主动将凯利分数由 $0.5 f^*$ 下调至 $0.2 f^*$，提升现金头寸以保全本金。"
          }
        ]
      }
    ]
  },
  {
    "id": "m07",
    "num": "07",
    "folder": "07_psychology_execution",
    "title": "交易心理学与执行纪律",
    "title_en": "Behavioral Finance & Psychology",
    "desc": "卡尼曼前景理论（Prospect Theory）、处置效应量化度量（PGR vs PLR）与交易冷静期风控状态机。",
    "icon": "🧠",
    "lessons_count": 4,
    "lessons": [
      {
        "id": "m07_l01",
        "num": "01",
        "title": "前景理论与处置效应量化度量",
        "difficulty": "核心",
        "time": "35 分钟",
        "status": "completed",
        "objectives": [
          "掌握卡尼曼与特沃斯基前景理论 S 型主观价值函数数学特征",
          "量化计算已实现盈利比例（PGR）与已实现亏损比例（PLR）的处置效应偏离",
          "建立生理内分泌与情绪对冲的机械化不可篡改硬止损契约"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：人类进化生理缺陷对交易的诅咒</div>\n                  <div class=\"callout-body\">\n                    人类大脑在数十万年丛林演化中形成了对确定性食物的渴望与对肉体伤害的逃避本能。但在二级市场中，这种生物本能表现为‘微赚即跑、大亏死扛’的处置效应，与‘截断亏损、让利润奔跑’的复利规律完全背道而驰。\n                  </div>\n                </div>\n\n                <p>下图展示了诺奖得主卡尼曼揭示的非对称 S 型主观效用价值曲线：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 7.1：前景理论主观效用 S 型价值函数与损失厌恶</span>\n        <span class=\"diagram-tag\">PSYCH-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Axis Center -->\n  <line x1=\"70\" y1=\"110\" x2=\"690\" y2=\"110\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <line x1=\"380\" y1=\"20\" x2=\"380\" y2=\"200\" stroke=\"#A6A095\" stroke-width=\"1.5\"/>\n  <text x=\"690\" y=\"105\" font-family=\"Inter, sans-serif\" font-size=\"11\" fill=\"#7D786F\" text-anchor=\"end\">真实收益 (+)</text>\n  <text x=\"75\" y=\"105\" font-family=\"Inter, sans-serif\" font-size=\"11\" fill=\"#7D786F\">真实亏损 (-)</text>\n  <text x=\"370\" y=\"30\" font-family=\"Inter, sans-serif\" font-size=\"11\" fill=\"#7D786F\" text-anchor=\"end\">主观效用 V(+)</text>\n  <text x=\"370\" y=\"195\" font-family=\"Inter, sans-serif\" font-size=\"11\" fill=\"#7D786F\" text-anchor=\"end\">痛苦程度 V(-)</text>\n  <!-- S-Curve -->\n  <path d=\"M 120 195 Q 260 185 380 110 Q 500 35 640 25\" fill=\"none\" stroke=\"#CC5A36\" stroke-width=\"2.5\"/>\n  <text x=\"540\" y=\"45\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#5F7355\">盈利区：凹函数 (厌恶风险, 急于获利了结)</text>\n  <text x=\"140\" y=\"175\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#CC5A36\">亏损区：凸函数 (追求风险, 死扛加仓摊平)</text>\n  <!-- Steepness comparison -->\n  <text x=\"380\" y=\"212\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#C08535\" text-anchor=\"middle\">斜率对比: 损失厌恶系数 λ ≈ 2.25 (亏损的痛苦是同等盈利快乐的 2 倍以上)</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[损失厌恶系数 $\\lambda \\approx 2.25$]</strong>：亏损 1 万元带来的精神痛苦，需要获得 2.25 万元以上的收益才能勉强抚平。</li>\n                  <li><strong>[盈利区凹函数]</strong>：散户在盈利时极度厌恶风险，生怕到手收益回吐，倾向于过早平仓出局。</li>\n                  <li><strong>[亏损区凸函数]</strong>：散户在套牢时反而转变为极端的风险偏好者，死扛翻本甚至不理智加仓，最终走向巨亏深渊。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{DE} = \\text{PGR} - \\text{PLR} = \\frac{\\text{RG}}{\\text{RG} + \\text{PG}} - \\frac{\\text{RL}}{\\text{RL} + \\text{PL}}</div>\n                  <div class=\"math-domain\">判断标准：\\text{DE} &gt; 0 \\implies \\text{显著的‘卖赢家抱输家’致命行为偏差}</div>\n                </div>\n                ",
        "code": "def calculate_disposition_effect(pgr: float, plr: float) -> float:\n    return float(pgr - plr)\n",
        "qa": [
          {
            "q": "Q1: 为什么散户被套 10% 时不愿割肉，而在被套 50% 时反而彻底躺平不再看盘？",
            "a": "根据 S 型价值函数的边际递减效应，从亏损 40% 扩大到 50% 带来的边际新增痛苦极小。散户通过不看盘将未实现账面亏损隔离在心理账户之外，逃避自尊心受挫。"
          },
          {
            "q": "Q2: 沉没成本谬误如何诱导交易员在逻辑破产的头寸上继续加仓？",
            "a": "交易员错误地将已经沉没的本金损失作为当前决策的参考点，试图通过在错误方向上追加风险敞口摊薄成本，直至触发穿仓。"
          },
          {
            "q": "Q3: 怎样利用程序化挂单强制消除人类决策犹豫？",
            "a": "开仓委托与止损挂单必须原子化同时送入交易所柜台，将平仓决策权彻底移交给撮合引擎，剥夺大脑临场情绪妥协的机会。"
          }
        ]
      }
    ]
  },
  {
    "id": "m08",
    "num": "08",
    "folder": "08_derivatives_hedge",
    "title": "衍生品定价与波动率对冲",
    "title_en": "Derivatives & Volatility Hedging",
    "desc": "Black-Scholes-Merton 欧式期权连续定价、Put-Call Parity、五大希腊字母（Delta/Gamma/Vega/Theta）与波动率交易。",
    "icon": "🛡️",
    "lessons_count": 4,
    "lessons": [
      {
        "id": "m08_l01",
        "num": "01",
        "title": "BSM 期权连续定价与平价公式",
        "difficulty": "进阶",
        "time": "45 分钟",
        "status": "completed",
        "objectives": [
          "推导 Black-Scholes-Merton 偏微分方程无套利动态复制闭式解",
          "掌握看涨看跌期权平价公式（Put-Call Parity）无套利均衡校验",
          "建立做市商转换套利（Conversion）与反转套利（Reversal）价差模型"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：从一维线性工具到多维曲面博弈</div>\n                  <div class=\"callout-body\">\n                    股票只能表达对方向（Direction）的一维线性观点；而期权衍生品赋予了专业机构对‘方向、时间价值耗损（Theta）与波动率水平（Vega）’三个独立自由度同时下注或对冲的高维统治力。\n                  </div>\n                </div>\n\n                <p>下图展示了期权希腊字母 Delta 随标的价格变化的 S 型曲面与 Gamma 极值峰值分布：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 8.1：期权 Delta 灵敏度曲线与 Gamma 加速度分布</span>\n        <span class=\"diagram-tag\">OPT-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Call Delta S-curve -->\n  <path d=\"M 100 170 Q 300 170 380 95 Q 460 20 660 20\" fill=\"none\" stroke=\"#486A7D\" stroke-width=\"2.5\"/>\n  <line x1=\"380\" y1=\"20\" x2=\"380\" y2=\"180\" stroke=\"#7D786F\" stroke-width=\"1\" stroke-dasharray=\"3 3\"/>\n  <circle cx=\"380\" cy=\"95\" r=\"4\" fill=\"#C08535\"/>\n  <text x=\"380\" y=\"112\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" font-weight=\"600\" fill=\"#C08535\" text-anchor=\"middle\">平值 ATM (Delta ≈ 0.50)</text>\n  <text x=\"150\" y=\"155\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\">深度虚值 OTM (Delta → 0)</text>\n  <text x=\"610\" y=\"40\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#5F7355\">深度实值 ITM (Delta → 1)</text>\n  <!-- Gamma Peak Bell Curve -->\n  <path d=\"M 220 180 Q 380 30 540 180\" fill=\"none\" stroke=\"#5F7355\" stroke-width=\"2\" stroke-dasharray=\"4 2\"/>\n  <text x=\"460\" y=\"55\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#5F7355\">Gamma 钟形曲线 (平值附近曲率与加速度最高)</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[Delta 复制与对冲]</strong>：Delta 度量标的价格变动对期权价值的一阶敏感度。通过持有现货并做空对应 Delta 份期权，可构造局部的 Delta 中性组合。</li>\n                  <li><strong>[Gamma 曲率与非线性]</strong>：平值期权（ATM）拥有最高的 Gamma，标的价格的微小跳跃会引发 Delta 的剧烈再平衡。</li>\n                  <li><strong>[无套利平价关系]</strong>：欧式看涨与看跌期权通过标的资产和无风险折现贴现紧密锚定，任何微小脱节都会被做市商光速抹平。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">C - P = S - K e^{-rT}, \\quad d_1 = \\frac{\\ln(S/K) + (r + \\frac{1}{2}\\sigma^2)T}{\\sigma \\sqrt{T}}</div>\n                  <div class=\"math-domain\">参数定义域：S, K &gt; 0, \\quad T &gt; 0, \\quad \\sigma &gt; 0, \\quad r \\ge 0</div>\n                </div>\n                ",
        "code": "import math\nfrom typing import Tuple\n\ndef normal_cdf(x: float) -> float:\n    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))\n\ndef bsm_call_put_price(S: float, K: float, T: float, r: float, sigma: float) -> Tuple[float, float]:\n    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))\n    d2 = d1 - sigma * math.sqrt(T)\n    call = S * normal_cdf(d1) - K * math.exp(-r * T) * normal_cdf(d2)\n    put = K * math.exp(-r * T) * normal_cdf(-d2) - S * normal_cdf(-d1)\n    return call, put\n",
        "qa": [
          {
            "q": "Q1: 为什么期权卖方（Short Vega / Short Gamma）在平时能每天稳赚时间价值，但极易在黑天鹅中瞬间爆仓？",
            "a": "卖方收益有上限（仅为收取的有限权利金），但下行敞口具有二次方非线性爆炸特征。一旦发生类似 1987 或 2020 暴跌，波动率飙升与 Delta 瞬间击穿将造成毁灭性亏损。"
          },
          {
            "q": "Q2: 2021 年 GME 事件中，散户大量购买虚值 Call 为什么会引发‘伽马挤压（Gamma Squeeze）’？",
            "a": "做市商做空看涨期权后必须买入现货对冲 Delta。随着股价暴涨，虚值期权迅速变为实值，Delta 从 0.1 暴增至接近 1.0，做市商被迫在现货市场不计成本爆买股票对冲，形成正反馈暴拉。"
          },
          {
            "q": "Q3: 为什么做多 VIX 的 ETF（如 UVXY）长期持有本金几乎 100% 必然归零？",
            "a": "因为正常市场中 VIX 期货处于升水结构（Contango，远月比近月贵）。ETF 必须每月卖出便宜的近月、买入昂贵的远月进行展期，产生每月 5%~10% 的结构性摩擦出血。"
          }
        ]
      }
    ]
  },
  {
    "id": "m09",
    "num": "09",
    "folder": "09_special_situations",
    "title": "特殊事件驱动与套利",
    "title_en": "Special Situations & Arbitrage",
    "desc": "并购套利（Merger Arbitrage）利差与破裂概率、中国特色可转债纯债底与双低轮动策略。",
    "icon": "🎯",
    "lessons_count": 4,
    "lessons": [
      {
        "id": "m09_l02",
        "num": "02",
        "title": "可转债定价、纯债底与双低轮动",
        "difficulty": "核心",
        "time": "40 分钟",
        "status": "completed",
        "objectives": [
          "掌握可转债债股二重性与纯债到期偿付价值硬安全垫",
          "量化计算转股价值、转股溢价率与双低综合得分模型",
          "建立考虑强赎条款与下修博弈的多券动态再平衡选股算法"
        ],
        "theory": "\n                <div class=\"callout callout-note\">\n                  <div class=\"callout-title\">📌 投决会核心心智模型：不对称凸性回报的最佳实践</div>\n                  <div class=\"callout-body\">\n                    中国可转债市场具备举世罕见的制度红利：向下有上市公司还本付息的纯债底刚性保护；向上有正股跟涨期权与上市公司极力促成转股消除债务的内生动力（下修条款）。\n                  </div>\n                </div>\n\n                <ul class=\"label-list\">\n                  <li><strong>[双低指标核心]</strong>：双低值 = 转债市价（元） + 转股溢价率（%）。低价格保证债底防守抗跌，低溢价保证正股上涨时跟涨弹性极高。</li>\n                  <li><strong>[下修条款博弈]</strong>：当正股持续阴跌触发下调转股价条款时，转股价值瞬间跳升，从而在熊市深处形成强大的防守反击动能。</li>\n                  <li><strong>[强赎杀溢价风险]</strong>：当正股涨超转股价 130% 触发提前赎回时，高溢价转债面临溢价率瞬间归零的暴跌踩踏，必须严格止盈离场。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{Double Low} = P_{\\text{cb}} + \\frac{P_{\\text{cb}} - \\text{CV}}{\\text{CV}} \\times 100, \\quad \\text{CV} = \\frac{S}{K} \\times 100</div>\n                  <div class=\"math-domain\">选券门槛：P_{\\text{cb}} \\le 130 \\text{ 元}, \\quad \\text{Credit Rating} \\ge \\text{AA-}</div>\n                </div>\n                ",
        "code": "import pandas as pd\n\ndef calculate_double_low_scores(cb_price: pd.Series, stock_price: pd.Series, convert_price: pd.Series) -> pd.Series:\n    convert_value = (stock_price / convert_price) * 100.0\n    premium_rate_pct = ((cb_price - convert_value) / convert_value) * 100.0\n    return cb_price + premium_rate_pct\n",
        "qa": [
          {
            "q": "Q1: 为什么可转债双低轮动策略在过去 10 年能战胜 90% 的股票型主动公募基金？",
            "a": "因为其规避了股票腰斩的单向毁灭性回撤，在熊市依靠高息债底与下修保全本金；在牛市依靠转股期权捕获超额涨幅，复利几何增长率极高。"
          },
          {
            "q": "Q2: 上市公司为什么具有极强的动力向下修正转股价促使投资者转股？",
            "a": "绝大多数发行可转债的企业并不希望在到期时拿出几十亿现金还本付息，而是希望债权人全部转为股权，将债务转化为永久免还资本公积。"
          },
          {
            "q": "Q3: 怎样在双低策略中防范民营垃圾转债的信用违约与退市风险？",
            "a": "设置硬性门槛：剔除正股有退市警示（*ST）、资产负债率超过 80% 或主体评级低于 AA- 的高危标的。"
          }
        ]
      }
    ]
  },
  {
    "id": "m10",
    "num": "10",
    "folder": "10_system_infra",
    "title": "量化系统架构与实盘工程",
    "title_en": "System Architecture & Execution Engineering",
    "desc": "彻底消灭回测谎言：AST 静态代码未来函数审计、真实微观撮合排队滑点、Point-in-Time 管道与实盘硬熔断哨兵。",
    "icon": "⚙️",
    "lessons_count": 4,
    "lessons": [
      {
        "id": "m10_l01",
        "num": "01",
        "title": "回测致命陷阱与前视偏差 (Lookahead) 审计",
        "difficulty": "核心",
        "time": "45 分钟",
        "status": "completed",
        "objectives": [
          "建立时间戳因果律铁则（Causality Contract）与数据生效可见性约束",
          "编写 Python AST 静态语法树未来函数（Future Leakage）检测器",
          "掌握 Point-in-Time 真实披露日对齐架构，杜绝回测假阳性神话"
        ],
        "theory": "\n                <div class=\"callout callout-warning\">\n                  <div class=\"callout-title\">⚠️ 投决会首要审查红线：回测谎言与过拟合神话</div>\n                  <div class=\"callout-body\">\n                    在量化投研中，几乎所有年化收益超过 100%、夏普比率大于 5.0 的回测代码，99.9% 都植入了隐蔽的前视偏差（Lookahead Bias）或幸存者偏差。不能通过严格时间戳审计的回测毫无实盘参考价值。\n                  </div>\n                </div>\n\n                <p>下图展示了 Point-in-Time（PIT）数据管道对财报报告期截止日与法定公告日的时间戳隔离机制：</p>\n\n                \n    <div class=\"diagram-card\">\n      <div class=\"diagram-header\">\n        <span class=\"diagram-title\">图 10.1：Point-in-Time (PIT) 数据对齐与前视偏差隔离</span>\n        <span class=\"diagram-tag\">INFRA-01</span>\n      </div>\n      <div class=\"diagram-svg-container\">\n        \n<svg viewBox=\"0 0 760 220\" width=\"100%\" height=\"220\" xmlns=\"http://www.w3.org/2000/svg\">\n  <rect width=\"760\" height=\"220\" fill=\"var(--bg-card-subtle)\" rx=\"8\" stroke=\"var(--border-light)\" stroke-width=\"1\"/>\n  <!-- Timeline Arrow -->\n  <line x1=\"50\" y1=\"120\" x2=\"710\" y2=\"120\" stroke=\"#1F1E1B\" stroke-width=\"2\"/>\n  <polygon points=\"710,120 700,115 700,125\" fill=\"#1F1E1B\"/>\n  <text x=\"710\" y=\"140\" font-family=\"JetBrains Mono, monospace\" font-size=\"10\" fill=\"#7D786F\" text-anchor=\"end\">时间轴 t</text>\n  <!-- Report Period End (3-31) -->\n  <circle cx=\"160\" cy=\"120\" r=\"5\" fill=\"#486A7D\"/>\n  <line x1=\"160\" y1=\"80\" x2=\"160\" y2=\"160\" stroke=\"#486A7D\" stroke-width=\"1.5\" stroke-dasharray=\"3 3\"/>\n  <text x=\"160\" y=\"70\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" font-weight=\"600\" fill=\"#486A7D\" text-anchor=\"middle\">一季报截止日 (3-31)</text>\n  <text x=\"160\" y=\"175\" font-family=\"Inter, sans-serif\" font-size=\"10\" fill=\"#CC5A36\" text-anchor=\"middle\">【禁忌】绝对不可在此点取用财报数据</text>\n  <!-- Announcement Date (4-25) -->\n  <circle cx=\"440\" cy=\"120\" r=\"5\" fill=\"#5F7355\"/>\n  <line x1=\"440\" y1=\"80\" x2=\"440\" y2=\"160\" stroke=\"#5F7355\" stroke-width=\"1.5\" stroke-dasharray=\"3 3\"/>\n  <text x=\"440\" y=\"70\" font-family=\"JetBrains Mono, monospace\" font-size=\"11\" font-weight=\"700\" fill=\"#5F7355\" text-anchor=\"middle\">法定公开披露日 (4-25)</text>\n  <text x=\"440\" y=\"175\" font-family=\"Inter, sans-serif\" font-size=\"10\" fill=\"#5F7355\" text-anchor=\"middle\">【合规】信号在此日开盘后首次可见 (PIT)</text>\n  <!-- Lookahead Danger Zone -->\n  <rect x=\"165\" y=\"95\" width=\"270\" height=\"25\" fill=\"rgba(204, 90, 54, 0.15)\"/>\n  <text x=\"300\" y=\"112\" font-family=\"Inter, sans-serif\" font-size=\"11\" font-weight=\"600\" fill=\"#CC5A36\" text-anchor=\"middle\">前视偏差黑洞 (Lookahead Bias Zone)</text>\n</svg>\n\n      </div>\n    </div>\n    \n\n                <ul class=\"label-list\">\n                  <li><strong>[报告期截止日 vs 披露公告日]</strong>：一季度财报截止日为 3 月 31 日，但在 4 月 25 日公告发布前，该财务指标在现实物理世界中根本不存在。</li>\n                  <li><strong>[未来函数静态审计]</strong>：代码中任何未加说明的 `shift(-1)` 反向位移或偷看当日收盘价的开盘买入，属于严重的因果律违背。</li>\n                  <li><strong>[幸存者偏差剔除]</strong>：若仅回测当前存续股票，便系统性漏掉了因造假退市的康美、乐视等失败样本，导致收益率严重高估。</li>\n                </ul>\n\n                <div class=\"math-block\">\n                  <div class=\"math-formula\">\\text{Valid Signal}: \\quad t_{\\text{decision}} \\ge \\max(t_{\\text{market\\_tick}}, \\; t_{\\text{filing\\_announcement}})</div>\n                  <div class=\"math-domain\">因果律硬约束：\\forall \\tau &gt; t, \\quad \\frac{\\partial \\text{Signal}_t}{\\partial X_\\tau} \\equiv 0</div>\n                </div>\n                ",
        "code": "def detect_lookahead_bias(signal_time: str, data_available_time: str) -> bool:\n    \"\"\"\n    判断是否存在前视偏差:\n    若决策信号产生的时间早于数据能够真实获取的时间，则存在前视偏差 (返回 True)\n    \"\"\"\n    return signal_time < data_available_time\n",
        "qa": [
          {
            "q": "Q1: 为什么使用当日收盘价（Close）直接作为当日开盘买入信号在实盘中是完全不可能执行的谎言？",
            "a": "收盘价在 15:00 集合竞价结束才生成，在 09:30 开盘时属于绝对的未来未知信息。实盘只能以收盘价生成信号并在次日开盘以滑点执行（shift(1)）。"
          },
          {
            "q": "Q2: 停牌股票在回测中如果没有做不可交易性过滤，会产生何种荒谬的造假？",
            "a": "回测引擎会自动在停牌首日高位完美‘逃顶’平仓套现，而实盘中股票一旦跌停停牌根本无法卖出，面临复牌后的连续补跌踩踏。"
          },
          {
            "q": "Q3: 怎样利用紧缩夏普比率（Deflated Sharpe Ratio, DSR）挤出过度拟合水分？",
            "a": "利用极值理论计算在成千上万次参数组合回测下最大夏普比率的期望膨胀值，修正由于反复试错测试导致的假阳性统计偏差。"
          }
        ]
      }
    ]
  }
];
