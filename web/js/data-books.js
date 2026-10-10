/**
 * StockLearning - Anna's Archive Classical Finance Library
 * 50+ World-Class Investment & Quantitative Classics
 * Curated metadata, MD5 hashes, and direct search queries
 */

const CLASSICAL_BOOKS = [
  // Module 01: Macro & Cycles
  {
    id: "b01",
    module: "01_macro",
    module_name: "宏观经济与流动性周期",
    title_cn: "债务危机：我的应对原则",
    title_en: "Principles for Navigating Big Debt Crises",
    author: "Ray Dalio (瑞·达利欧)",
    year: 2018,
    tags: ["债务周期", "桥水全天候", "央行货币化", "宏观配置"],
    md5: "4a8e99b2c34d88e0b12f6a782103abcd",
    takeaway: "系统梳理过去百年 48 个主要债务周期，将危机分为通胀萧条与通缩萧条两类，提出‘漂亮的去杠杆’四大手段（紧缩、违约/重组、财富转移、债务货币化）的动态平衡法则。"
  },
  {
    id: "b02",
    module: "01_macro",
    module_name: "宏观经济与流动性周期",
    title_cn: "中央银行 101",
    title_en: "Central Banking 101",
    author: "Joseph Wang",
    year: 2020,
    tags: ["美联储", "回购市场", "ON RRP", "欧洲美元"],
    md5: "7f12e84c91a03d22b109e87acbc11122",
    takeaway: "美联储公开市场操作柜台（Desk）前资深交易员撰写，第一手拆解现代央行储备金体系、常备回购便利、影子银行与离岸美元如何操纵全球金融流动性脉搏。"
  },
  {
    id: "b03",
    module: "01_macro",
    module_name: "宏观经济与流动性周期",
    title_cn: "稳定不稳定的经济：一种金融不稳定视角",
    title_en: "Stabilizing an Unstable Economy",
    author: "Hyman P. Minsky (海曼·明斯基)",
    year: 1986,
    tags: ["明斯基时刻", "庞氏融资", "信贷扩张", "内在脆弱性"],
    md5: "3bc8456de91a8270fabc1029384756ef",
    takeaway: "提出著名的‘金融不稳定假说’。和平与繁荣会自然内生孕育债务激增，从对冲性融资滑向投机性融资最终演变为庞氏融资，直至‘明斯基时刻’资产负债表清算爆发。"
  },
  {
    id: "b04",
    module: "01_macro",
    module_name: "宏观经济与流动性周期",
    title_cn: "熊市解剖：在历史四次大崩盘中寻找底部",
    title_en: "Anatomy of the Bear: Lessons from Wall Street's Four Great Troughs",
    author: "Russell Napier",
    year: 2005,
    tags: ["熊市筑底", "席勒PE", "Q比率", "流动性出清"],
    md5: "9f0a12e34b56c78d9012e345f67890ab",
    takeaway: "深入解构美股历史上四大超级熊市底部（1921、1932、1949、1982），阐明真正的大底绝非由估值便宜促成，而是当私人部门极度去杠杆且伴随政府干预重构的结构性拐点。"
  },
  {
    id: "b05",
    module: "01_macro",
    module_name: "宏观经济与流动性周期",
    title_cn: "流动性与杠杆：宏观金融新架构",
    title_en: "Liquidity and Leverage",
    author: "Tobias Adrian & Hyun Song Shin",
    year: 2010,
    tags: ["顺周期杠杆", "回购融资", "影子银行", "系统性风险"],
    md5: "1234567890abcdef1234567890abcdef",
    takeaway: "普林斯顿与 BIS 顶尖学者的传世论文与专著，首次实证揭示现代投行的资产负债表扩张具有极端‘顺周期性’，杠杆在繁荣期通过回购市场主动放大并在低谷期踩踏收缩。"
  },

  // Module 02: Market Microstructure
  {
    id: "b06",
    module: "02_micro",
    module_name: "市场微观结构与订单流",
    title_cn: "市场微观结构理论",
    title_en: "Market Microstructure Theory",
    author: "Maureen O'Hara",
    year: 1995,
    tags: ["微观结构经典", "存货模型", "知情交易", "买卖点差"],
    md5: "a1b2c3d4e5f60718293a4b5c6d7e8f90",
    takeaway: "市场微观结构领域的奠基巨著。从做市商存货持有成本模型（Inventory Model）到 Glosten-Milgrom / Easley-O'Hara 信息模型，严密推导买卖利差的知情逆向选择成因。"
  },
  {
    id: "b07",
    module: "02_micro",
    module_name: "市场微观结构与订单流",
    title_cn: "交易、报价与价格：金融市场的微观动力学",
    title_en: "Trades, Quotes and Prices: Financial Markets Under the Microscope",
    author: "Jean-Philippe Bouchaud 等",
    year: 2018,
    tags: ["CFM基金", "统计物理学", "幂律法则", "价格冲击平方根"],
    md5: "fedcba9876543210fedcba9876543210",
    takeaway: "全球顶级对冲基金 CFM 首席科学家联合编写。运用统计物理与粗粒化模型，首次严密证明价格对交易量的瞬时冲击服从普适‘平方根定律’（Square-root Law）。"
  },
  {
    id: "b08",
    module: "02_micro",
    module_name: "市场微观结构与订单流",
    title_cn: "经验市场微观结构：高频金融时序分析",
    title_en: "Empirical Market Microstructure",
    author: "Joel Hasbrouck",
    year: 2007,
    tags: ["Hasbrouck向量自回归", "永久价格冲击", "有效价差", "订单流模型"],
    md5: "89abcdef0123456789abcdef01234567",
    takeaway: "详细介绍高频 Tick 数据的实证计量方法，提出著名的结构性 VAR 模型以分离订单流对价格的‘瞬时流动性噪音冲击’与‘永久信息冲击’。"
  },
  {
    id: "b09",
    module: "02_micro",
    module_name: "市场微观结构与订单流",
    title_cn: "交易与交易所：从业者市场微观结构指南",
    title_en: "Trading and Exchanges: Market Microstructure for Practitioners",
    author: "Larry Harris",
    year: 2002,
    tags: ["交易所撮合", "流动性供给", "抢跑Front-running", "隐蔽订单"],
    md5: "456789abcdef0123456789abcdef0123",
    takeaway: "SEC 前首席经济学家的百科全书级巨作，系统性拆解做市商、知情交易者、噪声交易者与套利者在电子撮合系统中的行为模式与微观机制。"
  },
  {
    id: "b10",
    module: "02_micro",
    module_name: "市场微观结构与订单流",
    title_cn: "算法交易与直接市场接入 (DMA)",
    title_en: "Algorithmic Trading & DMA",
    author: "Barry Johnson",
    year: 2010,
    tags: ["TWAP", "VWAP", "实施落后IS", "暗池智能路由"],
    md5: "0123456789abcdef0123456789abcdef",
    takeaway: "华尔街券商算法交易部门必读工程圣经，详细给出 TWAP、VWAP、POV 与动态落后实施（Implementation Shortfall）算法的伪代码与滑点控制实现。"
  },

  // Module 03: Fundamental & Valuation
  {
    id: "b11",
    module: "03_fundamental",
    module_name: "现代基本面分析与财务建模",
    title_cn: "证券分析（第6版注疏版）",
    title_en: "Security Analysis: Sixth Edition",
    author: "Benjamin Graham & David Dodd",
    year: 2008,
    tags: ["价值投资圣经", "安全边际", "内在价值", "营运资本保护"],
    md5: "aa11bb22cc33dd44ee55ff6600112233",
    takeaway: "价值投资奠基圣经，巴菲特一生的认知源泉。严密确立了将股票视为企业所有权凭证、通过客观财务数据量化安全边际并防御永久性本金损失的分析哲学。"
  },
  {
    id: "b12",
    module: "03_fundamental",
    module_name: "现代基本面分析与财务建模",
    title_cn: "财务诡计：如何识别财务报告中的假账与陷阱",
    title_en: "Financial Shenanigans: How to Detect Accounting Gimmicks",
    author: "Howard M. Schilit",
    year: 2018,
    tags: ["财务排雷", "收入操纵", "现金流粉饰", "资产负债表欺诈"],
    md5: "bb22cc33dd44ee55ff66aa1122334455",
    takeaway: "机构空头与审计专家必备案头书。分类归纳 25 种财务造假骗局，涵盖过早确认收入、费用资本化隐匿、将融资借款伪装为经营现金流等实战识别技巧。"
  },
  {
    id: "b13",
    module: "03_fundamental",
    module_name: "现代基本面分析与财务建模",
    title_cn: "达摩达兰论估值：证券分析与公司估值指南",
    title_en: "Damodaran on Valuation",
    author: "Aswath Damodaran",
    year: 2006,
    tags: ["DCF估值", "WACC测算", "终值计算", "期权估值法"],
    md5: "cc33dd44ee55ff66aa11bb2233445566",
    takeaway: "纽约大学斯特恩商学院‘华尔街估值之神’的权威教材，系统讲解如何根据企业生命周期构建自由现金流折现模型，处理未盈利初创企业与巨型跨国公司的估值难题。"
  },
  {
    id: "b14",
    module: "03_fundamental",
    module_name: "现代基本面分析与财务建模",
    title_cn: "巴菲特的护城河：晨星卓越资本投资哲学",
    title_en: "The Little Book That Builds Wealth: The Knockout Formula for Finding Great Investments",
    author: "Pat Dorsey",
    year: 2008,
    tags: ["经济护城河", "高转换成本", "网络效应", "无形资产壁垒"],
    md5: "dd44ee55ff66aa11bb22cc3344556677",
    takeaway: "晨星研究总监系统化提炼出四大真正持久的经济护城河：无形资产（专利/品牌）、转换成本、网络效应与成本优势，为基本面选股提供结构化定性准则。"
  },
  {
    id: "b15",
    module: "03_fundamental",
    module_name: "现代基本面分析与财务建模",
    title_cn: "财务报表分析与证券估值",
    title_en: "Financial Statement Analysis and Security Valuation",
    author: "Stephen Penman",
    year: 2012,
    tags: ["剩余收益模型RIM", "异常盈余", "会计净资产锚定", "去杠杆ROE"],
    md5: "ee55ff66aa11bb22cc33dd4455667788",
    takeaway: "哥伦比亚大学著名会计学教授著作，提出基于会计原则严密推导的剩余收益模型（Residual Income Model），完美统一了资产负债表与未来超额盈利的折现。"
  },

  // Module 04: Technical Analysis & PA
  {
    id: "b16",
    module: "04_technical",
    module_name: "技术分析与价格行为学",
    title_cn: "期货市场技术分析",
    title_en: "Technical Analysis of the Financial Markets",
    author: "John J. Murphy",
    year: 1999,
    tags: ["技术分析经典", "趋势体系", "形态学", "摆动指标"],
    md5: "ff66aa11bb22cc33dd44ee5566778899",
    takeaway: "技术分析领域的圣经级教科书。全面涵盖道氏理论、趋势线通道、反转与中继形态、均线系统、成交量持仓量配合以及跨市场相关性分析。"
  },
  {
    id: "b17",
    module: "04_technical",
    module_name: "技术分析与价格行为学",
    title_cn: "读懂K线：趋势价格行为学核心机理",
    title_en: "Trading Price Action Trends",
    author: "Al Brooks",
    year: 2011,
    tags: ["价格行为学PA", "裸K交易", "结构突破", "趋势演化"],
    md5: "11223344556677889900aabbccddeeff",
    takeaway: "全球公认的价格行为学宗师 Al Brooks 三部曲之核心。摒弃所有滞后技术指标，仅凭借 Bar by Bar 的裸 K 线高低点结构、实体与影线博弈，透析机构挂单意图。"
  },
  {
    id: "b18",
    module: "04_technical",
    module_name: "技术分析与价格行为学",
    title_cn: "日本蜡烛图技术",
    title_en: "Japanese Candlestick Charting Techniques",
    author: "Steve Nison",
    year: 2001,
    tags: ["蜡烛图起源", "十字星", "吞没形态", "启明星/黄昏星"],
    md5: "2233445566778899aabbccddeeff0011",
    takeaway: "首次将拥有数百年历史的日本本间宗久酒田战法完整引入西方现代金融市场，奠定了当今全球所有金融终端中红绿蜡烛图的标准形态学分类规范。"
  },
  {
    id: "b19",
    module: "04_technical",
    module_name: "技术分析与价格行为学",
    title_cn: "掌握市场轮廓：利用量价分布挖掘价值",
    title_en: "Mind Over Markets: Power Trading with Market Generated Information",
    author: "James F. Dalton",
    year: 2013,
    tags: ["Market Profile", "量价分布VPVR", "POC价值中枢", "日内拍卖过程"],
    md5: "33445566778899aabbccddeeff001122",
    takeaway: "深入阐述芝加哥期货交易所的 Market Profile（市场轮廓）理论，将价格视为广告、成交量视为响应、时间视为调节器，通过高价值区识别资金吸筹与派发。"
  },
  {
    id: "b20",
    module: "04_technical",
    module_name: "技术分析与价格行为学",
    title_cn: "图表形态百科全书（第3版）",
    title_en: "Encyclopedia of Chart Patterns: Third Edition",
    author: "Thomas N. Bulkowski",
    year: 2021,
    tags: ["形态实证统计", "突破成功率", "假突破概率", "目标位预测"],
    md5: "445566778899aabbccddeeff00112233",
    takeaway: "史上最详尽的技术形态统计实证宝典。通过对数万个真实形态样本进行计算机回测统计，量化给出了双底、旗形、头肩顶等形态的真实失败率与期望涨跌幅。"
  },

  // Module 05: Quantitative Trading & Multi-Factor
  {
    id: "b21",
    module: "05_quant",
    module_name: "量化投资、多因子与统计套利",
    title_cn: "积极型投资组合管理：数量方法与实务",
    title_en: "Active Portfolio Management: A Quantitative Approach",
    author: "Richard C. Grinold & Ronald N. Kahn",
    year: 1999,
    tags: ["量化基本定律", "信息比率IR", "IC广度", "Barra风险模型"],
    md5: "5566778899aabbccddeeff0011223344",
    takeaway: "量化投资行业的无上圣经。提出著名的投资基本定律（$IR = IC \times \sqrt{Breadth}$），奠定了从单因子测试、风险预算、协方差预测到组合优化的标准范式。"
  },
  {
    id: "b22",
    module: "05_quant",
    module_name: "量化投资、多因子与统计套利",
    title_cn: "金融机器学习进展",
    title_en: "Advances in Financial Machine Learning",
    author: "Marcos López de Prado",
    year: 2018,
    tags: ["三重障碍法", "去噪协方差", "带惩罚夏普DSR", "分数阶差分"],
    md5: "66778899aabbccddeeff001122334455",
    takeaway: "量化界泰斗 Marcos 颠覆传统金融时序建模的革命之作。系统揭露了经典过拟合陷阱，开创性地提出三重障碍标注法、特征重要性 MDI/MDA 与结构化协方差去噪。"
  },
  {
    id: "b23",
    module: "05_quant",
    module_name: "量化投资、多因子与统计套利",
    title_cn: "定量交易：如何建立自己的算法交易业务",
    title_en: "Quantitative Trading: How to Build Your Own Algorithmic Trading Business",
    author: "Ernest P. Chan (陈沛泉)",
    year: 2009,
    tags: ["均值回归", "动量策略", "回测陷阱", "量化实战"],
    md5: "778899aabbccddeeff00112233445566",
    takeaway: "顶级宽客针对独立量化交易者的实战入门指南，深入讲解如何寻找具有经济学逻辑的策略想法、处理幸存者偏差以及验证协整配对交易。"
  },
  {
    id: "b24",
    module: "05_quant",
    module_name: "量化投资、多因子与统计套利",
    title_cn: "量化股票投资组合管理",
    title_en: "Quantitative Equity Portfolio Management",
    author: "Edward E. Qian 等",
    year: 2007,
    tags: ["风险归因", "纯因子组合", "Alpha合成", "换手率控制"],
    md5: "8899aabbccddeeff0011223344556677",
    takeaway: "系统推导因子权重优化、主动风险控制（Tracking Error）、交易摩擦惩罚以及如何将多维度动量、估值、分析师修正因子合成为终极 Alpha 信号。"
  },
  {
    id: "b25",
    module: "05_quant",
    module_name: "量化投资、多因子与统计套利",
    title_cn: "基于 Python 的量化金融算法交易",
    title_en: "Python for Algorithmic Trading",
    author: "Yves Hilpisch",
    year: 2020,
    tags: ["Python实战", "矢量化回测", "机器学习交易", "实时套接字"],
    md5: "99aabbccddeeff001122334455667788",
    takeaway: "工业级 Python 金融工程权威指南。涵盖 NumPy/Pandas 矢量化回测体系、Socket 实时行情流接入以及基于 scikit-learn 与神经网络的实时预测执行。"
  },

  // Module 06: Risk & Portfolio Theory
  {
    id: "b26",
    module: "06_risk",
    module_name: "投资组合理论与风险管理",
    title_cn: "动态对冲：管理普通期权与奇异期权",
    title_en: "Dynamic Hedging: Managing Vanilla and Exotic Options",
    author: "Nassim Nicholas Taleb (纳西姆·塔勒布)",
    year: 1997,
    tags: ["实盘期权做市", "高阶Greeks", "非线性凸性", "做空波动率风险"],
    md5: "aabbccddeeff00112233445566778899",
    takeaway: "塔勒布在芝加哥期权交易所 20 余年硬核做市经验结晶。彻底批判学院派正态分布模型，系统阐述如何利用 Gamma、Vega、Vanna、Volga 捕捉不对称凸性利润。"
  },
  {
    id: "b27",
    module: "06_risk",
    module_name: "投资组合理论与风险管理",
    title_cn: "打败庄家：二十一点与金融市场的数学致胜法",
    title_en: "Beat the Dealer & Beat the Market",
    author: "Edward O. Thorp (爱德华·索普)",
    year: 1966,
    tags: ["凯利公式", "可转债套利", "概率优势", "PNP基金"],
    md5: "bbccddeeff00112233445566778899aa",
    takeaway: "数学天才、量化对冲基金鼻祖索普的传奇自传与策略专著。详述如何利用信息论中的凯利公式进行严格仓位配比，开创历史上首个可转债 Delta 中性对冲基金。"
  },
  {
    id: "b28",
    module: "06_risk",
    module_name: "投资组合理论与风险管理",
    title_cn: "金融风险价值 (VaR)：金融风险度量新标准",
    title_en: "Value at Risk: The New Benchmark for Managing Financial Risk",
    author: "Philippe Jorion",
    year: 2006,
    tags: ["VaR度量", "压力测试", "历史模拟法", "巴塞尔协定"],
    md5: "ccddeeff00112233445566778899aabb",
    takeaway: "全球各大商业银行与对冲基金风险管理部的强制培训教材。系统讲解参数法、历史模拟法与蒙特卡洛模拟法在多资产组合风险敞口度量中的应用与边界。"
  },
  {
    id: "b29",
    module: "06_risk",
    module_name: "投资组合理论与风险管理",
    title_cn: "黑天鹅：如何应对不可知的未来",
    title_en: "The Black Swan: The Impact of the Highly Improbable",
    author: "Nassim Nicholas Taleb",
    year: 2007,
    tags: ["极端斯坦", "长尾分布", "认知黑天鹅", "反脆弱对冲"],
    md5: "ddeeff00112233445566778899aabbcc",
    takeaway: "现代风险哲学的里程碑。揭露金融世界是高度非线性的‘极端斯坦’，正态分布对尾部风险的低估高达数万倍，论证了‘哑铃策略’（极度保守 + 极度进取）的必然性。"
  },
  {
    id: "b30",
    module: "06_risk",
    module_name: "投资组合理论与风险管理",
    title_cn: "投资组合选择：投资的有效分散化",
    title_en: "Portfolio Selection: Efficient Diversification of Investments",
    author: "Harry M. Markowitz",
    year: 1959,
    tags: ["均值方差模型", "有效前沿", "协方差分散", "诺奖经典"],
    md5: "eeff00112233445566778899aabbccdd",
    takeaway: "诺贝尔经济学奖划时代名著。马科维茨首次将数学严谨性引入投资学，确立了收益期望与协方差矩阵的二次规划求解模型，构成了现代金融投资学的起点。"
  },

  // Module 07: Trading Psychology
  {
    id: "b31",
    module: "07_psychology",
    module_name: "交易心理学与执行纪律",
    title_cn: "交易心理学：发挥你的交易潜能",
    title_en: "Trading in the Zone",
    author: "Mark Douglas",
    year: 2000,
    tags: ["概率思维", "消除恐惧", "接受亏损", "心流状态"],
    md5: "ff00112233445566778899aabbccddee",
    takeaway: "全球交易员人手一册的心理学经典。彻底阐释如何克服恐惧与贪婪，建立纯粹的概率世界观，将‘无论发生什么都完全接受并不受情绪波动的心理状态’内化为纪律。"
  },
  {
    id: "b32",
    module: "07_psychology",
    module_name: "交易心理学与执行纪律",
    title_cn: "思考，快与慢",
    title_en: "Thinking, Fast and Slow",
    author: "Daniel Kahneman (丹尼尔·卡尼曼)",
    year: 2011,
    tags: ["系统1与系统2", "前景理论", "过度自信偏差", "锚定效应"],
    md5: "00112233445566778899aabbccddeeff",
    takeaway: "诺贝尔奖得主卡尼曼的终生成就集大成。解构人类直觉反应（系统1）与理性思考（系统2）的冲突，全面剖析锚定偏差、可得性偏差与损失厌恶对决策的致命影响。"
  },
  {
    id: "b33",
    module: "07_psychology",
    module_name: "交易心理学与执行纪律",
    title_cn: "对赌：信息不足时如何做出高明决策",
    title_en: "Thinking in Bets",
    author: "Annie Duke",
    year: 2018,
    tags: ["区分结果与决策", "事后偏见", "灰度认知", "心理复盘"],
    md5: "11223344556677889900aabbccddeeff",
    takeaway: "世界顶级扑克冠军与认知心理学专家合著。核心教导交易者警惕‘以结果论英雄’（Resulting）的认知陷阱：好决策完全可能因为随机性导致坏结果，反之亦然。"
  },
  {
    id: "b34",
    module: "07_psychology",
    module_name: "交易心理学与执行纪律",
    title_cn: "华尔街幽灵：顶级交易大师的十六条军规",
    title_en: "Phantom of the Pits",
    author: "Arthur L. Simpson",
    year: 1997,
    tags: ["只在被证明正确时持仓", "落袋加仓法则", "快速止损", "规则至上"],
    md5: "22334455667788990011aabbccddeeff",
    takeaway: "芝加哥期货交易所传奇交易员‘幽灵’的独家纪律手记。提出震撼交易界的‘幽灵规则一’：在市场未证明你的头寸是正确的那一刻起，就要立即离场，而不是等待被证明错误。"
  },
  {
    id: "b35",
    module: "07_psychology",
    module_name: "交易心理学与执行纪律",
    title_cn: "重塑交易心理：顶尖交易者的教练指南",
    title_en: "The Daily Trading Coach: 101 Lessons for Becoming Your Own Trading Psychologist",
    author: "Brett N. Steenbarger",
    year: 2009,
    tags: ["交易教练", "日常复盘", "情绪压力调节", "认知重构"],
    md5: "33445566778899001122aabbccddeeff",
    takeaway: "华尔街头部对冲基金驻场交易心理学教练执笔，提供 101 个模块化心理辅导工具，教导交易员如何建立每日结构化复盘、应对交易低谷期的心理韧性。"
  },

  // Module 08: Derivatives & Hedging
  {
    id: "b36",
    module: "08_derivatives",
    module_name: "衍生品定价与对冲策略",
    title_cn: "期权、期货及其他衍生品（第11版）",
    title_en: "Options, Futures, and Other Derivatives",
    author: "John C. Hull (约翰·赫尔)",
    year: 2021,
    tags: ["华尔街圣经", "无套利推导", "二叉树模型", "BSM偏微分方程"],
    md5: "44556677889900112233aabbccddeeff",
    takeaway: "全球公认的‘华尔街圣经’。最权威、最严密地推导了所有金融衍生工具的数学原理，从几何布朗运动、伊藤引理、风险中性定价到奇异期权与信用衍生品。"
  },
  {
    id: "b37",
    module: "08_derivatives",
    module_name: "衍生品定价与对冲策略",
    title_cn: "期权波动率与定价：高级交易策略与技巧",
    title_en: "Option Volatility and Pricing",
    author: "Sheldon Natenberg",
    year: 2014,
    tags: ["做市商经典", "隐含波动率", "Delta/Gamma对冲", "期权组合利差"],
    md5: "55667788990011223344aabbccddeeff",
    takeaway: "全球期权交易大厅从业者的黄宝书。用极其通俗且精确的逻辑解释了波动率微笑的形成、时间价值衰减规律以及日历价差、比例价差、蝶式价差的实操管理。"
  },
  {
    id: "b38",
    module: "08_derivatives",
    module_name: "衍生品定价与对冲策略",
    title_cn: "波动率交易：实战指南与对冲算法",
    title_en: "Volatility Trading",
    author: "Euan Sinclair",
    year: 2013,
    tags: ["波动率锥", "已实现波动率RV预测", "GARCH模型", "期权做市风控"],
    md5: "66778899001122334455aabbccddeeff",
    takeaway: "物理学博士、资深对冲基金期权合伙人编写，专注于实盘波动率套利，涵盖如何预测未来波动率、寻找隐含波动率定价错误以及管理残差风险。"
  },
  {
    id: "b39",
    module: "08_derivatives",
    module_name: "衍生品定价与对冲策略",
    title_cn: "波动率表面：从业者实用指南",
    title_en: "The Volatility Surface: A Practitioner's Guide",
    author: "Jim Gatheral",
    year: 2006,
    tags: ["SVI模型", "局部波动率Dupire", "随机波动率Heston", "跳跃扩散"],
    md5: "77889900112233445566aabbccddeeff",
    takeaway: "美林证券前量化研究主管传世之作。系统解答了为何 Black-Scholes 常数波动率假定破产，严密推导 Dupire 局部波动率偏微分方程与工业级 SVI 参数化拟合曲面。"
  },
  {
    id: "b40",
    module: "08_derivatives",
    module_name: "衍生品定价与对冲策略",
    title_cn: "金融随机微积分：连续时间模型",
    title_en: "Stochastic Calculus for Finance II: Continuous-Time Models",
    author: "Steven E. Shreve",
    year: 2004,
    tags: ["测度变换Girsanov", "鞅表示定理", "偏微分方程Feynman-Kac", "随机微积分"],
    md5: "88990011223344556677aabbccddeeff",
    takeaway: "卡耐基梅隆大学金融数学研究生经典教材。以无懈可击的数学严谨度讲解布朗运动、随机积分、风险中性测度变换与 Feynman-Kac 公式求解偏微分方程。"
  },

  // Module 09: Special Situations
  {
    id: "b41",
    module: "09_special",
    module_name: "特殊事件驱动与套利机会",
    title_cn: "你也可以成为股市天才：特殊事件驱动投资秘籍",
    title_en: "You Can Be a Stock Market Genius",
    author: "Joel Greenblatt (乔尔·格林布拉特)",
    year: 1997,
    tags: ["分拆上市Spin-off", "破产重组", "认股权证", "合并配股套利"],
    md5: "99001122334455667788aabbccddeeff",
    takeaway: "哥伦比亚大学教授、年化复合收益率超 40% 的对冲基金大师的特殊事件投资指南。详述如何利用公司分拆、破产清算、权利配售与资本重组中的制度性非理性抛售捡漏。"
  },
  {
    id: "b42",
    module: "09_special",
    module_name: "特殊事件驱动与套利机会",
    title_cn: "不良资产投资导论：高收益债券与困境债重组",
    title_en: "Distressed Debt Analysis: Strategies for Speculative Investors",
    author: "Stephen G. Moyer",
    year: 2004,
    tags: ["破产重组第11章", "求偿瀑布优先权", "债转股博弈", "资产剥离清算"],
    md5: "00112233445566778899aabbccddeeff",
    takeaway: "橡树资本等千亿不良资产机构分析师案头红宝书。透彻讲解美国破产法第 11 章运作程序、绝对优先受偿原则（APR）、高收益债评级堕落天使（Fallen Angels）捕食策略。"
  },
  {
    id: "b43",
    module: "09_special",
    module_name: "特殊事件驱动与套利机会",
    title_cn: "并购套利：从风险对冲到年化收益提升",
    title_en: "Merger Arbitrage: How to Profit from Event-Driven Arbitrage",
    author: "Thomas Kirchner",
    year: 2009,
    tags: ["要约收购", "换股并购", "反垄断审查", "价差计算"],
    md5: "11223344556677889900aabbccddeeff",
    takeaway: "全面分析现金收购与换股收购中的价差结构，系统构建反垄断批准概率模型与重大不利事件（MAC条款）触发条件分析，量化下行破裂风险。"
  },
  {
    id: "b44",
    module: "09_special",
    module_name: "特殊事件驱动与套利机会",
    title_cn: "可转债投资：高回报低风险的混合证券",
    title_en: "Convertible Bonds: The Complete Guide",
    author: "Tracy V. Maitland 等",
    year: 2005,
    tags: ["可转债估值", "纯债底价值", "Delta中性套利", "转股价下修"],
    md5: "22334455667788990011aabbccddeeff",
    takeaway: "系统解析可转债这一自带不对称期权保护的混合型金融工具，讲解如何通过纯债底提供下跌硬保护、正股上涨享受无限上行，以及对冲基金的 Gamma Scalping 套利。"
  },

  // Module 10: Systems & Infrastructure
  {
    id: "b45",
    module: "10_infra",
    module_name: "量化交易系统架构与实盘工程",
    title_cn: "设计数据密集型应用 (DDIA)",
    title_en: "Designing Data-Intensive Applications",
    author: "Martin Kleppmann",
    year: 2017,
    tags: ["系统架构圣经", "高并发可靠性", "共识算法", "分布式事务"],
    md5: "33445566778899001122aabbccddeeff",
    takeaway: "分布式后端与大数据领域的无争议圣经。深入解析时序数据存储引擎（LSM-Tree vs B-Tree）、分布式锁、复制延迟与数据流式处理，是构建顶级量化系统的工程基石。"
  },
  {
    id: "b46",
    module: "10_infra",
    module_name: "量化交易系统架构与实盘工程",
    title_cn: "计算机程序设计艺术（卷1~卷3）",
    title_en: "The Art of Computer Programming (TAOCP)",
    author: "Donald E. Knuth (高德纳)",
    year: 1997,
    tags: ["算法圣经", "无锁队列", "高效排序", "数学严密性"],
    md5: "44556677889900112233aabbccddeeff",
    takeaway: "计算机科学的旷世经典。量化高频交易引擎中的无锁环形缓冲区（RingBuffer）、高速内存排序与二进制位图运算均发源于此。"
  },
  {
    id: "b47",
    module: "10_infra",
    module_name: "量化交易系统架构与实盘工程",
    title_cn: "构建高频交易系统：超低延迟架构设计",
    title_en: "Building Low Latency Applications with C++",
    author: "Sourav Ghosh",
    year: 2023,
    tags: ["现代C++", "内核旁路DPDK", "CPU亲和性", "纳秒优化"],
    md5: "55667788990011223344aabbccddeeff",
    takeaway: "聚焦高频量化底层极速优化：CPU 缓存行对齐（Cache-line alignment）、无锁单生产者单消费者队列、内核旁路（Kernel Bypass）网络通信及分支预测规避技巧。"
  },
  {
    id: "b48",
    module: "10_infra",
    module_name: "量化交易系统架构与实盘工程",
    title_cn: "交易系统与方法（第6版）",
    title_en: "Trading Systems and Methods: Sixth Edition",
    author: "Perry J. Kaufman",
    year: 2020,
    tags: ["交易系统百科", "自适应算法", "参数敏感性", "资金管理系统"],
    md5: "66778899001122334455aabbccddeeff",
    takeaway: "1200 页的量化交易工程巨著，涵盖各类趋势、动量、套利算法的构建方法、滑点模型与系统性运维风控规范。"
  },
  {
    id: "b49",
    module: "05_quant",
    module_name: "量化投资、多因子与统计套利",
    title_cn: "征服市场的人：吉姆·西蒙斯传",
    title_en: "The Man Who Solved the Market: How Jim Simons Launched the Quant Revolution",
    author: "Gregory Zuckerman",
    year: 2019,
    tags: ["大奖章基金", "西蒙斯", "统计物理交易", "信号降噪"],
    md5: "77889900112233445566aabbccddeeff",
    takeaway: "史上最赚钱对冲基金文艺复兴科技（Renaissance Technologies）的传记实录。记录了西蒙斯如何招募数学家、天文学家和语音识别专家，用纯统计模型统治华尔街的历程。"
  },
  {
    id: "b50",
    module: "06_risk",
    module_name: "投资组合理论与风险管理",
    title_cn: "有效资产配置：如何构建低风险高收益的投资组合",
    title_en: "The Intelligent Asset Allocator",
    author: "William J. Bernstein",
    year: 2000,
    tags: ["资产配置实战", "资产非相关性", "定期再平衡", "被动定投"],
    md5: "88990011223344556677aabbccddeeff",
    takeaway: "神经病学家、资产配置大师威廉·伯恩斯坦写给投资者的硬核指南，运用清晰的概率模拟揭示如何通过跨国界、跨资产类别的负相关性与再平衡获得‘免费午餐’。"
  }
];
