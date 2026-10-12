---
name: githubpages
description: End-to-end engineering skill for building, optimizing, and deploying institutional-grade, low-barrier interactive online course repositories and GitHub Pages SPA websites (modeled after hpclearning and investlearning). Enforces Anthropic 3-color minimalist aesthetics, single-concept lesson focus (1:1:1:1), Feynman intuition bridges, plain-Chinese formula translations, 860px scientific vector SVG diagrams with fullscreen zoom lightboxes, single-page continuous section expansion, real-time GitHub Actions data pipelines with dynamic conclusion engines, and bulletproof KaTeX/DOM rendering.
---

# GitHub Pages Interactive Course Engineering Skill (`githubpages`)

本规范完整沉淀了从零构建、深度打磨并部署标杆级开源课程代码库与 GitHub Pages 交互式在线研习平台（如 `hpclearning`、`investlearning`）的全套课程设计方法论、认知减负工程、前端防崩溃规范与自动化运维流水线。在制作任何学科（金融投资、计算机系统、AI 算法、自然科学、工程技术等）的系统化网页课程时，可直接复用本规范。

---

## 零、 十条核心工程铁律（违反即生产事故）

### 铁律一：单课单核心概念（1:1:1:1 聚焦减负法则）
- **痛点根因**：单节课塞入 2~3 个子课题、3~5 个公式和 2~3 幅大图会导致严重的认知过载。
- **强制标准**：
  - **课程标题极简化**：每节课标题只锚定 **1 个核心概念**，去掉冗长的多概念并列与英文括号尾巴（如用 `国债收益率曲线与利差倒挂` 替代 `利率期限结构与利差倒挂衰退预警模型 (Yield Curve & Recession Forecasting)`）。
  - **严格执行 1:1:1:1 配比**：每门课正文严格聚焦 **1 个直观类比与算例 + 1 幅核心科学矢量图 + 1 个核心量化主公式 + 1 个常见误区与风控边界框**（外加必要的交互式仿真沙盒），砍掉所有次要支线概念与生僻副公式。

### 铁律二：单页全量垂直展开，严禁隐藏式 Tab 折叠内容
- **痛点根因**：将课程的“实战清单/代码”或“思考题问答”藏在默认 `display: none` 的 Tab 页签后，90% 的普通读者根本不知道点击后还有内容。
- **强制标准**：
  - 每门课的三大核心板块（`PART 01 核心理论与机制`、`PART 02 实测成果数据与实战清单/工程实现`、`PART 03 核心思考与问答`）必须在**同一页面自上而下全部连续展开**（`.lesson-unified-section { display: block; }`）。
  - 顶部导航条仅作为**页内快速定位锚点**（点击触发 `scrollIntoView({ behavior: "smooth" })`），绝不隐藏其余板块。
  - 页面最底部必须配备 **`⬅ 上一课 / 下一课 ➡` 连续翻页导航栏**，实现从头读到尾一键翻篇的沉浸式阅读流。

### 铁律三：零形式化包装词与脚手架标签泄露
- **痛点根因**：在正文中露出 `[引导句锚点 1]`、`[架构要点拆解 2]`、`锚点指引：`、`核心概念与就近图文排版`、`📌 投决会核心心智模型：`、`零基础费曼降维导读：大白话直觉 × 黑话翻译 × 小学生算术` 等包装词，显得生硬且喧宾夺主。
- **强制标准**：
  - 彻底删除一切排版脚手架标签，用自然流畅的段落引出图表。
  - 统一使用干净、克制的实质性小标题：**`直观类比`**、**`实例验算`**、**`核心机制与图解`**、**`核心量化公式`**、**`常见误区与风控边界`**、**`参考解析`**。
  - 删除正文开头与顶部 `<h1>` 标题重复的 `<p>模块 XX · 第 X 课...</p>` 冗余段落；去除列表加粗项外层多余的方括号与序号（如将 `<strong>[1. 资产端扩缩]</strong>` 简化为 `<strong>资产端扩缩</strong>`）。

### 铁律四：严禁跨课模板套话重复（100% 定制化内容）
- **痛点根因**：用脚本向多门课注入相同的万金油套话（如重复的“以严谨的恒等式为基准…”或千篇一律的“剖析核心数理方程中各项的映射关系”）会严重破坏课程专业信誉。
- **强制标准**：
  - 每门课的 `objectives`（严格精炼为 2 条：`核心内容：...` 与 `掌握标准：...`）、`feynman_analogy`、`feynman_calc`、`theory`、`result_dashboard`、`practical_guide` 与 `qa` 必须 100% 针对本课唯一核心主题专门撰写，全局重复套话率必须为 `0`。

### 铁律五：降门槛而不降深度——“直观类比 + 实例验算 + 直白算式”三件套
- **强制标准**：
  1. **直观类比（30秒破冰）**：在接触任何专业术语前，先用日常水库、菜市场拍卖、相亲查家底、给爱车买车险等生活场景，让零基础读者在 30 秒内秒懂底层逻辑。
  2. **实例验算（1分钟算术）**：用最简单的真实数字（如 10 元价格、900 手买单、10 万元本金）代入本课模型手把手算一遍账，先看清数字怎么指导决策，再看正式推导。
  3. **公式内嵌「🗣️ 直白算式」中文对照条（`.math-plain-bar`）**：在每个 `.math-block` 的 KaTeX 公式正下方，必须内嵌一行纯中文等式翻译（如 `🗣️ 直白算式：市场真实净活水 ＝ 美联储总资产 －（财政部存款 TGA ＋ 隔夜逆回购 ON RRP）`），并在公式框下方紧跟 `<ul class="label-list">` 逐一解释每个符号的含义与实盘阈值。
  4. **清除集合论恐吓符号**：全面删除 `\in \mathbb{R}^+`、`\in \mathbb{N}^+`、测度论 $\sigma$-代数 $\mathcal{F}_t$ 等对实战无益的纯数学装饰符。

### 铁律六：按受众精准分流——砍掉鸡肋网页代码自测台，应用课给“实战清单”，算法课给“完整源码”
- **痛点根因**：非编程受众在学习理论/实务章节时根本用不到 Python 代码；而在网页端放一个简陋的 `textarea` 代码填空自测台（Workbench）既不实用又增加冗余复杂度。
- **强制标准**：
  - **彻底移除网页代码自测台（Workbench）**，以及打卡、假进度条、难度标签（入门/进阶/核心）等花哨游戏化组件。
  - **应用/实务型模块**：`PART 02` 展示 **「📊 实测成果数据看板 + 📋 个人实战决策清单（免费工具获取路径、四步标准化实操、常见致命陷阱、真实案例复盘）」**，隐藏代码框。
  - **算法/工程型模块**：`PART 02` 展示 **「📊 实测成果数据看板 + ⚡ 量化算法与工程实现（直接展示 100% 验证通过的 `answers/` 完整源码，严禁出现 `# TODO` 或空白 `pass`）」**。

### 铁律七：拒绝小字号 Mermaid，全量采用 860px 科学绘图矢量 SVG + 全屏无级缩放灯箱
- **痛点根因**：Mermaid 运行时引擎在遇到多分支横排节点时，会将画布拉宽至 2500px+ 再等比缩小到容器宽度，导致图内文字缩成 5px~7px 的蚂蚁字。
- **强制标准**：
  - **全量编译为 860px 满宽 Anthropic 科学矢量图（`.scientific-svg`）**：
    - 暖羊皮纸科研网格底板（`#FAF8F5` + `#EFECE6` 坐标网格）+ 纯白节点卡片（`#FFFFFF`）+ 陶土红（`#CC5A36`）/ 鼠尾草绿（`#5F7355`）/ 岩灰蓝（`#486A7D`）侧边强调条。
    - **最多双列栅格换行（Max 2-Column Wrapping）**：单行最多并排 2 张宽卡片（每张宽 `384px`）或 1 张通栏主干卡片（宽 `620px`），节点内文字拆分为 `14px` 粗体主标题 + `12px` 机制副标题，确保在正文中无需放大即保持 1:1 清晰可读。
    - **专属图题**：每幅图必须配置直指本课机制的专属图题（如 `图：美联储资产负债表三池分流与市场净流动性传导机制`），严禁使用通用标题“决策流转与因果拓扑图”。
  - **内置全屏无级缩放科学灯箱（`#diagramLightboxModal`）**：每张图解卡片右上角自动挂载 `🔍 点击全屏放大` 按钮，支持 `60% ~ 350%` 鼠标滚轮与按钮无级缩放及 `ESC` 一键关闭。

### 铁律八：成果数据看板页面直出 + 云端定时自动更新 + 动态结论联动
- **强制标准**：
  1. **页面直出成果数据（`.result-data-card`）**：不要只叫读者“自己打开 Excel 去算”，在每门课 `PART 02` 顶部直接展示算好的 **4 个核心 KPI 摘要卡 + 历史与最新期实测对比表 + 底部操作结论框（`.result-table-footnote`）**。
  2. **GitHub Actions 云端自动更新流水线（`.github/workflows/update-live-data.yml`）**：配置每日定时运行的 Python 脚本（`scripts/fetch_live_data.py`），在 GitHub 海外云端服务器直接拉取官方权威数据（如 FRED / 交易所行情），生成 `web/js/live-market-data.json` 并自动提交同步至 `main` 与 `gh-pages`。
  3. **数据 ➔ 信号 ➔ 结论全链路动态联动**：当前端拉取到最新 `live-market-data.json` 或用户在页面内置的「⚡ 交互式实时重算器」中修改输入数值时，**顶部 KPI 读数、表格末行信号单元格以及底部的【💡 实时动态结论与仓位建议】必须同步重新计算并切换状态（🟢 扩张进攻 / 🟡 存量标配 / 🔴 紧缩防御）**！

### 铁律九：全局体系架构图谱与章节承上启下脉络闭环
- **强制标准**：
  1. **独立「📖 课程总览」大页（`#overviewSection`）**：
     - 包含课程第一性原理、学习方法、**《四大战略层级与模块因果传导总图谱》SVG 大图**，以及 **10 大模块的【在体系中的角色】【跨模块咬合关系】【模块内 L01➔L05 递进逻辑】详解卡片**。
     - 任何外部工具/生产力推荐（如海外 AI 充值推荐）严格隔离在总览页展示 **1 次**，确保所有课程内页 100% 纯净无推广干扰。
  2. **单课顶部「本课脉络与章节路径」（`#lessonSystemContextBox`）**：
     - 展示 1 句话的 **本课承上启下脉络**（回答“上一课解决了什么 $\to$ 为什么引出本课 $\to$ 如何通向下一课”）+ 单行水平滚动的 **`L01 ➔ L02 ➔ L03...` 章节胶囊导航条**（当前课陶土红高亮，点击任意胶囊秒级跳转）。
  3. **经典文献文库双通道审核（`#librarySection`）**：
     - 彻底杜绝 `/search?q=` 搜索中转链接与 404 错误页！有公开合法源的提供 `📖 官方开放阅读直达`，受商业版权保护的明确标明 `🔒 仅限下载借阅` 并提供基于真实 MD5 的 `📥 Anna's Archive 极速下载直达`（`https://annas-archive.org/md5/{md5}`）。

### 铁律十：防御性前端工程——本地常驻 KaTeX、纯 HTML 输出防重影、自愈渲染与防缓存版本戳
- **强制标准**：
  1. **KaTeX 本地常驻与纯 HTML 输出**：
     - 将 `katex.min.js`、`katex.min.css` 及 `fonts/*.woff2` 完整存入 `web/vendor/katex/`，摆脱对不稳定公共 CDN 的单点依赖。
     - 调用 `katex.renderToString` 与 `renderMathInElement` 时强制传入 `{ output: "html" }`，并在 `style.css` 中添加 `.katex-mathml { display: none !important; }`，彻底根除公式重影与字符竖排重复。
  2. **运行时公式与 SVG 自愈函数（`sanitizeMath` & `sanitizeSvgHtml`）**：
     - 在渲染前自动修复 JSON 字符串转义吃掉反斜杠的问题（如 `\f` 换页符恢复为 `\frac`、`\t` 制表符恢复为 `\text`、`\b` 退格符恢复为 `\beta`），并自动剥离混入 `<svg>` 内部的非法 `<p>` 标签。
  3. **空安全守卫与侧边栏持久化状态机**：
     - 在 `InvestLearningApp` 的 `constructor()` 第一行立即执行 `window.app = this;`，确保全局引用永远可用。
     - 所有 `document.getElementById(...)` 必须加空安全判断（`if (el)`），严禁因单个 DOM 节点调整导致构造函数崩溃冻结侧边栏。
     - 使用 `this.expandedModules = new Set([0])` 持久化记录侧边栏模块展开状态；侧边栏在总览页与课程页常驻显示，点击任意课程自动调用 `this.switchMainView('curriculum')` 秒切视图；严禁混用行内 `style.display = 'none'` 与 `.collapsed` 类。
     - 嵌套列表样式强制声明 `.prose ul.label-list ul { list-style: none !important; }`，防止出现 `○ •` 双圆点。
  4. **防缓存版本戳与双分支同步部署**：
     - 每次更新必须在 `index.html` 的所有 CSS/JS 引用后递增版本参数（如 `?v=20261011_v24`）。
     - 同步推送 `git push origin main` 与 `git subtree push --prefix web origin gh-pages`，并通过 `gh api repos/{owner}/{repo}/pages` 验证状态达到 `"status": "built"`。

---

## 一、 严格三色极简视觉系统 (Anthropic 3-Color Design Tokens)

除图表内部语义色外，全站 UI 界面严格收敛于**三种核心色彩**（暖麻羊皮纸/黑曜石底色 + 石墨墨色 + Claude 陶土红唯一点缀色）：

```css
:root {
  /* 1. 基底画布色 (Warm Parchment Canvas) */
  --bg-primary: #FAF8F5;
  --bg-secondary: #FFFFFF;
  --bg-tertiary: #F3EFEA;
  --bg-surface: #EBE5DC;

  /* 2. 中性墨水与边框色 (Charcoal Ink & Borders) */
  --text-primary: #1F1E1B;
  --text-secondary: #4E4B45;
  --text-muted: #7D786F;
  --border-primary: #E2DDD5;
  --border-subtle: #EFECE6;

  /* 3. 唯一品牌点缀色 (Claude Terracotta Accent) */
  --claude-terracotta: #CC5A36;
  --claude-terracotta-light: rgba(204, 90, 54, 0.10);
  --claude-terracotta-border: rgba(204, 90, 54, 0.30);

  /* 权威学术字体排印 */
  --font-serif: 'Newsreader', Georgia, serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

[data-theme="dark"] {
  --bg-primary: #0D0F12;
  --bg-secondary: #15181E;
  --bg-tertiary: #1C2028;
  --bg-surface: #242933;
  --text-primary: #F3F1EC;
  --text-secondary: #B8B4AA;
  --text-muted: #7E7A70;
  --border-primary: #262B36;
  --border-subtle: #1E222B;
  --claude-terracotta: #E06D48;
  --claude-terracotta-light: rgba(224, 109, 72, 0.14);
  --claude-terracotta-border: rgba(224, 109, 72, 0.35);
}
```

---

## 二、 单门课程标准页面结构模板 (Single-Page Unified Template)

每一门课程在 `#lessonViewContainer` 中按如下顺序自上而下垂直渲染：

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. 课程头部卡片 (.lesson-card-header)                                         │
│    • 面包屑：课程总览 / 模块编号与名称 / 第 XX 课                              │
│    • 主标题：单一核心概念短标题 (#lessonMainTitle)                             │
│    • 脉络框 (#lessonSystemContextBox)：                                       │
│      - 本课脉络：1 句话说明承上启下关系                                       │
│      - 章节路径：[L01 标题] ➔ [L02 标题 (当前高亮)] ➔ [L03 标题] ...          │
│    • 本课学习目标 (#lessonObjectivesList)：                                   │
│      - 核心内容：1 句话明确本课核心机制                                       │
│      - 掌握标准：1 句话明确学完后的定量实操标准                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ 2. PART 01 📖 核心理论与市场机制 (#tabPanel_theory — 默认同页展开)            │
│    • 导读卡 (.feynman-bridge-card)：                                          │
│      - 直观类比：30 秒日常场景类比破冰                                        │
│      - 实例验算：1 分钟具体数字算术推演                                       │
│    • 核心机制与图解：                                                         │
│      - 1 幅 860px 科学绘图矢量大图 (带 🔍 点击全屏放大按钮)                   │
│      - 3 条核心机制要点拆解 (<ul class="label-list">)                         │
│    • 核心量化公式：                                                           │
│      - 1 个核心 KaTeX 公式 + 内部正下方「🗣️ 直白算式」中文等式条              │
│      - 公式下方紧跟符号含义与实盘阈值列表 (<ul class="label-list">)           │
│    • 专属伴随交互仿真沙盒 (仅在最匹配的 5 门核心课中内嵌，附三步操作指引)     │
│    • 常见误区与风控边界 (1 个 .callout-warning 总结框)                        │
├──────────────────────────────────────────────────────────────────────────────┤
│ 3. PART 02 📊 实测成果数据与实战清单 / 工程实现 (默认同页展开)                │
│    • 实测成果数据看板 (.result-data-card)：                                   │
│      - 右上角：🟢 实时同步状态标 + [🔄 实时刷新数据] 按钮                     │
│      - 顶部：4 个核心 KPI 读数摘要卡 (.result-kpi-grid)                       │
│      - 中部：交互式实时重算器 (.live-calc-bar) + 历史与最新期实测对比表       │
│      - 底部：💡 实时动态结论与仓位建议框 (随数据变化自动重算切换结论)         │
│    • 非代码模块展示：四步标准化实操流程 + 常见致命陷阱 + 真实案例复盘         │
│    • 算法工程模块展示：Python 3.12 完整可运行参考源码 + 一键复制按钮          │
├──────────────────────────────────────────────────────────────────────────────┤
│ 4. PART 03 ❓ 核心思考与问答 (#tabPanel_qa — 默认同页展开)                    │
│    • 2 道紧扣本课核心概念的深度思考题 (Q1, Q2)                                │
│    • 默认展开的「✔ 参考解析」卡片（完整编译为多级 HTML 列表与 KaTeX 公式）   │
├──────────────────────────────────────────────────────────────────────────────┤
│ 5. 底部连续翻页栏 (#lessonBottomNav)                                          │
│    • [⬅ 上一课：标题]                                    [下一课：标题 ➡]     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、 标准化仓库目录结构

```text
<course-repo>/
├── README.md                          # 课程总纲、四大层级架构、本地与在线使用指南
├── GITHUBPAGES_SKILL.md               # 本课程制作规范文档
├── test_all_answers.py                # 全量课程参考代码 100% 自动化回归测试套件
├── .github/
│   └── workflows/
│       └── update-live-data.yml       # 每日定时拉取权威实时数据并同步 main & gh-pages
├── scripts/
│   └── fetch_live_data.py             # 实时数据抓取、指标核算与动态结论生成脚本
├── 01_module_one/                     # 各模块源码与参考答案目录 (01 ~ 10)
│   ├── lesson01_xxx.py
│   └── answers/
│       └── lesson01_xxx.py
└── web/                               # GitHub Pages 静态单页应用根目录 (subtree 发布源)
    ├── index.html                     # 主入口（含总览页、课程页、文献库、全屏缩放灯箱）
    ├── css/
    │   └── style.css                  # 严格三色系统与响应式排版样式表
    ├── js/
    │   ├── data-curriculum.js         # 全量课程结构化数据库
    │   ├── data-books.js              # 经典文献库数据库（开放阅读直达 + MD5 下载直达）
    │   ├── live-market-data.json      # 云端定时自动更新的实时数据快照
    │   ├── charts.js                  # 交互式 Canvas 仿真引擎
    │   └── app.js                     # SPA 路由、KaTeX/SVG 自愈渲染、实时数据联动控制器
    └── vendor/
        └── katex/                     # 本地常驻 KaTeX 0.16.9 核心脚本、样式与 WOFF2 字体
```

---

## 四、 交付前自动化验收核对清单 (Pre-Delivery Verification Checklist)

每次构建或更新课程后，必须通过以下 8 项自动化检查方可交付：

- [ ] **1. 单元测试 100% 通过**：运行 `python3 test_all_answers.py`，确保所有课程参考实现 `100% PASS (0 Failed)`。
- [ ] **2. 零形式化包装词与套话残留**：全局检索 `data-curriculum.js`，确保 `引导句锚点`、`架构要点拆解`、`投决会核心心智模型`、`核心概念与就近图文排版`、`锚点指引`、`零基础费曼降维导读` 出现次数严格为 `0`。
- [ ] **3. 单课 1:1:1:1 密度合规**：核验全量 N 门课中，`math-block`、`scientific-svg`、`callout-warning` 数量严格等于 N（每课各 1 个），且 100% 包含 `.math-plain-bar`（`🗣️ 直白算式`）与公式下方的变量列表。
- [ ] **4. 零未编译 Markdown 与零 KaTeX 报错**：使用 Node.js + 本地 `katex.min.js` 遍历编译全站所有块级与行内公式，确保 `0` 语法报错；确保正文、风控框与问答解析中 `**`、`` ` ``、`:::`、`$$` 原始标记残留为 `0`。
- [ ] **5. 严格空安全 DOM 仿真测试**：在严格模式（未定义 ID 返回 `null`）下运行 Node.js 仿真测试：`初始化 -> 点击总览 -> 展开侧边栏模块 -> 点击进入课程 -> 触发全屏图表缩放 -> 触发实时数据重算`，确保 `0` 异常抛出。
- [ ] **6. 文献链接可访问性核验**：确保 `data-books.js` 中 `/search?q=` 模糊搜索链接为 `0`，所有文献均具备已验证的直达阅读链接或明确的 `🔒 仅限下载借阅` 标识 + MD5 下载直链。
- [ ] **7. 防缓存版本戳递增**：检查 `web/index.html` 中 `style.css?v=...` 与 `app.js?v=...` 版本号已递增。
- [ ] **8. 双分支推送与线上 CDN 探活**：执行 `git push origin main && git subtree push --prefix web origin gh-pages`，轮询 `gh api repos/{owner}/{repo}/pages` 直至 `"status": "built"`，并用 `curl` 验证线上最新内容已生效。
