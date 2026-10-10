r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 5/5 课
第 5 课：资金流向、两融杠杆与龙虎榜席位多维博弈打分模型 (参考答案版)
================================================================================

【Q1 深度参考答案】
为什么盲目跟风“龙虎榜知名游资席位”（如“作手新一”、“方新侠”）买入往往不仅赚不到钱，
反而极易在次日开盘遭遇“核按钮”被深套？请从游资的持仓久期（T+1 极限周期）、抢跑博弈与流动性收割逻辑推导：
- **微观流动性收割与非对称持仓久期**：
  1. **极端持仓周期（T+1 超短博弈）**：顶级游资的核心盈利模式是“打造市场情绪标杆、次日享受确定性溢价并兑现离场”。
     其买入当天的唯一目标是“用大单封死涨停板”，制造全市场稀缺感；
     其持仓周期极其短暂（通常只有 1 天），次日开盘的第一诉求就是寻找对手盘出逃，根本不具备中长期持股意图。
  2. **信息时间差与“明牌接盘”**：交易所龙虎榜公布时间是每个交易日下午 16:30 至 17:30，
     此时当日交易早已彻底结束。散户在晚上看到龙虎榜“知名游资大买 1 亿元”时，
     游资的筹码在次日 9:30 已经全部变成了具有随时卖出权限的 T+0 可卖状态，而散户在次日开盘买入却必须承受 T+1 锁仓限制。
  3. **核按钮抢跑出货（Liquidity Extraction）**：次日开盘，一旦集合竞价未能大幅高开（缺乏接盘意愿），
     游资为了保全利润或止损，会毫不犹豫利用集合竞价直接挂跌停价甚至市价单疯狂砸盘（核按钮）。
     被龙虎榜吸引进场的跟风散户恰好充当了游资出逃的流动性接盘侠，买入瞬间直接被套，全天动弹不得。

【Q2 深度参考答案】
什么是股票的“筹码集中度（Concentration Ratio）”与“筹码获利比例（Profit Ratio）”？
当一只股票处于高位横盘、筹码集中度急剧下降且“拉萨散户席位”连续数日登上龙虎榜买一买二时，微观筹码结构发生了怎样的质变？
- **筹码分布演化与筹码发散警报**：
  1. **微观筹码定义**：
     - **筹码集中度**：度量全市场持股成本的离散程度（如 90% 筹码集中度 = (Cost_95 - Cost_05) / (Cost_95 + Cost_05)）。
       集中度数值越小，代表筹码越集中在极窄的价格区间（主力控盘度高）；数值越大，代表筹码分布极度发散；
     - **筹码获利比例**：当前收盘价位于所有历史持仓成本之上的筹码比例。
  2. **高位拉萨霸榜的微观质变（Distribution Phase）**：
     - 在股票连续拉升数倍后的高位震荡区间，如果筹码集中度快速发散、振幅加剧；
     - 东方财富“拉萨天团”（拉萨团结路/东环路）由于集中了全国数以百万计的散户移动端账户，
       当拉萨席位连续霸占龙虎榜买一、买二且净买入数亿元，而卖方频现“机构专用”或顶级游资时；
     - 这一结构性异变确凿证明：**底层微观筹码已经从少数高风险偏好、高定价权的主力大资金手中，
       不可逆地碎屑化分散到了成千上万个毫无协同能力的短线散户手中**。
       由于散户缺乏统一锁仓意志，一旦次日稍有风吹草动便会引发群体性踩踏，是股票即将见顶雪崩的最高级别危险信号。

【Q3 深度参考答案】
为什么说单纯看“北向资金单日净买入额”是极具欺骗性的？在量化微观层面，怎样通过区分
“托管在国际投行（外资长线）”与“托管在中资券商香港分行（离岸配资）”来剔除虚假北向信号？
- **穿透式席位分拆与假外资剥离**：
  1. **北向资金总额的“杂质污染”**：港交所披露的北向资金总净买入数据，将全球主权基金、国际对冲基金、
     高频做市商以及披着离岸外衣的境内游资配资混同统计。
     在题材炒作狂热期，单日北向净买入可能高达 50 亿元，但其中 40 亿元可能来自于境内配资团队在香港开设的杠杆账户回流，
     并非真实的国际长线外资增配。
  2. **香港中央结算系统（CCASS）托管行穿透工程**：
     - **国际长线机构（True Smart Money）**：持仓主要托管在传统外资托管行，如香港上海汇丰银行（HSBC）、
       渣打银行（Standard Chartered）、花旗银行（Citibank）、摩根大通（JPMorgan Chase）。
       这些席位的资金流动体现出极高的低换手率与基本面配置导向；
     - **对冲与高频量化席位**：主要托管在高盛（Goldman Sachs）、摩根士丹利（Morgan Stanley）、瑞银（UBS）；
     - **假外资与离岸配资**：主要托管在中资券商香港子公司，如国泰君安国际、中信证券国际、海通国际等。
  3. **量化纯净因子构建**：通过港交所每日披露的 CCASS 托管行持股变动数据，构建外资纯度差分因子：
     $$\text{Pure\_Northbound} = \Delta \text{Holding}_{\text{Tier1\_Custodians}} - \Delta \text{Holding}_{\text{Chinese\_HK\_Brokers}}$$
     过滤掉游资借道的假外资噪音，方能提炼出对 A 股核心资产具备真实定价指导力的长线 Alpha。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def score_capital_sentiment(north_inflow: float, margin_buy_ratio: float, inst_net_buy: float) -> float:
    """
    计算资金情绪多维综合评分 (0.0 ~ 100.0)
    """
    score = 50.0
    score += north_inflow * 0.3
    score += (margin_buy_ratio - 8.0) * 2.5
    score += inst_net_buy * 0.5
    return float(np.clip(score, 0.0, 100.0))


def analyze_dragon_tiger_seats(
    buy_seats: List[Dict[str, float]],
    sell_seats: List[Dict[str, float]],
) -> Dict[str, float]:
    """
    解析龙虎榜前五买卖席位结构并量化博弈属性
    """
    inst_buy = sum(s["amount"] for s in buy_seats if "机构专用" in s["name"])
    inst_sell = sum(s["amount"] for s in sell_seats if "机构专用" in s["name"])
    inst_net = inst_buy - inst_sell

    hot_keywords = ["溧阳路", "江苏路", "金融大街", "益田路"]
    hot_buy = sum(s["amount"] for s in buy_seats if any(k in s["name"] for k in hot_keywords))
    hot_sell = sum(s["amount"] for s in sell_seats if any(k in s["name"] for k in hot_keywords))
    hot_net = hot_buy - hot_sell

    retail_keywords = ["拉萨", "团结路", "东环路"]
    ret_buy = sum(s["amount"] for s in buy_seats if any(k in s["name"] for k in retail_keywords))
    ret_sell = sum(s["amount"] for s in sell_seats if any(k in s["name"] for k in retail_keywords))
    retail_net = ret_buy - ret_sell

    seat_quality = (inst_net * 1.0 + hot_net * 0.2 - retail_net * 1.5) / 1000.0

    return {
        "inst_net": float(inst_net),
        "hot_money_net": float(hot_net),
        "retail_net": float(retail_net),
        "seat_quality_score": float(seat_quality),
    }


def evaluate_comprehensive_capital_flow(
    north_inflow: float,
    margin_ratio: float,
    seat_analysis: Dict[str, float],
) -> Dict[str, any]:
    """
    结合多源数据生成最终多维资金博弈综合报告
    """
    inst_net_yi = seat_analysis["inst_net"] / 10000.0
    base_score = score_capital_sentiment(north_inflow, margin_ratio, inst_net_yi)
    final_score = float(np.clip(base_score + seat_analysis["seat_quality_score"] * 0.5, 0.0, 100.0))

    if final_score >= 75.0:
        regime = "Strong_Bull"
    elif final_score >= 55.0:
        regime = "Moderate_Bull"
    elif final_score >= 45.0:
        regime = "Neutral"
    else:
        regime = "High_Risk_Distribution"

    retail_trap = bool(seat_analysis["retail_net"] > 5000.0 and seat_analysis["inst_net"] < 0.0)

    return {
        "final_score": float(final_score),
        "regime": regime,
        "retail_trap_warning": retail_trap,
    }


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础资金情绪打分 ----------------
    score1 = score_capital_sentiment(50.0, 12.0, 20.0)
    score2 = score_capital_sentiment(-40.0, 4.0, -15.0)
    assert score1 > 70.0, f"Expected > 70.0, got {score1}"
    assert score2 < 40.0, f"Expected < 40.0, got {score2}"

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
    assert analysis["inst_net"] == 7000.0
    assert analysis["hot_money_net"] == 4000.0
    assert analysis["retail_net"] == -3000.0
    assert analysis["seat_quality_score"] > 5.0, f"机构大买散户卖出，质量分应显著为正: {analysis['seat_quality_score']}"

    # ---------------- 基础测试 3: 综合资金流报告与陷阱预警 ----------------
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

    print("Lesson 05 Answer Verified!")
