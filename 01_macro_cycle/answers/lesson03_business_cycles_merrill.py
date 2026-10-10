r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 3/5 课
第 3 课：经济周期、美林投资时钟与基钦库存周期轮动 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么在 2010 年之后的中国宏观经济实战中，“美林时钟”经常被机构投资者调侃为“美林电风扇”？请从逆周期宏观调控干预频率、金融去杠杆与供给侧结构性改革（行政化产能出清）的角度剖析：
- **[政策干预频率与体制跃迁机制]**：
  - **[1. 逆周期与跨周期调控的敏捷干预]**：成熟市场经济体（如美国）的内生市场出清通常依赖长时间的商业信用违约、企业破产与失业率自然出清；而中国政府拥有强大的逆周期宏观调控工具箱（专项债、产业政策、信贷窗口指导、发改委重大项目批复）。当增长下滑刚进入衰退初期，稳增长政策即强力出台，直接将经济拉入政策驱动型反弹，导致周期阶段被高度压缩。
  - **[2. 供给侧结构性改革重塑通胀形态]**：2016~2018 年供给侧结构性改革通过环保限产与淘汰落后产能，在终端总需求尚未明显过热的情况下，人为推高上游原材料价格，造成 PPI 暴涨而 CPI 低迷的结构性分化。美林时钟经典的“需求拉动型通胀”演变为“供给约束型通胀”，导致大类资产价格脱离经典时钟顺序。
  - **[3. 象限跳跃与资产轮动加速]**：由于政策脉冲式发力与金融严监管（如资管新规破刚兑、地产三道红线去杠杆）交替出现，经济常在一个季度内从“复苏”跳向“滞胀”，再迅速被政策平抑滑入“被动补库”，资产轮动速度极快，呈现出“电风扇般”的高频顺时针或逆时针跳跃。

【Q2 投决会深度解析】
为什么在“被动去库存”阶段往往是股票权益资产夏普比率最高、赔率与胜率最确定性的黄金买点？请从企业自由现金流（FCF）、净资产收益率（ROE）与估值修复的微观财务驱动力推导：
- **[微观企业财务与估值共振机制]**：
  - **[1. 需求拐头与存货消耗的戴维斯双击先兆]**：在被动去库存阶段，终端需求（营业收入、新订单）已率先见底回暖，但企业前期因悲观预期未及扩产，只能加速消耗前期积压的存货。此时产品供求关系改善，企业具备边际提价权或折扣收窄能力，毛利率与资产周转率同步回升。
  - **[2. 自由现金流（FCF）爆发式释放]**：由于此时管理层对中长期前景尚持谨慎态度，资本开支（CapEx）仍处于低位冻结期；同时存货去化带来营运资本减少（$\Delta \text{NWC} < 0$），导致经营现金流（CFO）极速膨胀。$FCFF = CFO - CapEx$ 达到阶段性高点，企业账面真金白银充沛。
  - **[3. 预期差与估值修复弹性最大]**：市场在此阶段往往仍沉浸在前期的悲观线性外推中，股票静态估值处于历史估值分位数的底部（低 PE/低 PB）。随着财报超预期漂移（PEAD）逐步被验证，估值修复与盈利反转形成戴维斯双击，该阶段回撤极低且向上赔率极大。

【Q3 投决会深度解析】
滞胀期（Stagflation）为什么是多资产配置的“百慕大三角”？请阐述为什么经典 60/40 股债平衡组合在滞胀期会遭遇股债相关性由负转正（Positive Stock-Bond Correlation）的系统性失效？
- **[折现率与现金流双向夹击机制]**：
  - **[1. 传统股债负相关的平稳期基石]**：在温和通胀或通缩环境下，股票由分子端企业盈利驱动，债券由分母端无风险利率驱动。经济下行时，央行降息使债券上涨，对冲股票下跌（负相关性），这是 60/40 组合成立的理论基石。
  - **[2. 滞胀期通胀成为统御一切的主导变量]**：在滞胀期，供给冲击导致通胀高企，央行为了抗通胀被迫持续加息或维持高利率，无风险利率飙升重创债券（长端国债资本利得大亏）；与此同时，成本端大宗原材料与工资飞涨严重侵蚀企业净利润（分子端萎缩），叠加高折现率（分母端膨胀），股票遭遇估值与盈利双杀。
  - **[3. 股债相关性由负转正导致风险暴露失控]**：当通胀主导定价时，$\text{Cov}(R_{\text{Equity}}, R_{\text{Bond}}) > 0$。股债资产不仅不能相互平抑波动，反而在同一方向上发生共振杀跌。多资产基金如果不强制引入现金等价物或商品套保，组合净值将遭遇无处可逃的灾难性回撤。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def classify_merrill_clock(growth_trend: pd.Series, inflation_trend: pd.Series) -> pd.Series:
    """
    分类美林时钟四象限:
    - growth > 0 and inflation <= 0 -> 'Recovery' (复苏)
    - growth > 0 and inflation > 0  -> 'Overheat' (过热)
    - growth <= 0 and inflation > 0 -> 'Stagflation' (滞胀)
    - growth <= 0 and inflation <= 0 -> 'Recession' (衰退)
    """
    results = []
    for g, inf in zip(growth_trend, inflation_trend):
        if g > 0 and inf <= 0:
            results.append('Recovery')
        elif g > 0 and inf > 0:
            results.append('Overheat')
        elif g <= 0 and inf > 0:
            results.append('Stagflation')
        else:
            results.append('Recession')
    return pd.Series(results, index=growth_trend.index)


def classify_kitchin_inventory_cycle(sales_growth: pd.Series, inventory_growth: pd.Series) -> pd.Series:
    """
    分类基钦工业库存周期四阶段:
    - sales > 0 and inventory <= 0 -> 'Passive_Destock' (被动去库存)
    - sales > 0 and inventory > 0  -> 'Active_Restock' (主动补库存)
    - sales <= 0 and inventory > 0 -> 'Passive_Restock' (被动补库存)
    - sales <= 0 and inventory <= 0 -> 'Active_Destock' (主动去库存)
    """
    phases = []
    for s, inv in zip(sales_growth, inventory_growth):
        if s > 0 and inv <= 0:
            phases.append('Passive_Destock')
        elif s > 0 and inv > 0:
            phases.append('Active_Restock')
        elif s <= 0 and inv > 0:
            phases.append('Passive_Restock')
        else:
            phases.append('Active_Destock')
    return pd.Series(phases, index=sales_growth.index)


def backtest_asset_rotation(
    regimes: pd.Series,
    asset_returns: pd.DataFrame,
    regime_asset_map: Optional[Dict[str, str]] = None,
) -> Dict[str, float]:
    """
    基于宏观周期体制的大类资产动态轮动策略回测
    """
    if regime_asset_map is None:
        regime_asset_map = {
            'Recovery': 'Stocks',
            'Overheat': 'Commodities',
            'Stagflation': 'Cash',
            'Recession': 'Bonds',
            'Passive_Destock': 'Stocks',
            'Active_Restock': 'Commodities',
            'Passive_Restock': 'Cash',
            'Active_Destock': 'Bonds',
        }

    n_periods = len(regimes)
    strat_returns = []

    for i in range(n_periods):
        regime = regimes.iloc[i]
        target_asset = regime_asset_map.get(regime, 'Cash')
        ret = asset_returns[target_asset].iloc[i]
        strat_returns.append(ret)

    strat_returns = np.array(strat_returns)

    # 计算净值轨迹
    nav_series = np.cumprod(1.0 + strat_returns)
    total_ret = (nav_series[-1] - 1.0) * 100.0

    # 年化收益率 (按 12 期/年 年化)
    ann_ret = ((nav_series[-1] ** (12.0 / n_periods)) - 1.0) * 100.0

    # 最大回撤
    peaks = np.maximum.accumulate(nav_series)
    drawdowns = (peaks - nav_series) / peaks * 100.0
    max_dd = float(np.max(drawdowns))

    # 年化夏普比率 (无风险利率假定 0.0)
    std_ret = np.std(strat_returns, ddof=1) if len(strat_returns) > 1 else 1e-4
    if std_ret < 1e-12:
        sharpe = 0.0
    else:
        sharpe = float(np.mean(strat_returns) / std_ret * np.sqrt(12.0))

    return {
        "total_return": float(total_ret),
        "annualized_return": float(ann_ret),
        "max_drawdown": float(max_dd),
        "sharpe_ratio": float(sharpe),
    }


if __name__ == "__main__":
    # ---------------- 基础测试 1: 美林时钟划分 ----------------
    g = pd.Series([1.2, 0.8, -0.5, -0.2])
    inf = pd.Series([-0.3, 0.5, 0.6, -0.4])
    regimes = classify_merrill_clock(g, inf)
    assert regimes.tolist() == ['Recovery', 'Overheat', 'Stagflation', 'Recession'], f"美林时钟划分错误: {regimes.tolist()}"

    # ---------------- 基础测试 2: 基钦库存周期四阶段划分 ----------------
    sales = pd.Series([5.0, 3.0, -2.0, -4.0])
    inv = pd.Series([-1.0, 2.0, 1.5, -3.0])
    kitchin_phases = classify_kitchin_inventory_cycle(sales, inv)
    expected_kitchin = ['Passive_Destock', 'Active_Restock', 'Passive_Restock', 'Active_Destock']
    assert kitchin_phases.tolist() == expected_kitchin, f"库存周期划分错误: {kitchin_phases.tolist()}"

    # ---------------- 基础测试 3: 宏观资产轮动回测引擎 ----------------
    test_regimes = pd.Series([
        'Recovery', 'Recovery', 'Recovery',
        'Overheat', 'Overheat', 'Overheat',
        'Stagflation', 'Stagflation', 'Stagflation',
        'Recession', 'Recession', 'Recession'
    ])
    returns_data = {
        'Stocks':      [0.05, 0.04, 0.03,  0.01, -0.02, 0.00,  -0.06, -0.04, -0.05,  -0.02, 0.01, 0.02],
        'Commodities': [0.01, 0.02, 0.01,  0.06,  0.07, 0.05,   0.02, -0.01, -0.03,  -0.05, -0.04, -0.03],
        'Cash':        [0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002],
        'Bonds':       [-0.01, 0.00, 0.00, -0.02, -0.01, -0.02, -0.01, 0.00, 0.00,   0.04,  0.03,  0.04],
    }
    asset_df = pd.DataFrame(returns_data)

    metrics = backtest_asset_rotation(test_regimes, asset_df)
    assert metrics["total_return"] > 25.0, f"资产轮动累计回报应大于25%, 实际为: {metrics['total_return']}%"
    assert metrics["max_drawdown"] >= 0.0, f"最大回撤应为非负数, 实际为: {metrics['max_drawdown']}"
    assert metrics["sharpe_ratio"] > 1.5, f"资产轮动夏普比率应大于1.5, 实际为: {metrics['sharpe_ratio']}"

    print("Lesson 03 Answer Verified!")
