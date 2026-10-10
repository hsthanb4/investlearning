r"""
================================================================================
模块 06：现代投资组合理论与仓位风控算法 · 第 5/5 课
第 5 课：尾部风险度量与反脆弱杠铃配置 (Tail Risk & Antifragile Barbell Allocation)
================================================================================

【课程定位与第一性原理】
纳西姆·尼古拉斯·塔勒布（Nassim Nicholas Taleb）的反脆弱哲学指出：
金融资产的收益分布绝非温和的高斯钟形曲线，而是充斥着极度厚尾、负偏度与黑天鹅跳跃的柯西/帕累托长尾分布。
传统的“中间派平庸配置”（如持有 100% 所谓稳健的中等风险股债资产）在危机降临时往往最脆弱，
其平时累积的微薄收益会在单次黑天鹅冲击中被彻底抹平。
投资委员会在构建反脆弱资产底座时，必须拥抱非对称凸性（Convexity），建立塔勒布反脆弱杠铃架构。

- **[杠铃配置的双极端物理架构]**：极端保守端（85%~90%）配置超短期国债或现金，锁定绝对流动性确保绝不破产；极端进取端（10%~15%）配置高凸性虚值期权或不对称衍生品，享受正向黑天鹅狂暴脉冲。
- **[收益率高阶矩度量]**：偏度（Skewness）度量非对称性，超额峰度（Excess Kurtosis）度量肥尾爆发力；高算术夏普往往由严重的负偏度与虚假高胜率粉饰而成。
- **[非对称凸性回报剖面]**：常态下承担有限且确定性的权利金耗损（Theta），在全市场崩盘或狂热时爆发 50~100 倍的指数级利润，反哺母基金在地板价抄底。

【核心概念与就近图文排版】

1. 塔勒布反脆弱杠铃资产配置架构：
观察下图关于杠铃配置极端保守端与极端进取凸性端的双极架构，以及对中间平庸资产的彻底抛弃：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.5.1：塔勒布反脆弱杠铃 (Antifragile Barbell) 顶层资产配置架构</span>
    <span class="diagram-tag">TALEB-BARBELL</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m06_l05_barbell_allocation_architecture.svg -->
  </div>
</div>

- **[极端保守底座 (85%~90%)]**：配置零违约风险、零久期利率风险的超短期国债（T-Bills）与现金。最大下行风险被硬性锁定为 $0\%$。
- **[中间平庸资产为 0%]**：彻底抛弃中等风险资产（如高收益垃圾债、次级信贷、普通混合基金），消除中度风险在危机中的伪稳健陷阱。
- **[极端进取凸性端 (10%~15%)]**：配置深度虚值看跌期权、长久期不对称创新科技期权或危机 Alpha 策略，拥有理论上的无限上行潜能。

2. 资产收益率高阶统计矩：负偏度 vs 正偏度：
下图展示了“压路机前捡硬币”的负偏度资产与“彩票型反脆弱”正偏度资产的分布对比：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.5.2：高阶统计矩：偏度 (Skewness) 与超额峰度 (Excess Kurtosis) 非对称图谱</span>
    <span class="diagram-tag">HIGHER-MOMENTS</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m06_l05_higher_moments_skew_kurt.svg -->
  </div>
</div>

- **[负偏度 (Negative Skew)]**：平时小幅稳定盈利，左侧拖着长长的厚尾，一旦暴雷发生断崖式穿仓（如卖出虚值期权、套息交易 Carry Trade）。
- **[正偏度 (Positive Skew)]**：平时微幅亏损保费，右侧拥有极长的高爆发厚尾（如买入深度虚值期权、趋势跟踪、早期创投 VC）。
- **[超额峰度 (Excess Kurtosis)]**：$\text{Kurt} = \frac{\mathbb{E}[(R-\mu)^4]}{\sigma^4} - 3.0$。正态分布峰度为 0，金融资产峰度通常 $> 6.0$。

3. 非对称凸性收益回报剖面 (Convex Payoff)：
下图展示了杠铃策略在不同市场波动状态下的非对称 PnL 凸性抛物线：

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">图 6.5.3：非对称凸性回报剖面：常态 Theta 磨损 vs 极端危机 Gamma / Vega 暴击</span>
    <span class="diagram-tag">CONVEXITY-PAYOFF</span>
  </div>
  <div class="diagram-svg-container">
    <!-- SVG 锚点: assets/m06_l05_convexity_payoff_asymmetry.svg -->
  </div>
</div>

- **[常态平稳期]**：仅承受极其微小、确定性且可控的权利金耗损（$- \text{Theta}$），底座 90% 的国债利息足以完全覆盖此成本。
- **[单边崩盘爆发期]**：极端杀跌引发 Gamma 爆发与波动率指数暴涨（$+\text{Vega}$），虚值期权产生数十倍非线性利润爆发。
- **[危机收割与再平衡]**：在全市场流动性枯竭断崖时兑现期权暴利，用充沛现金在底部狂暴抄底被错杀的超级核心资产。

<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：凸性（Convexity）是不确定性世界中的唯一盟友</div>
  <div class="callout-body">
    根据琴生不等式（Jensen's Inequality），对于凸函数 $f(x)$，$\mathbb{E}[f(x)] \ge f(\mathbb{E}[x])$。这意味着：只要收益结构具有正向凸性，世界的不确定性与波动率越大，策略的最终期望回报反而越高。反脆弱的核心就是成为波动率的朋友。
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控警示与认知陷阱</div>
  <div class="callout-body">
    严禁被高胜率策略（Win Rate > 95%）的虚假光环蒙蔽！依靠卖出深度虚值期权维持连续数年不回撤的基金，其超额收益完全是预支未来的尾部自杀借款，投决会必须强制审查其收益率分布的超额峰度与偏度。
  </div>
</div>

【数学与高阶矩模型】
$$\text{Skewness} = \mathbb{E}\left[\left(\frac{R - \mu}{\sigma}\right)^3\right] = \frac{\frac{1}{N}\sum (R_i - \bar{R})^3}{\sigma^3}$$
$$\text{Excess\_Kurtosis} = \mathbb{E}\left[\left(\frac{R - \mu}{\sigma}\right)^4\right] - 3.0 = \frac{\frac{1}{N}\sum (R_i - \bar{R})^4}{\sigma^4} - 3.0$$
$$\text{Barbell\_Allocation} = 0.90 \times \text{RiskFree\_Cash} + 0.10 \times \text{Convex\_Option}$$
定义域：$\sigma > 0, \quad \text{Excess\_Kurtosis} \in [-3, +\infty), \quad \text{Normal Distribution} \equiv 0.0$。

【思考题】
Q1: 塔勒布反脆弱杠铃策略（Barbell Strategy）对中间派平庸资产的彻底否定：为什么将 85%~90% 资金置于零违约风险的超短国债，同时将 10%~15% 资金配置于具有极端凸性（Convexity）的虚值看跌期权，其抗脆弱性远高于持有 100%“中等风险、中等收益”的普通股债混合组合？从极端黑天鹅事件下的生存概率推导。
Q2: 收益率分布的高阶矩：负偏度（Negative Skewness）与超额厚尾峰度（Excess Kurtosis）：为什么在量化私募基金中，单纯看年化夏普比率高达 3.0 的策略往往是潜伏的巨型炸弹（如压路机前捡硬币的卖出深度虚值期权策略）？如何通过高阶统计矩穿透识别其隐蔽的尾部穿仓风险？
Q3: 尾部对冲基金（Tail Risk Funds，如 Universa Investments）的非对称数学本质：平时持续购买深度虚值看跌期权（OTM Puts）每年会产生约 1%~2% 的时间价值（Theta）确定性耗损；但这笔“负现金流保费”是如何在 2008 金融海啸或 2020 疫情流动性危机中爆发高达 3000%~5000% 的非线性回报，从而反哺母基金在全市场地板价大肆扫货优质资产的？

【评分与通过规则】
- 代码 4 分：超额峰度 (Excess Kurtosis) 准确计算 (2分) + 肥尾与正态对比断言 (2分)
- Q1~Q3 深度思考题各 2 分（共 6 分）：从反脆弱杠铃双极架构、高阶统计矩穿透与期权凸性再平衡展开
- 通过线：8/10 分。一票否决：正态分布超额峰度未归零、峰度计算符号倒置
"""

import numpy as np

def calculate_kurtosis(returns: np.ndarray) -> float:
    """
    计算超额峰度 (Excess Kurtosis, 标量 float):
    正态分布超额峰度为 0.0，金融肥尾超额峰度 > 0
        Excess_Kurtosis = (E[(R - mu)^4] / sigma^4) - 3.0
    """
    # TODO: 实现超额峰度计算
    pass

if __name__ == "__main__":
    normal_like = np.array([-0.02, -0.01, 0.0, 0.01, 0.02])
    fat_tail = np.array([-0.15, -0.01, 0.0, 0.01, 0.20])
    k_fat = calculate_kurtosis(fat_tail)
    k_norm = calculate_kurtosis(normal_like)
    assert k_fat > k_norm
    print("Lesson 05 (Tail Risk) Exercise Passed!")
