r"""
================================================================================
模块 01：宏观经济学、货币周期与流动性传导 · 第 3/5 课
第 3 课：经济周期、美林投资时钟与基钦库存周期轮动 (Business Cycles & Inventory Dynamics)
================================================================================

【课程定位与第一性原理】
自 1930 年代康德拉季耶夫、朱格拉与基钦提出宏观周期理论以来，资产定价的核心逻辑始终在于
“大类资产收益率与宏观经济周期阶段的高度协变性”。

美林证券（Merrill Lynch, 2004）总结出著名的“美林投资时钟”（Investment Clock），将宏观周期按照
“经济增长（产出缺口 Growth）”与“通胀趋势（CPI/PPI Inflation）”两个维度划分为四个象限：
1. 衰退期（Growth ↓, Inflation ↓）：产能过剩、信贷萎缩、利率快速下行。
   - 大类资产排序：债券 (Bonds) > 现金 (Cash) > 股票 (Stocks) > 大宗商品 (Commodities)。
2. 复苏期（Growth ↑, Inflation ↓）：宽松政策见效、需求回暖、企业利润恢复，折现率仍处低位。
   - 大类资产排序：股票 (Stocks) > 债券 (Bonds) > 现金 (Cash) > 大宗商品 (Commodities)。
3. 过热期（Growth ↑, Inflation ↑）：产能利用率触顶、原材料供不应求、央行开始加息紧缩。
   - 大类资产排序：大宗商品 (Commodities) > 股票 (Stocks) > 现金 (Cash) > 债券 (Bonds)。
4. 滞胀期（Growth ↓, Inflation ↑）：生产成本高企压垮企业盈利，央行受困于高通胀无法降息，股债双杀。
   - 大类资产排序：现金 (Cash) > 大宗商品 (Commodities) > 债券 (Bonds) > 股票 (Stocks)。

【微观实战：基钦库存周期（40个月小周期）四阶段量化】
在工业与制造业国家（如中国、德国、日韩），宏观经济的高频脉搏集中体现为“工业企业库存周期”：
以“需求/营业收入增速（Demand/Sales Growth）”与“产成品存货增速（Inventory Growth）”两维交织：
```mermaid
flowchart TD
    Phase1["1. 被动去库存 (需求↑, 存货↓) ➔ 景气初见曙光，企业产品供不应求，盈利暴增 (股票黄金期)"] --> Phase2
    Phase2["2. 主动补库存 (需求↑, 存货↑) ➔ 产销两旺，开足马力扩产，商品原材料暴涨 (商品/周期股繁荣)"] --> Phase3
    Phase3["3. 被动补库存 (需求↓, 存货↑) ➔ 终端需求见顶下滑，生产惯性导致库存积压 (现金为王/防守)"] --> Phase4
    Phase4["4. 主动去库存 (需求↓, 存货↓) ➔ 深度出清，降价甩卖关停产能，货币全面宽松 (长久期国债牛市)"] --> Phase1
```

【思考题】
Q1: 为什么在 2010 年之后的中国宏观经济实战中，“美林时钟”经常被机构投资者调侃为“美林电风扇”？
    请从逆周期宏观调控干预频率、金融去杠杆与供给侧结构性改革（行政化产能出清）的角度，
    剖析中国宏观周期为何频繁发生象限跳跃与阶段压缩？
Q2: 为什么在“被动去库存”阶段往往是股票权益资产夏普比率最高、赔率与胜率最确定性的黄金买点？
    请从企业自由现金流（FCF）、净资产收益率（ROE）与估值修复的微观财务驱动力推导。
Q3: 滞胀期（Stagflation）为什么是多资产配置的“百慕大三角”？请阐述为什么经典 60/40 股债平衡组合
    在滞胀期会遭遇股债相关性由负转正（Positive Stock-Bond Correlation）的系统性失效？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现经典美林时钟四象限判别 (1分)；
  2. 准确实现基钦库存周期四阶段判别 (1.5分)；
  3. 准确实现大类资产动态轮动策略回测引擎与绩效指标计算 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须说明底层微观财务与宏观机制因果链；
- 通过线：8/10 分。一票否决：库存阶段划分颠倒、回测净值计算前视偏差、删除断言。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def classify_merrill_clock(growth_trend: pd.Series, inflation_trend: pd.Series) -> pd.Series:
    """
    分类美林时钟四象限:
    - growth > 0 and inflation <= 0 -> 'Recovery' (复苏: 股票最优)
    - growth > 0 and inflation > 0  -> 'Overheat' (过热: 大宗商品最优)
    - growth <= 0 and inflation > 0 -> 'Stagflation' (滞胀: 现金最优)
    - growth <= 0 and inflation <= 0 -> 'Recession' (衰退: 债券最优)

    参数:
        growth_trend: 产出缺口或增长加速度序列 (如 GDP/PMI 偏离度)
        inflation_trend: 通胀动量序列 (如 CPI/PPI 同比变动加速度)

    返回:
        pd.Series: 宏观阶段类别字符串
    """
    # TODO: 实现四象限分类判定
    pass


def classify_kitchin_inventory_cycle(sales_growth: pd.Series, inventory_growth: pd.Series) -> pd.Series:
    """
    分类基钦工业库存周期四阶段:
    - sales > 0 and inventory <= 0 -> 'Passive_Destock' (被动去库存: 需求好转，库存被动消耗，利好权益)
    - sales > 0 and inventory > 0  -> 'Active_Restock' (主动补库存: 需求强劲，产能全开，利好商品与周期)
    - sales <= 0 and inventory > 0 -> 'Passive_Restock' (被动补库存: 需求恶化，产品积压滞销，现金为王)
    - sales <= 0 and inventory <= 0 -> 'Active_Destock' (主动去库存: 需求萧条，低价甩货出清，利好长债)

    参数:
        sales_growth: 工业企业营收或销售增速偏离度 (一阶导/环比加速)
        inventory_growth: 工业产成品存货增速偏离度

    返回:
        pd.Series: 库存阶段标签
    """
    # TODO: 实现库存周期四阶段判定
    pass


def backtest_asset_rotation(
    regimes: pd.Series,
    asset_returns: pd.DataFrame,
    regime_asset_map: Optional[Dict[str, str]] = None,
) -> Dict[str, float]:
    """
    基于宏观周期体制的大类资产动态轮动策略回测:
    在每个期初，根据当前处于的宏观体制 (regime_t)，全仓配置对应胜率最高的大类资产。

    默认资产映射:
    {
        'Recovery': 'Stocks',
        'Overheat': 'Commodities',
        'Stagflation': 'Cash',
        'Recession': 'Bonds',
        'Passive_Destock': 'Stocks',
        'Active_Restock': 'Commodities',
        'Passive_Restock': 'Cash',
        'Active_Destock': 'Bonds'
    }

    参数:
        regimes: 各期宏观体制时序
        asset_returns: 各大类资产当期单期收益率 DataFrame (例如列: ['Stocks', 'Bonds', 'Commodities', 'Cash'])
        regime_asset_map: 体制至目标资产的映射字典

    返回:
        Dict[str, float]: 包含策略绩效指标:
            - 'total_return': 累计总回报率 (%)
            - 'annualized_return': 年化复合收益率 (%) (假设单期为月频，按 12 期年化)
            - 'max_drawdown': 最大回撤幅度 (%)
            - 'sharpe_ratio': 年化夏普比率 (无风险利率设为 0.0)
    """
    # TODO: 实现资产轮动收益核算、净值曲线追踪、回撤与夏普比率计算
    pass


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
    # 构造跨周期的典型收益率矩阵 (12个月)
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

    print("Lesson 03 Exercise Passed!")
