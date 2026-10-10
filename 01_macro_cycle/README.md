# 模块 01：宏观经济、货币周期与流动性传导 (01_macro_cycle)

> **"Top-down determines the beta, bottom-up extracts the alpha."**  
> 宏观经济与货币政策并非飘在空中的理论叙事，而是主宰大类资产定价与股票市场系统性 Beta 的底层水龙头。

---

## 一、模块全景导读与第一性原理

在量化投资与全球宏观对冲（Global Macro）体系中，股票资产的价格变动由两个核心驱动力决定：**分子端的企业盈利（Earnings）** 与 **分母端的折现率与流动性（Discount Rate & Liquidity）**：

$$P = \sum_{t=1}^{\infty} \frac{\mathbb{E}[CF_t]}{(1 + r_f + \text{ERP})^t}$$

- **无风险利率 ($r_f$) 与流动性净额**：由全球央行（美联储 Fed、中国央行 PBOC）资产负债表与货币供给机制主导；
- **股权风险溢价 ($\text{ERP}$)**：由经济增长预期、衰退风险、违约风险及风险偏好主导；
- **企业现金流 ($CF_t$)**：由宏观商业周期、产能周期（朱格拉周期）与库存周期（基钦周期）所塑造的企业盈利能力主导。

本模块聚焦于**宏观周期与流动性向权益市场的传导链条**，通过第一性原理剖析从“中央银行资产负债表”到“跨国资本流动”，再到“大类资产轮动与宏观体制自适应”的完整量化框架。

---

## 二、知识图谱与流动性传导因果链

```mermaid
flowchart TD
    subgraph 央行基础货币层
        Fed[美联储资产负债表 / PBOC资产负债表]
        FedBalance[美联储总资产: SOMA国债/MBS]
        TGA[财政部一般账户 TGA]
        ONRRP[隔夜逆回购 ON RRP]
        FedNet[Fed净流动性 = Fed资产 - TGA - RRP]
        PBOC[PBOC MLF/逆回购/降准/超额准备金]
    end

    subgraph 利率期限结构与信贷层
        FedNet --> Interbank[银行间流动性: SOFR / DR007]
        Interbank --> YieldCurve[国债收益率曲线: 2Y, 10Y, 3M]
        YieldCurve --> Inversion[期限利差倒挂: 10Y-2Y / 10Y-3M]
        Inversion --> CreditCycle[银行净息差收缩 ➔ 信贷紧缩 ➔ 衰退预警]
    end

    subgraph 宏观经济与周期层
        CreditCycle --> BusinessCycle[经济周期: 美林投资时钟]
        BusinessCycle --> Kitchen[基钦周期: 3~4年库存周期]
        BusinessCycle --> Juglar[朱格拉周期: 8~10年设备投资周期]
        Kitchen --> Rotation[资产轮动: 衰退债 -> 复苏股 -> 过热宗 -> 滞胀币]
    end

    subgraph 跨国汇率与资本流动层
        YieldCurve --> RateDiff[中美利差 (10Y US - 10Y CN)]
        RateDiff --> DXY[美元指数 (DXY) 强弱]
        DXY --> USDCNH[人民币汇率 (USD/CNH) 贬值/升值压力]
        USDCNH --> Northbound[北向资金 / 离岸资本跨国流动冲击]
    end

    subgraph 投资组合与动态配置层
        Rotation --> Regime[宏观体制识别: Markov Switching / 状态机]
        Northbound --> Regime
        Regime --> AllWeather[全天候自适应对冲: 动态波动率目标与股票Beta调控]
    end
```

---

## 三、课程目录与学习路径

| 课程编号 | 课程主题 | 核心理论与量化方法 | 对应代码文件 | 对应答案文件 |
| :--- | :--- | :--- | :--- | :--- |
| **Lesson 01** | **央行流动性与资产负债表传导模型** | Fed/PBOC 资产负债表拆解、准备金、ON RRP、TGA账户、净流动性传导模型 | `lesson01_central_bank_liquidity.py` | `answers/lesson01_central_bank_liquidity.py` |
| **Lesson 02** | **利率期限结构与利差倒挂监控** | 利率期限结构、Nelson-Siegel / 三次样条插值、10Y-2Y / 10Y-3M 利差倒挂、衰退领先指标 | `lesson02_yield_curve_recession.py` | `answers/lesson02_yield_curve_recession.py` |
| **Lesson 03** | **经济周期、美林时钟与库存周期轮动** | 经典美林投资时钟、基钦库存周期四阶段判别（主动去/被动去/主动补/被动补） | `lesson03_business_cycles_merrill.py` | `answers/lesson03_business_cycles_merrill.py` |
| **Lesson 04** | **美元指数、汇率与跨国资本流动** | 抛补利率平价 (CIP)、DXY 美元强弱周期、中美利差、汇率弹性与资本外流冲击指数 | `lesson04_dollar_exchange_capital_flow.py` | `answers/lesson04_dollar_exchange_capital_flow.py` |
| **Lesson 05** | **宏观体制切换与全天候对冲配置** | 宏观体制切换（Markov Switching / 状态机）、全天候（All-Weather）风险平价、自适应暴露 | `lesson05_macro_hedge_regime.py` | `answers/lesson05_macro_hedge_regime.py` |

---

## 四、工业界投研标准与通关准则

本模块严格遵循顶尖宏观对冲基金（Bridgewater, Brevan Howard, Citadel Global Macro）的投研工程标准：
1. **数据事实优先**：严禁把纸面理论直接当做交易信号，必须理解央行操作的日历效应、结算日摩擦与政策时滞。
2. **严防前视偏差（Lookahead Bias）**：宏观指标发布均有滞后性（如 CPI、GDP 等通常滞后发布，且有初值与修正值）。量化系统必须严格基于“信息发生截面”进行回测。
3. **完成与考核标准**：
   - 每课提供**练习版本**（含 `# TODO` 及测试断言）与 **`answers/` 参考答案版本**。
   - 必须通过该课全部单元测试断言（`assert`），运行结果返回 `exit code 0`。
   - 每课包含 3 道深度机制思考题（Q1, Q2, Q3），考核标准：代码 4 分 + 思考题各 2 分，满分 10 分，8 分达标通过。一票否决：概念倒置、删除断言校验、未能解释因果链条。
