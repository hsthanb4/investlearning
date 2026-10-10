r"""
================================================================================
模块 04：价格行为学、趋势跟踪与技术形态论 · 第 5/5 课
第 5 课：订单流成交量分布 (Volume Profile) 与锚定 VWAP (POC, VAH/VAL & Anchored VWAP)
================================================================================

【课程定位与第一性原理】
传统技术图表只关注价格随“时间（Time）”的展开，却对交易博弈的最关键维度——“成交量在价格上的分布（Volume-at-Price）”完全盲目。
拍卖市场理论（Auction Market Theory, AMT）指出，金融市场本质是一个双向连续竞价的拍卖撮合场，
其唯一终极目的就是在不同价格水平寻找能够促成最大换手交易量的公允价值区（Fair Value）。

- **[成交量分布 VPVR 的博弈本质]**：控制点（POC, Point of Control）是多空双方沉淀筹码最厚重的绝对公允价值共识点；离开价值区意味着拍卖失衡。
- **[70% 价值区与高斯正态分布]**：价值区（VA, Value Area）覆盖约 70% 的历史成交量（对应正态分布 1 个标准差范围 $\pm 1\sigma$），其高轨（VAH）与低轨（VAL）构成最天然的机构供需边界。
- **[锚定 VWAP 的真实持仓成本]**：锚定自重大事件（加息、财报、结构破位）的 Anchored VWAP，代表了自该事件发生以来全市场参与者的加权平均持仓成本线，具有不可逆转的心理防线意义。

【核心概念与就近图文排版】

1. 可见范围成交量分布与 70% 价值区：
观察下图关于水平成交量分箱、POC 控制点与 VAH / VAL 价值区的微观结构：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.1：可见范围成交量分布 (VPVR)：POC 控制点与 70% 价值区 (VAH / VAL)</span>
    <span class="diagram-tag">VOLUME-PROFILE</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l05_volume_profile_vpvr.svg -->
  </div>
</div>

- **[POC 控制点最大共识]**：成交量最高的水平价格分箱（Point of Control），是全市场多空换手博弈最充分的公允锚点。
- **[VAH / VAL 价值区边界]**：从 POC 开始向双向按成交量贪婪扩张直至覆盖 70% 总成交量，上边界为 VAH，下边界为 VAL。
- **[低成交量节点 LVN 真空加速]**：成交量稀薄的低成交量区（Low Volume Node），价格穿透时阻力最小，常发生跳空或单边脉冲快速滑过。

2. 重大事件锚定 VWAP 与动态标准差通道：
下图展示了从重大宏观事件锚定的 AVWAP 及其 $\pm 2\sigma$ 标准差偏离通道：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.2：事件锚定 VWAP (Anchored VWAP) 与动态标准差通道防御模型</span>
    <span class="diagram-tag">ANCHORED-VWAP</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l05_anchored_vwap_dynamics.svg -->
  </div>
</div>

- **[加权成交均价公式]**：$\text{VWAP}_t = \frac{\sum_{i=1}^t P_i \cdot V_i}{\sum_{i=1}^t V_i}$，真实反映资本平均盈亏平衡线。
- **[加权方差通道]**：基于成交量加权方差计算通道上轨与下轨，提供确定性的对冲与均值回归边界。
- **[均线支撑回踩]**：在牛市主升浪中，价格回调至 AVWAP 往往引发机构被动加仓算法的强力买盘拦截。

3. 市场筹码分布三态演进图谱：
下图对比了 P 型分布（空头回补）、b 型分布（长线出逃）与 D 型分布（公允平衡）的三态转换：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 4.5.3：市场筹码分布三态：P 型多头冲刺、b 型空头派发与 D 型公允平衡</span>
    <span class="diagram-tag">PROFILE-REGIMES</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m04_l05_liquidity_distribution_regimes.svg -->
  </div>
</div>

- **[P 型分布 (空头回补轧空)]**：成交量集中在当日顶部，底部单薄，反映空头被迫平仓诱发短跑冲刺，高位往往出现接力滞胀。
- **[b 型分布 (多头踩踏清算)]**：成交量堆积在当日底部，顶部单薄，反映多头资金认赔出逃，但在低位存在大资金吸筹。
- **[D 型分布 (经典公允均衡)]**：呈经典高斯钟形分布，POC 居中，多空充分换手，处于无趋势震荡箱体。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：价值区内的均值回归 vs 价值区外的趋势爆发</div>
  <div class="callout-body">
    当价格运行在 70% 价值区内（VAL ~ VAH）时，交易主线是均值回归，做多低点做空高点；一旦价格伴随放量有效跳出价值区并完成回踩确认，意味着全市场对估值共识发生永久性跃迁，必须立刻切换为顺势突破单边策略。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁逆向对抗从关键结构低点锚定的上升 AVWAP！机构执行算法（VWAP Execution Engine）在价格接近 VWAP 时具有自动平滑挂单吸收指令，逆势做空将被机构流动性碾压。
  </div>
</div>

【数学与拍卖模型】
$$\text{Typical\_Price}_t = \frac{H_t + L_t + C_t}{3}$$
$$\text{VWAP}_t = \frac{\sum_{s=1}^t \text{Typical\_Price}_s \times V_s}{\sum_{s=1}^t V_s}$$
$$\sigma_{\text{VWAP}, t} = \sqrt{\frac{\sum_{s=1}^t V_s \times (\text{Typical\_Price}_s - \text{VWAP}_t)^2}{\sum_{s=1}^t V_s}}$$
$$\text{Z-Score}_t = \frac{\text{Typical\_Price}_t - \text{VWAP}_t}{\sigma_{\text{VWAP}, t}}$$
定义域：$V_s > 0, \quad \sigma_{\text{VWAP}, t} > 0, \quad \text{Value\_Area\_Ratio} = 0.70$。

【思考题】
Q1: 价值区（Value Area 70% 规则）的数理统计依据：为什么华尔街拍卖市场理论（Auction Market Theory, AMT）将 70% 的成交量区域定义为“价值区（Value Area）”？当价格由内向外有效突破 VAH 或 VAL 时，为什么传统“均值回归”交易者会被迫止损而演变为单边暴利“趋势行情”？
Q2: 机构算法交易的 VWAP 基准考核：为什么高盛、摩根士丹利等顶级投行的机构大单执行算法（如 TWAP, VWAP 算法执行器）将当天的日内成交均价是否优于市场 VWAP 作为核心考核 KPI？这如何直接导致市场价格在触及日内 VWAP 时产生天然的强支撑与阻力效应？
Q3: 锚定 VWAP（Anchored VWAP, AVWAP）的锚点选择科学：与普通从固定早盘 9:30 开始计算的日内 VWAP 相比，为什么从“年内历史最低点”、“重大利好财报公布日”或“重大结构突破日”锚定的长期 AVWAP 具有强大的中长期筹码支撑力？请从“该事件以来全市场持仓筹码平均盈亏平衡点”的角度进行博弈论解释。

【评分与通过规则】
- 代码 4 分：基于典型价格的成交量分箱与 70% 价值区算法 (2.5分) + 累积 VWAP 与加权标准差通道 (1.5分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：从拍卖理论、大单执行与持仓筹码加权成本展开
- 通过线：8/10 分。一票否决：价值区计算逻辑混乱、删除断言
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple


def build_volume_profile(
    df: pd.DataFrame,
    num_bins: int = 10,
    value_area_pct: float = 0.70
) -> Dict[str, Any]:
    """
    构建价格成交量分布直方图 (Volume Profile) 并计算 POC, VAH, VAL
    
    参数:
    df: 包含 'high', 'low', 'close', 'volume' 列的行情 DataFrame
    num_bins: 价格离散化区间分箱数量 (默认 10)
    value_area_pct: 价值区成交量覆盖比例 (默认 0.70 即 70%)
    
    返回字典:
    - 'poc_price': 控制点价格 (成交量最大分箱的中心价格)
    - 'vah_price': 价值区高点价格 (Value Area High)
    - 'val_price': 价值区低点价格 (Value Area Low)
    - 'total_volume': 统计总成交量
    - 'binned_profile': pd.DataFrame，各分箱的价格区间与对应成交量
    """
    # TODO: 请实现基于典型价格的成交量垂直分箱与 70% 价值区扩张算法
    pass


def calculate_anchored_vwap_bands(
    df: pd.DataFrame,
    num_std: float = 2.0
) -> pd.DataFrame:
    """
    计算累积 VWAP 以及基于成交量加权方差的上下标准差偏离通道
    
    参数:
    df: 包含 'high', 'low', 'close', 'volume' 列的 DataFrame
    num_std: 偏离通道标准差倍数 (默认 2.0)
    
    返回包含以下列的 DataFrame 副本:
    - 'typical_price': (high + low + close) / 3
    - 'vwap': 累积加权成交均价
    - 'vwap_upper': vwap + num_std * vwap_std
    - 'vwap_lower': vwap - num_std * vwap_std
    - 'vwap_zscore': (typical_price - vwap) / vwap_std
    """
    # TODO: 请实现累积 VWAP 与成交量加权标准差通道计算
    pass


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 05: 成交量分布与 VWAP 偏离对冲策略测试")
    print("=" * 60)

    # 1. 验证 Volume Profile 计算
    # 构造清晰的筹码分布数据: 在 100 附近有天量成交，而在 90 和 110 成交量稀少
    vp_df = pd.DataFrame({
        "high":   [ 92.0,  96.0,  99.0, 101.0, 102.0, 101.0, 100.0, 105.0, 109.0, 112.0],
        "low":    [ 89.0,  93.0,  97.0,  99.0,  99.0,  98.0,  97.0, 102.0, 106.0, 108.0],
        "close":  [ 90.0,  95.0,  98.0, 100.0, 101.0, 100.0,  99.0, 104.0, 108.0, 110.0],
        "volume": [  100,   200,   800,  1500,  2000,  1600,   900,   300,   150,   100]
    })

    profile_res = build_volume_profile(vp_df, num_bins=10, value_area_pct=0.70)
    print("Volume Profile 结果:")
    print("POC 价格:", profile_res["poc_price"])
    print("VAH (价值区高点):", profile_res["vah_price"])
    print("VAL (价值区低点):", profile_res["val_price"])

    assert profile_res is not None, "结果不能为 None"
    # POC 必须落在天量成交价位 100 附近 ([98, 102] 区间)
    assert 98.0 <= profile_res["poc_price"] <= 102.0
    # 价值区高点必须大于低点，且 POC 落在价值区内
    assert profile_res["vah_price"] >= profile_res["poc_price"] >= profile_res["val_price"]
    assert profile_res["total_volume"] == sum(vp_df["volume"])

    # 2. 验证 VWAP 与加权标准差通道
    vwap_df = calculate_anchored_vwap_bands(vp_df, num_std=2.0)
    print("VWAP 计算结果 (尾部5行):\n", vwap_df[["typical_price", "vwap", "vwap_upper", "vwap_lower", "vwap_zscore"]].tail())

    assert "vwap" in vwap_df.columns
    assert "vwap_upper" in vwap_df.columns
    assert "vwap_lower" in vwap_df.columns
    assert "vwap_zscore" in vwap_df.columns
    # 验证上轨大于下轨
    for i in range(1, len(vwap_df)):
        assert vwap_df.loc[i, "vwap_upper"] >= vwap_df.loc[i, "vwap"] >= vwap_df.loc[i, "vwap_lower"]

    print("Lesson 05 练习题测试全部通过！")
