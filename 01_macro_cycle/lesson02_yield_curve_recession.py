r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 2/5 课
第 2 课：利率期限结构与利差倒挂衰退预警模型 (Yield Curve & Recession Forecasting)
================================================================================

::: {.callout-note}
### 投决会核心心智模型：收益率曲线的无风险折现基准与预期假说
- **[商业与金融本质]**：国债收益率曲线（Yield Curve）是全市场固定收益投资者对经济增长、通胀中枢与货币政策路径的无套利预期联合概率分布。
- **[期限溢价规律]**：正常经济周期中，长端国债具有向上倾斜的期限溢价（Term Premium），以补偿长久期所承担的通胀不确定性与流动性风险。
- **[倒挂的物理本质]**：当央行短端政策利率被动高企以压制通胀，而远期市场预期需求萎缩与降息周期时，收益率曲线出现曲率畸变与利差倒挂（10Y-2Y < 0, 10Y-3M < 0）。
:::

- **[理论传导机制]**：收益率利差是衡量经济周期健康度的终极先行指标，定义如下：

$$
\text{Spread}_{10Y-2Y}(t) = y(10, t) - y(2, t) \quad [\text{bps}]
$$

- **[变量定义域与物理意义]**：
  - $y(m, t) \in (0, 0.20)$：到期期限 $m$ 年的无风险国债零息年化收益率。
  - $\text{Spread}_{10Y-2Y} < 0$：进入利差倒挂状态（Inverted Curve），历史统计对未来 6~18 个月内的经济衰退具备高达 90% 以上的预测置信度。

- **[引导句锚点 1]**：如下收益率曲线形态演化图所示，展示了收益率曲线从常态向上倾斜到倒挂形态的微观演化：

```mermaid
flowchart TD
    FedHikes["央行抗通胀激进加息 ➔ 短端利率 (3M, 2Y) 飙升"] --> CurveInversion["10Y - 2Y / 10Y - 3M 收益率利差倒挂 (< 0)"]
    CurveInversion --> BankNIM["商业银行净息差 (NIM) 遭受毁灭性压缩 (借短贷长倒贴)"]
    BankNIM --> CreditCrunch["银行信贷标准急剧收紧 (SLOOS 紧缩指数飙升) ➔ 实体信贷萎缩"]
    CreditCrunch --> EarningsDrop["企业现金流断裂、违约率上升 ➔ 盈利衰退 (Earnings Recession)"]
    EarningsDrop --> EquityCrash["股市戴维斯双杀 (估值折现压制 + 盈利崩塌)"]
```

- **[架构要点拆解 1]**：
  - **[1. 常态正斜率]**：复苏与繁荣期，10Y 收益率显著高于 2Y，反映实体信贷需求旺盛与健康期限溢价。
  - **[2. 平坦化警报]**：央行持续加息抬高短端成本，长端受制于增长预期放缓，利差收敛至零。
  - **[3. 深度倒挂]**：短端无风险利息超过长期资产回报率，对实体信贷体系形成刚性负反馈。

- **[数学原理：自然三次样条插值与远期利率提取]**：
  - 对于给定期限节点 $t_0 < t_1 < \dots < t_n$ 及其收益率 $y_0, y_1, \dots, y_n$，通过自然三次样条插值保证 $C^2$ 连续性。
  - 瞬时远期利率（Instantaneous Forward Rate）定义为：

$$
f(t) = y(t) + t \cdot \frac{\partial y(t)}{\partial t}
$$

- **[变量定义域与物理意义]**：
  - $f(t)$：未来时刻 $t$ 的边际瞬时再投资无风险收益率，若 $f(t) < y(t)$，数学上严格证明即期曲线呈现凸性倒挂。

- **[引导句锚点 2]**：利差倒挂对商业银行净息差（NIM）与实体信贷传导的挤兑机制如下所示：

```mermaid
flowchart LR
    InvertNode["利差深度倒挂 (10Y-2Y < 0)"] --> NIMCollapse["银行借短贷长利差倒挂 ➔ NIM 崩塌"]
    NIMCollapse --> RiskAversion["银行风险偏好断崖下行 ➔ 压缩信用敞口"]
    RiskAversion --> DefaultWave["高负债实体企业融资断流 ➔ 违约率飙升"]
```

- **[架构要点拆解 2]**：
  - **[1. 存贷利差倒挂]**：商业银行借短贷长模式遭受毁灭性打击，新增信贷边际收益降为负数。
  - **[2. 信贷标准骤紧]**：美联储高级贷款专员意见调查（SLOOS）指数飙升，中小企业再融资渠道被掐断。
  - **[3. 实体违约扩散]**：现金流断裂引爆企业破产与裁员，基本面 EPS 崩塌完成闭环传导。

- **[Estrella & Mishkin 衰退概率预测模型 (Probit 框架)]**：
  - 美联储经典研究表明，10Y-3M 或 10Y-2Y 利差与未来 12 个月内衰退发生概率服从 Logistic 映射：

$$
P(\text{Recession}_{t+12} = 1 \mid \text{Spread}_t) = \frac{1}{1 + \exp(-(\alpha + \beta \cdot \text{Spread}_t))}
$$

- **[变量定义域与物理意义]**：
  - $\beta < 0$：参数常取 $\alpha \approx -0.53, \beta \approx -0.018$。利差越负（倒挂越深），模型预测未来 12 个月内衰退概率呈非线性指数级攀升。

::: {.callout-warning}
### 投决会风控红线与认知陷阱
- **[牛陡踩踏陷阱]**：历史暴跌几乎全部发生在“倒挂结束、曲线重新变陡（Bull Steepening）”的阶段，而非初次倒挂期。
- **[确诊降息陷阱]**：央行紧急大幅降息意味着衰退与信用危机已被确诊，企业盈利下修速度远超降息带来的折现率修复。
:::

【思考题】
Q1: 为什么在历史统计中，利差刚发生倒挂的时刻（First Inversion），股票市场往往还在继续创出新高；而在倒挂结束、“曲线重新变陡”（Un-inversion / Bull Steepening）时，美股反而会迎来最惨烈的暴跌？请从货币政策转向时滞与实体违约传导的角度阐述因果逻辑。
Q2: 为什么在量化估值（DCF 模型）中，实际利率（TIPS 收益率）对长久期资产（如纳斯达克科技股、生物医药）估值的压制弹性，远大于名义利率？高通胀环境如何扭曲这一折现机制？
Q3: 为什么中国国债收益率曲线发生利差倒挂的频率与持续时间远低于美债？请从中国商业银行配债行为、央行跨周期调节与外汇管制的微观约束进行剖析。

【评分与通过规则】
- 代码 4 分：
  1. 基础利差与倒挂体制判定 (1分)；
  2. 纯 Python/NumPy 实现自然三次样条插值器及远期利率推导 (2分)；
  3. Estrella-Mishkin 衰退概率模型计算 (1分)；
- Q1~Q3 问答题各 2 分（共 6 分）：深入阐明因果链，而非简单背诵定义；
- 通过线：8/10 分。一票否决：样条插值不收敛、将倒挂解除误判为利好买入信号。
"""

from typing import List, Tuple
import numpy as np
import pandas as pd


def calculate_yield_spread(yield_10y: pd.Series, yield_2y: pd.Series) -> pd.Series:
    """
    计算 10Y - 2Y 国债利差 (单位: 基点 bps, 1% = 100 bps)

    参数:
        yield_10y: 10年期国债收益率 (%)
        yield_2y: 2年期国债收益率 (%)

    返回:
        pd.Series: 利差 (bps)
    """
    # TODO: 实现利差计算公式 (单位: bps, 1% = 100 bps)
    pass


def detect_inversion_regime(spread_bps: pd.Series) -> pd.Series:
    """
    返回布尔序列: True 表示处于倒挂体制 (spread < 0)
    """
    # TODO: 实现倒挂状态判定
    pass


class CubicSplineCurve:
    """
    无套利自然三次样条插值收益率曲线 (Natural Cubic Spline)
    自主实现三对角线性方程求解，不依赖外部 scipy
    """

    def __init__(self, tenors: List[float], yields: List[float]):
        """
        tenors: 期限列表 (如 [0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0], 年)
        yields: 对应年化收益率 (%)
        """
        self.tenors = np.array(tenors, dtype=float)
        self.yields = np.array(yields, dtype=float)
        assert len(self.tenors) == len(self.yields), "期限与收益率数据长度必须一致"
        assert len(self.tenors) >= 3, "样条插值至少需要3个不同节点"
        assert np.all(np.diff(self.tenors) > 0), "期限必须严格递增"

        self._fit_spline()

    def _fit_spline(self):
        """
        计算各子区间自然三次样条系数及二阶导数 M_i
        """
        # TODO: 求解三对角方程组计算节点二阶导数 M
        pass

    def interpolate(self, t: float) -> float:
        """
        在任意期限 t (年) 处估算平滑收益率 y(t)
        """
        # TODO: 定位子区间并计算样条插值收益率
        pass

    def get_forward_rate(self, t: float, dt: float = 1e-4) -> float:
        """
        计算瞬时远期利率 (Instantaneous Forward Rate):
            f(t) = y(t) + t * y'(t)
        """
        # TODO: 计算远期利率
        pass


def calculate_recession_probability(
    spread_bps: float,
    alpha: float = -0.5,
    beta: float = -0.015,
) -> float:
    """
    Estrella-Mishkin 衰退概率预测模型 (Logistic 形式):
        P(Recession) = 1.0 / (1.0 + exp(-(alpha + beta * spread_bps)))
    """
    # TODO: 实现 Logistic 衰退概率映射
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 利差与倒挂状态 ----------------
    y10 = pd.Series([4.2, 4.0, 3.8, 3.7, 3.9])
    y2 = pd.Series([4.0, 4.2, 4.1, 3.6, 3.5])
    spread = calculate_yield_spread(y10, y2)
    assert abs(spread.iloc[0] - 20.0) < 1e-4, f"Expected 20.0 bps, got {spread.iloc[0]}"
    assert abs(spread.iloc[1] - (-20.0)) < 1e-4, f"Expected -20.0 bps, got {spread.iloc[1]}"

    inv = detect_inversion_regime(spread)
    assert inv.iloc[0] is False or inv.iloc[0] == False
    assert inv.iloc[1] is True or inv.iloc[1] == True

    # ---------------- 基础测试 2: 自然三次样条插值 ----------------
    tenors = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
    yields = [5.40, 5.30, 5.00, 4.60, 4.20, 4.10, 4.30]

    curve = CubicSplineCurve(tenors, yields)

    # 验证插值精确穿过原始已知节点
    for t_node, y_node in zip(tenors, yields):
        interp_val = curve.interpolate(t_node)
        assert abs(interp_val - y_node) < 1e-5, f"节点 {t_node}Y 插值误差过大: {interp_val} vs {y_node}"

    # 验证非标准期限插值的平滑性与单调合理性
    y_3y = curve.interpolate(3.0)
    assert 4.20 < y_3y < 4.60, f"3Y 收益率应介于 5Y 与 2Y 之间, 实际为: {y_3y}"

    # 验证瞬时远期利率计算
    f_2y = curve.get_forward_rate(2.0)
    assert isinstance(f_2y, float) and not np.isnan(f_2y)

    # ---------------- 基础测试 3: 衰退概率计算 ----------------
    prob_normal = calculate_recession_probability(150.0)
    assert prob_normal < 0.15, f"正常利差下衰退概率过高: {prob_normal}"

    prob_inverted = calculate_recession_probability(-100.0)
    assert prob_inverted > 0.60, f"深度倒挂下衰退概率偏低: {prob_inverted}"

    print("Lesson 02 Exercise Passed!")
