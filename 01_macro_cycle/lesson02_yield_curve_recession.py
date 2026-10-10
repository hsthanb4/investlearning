r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 2/5 课
第 2 课：利率期限结构与利差倒挂衰退预警模型 (Yield Curve & Recession Forecasting)
================================================================================

【课程定位与第一性原理】
国债收益率曲线（Yield Curve）被誉为宏观经济的“水晶球”，其形态变化蕴含着全市场对未来增长、
通胀与货币政策的边际定价。

在正常健康的经济扩张期，由于投资者要求承担长期持有带来的期限风险与通胀不确定性补偿
（期限溢价, Term Premium），收益率曲线向上倾斜（Upward Sloping: y_10Y > y_2Y）。
然而，当央行为了抑制过热通胀而大幅提高短期政策利率，同时市场对远期经济增长丧失信心、
预期经济将陷入停滞并迫使央行最终降息时，短端收益率飙升而长端收益率受压，
形成“利差倒挂”（Curve Inversion，如 10Y-2Y < 0 或 10Y-3M < 0）。

【核心传导机制与商业银行信用周期】
```mermaid
flowchart TD
    FedHike["央行连续加息 ➔ 短端利率 (3M, 2Y) 飙升"] --> CurveInvert["10Y - 2Y / 10Y - 3M 收益率利差倒挂 (< 0)"]
    CurveInvert --> BankNIM["商业银行净息差 (NIM) 遭受毁灭性压缩 (借短贷长倒贴)"]
    BankNIM --> CreditCrunch["银行信贷标准急剧收紧 (SLOOS 紧缩指数飙升) ➔ 实体信贷萎缩"]
    CreditCrunch --> EarningsDrop["企业现金流断裂、违约率上升 ➔ 盈利衰退 (Earnings Recession)"]
    EarningsDrop --> EquityCrash["美股/全球股市戴维斯双杀 (估值折现压制 + 盈利崩塌)"]
```

【数学原理：无套利收益率曲线三次样条插值 (Natural Cubic Spline)】
金融市场仅直接观测有限的标准关键期限（Key Tenors, 如 0.25Y, 0.5Y, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 30Y）。
为了给非标准期限资产定价并提取瞬时远期利率曲线（Instantaneous Forward Rate），必须使用平滑插值。
对于节点 t_0 < t_1 < ... < t_n 及其收益率 y_0, y_1, ..., y_n，通过自然三次样条插值保证 C^2 连续性。

瞬时远期利率定义为：
    f(t) = y(t) + t * y'(t)

【Estrella & Mishkin 衰退概率预测模型 (Probit/Logit 框架)】
美联储经典研究表明，10Y-3M 或 10Y-2Y 利差与未来 12 个月内衰退发生概率服从 Logistic 映射：
    P(Recession) = 1.0 / (1.0 + exp(-(alpha + beta * spread_bps)))
其中 beta < 0，即利差倒挂越深（Spread 为负且绝对值越大），模型预测的衰退概率越高。

【思考题】
Q1: 为什么在历史统计中，利差刚发生倒挂的时刻（First Inversion），股票市场往往还在继续创出新高；
    而在倒挂结束、“曲线重新变陡”（Un-inversion / Bull Steepening）时，美股反而会迎来最惨烈的暴跌？
    请从货币政策转向时滞与实体违约传导的角度阐述因果逻辑。
Q2: 为什么在量化估值（DCF 模型）中，实际利率（TIPS 收益率）对长久期资产（如纳斯达克科技股、生物医药）
    估值的压制弹性，远大于名义利率？高通胀环境如何扭曲这一折现机制？
Q3: 为什么中国国债收益率曲线发生利差倒挂的频率与持续时间远低于美债？
    请从中国商业银行配债行为、央行跨周期调节与外汇管制的微观约束进行剖析。

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
