r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 5/5 课
第 5 课：资金流向、两融杠杆与龙虎榜席位多维博弈打分模型 (Capital Flow & Seat Tracker)
================================================================================

【课程定位与第一性原理】
在 A 股高度散户化与机构博弈交织的市场生态中，“资金流向（Capital Flow）”与“筹码结构”
是洞悉主力资金真实底牌的终极微观放大镜。

A 股特色资金三大生态层：
1. 北向资金（陆股通 / HKEX Connect）：
   曾被市场誉为“聪明钱”（Smart Money）。但量化机构必须穿透其持仓托管行（Custodian）：
   - 外资长线机构（Long-only，如托管于汇丰、花旗、摩根大通的养老金与主权基金）：风格稳健，久期长，重仓行业白马龙头；
   - 对冲与高频量化（Hedge Funds，如托管于高盛、摩根士丹利的离岸对冲基金）：追求日内或短期套利，快进快出；
   - 返程假外资：境内配资通过香港通道披上外资马甲回流炒作题材。
2. 融资融券杠杆（Margin Financing & Leverage）：
   融资买入额占个股总成交额比例（Margin Buy Ratio）是全市场风险偏好与杠杆做多情绪的温度计：
   - 正常区间一般在 6%~10%；
   - 超过 15%~20% 意味着过度杠杆亢奋，一旦股价见顶将引发强制平仓连锁暴跌。
3. 交易所龙虎榜（Dragon & Tiger List / Top Seat Trades）：
   交易所每日盘后披露异常波动个股（日振幅 > 15%、日换手 > 20%、偏离度 > 7%）的前五大买卖营业部：
   - **机构专用席位（Institutional Seats）**：公募、险资、社保基金席位，持仓周期长，溢价具有中长期持续性；
   - **顶级知名游资席位（Hot Money）**：如“溧阳路”、“江苏路”、“金融大街”、“中关村”，擅长点火涨停板与隔夜超短线博弈；
   - **散户大本营（Retail Clusters / “拉萨天团”）**：如东方财富拉萨团结路、东环路营业部。由于东财 App 散户开户默认归属拉萨，
     拉萨席位霸榜买入往往意味着“主力机构成功派发、无数中小散户接盘”，是短期筹码崩塌的强烈警报。

【资金多维博弈打分架构】
```mermaid
flowchart TD
    RawData["多源资金输入: 北向净流入 + 两融杠杆比例 + 龙虎榜席位明细"] --> Processor["席位标签穿透与资金分类引擎"]
    Processor --> Inst["机构专用席位 ➔ 正向 Alpha 加分 [+]"]
    Processor --> HotMoney["顶级游资席位 ➔ 动量加分但扣减隔夜稳定性 [+/-]"]
    Processor --> Retail["拉萨散户席位 ➔ 筹码发散接盘逆向减分 [-]"]
    Processor --> NorthMargin["北向增量 + 两融杠杆适度偏离度评估"]
    Inst --> FinalScore["综合资金情绪打分 (0 ~ 100 分)"]
    HotMoney --> FinalScore
    Retail --> FinalScore
    NorthMargin --> FinalScore
    FinalScore --> SignalCheck{"Score 等级判定"}
    SignalCheck -->|Score > 75| StrongBull["强力主升 / 机构共振 (Strong_Bull)"]
    SignalCheck -->|Score < 45| Trap["主力出逃 / 散户接盘陷阱 (High_Risk_Distribution)"]
```

【思考题】
Q1: 为什么盲目跟风“龙虎榜知名游资席位”（如“作手新一”、“方新侠”）买入往往不仅赚不到钱，
    反而极易在次日开盘遭遇“核按钮”被深套？请从游资的持仓久期（T+1 极限周期）、抢跑博弈与流动性收割逻辑推导。
Q2: 什么是股票的“筹码集中度（Concentration Ratio）”与“筹码获利比例（Profit Ratio）”？
    当一只股票处于高位横盘、筹码集中度急剧下降且“拉萨散户席位”连续数日登上龙虎榜买一买二时，微观筹码结构发生了怎样的质变？
Q3: 为什么说单纯看“北向资金单日净买入额”是极具欺骗性的？在量化微观层面，怎样通过区分
    “托管在国际投行（外资长线）”与“托管在中资券商香港分行（离岸配资）”来剔除虚假北向信号？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现多维资金情绪综合打分基准模型 (1分)；
  2. 准确穿透解析龙虎榜席位属性（机构/游资/散户）并计算席位质量分 (1.5分)；
  3. 准确输出多维资金博弈综合评级与跟庄陷阱预警 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：深入阐释席位博弈因果链与微观收割陷阱；
- 通过线：8/10 分。一票否决：拉萨散户席位算作利好加分、打分溢出未截断、删除断言。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def score_capital_sentiment(north_inflow: float, margin_buy_ratio: float, inst_net_buy: float) -> float:
    """
    计算资金情绪多维综合评分 (0.0 ~ 100.0):
    - 基准分 50.0 分
    - north_inflow: 北向净买入 (亿元)，每 +1 亿元贡献 +0.3 分，每 -1 亿元扣减 0.3 分
    - margin_buy_ratio: 融资买入占成交额比例 (%)，基准为 8.0%，每偏离 +1% 贡献 +2.5 分，低出则扣分
    - inst_net_buy: 机构席位净买入 (亿元)，每 +1 亿元贡献 +0.5 分，每 -1 亿元扣减 0.5 分
    最终结果强制截断在 [0.0, 100.0] 区间。
    """
    # TODO: 实现资金情绪多维打分逻辑
    pass


def analyze_dragon_tiger_seats(
    buy_seats: List[Dict[str, float]],
    sell_seats: List[Dict[str, float]],
) -> Dict[str, float]:
    """
    解析龙虎榜前五买卖席位结构并量化博弈属性:
    席位数据格式: [{"name": "机构专用", "amount": 5000.0}, ...] (amount: 万元)

    席位识别规则:
    1. 机构席位 (Institutional): 席位名称包含 "机构专用"
    2. 散户拉萨席位 (Retail): 席位名称包含 "拉萨" 或 "团结路" 或 "东环路"
    3. 知名游资席位 (Hot Money): 席位名称包含 "溧阳路" 或 "江苏路" 或 "金融大街" 或 "益田路"

    席位质量综合分 (Seat Quality Score):
        净额 (万元) = 买入总额 - 卖出总额
        seat_quality_score = (inst_net * 1.0 + hot_money_net * 0.2 - retail_net * 1.5) / 1000.0

    返回字典:
        {
            "inst_net": 机构净买入额 (万元),
            "hot_money_net": 知名游资净买入额 (万元),
            "retail_net": 散户拉萨净买入额 (万元),
            "seat_quality_score": 席位质量纯度得分
        }
    """
    # TODO: 解析买卖席位并分类统计净买入额与席位质量得分
    pass


def evaluate_comprehensive_capital_flow(
    north_inflow: float,
    margin_ratio: float,
    seat_analysis: Dict[str, float],
) -> Dict[str, any]:
    """
    结合多源数据生成最终多维资金博弈综合报告:
    机构净买入换算为亿元: inst_net_yi = seat_analysis["inst_net"] / 10000.0
    基础资金得分 = score_capital_sentiment(north_inflow, margin_ratio, inst_net_yi)
    叠加席位质量修正分: final_score = clip(base_score + seat_analysis["seat_quality_score"] * 0.5, 0, 100)

    博弈状态等级划分:
    - final_score >= 75.0: "Strong_Bull" (机构共振强力主升)
    - 55.0 <= final_score < 75.0: "Moderate_Bull" (温和走强)
    - 45.0 <= final_score < 55.0: "Neutral" (中性博弈)
    - final_score < 45.0: "High_Risk_Distribution" (筹码发散/散户接盘高危)

    返回字典:
        {
            "final_score": float 最终综合得分,
            "regime": str 状态标签,
            "retail_trap_warning": bool (若 retail_net > 5000 万元且 inst_net < 0 则为 True)
        }
    """
    # TODO: 计算最终得分并判定博弈体制与散户接盘陷阱预警
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础资金情绪打分 ----------------
    score1 = score_capital_sentiment(50.0, 12.0, 20.0)  # 强烈做多
    score2 = score_capital_sentiment(-40.0, 4.0, -15.0)  # 极度悲观
    assert score1 > 70.0, f"Expected > 70.0, got {score1}"
    assert score2 < 40.0, f"Expected < 40.0, got {score2}"

    # 边界截断测试
    assert score_capital_sentiment(500.0, 50.0, 200.0) == 100.0
    assert score_capital_sentiment(-500.0, 0.0, -200.0) == 0.0

    # ---------------- 基础测试 2: 龙虎榜席位穿透分析 ----------------
    buys = [
        {"name": "机构专用", "amount": 8000.0},
        {"name": "中信证券股份有限公司上海溧阳路证券营业部", "amount": 6000.0},
        {"name": "东方财富证券股份有限公司拉萨团结路第二证券营业部", "amount": 2000.0},
    ]
    sells = [
        {"name": "机构专用", "amount": 1000.0},
        {"name": "国泰君安证券股份有限公司上海江苏路证券营业部", "amount": 2000.0},
        {"name": "东方财富证券股份有限公司拉萨东环路第一证券营业部", "amount": 5000.0},
    ]

    analysis = analyze_dragon_tiger_seats(buys, sells)
    assert analysis["inst_net"] == 7000.0  # 8000 - 1000
    assert analysis["hot_money_net"] == 4000.0  # 6000 - 2000
    assert analysis["retail_net"] == -3000.0  # 2000 - 5000
    assert analysis["seat_quality_score"] > 5.0, f"机构大买散户卖出，质量分应显著为正: {analysis['seat_quality_score']}"

    # ---------------- 基础测试 3: 综合资金流报告与陷阱预警 ----------------
    # 模拟散户接盘陷阱案例: 机构砸盘出逃，拉萨天团接盘
    trap_buys = [
        {"name": "东方财富证券股份有限公司拉萨团结路第一证券营业部", "amount": 8000.0},
        {"name": "东方财富证券股份有限公司拉萨东环路第二证券营业部", "amount": 7000.0},
    ]
    trap_sells = [
        {"name": "机构专用", "amount": 15000.0},
    ]
    trap_analysis = analyze_dragon_tiger_seats(trap_buys, trap_sells)
    report = evaluate_comprehensive_capital_flow(
        north_inflow=-30.0,
        margin_ratio=6.0,
        seat_analysis=trap_analysis,
    )
    assert report["final_score"] < 45.0, f"陷阱场景得分应低于 45, 实际为: {report['final_score']}"
    assert report["regime"] == "High_Risk_Distribution"
    assert report["retail_trap_warning"] is True, "应精准触发散户接盘陷阱预警 (retail_trap_warning)"

    print("Lesson 05 Exercise Passed!")
