r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 1/5 课
第 1 课：央行资产负债表与法币流动性净额传导模型 (Central Bank Liquidity Transmission)
================================================================================

【课程定位与第一性原理】
在现代法币信贷货币体系（Fiat Fractional-Reserve System）下，股票等风险资产的系统性估值水平
并非由静态的企业会计账面价值决定，而是由央行资产负债表扩张/收缩所决定的“高能货币（基础货币）”
在银行间金融系统与实体经济间的流动性潮汐所决定。

美联储（Federal Reserve）和中国人民银行（PBOC）是全球最重要的两大多头流动性供给源：
1. 美联储体系核心等式：
   Fed 负债端包含四大核心项：
   - 银行准备金存款 (Reserves)
   - 财政部一般账户 (Treasury General Account, TGA)
   - 隔夜逆回购协议 (Overnight Reverse Repurchase Agreement, ON RRP)
   - 流通中现金 (Currency in Circulation)
   
   由于准备金是支撑商业银行信贷扩张、金融中介加杠杆和证券买卖的核心高能资产，
   金融市场的“实际净流动性”（Fed Net Liquidity）定义为：
       Net_Liquidity = Fed_Total_Assets - (TGA_Balance + ON_RRP_Balance)
   
   - TGA 上升：财政部吸收民间资金存入美联储账户，流动性被锁死在国库，相当于从金融市场抽水（紧缩）；
   - ON RRP 上升：货币市场基金（MMF）与非银金融机构把现金存入美联储吃无风险隔夜利息，资金退出二级市场；
   - TGA / RRP 下降：资金泄洪流入银行存款与商业票据/国债市场，推高金融资产估值（宽松）。

2. 中国央行（PBOC）体系核心特征：
   - 价格型工具与数量型工具并重；
   - 公开市场操作（OMO 逆回购 7D/14D）、中期借贷便利（MLF 1Y）、买断式逆回购、国债买卖；
   - 法定存款准备金率（RRR）调节：降准直接释放无成本长期资金（High-powered Money）。
   PBOC 净流动性注入公式：
       PBOC_Net_Injection = OMO_投放 - OMO_到期 + MLF_净投放 + 降准释放长期流动性

【核心流程与心智模型】
```mermaid
flowchart TD
    FedAssets["美联储总资产 (SOMA 国债/MBS)"] --> FedLiab["美联储负债端拆解"]
    FedLiab --> TGA["财政部 TGA (国库抽水池) [-]"]
    FedLiab --> ONRRP["隔夜逆回购 ON RRP (闲钱锁定池) [-]"]
    FedLiab --> Reserves["商业银行存款准备金 [+]"]
    Reserves --> Interbank["银行间充裕流动性 (SOFR 保持低位)"]
    Interbank --> RiskAppetite["一级交易商/对冲基金加杠杆 ➔ 标普500/纳斯达克估值扩张"]
```

【工业界实战场景与风控陷阱】
1. 纳税日效应与发债抽水：每年4月中旬美国税期，居民/机构向财政部缴税，TGA 往往在 1~2 周内暴增 2000~4000 亿美元，
   若同期 RRP 未能同等幅度流出缓冲，将引发商业银行储备金断崖式下挫，美股往往出现季节性深度回调。
2. 数据发布频率与信息对齐（Lookahead Bias 防范）：
   美联储 H.4.1 报告每周四发布（截至于周三收盘），而财政部 TGA 和纽约联储 ON RRP 数据按工作日每日发布。
   做日频/周频流动性因子回测时，必须使用发布时刻可见的数据截面，严禁把周日后修正值提前代入历史日。

【思考题】
Q1: 为什么当财政部（Treasury）大幅提高国债发债规模补充 TGA 账户时，如果在逆回购（RRP）池子几乎见底枯竭的情况下，
    标普500往往承受极其剧烈的下行压制？请从商业银行资产负债表与准备金的借贷记账法因果链推导。
Q2: 2023年美联储虽然持续进行量化紧缩（QT, 缩减资产负债表约 1 万亿美元），但美股（尤其是纳斯达克100）却走出单边大牛市。
    请利用“Net Liquidity = Assets - TGA - RRP”模型，量化拆解该时期美联储净流动性为何不降反升？
Q3: 为什么在中国市场，仅仅跟踪央行每日 OMO 逆回购的单日净投放往往是“噪音”，而必须跟踪“超额准备金率（超储率）”、
    “政府债净缴款”与“DR007/DR001”利差才能真正穿透 A 股的宏观流动性底座？

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
