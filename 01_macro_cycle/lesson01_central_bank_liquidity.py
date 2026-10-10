r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 1/5 课
第 1 课：央行资产负债表与法币流动性净额传导模型 (Central Bank Liquidity Transmission)
================================================================================

::: {.callout-note}
### 投决会核心心智模型：现代法币体系的负债本质与准备金守恒
- **[商业与金融本质]**：在纯信用法币制度下，货币并非实物金属的储值替代品，而是中央银行与商业银行的资产负债表负债凭证。
- **[资产定价第一性原理]**：股票等系统性风险资产的估值中枢（PE/PS）由分母端无风险利率与股权风险溢价（ERP）共同决定，而银行体系超额准备金的水位直接决定了一级交易商的资产负债表承载容量与风险偏好。
- **[流动性守恒公理]**：中央银行资产端资产总计严格恒等于负债端准备金、财政部存款（TGA）、隔夜逆回购（ON RRP）与流通中现金之和。准备金是金融机构扩张信贷与杠杆交易的唯一高能资产。
:::

- **[理论传导机制]**：华尔街顶级宏观对冲基金所监控的美联储“实际净流动性”（Fed Net Liquidity）由以下资产负债表三方博弈决定：

$$
\text{Net Liquidity}_t = \text{Fed Total Assets}_t - (\text{TGA}_t + \text{ON RRP}_t)
$$

- **[变量定义域与物理意义]**：
  - $\text{Fed Total Assets}_t \in \mathbb{R}^+$：美联储总资产规模（单位：十亿美元）。扩表购债（QE）注入基础货币，被动缩表（QT）按月度上限销毁基础货币。
  - $\text{TGA}_t \in \mathbb{R}^+$：财政部一般账户（Treasury General Account）。财政部发债收回私营资金存入美联储，属于系统性流动性抽水；财政部支出则向银行间注水。
  - $\text{ON RRP}_t \in \mathbb{R}^+$：隔夜逆回购便利（Overnight Reverse Repo）。货币市场基金停泊在联储的闲置资金。资金撤出 RRP 认购国库券等于向二级市场释放流动性。
  - $\text{Net Liquidity}_t \in \mathbb{R}^+$：商业银行在联储的真实准备金备付总额，构成金融资产折现率的物理铁底。

- **[引导句锚点 1]**：如下架构拓扑所示，美联储总资产通过负债端不同资金池的分流，决定了最终注入二级金融市场的有效流动性：

```mermaid
flowchart TD
    FedAssets["美联储总资产 (SOMA 国债/MBS) [+]"] --> BalanceSplit["负债端资金池分流"]
    BalanceSplit --> TGA["财政部 TGA 存款 (国库抽水池) [-]"]
    BalanceSplit --> ONRRP["隔夜逆回购 ON RRP (非银闲钱沉淀池) [-]"]
    BalanceSplit --> Reserves["商业银行存款准备金 (净流动性 Net Liquidity)"]
    Reserves --> Interbank["银行间体系资金充裕 (SOFR 保持低位贴水)"]
    Interbank --> RiskAssets["一级交易商/对冲基金加杠杆 ➔ 标普500/纳斯达克估值倍数扩张"]
```

- **[架构要点拆解 1]**：
  - **[1. 资产端扩缩惯性]**：QE 期间资产端扩张直接派生准备金；QT 期间资产端每月被动到期削减，构成流动性收缩的主动约束。
  - **[2. 负债端内部抵消]**：当美联储缩表时，若 ON RRP 资金以更快速度撤出并认购财政部短债，净流动性可能不降反升，形成“名义紧缩、实质宽松”的估值反常驱动。
  - **[3. 最终权益映射]**：流动性向权益资产的传导具有显著的统计时滞（通常为 4~8 周），一阶加速度（Liquidity Impulse）是预测宽基指数中期走势的核心领先指标。

- **[中国人民银行 (PBOC) 数量型调控机制]**：
  - **[价格与数量双轨制]**：PBOC 通过公开市场逆回购（OMO）、中期借贷便利（MLF）、买断式逆回购与法定准备金率（RRR）综合调节银行间超储水位：

$$
\text{PBOC Net Injection}_t = (\text{OMO}^{\text{In}}_t - \text{OMO}^{\text{Mat}}_t) + \text{MLF}^{\text{Net}}_t + \text{RRR Cut Release}_t
$$

- **[变量定义域与物理意义]**：
  - $\text{OMO}^{\text{In}}_t, \text{OMO}^{\text{Mat}}_t \in \mathbb{R}^+$：7天/14天期 OMO 投放与到期量（单位：亿元）。属于短期高频日间平滑工具。
  - $\text{MLF}^{\text{Net}}_t \in \mathbb{R}$：1年期中期借贷便利净投放。属于中期政策性信贷引导中枢。
  - $\text{RRR Cut Release}_t \in \mathbb{R}^+$：降准直接释放的零成本长期法定存款准备金，属于最强力的高能货币注入。

- **[引导句锚点 2]**：如下利率走廊架构所示，中国人民银行通过走廊边界设定与银行间质押式回购利率（DR007）实施宏观流动性引导：

```mermaid
flowchart TD
    CorridorUpper["常备借贷便利 (SLF) 利率 ➔ 走廊刚性上限"] --> InterbankFlow
    InterbankFlow["DR007 存款类金融机构间质押式回购 7 天加权利率"] --> PolicyAnchor["7天 OMO 逆回购利率 ➔ 政策调控锚"]
    InterbankFlow --> CorridorLower["超额存款准备金利率 (IOER) ➔ 走廊绝对铁底"]
    InterbankFlow --> SpreadCheck{"R007 - DR007 利差走阔?"}
    SpreadCheck -->|是| NonBankStress["非银机构流动性紧缩 ➔ A股增量配资与两融承压"]
    SpreadCheck -->|否| SystemicAmple["全市场资金面平稳宽松 ➔ 资产估值支撑稳固"]
```

- **[架构要点拆解 2]**：
  - **[1. 政策利率中枢]**：OMO 7天利率为央行短端基准锚，DR007 围绕 OMO 利率在窄幅区间内波动即为流动性“合理充裕”。
  - **[2. 信用分层剪刀差]**：DR007 仅限存款类商业银行参与，剔除了信用违约风险；R007 包含非银机构（公募、券商、信托）。当 R007 远高于 DR007 时，表明非银流动性干涸。
  - **[3. 股市微观关联]**：A 股杠杆资金与量化多头高度依赖非银拆借资金面，R007 异常飙升往往领先于中小盘股票流动性踩踏。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[名义资产误区]**：严禁将“美联储总资产”简单等同于“市场净流动性”。若忽视发债导致的 TGA 暴增或 RRP 资金淤积，将发生方向性误判。
- **[数据发布时滞陷阱]**：美联储 H.4.1 报告周四发布（截至于周三收盘），而 TGA 与 RRP 每日披露。做日频量化回测时严禁使用修正后的跨期数据，坚决防范 Lookahead Bias。
:::

【思考题】
Q1: 为什么当财政部（Treasury）大幅提高国债发债规模补充 TGA 账户时，如果在逆回购（RRP）池子几乎见底枯竭的情况下，标普500往往承受极其剧烈的下行压制？请从商业银行资产负债表与准备金借贷记账因果链推导。
Q2: 2023年美联储虽然持续进行量化紧缩（QT, 缩减资产负债表约 1 万亿美元），但美股（尤其是纳斯达克100）却走出单边大牛市。请利用“Net Liquidity = Assets - TGA - RRP”模型，量化拆解该时期美联储净流动性为何不降反升？
Q3: 为什么在中国市场，仅仅跟踪央行每日 OMO 逆回购的单日净投放往往是“噪音”，而必须跟踪“超额准备金率（超储率）”、“政府债净缴款”与“DR007/DR001”利差才能真正穿透 A 股的宏观流动性底座？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现 Fed 净流动性与流动性脉冲 (1.5分)；
  2. 准确实现 PBOC 净流动性综合投放计算 (1分)；
  3. 准确实现流动性对股票资产的跨期时滞敏感度（Beta与协方差弹性）(1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须说明底层借贷/资产负债表因果链，而非堆砌术语；
- 通过线：8/10 分。一票否决：概念颠倒（如将 TGA 上升误当作流动性利好）、删除断言。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def calculate_fed_net_liquidity(fed_total_assets: pd.Series, tga: pd.Series, rrp: pd.Series) -> pd.Series:
    """
    计算美联储法币净流动性指标序列:
        Net_Liquidity = Fed_Total_Assets - (TGA + RRP)

    参数:
        fed_total_assets: 美联储总资产规模时序 (百万/十亿美元)
        tga: 财政部一般账户余额时序 (同单位)
        rrp: 美联储隔夜逆回购规模时序 (同单位)

    返回:
        pd.Series: 净流动性时序 (索引与输入保持一致)
    """
    # TODO: 实现美联储净流动性计算公式
    pass


def compute_liquidity_impulse(net_liquidity: pd.Series, window: int = 4) -> pd.Series:
    """
    计算流动性脉冲 (Liquidity Impulse):
    度量净流动性在过去 window 期内的百分比加速度变动:
        Impulse_t = ((Net_Liquidity_t - Net_Liquidity_{t-window}) / Net_Liquidity_{t-window}) * 100.0

    参数:
        net_liquidity: 净流动性序列
        window: 滚动窗口期数 (如 4 周 / 4 天)

    返回:
        pd.Series: 变动百分比序列 (前 window 期为 NaN)
    """
    # TODO: 计算流动性脉冲百分比变化率
    pass


def calculate_pboc_net_injection(
    omo_inflow: pd.Series,
    omo_mature: pd.Series,
    mlf_net: pd.Series,
    rrr_cut_release: pd.Series,
) -> pd.Series:
    """
    计算中国央行 (PBOC) 综合流动性净投放 (亿元):
        Net_Injection = (omo_inflow - omo_mature) + mlf_net + rrr_cut_release

    参数:
        omo_inflow: 公开市场逆回购新投放金额
        omo_mature: 公开市场逆回购到期回笼金额
        mlf_net: MLF 净投放金额 (新投放 - 到期量)
        rrr_cut_release: 降准释放的长期中长期流动性现金金额 (未降准日为 0)

    返回:
        pd.Series: 单日/单周 PBOC 综合净投放金额
    """
    # TODO: 实现 PBOC 净投放汇总逻辑
    pass


def estimate_liquidity_equity_transmission(
    net_liquidity: pd.Series,
    equity_index: pd.Series,
    lag_steps: List[int] = [0, 1, 2, 4],
) -> Dict[str, float]:
    """
    量化评估流动性变化向股票市场传导的时滞 (Transmission Lag) 与弹性 Beta:
    通过一阶差分对齐:
        d_liq_t = net_liquidity_t - net_liquidity_{t-1}
        d_eq_{t+lag} = equity_index_{t+lag} - equity_index_{t+lag-1}
    计算相关系数与 OLS 斜率 Beta = Cov(d_liq, d_eq_lag) / Var(d_liq)

    返回字典:
        {
            "best_lag": 传导相关系数绝对值最大的滞后期数,
            "best_corr": 最佳时滞下的相关系数,
            "best_beta": 最佳时滞下股票对流动性的一阶敏感度 Beta (d_eq / d_liq)
        }
    """
    # TODO: 遍历各滞后期，对齐后计算 Pearson 相关系数与一阶斜率 Beta，选出绝对相关度最高的 lag
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 美联储净流动性与脉冲计算 ----------------
    dates = pd.date_range("2024-01-01", periods=5, freq="W")
    assets = pd.Series([77000.0, 76800.0, 76500.0, 76300.0, 76000.0], index=dates)
    tga = pd.Series([7500.0, 7800.0, 8000.0, 8200.0, 8500.0], index=dates)
    rrp = pd.Series([6500.0, 6200.0, 5800.0, 5500.0, 5200.0], index=dates)

    net_liq = calculate_fed_net_liquidity(assets, tga, rrp)
    assert net_liq is not None and len(net_liq) == 5, "Net liquidity 输出长度不符"
    assert net_liq.iloc[0] == 63000.0, f"Expected 63000.0, got {net_liq.iloc[0]}"
    assert net_liq.iloc[4] == 62300.0, f"Expected 62300.0, got {net_liq.iloc[4]}"

    imp = compute_liquidity_impulse(net_liq, window=2)
    expected_imp_idx2 = ((62700.0 - 63000.0) / 63000.0) * 100.0
    assert abs(imp.iloc[2] - expected_imp_idx2) < 1e-4, f"流动性脉冲计算偏差: {imp.iloc[2]}"

    # ---------------- 基础测试 2: PBOC 综合流动性核算 ----------------
    pboc_dates = pd.date_range("2024-03-01", periods=3, freq="D")
    omo_in = pd.Series([1000.0, 500.0, 2000.0], index=pboc_dates)
    omo_mat = pd.Series([800.0, 1200.0, 500.0], index=pboc_dates)
    mlf = pd.Series([0.0, 1000.0, 0.0], index=pboc_dates)
    rrr = pd.Series([5000.0, 0.0, 0.0], index=pboc_dates)

    pboc_net = calculate_pboc_net_injection(omo_in, omo_mat, mlf, rrr)
    assert pboc_net.iloc[0] == 5200.0, f"PBOC 第1天净投放应为 5200, 实际: {pboc_net.iloc[0]}"
    assert pboc_net.iloc[1] == 300.0, f"PBOC 第2天净投放应为 300, 实际: {pboc_net.iloc[1]}"
    assert pboc_net.iloc[2] == 1500.0, f"PBOC 第3天净投放应为 1500, 实际: {pboc_net.iloc[2]}"

    # ---------------- 基础测试 3: 流动性时滞传导模型与 Beta ----------------
    np.random.seed(42)
    t_len = 50
    synth_liq = 60000.0 + np.cumsum(np.random.normal(50.0, 150.0, t_len))
    synth_liq_s = pd.Series(synth_liq)
    # 模拟真实市场中 1 周时滞的传导机制: 股票收益受 t-1 期流动性脉冲驱动
    d_liq = synth_liq_s.diff().fillna(0)
    d_eq = 0.8 * d_liq.shift(1).fillna(0) + np.random.normal(0, 10.0, t_len)
    synth_eq_s = pd.Series(5000.0 + np.cumsum(d_eq))

    metrics = estimate_liquidity_equity_transmission(synth_liq_s, synth_eq_s, lag_steps=[0, 1, 2])
    assert metrics["best_lag"] == 1, f"应成功识别滞后1期为最佳传导时滞, 实际检测为: {metrics['best_lag']}"
    assert metrics["best_corr"] > 0.7, f"最佳滞后相关性应大于0.7, 实际为: {metrics['best_corr']}"
    assert 0.6 <= metrics["best_beta"] <= 1.0, f"最佳 Beta 应在 0.6~1.0 之间, 实际为: {metrics['best_beta']}"

    print("Lesson 01 Exercise Code assertions successfully completed!")
