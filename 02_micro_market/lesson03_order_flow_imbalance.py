r"""
================================================================================
模块 02：市场微观结构与订单簿动力学 · 第 3/5 课
第 3 课：订单流不平衡 (Order Flow Imbalance, OFI) 与高频价格预测
================================================================================

【课程定位与第一性原理】
在量化高频交易与微观结构计量学中，Cont, Kukanov and Stoikov (2014) 提出的
订单流不平衡指标（Order Flow Imbalance, OFI）被公认为预测短期盘口价格跳跃的最强领先因子。

传统分析依赖“已成交量（Trade Volume）”，但成交量本质上是滞后发生的事实；
而盘口静态挂单量（Static Depth）又充斥着大量虚假撤单与远端无意义挂单。
OFI 的核心第一性原理在于：
“价格的变动是由连续两个微观快照时刻之间，买卖双方盘口最优档位所发生的
净挂单增加、吃单成交与撤单流所产生的净驱动力（Net Flux）决定的。”

【数学推导：Cont-Kukanov-Stoikov (2014) OFI 模型】
考虑连续两个快照时刻 t-1 到 t，最优买价/买量分别为 (P^b_{t-1}, q^b_{t-1}) 与 (P^b_t, q^b_t)；
最优卖价/卖量分别为 (P^a_{t-1}, q^a_{t-1}) 与 (P^a_t, q^a_t)。

1. 买方订单流驱动项 (I^b_t)：
   - 若 P^b_t > P^b_{t-1}：买一价向上跳升，意味着激进限价买单建立新价格档位，驱动力为新档位全部挂单量：
     I^b_t = q^b_t
   - 若 P^b_t == P^b_{t-1}：买一价未变，挂单量变动由新挂单（增加）与撤单/被动成交（减少）主导：
     I^b_t = q^b_t - q^b_{t-1}
   - 若 P^b_t < P^b_{t-1}：买一价向下破位，原买一档挂单被市价卖单全部吃穿或全部撤单：
     I^b_t = -q^b_{t-1}

2. 卖方订单流驱动项 (I^a_t)（对称推导）：
   - 若 P^a_t < P^a_{t-1}：卖一价向下跳跌（激进卖单下压）：
     I^a_t = q^a_t
   - 若 P^a_t == P^a_{t-1}：卖一价未变：
     I^a_t = q^a_t - q^a_{t-1}
   - 若 P^a_t > P^a_{t-1}：卖一价向上抬升（原卖一档被市价买单全部吃空）：
     I^a_t = -q^a_{t-1}

3. 单步 L1 订单流不平衡定义：
   OFI_t = I^b_t - I^a_t

4. 中间价冲击与 Kyle's Lambda 线性关系：
   实证表明，短期中间价变化与 OFI 存在极强的线性关系：
       \Delta P^{\text{mid}}_t = P^{\text{mid}}_t - P^{\text{mid}}_{t-1} = \beta \cdot OFI_t + \epsilon_t
   其中 \beta > 0 为盘口价格冲击弹性系数（Kyle's Lambda 的微观度量）。

【微观订单流控制图解】
```mermaid
flowchart TD
    SnapshotPrev["盘口快照 t-1: (P_prev^b, q_prev^b), (P_prev^a, q_prev^a)"] --> Event["微观订单簿事件: 挂单 / 吃单 / 撤单"]
    Event --> SnapshotCurr["盘口快照 t: (P_curr^b, q_curr^b), (P_curr^a, q_curr^a)"]
    SnapshotCurr --> CalcIb["计算买方驱动项 I^b_t (价格上跳 / 维持 / 破位)"]
    SnapshotCurr --> CalcIa["计算卖方驱动项 I^a_t (价格下跳 / 维持 / 上抬)"]
    CalcIb --> CalcOFI["OFI_t = I^b_t - I^a_t"]
    CalcIa --> CalcOFI
    CalcOFI --> Impact["线性冲击拟合: \Delta Mid_Price = \beta * OFI_t + \epsilon"]
```

【思考题】
Q1: 为什么 OFI 相比于单纯的“主动买入成交量减主动卖出成交量”（净主动买入额 Net Taker Volume），
    能够提供信噪比更高、更纯净的短期价格预测能力？
    请从做市商被动撤单与盘口新挂单事件的信息含量角度推导。
Q2: 为什么在实盘高频量化交易中，单步 OFI 对价格变化的解释力在毫秒至秒级极强（R^2 常常达到 50%~70%），
    但随着预测时间窗口拉长（如 5分钟、15分钟），其预测能力呈现指数级衰减？做市商如何利用 OFI 衰减半衰期设定库存管理风控？
Q3: 在跨多档盘口（Level 1 至 Level 10）拓展 Multi-Level OFI 时，为什么越深的档位（如买五、买十）
    需要赋予越大的权重衰减（如指数衰减 exp(-alpha * k)）？深档挂单中存在大量“虚假挂单（Ghost Orders / Spoofing）”
    会对未加权的多档 OFI 造成怎样的污染？

【评分与通过规则】
- 代码 4 分：
  1. 准确实现单步 L1 OFI 驱动项分支判定 (1分)；
  2. 准确批量计算高频分笔 Tick 序列 OFI 并拓展多档加权 OFI (1.5分)；
  3. 准确实现 OFI 与中间价变动的价格冲击回归估计与 R^2 评估 (1.5分)；
- Q1~Q3 问答题各 2 分（共 6 分）：必须深入说明微观订单流信息含量与半衰期因果链；
- 通过线：8/10 分。一票否决：买卖驱动项逻辑反转、OFI 符号倒置、删除断言。
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


def calculate_ofi(
    b_price_prev: float,
    b_size_prev: int,
    b_price_curr: float,
    b_size_curr: int,
    a_price_prev: float,
    a_size_prev: int,
    a_price_curr: float,
    a_size_curr: int,
) -> float:
    """
    计算单个 Tick 步长的 Level 1 订单流不平衡 (OFI):
        OFI = I_Bid - I_Ask
    """
    # TODO: 实现 Cont-Kukanov-Stoikov (2014) 单步 OFI 计算逻辑
    pass


def calculate_tick_ofi_series(tick_df: pd.DataFrame) -> pd.Series:
    """
    从连续的 Tick 快照数据集中批量计算单步 OFI 序列:
    输入 tick_df 必须包含列: ['b_price', 'b_size', 'a_price', 'a_size']
    第 0 个时刻因为没有前值，OFI 记为 0.0。
    """
    # TODO: 滚动遍历计算整个时序的 OFI 序列
    pass


def calculate_multi_level_ofi(
    b_prices_prev: List[float],
    b_sizes_prev: List[int],
    b_prices_curr: List[float],
    b_sizes_curr: List[int],
    a_prices_prev: List[float],
    a_sizes_prev: List[int],
    a_prices_curr: List[float],
    a_sizes_curr: List[int],
    decay: float = 0.5,
) -> float:
    """
    计算跨多档深度 (Multi-Level) 加权订单流不平衡:
    对于档位 k = 0, 1, ..., K-1:
        权重 w_k = exp(-decay * k)
        OFI_k = calculate_ofi(...)
        Multi_OFI = sum(w_k * OFI_k)
    """
    # TODO: 对各档位按指数衰减加权求和
    pass


def estimate_ofi_price_impact(ofi_series: pd.Series, mid_price_series: pd.Series) -> Dict[str, float]:
    """
    估计 OFI 对中间价变化的一阶价格冲击系数与预测拟合度:
        d_mid_t = mid_price_series_t - mid_price_series_{t-1}
        拟合线性模型: d_mid = beta * ofi + epsilon
    返回:
        {
            "correlation": Pearson 相关系数,
            "beta": 价格冲击弹性系数 (OLS 斜率),
            "r_squared": 拟合优度 R^2
        }
    """
    # TODO: 计算差分对齐后的一阶回归斜率、相关系数与 R^2
    pass


if __name__ == "__main__":
    # ---------------- 基础测试 1: 基础单步 OFI 计算 ----------------
    # 场景: 买一价提升 (10.0 -> 10.1, size 100), 卖一价不变 (10.2 -> 10.2, size 50 -> 40)
    # I_bid = 100, I_ask = 40 - 50 = -10, OFI = 100 - (-10) = 110.0
    ofi = calculate_ofi(10.0, 80, 10.1, 100, 10.2, 50, 10.2, 40)
    assert abs(ofi - 110.0) < 1e-4, f"Expected 110.0, got {ofi}"

    # 场景 2: 买一价下跌 (10.1 -> 10.0, 原挂单被吃), 卖一价下跌 (10.2 -> 10.15, 卖方压盘)
    # I_bid = -100, I_ask = 60, OFI = -100 - 60 = -160.0
    ofi2 = calculate_ofi(10.1, 100, 10.0, 70, 10.2, 50, 10.15, 60)
    assert abs(ofi2 - (-160.0)) < 1e-4, f"Expected -160.0, got {ofi2}"

    # ---------------- 基础测试 2: 多档 Multi-Level OFI ----------------
    # 2 档盘口示例
    bp_prev = [10.0, 9.9]
    bs_prev = [100, 200]
    bp_curr = [10.0, 9.9]
    bs_curr = [150, 200]  # L1 买量增加 50, L2 买量未变

    ap_prev = [10.1, 10.2]
    as_prev = [80, 150]
    ap_curr = [10.1, 10.2]
    as_curr = [60, 150]  # L1 卖量减少 20 (被吃20)

    # L1: I_bid = 50, I_ask = -20, OFI_1 = 70.0, 权重 exp(0) = 1.0
    # L2: I_bid = 0, I_ask = 0, OFI_2 = 0.0
    multi_ofi = calculate_multi_level_ofi(
        bp_prev, bs_prev, bp_curr, bs_curr,
        ap_prev, as_prev, ap_curr, as_curr,
        decay=0.5,
    )
    assert abs(multi_ofi - 70.0) < 1e-4, f"Expected 70.0, got {multi_ofi}"

    # ---------------- 基础测试 3: OFI 时序与价格冲击回归 ----------------
    np.random.seed(42)
    n_ticks = 100
    # 生成合成盘口数据: OFI 净买入正向驱动中间价上涨
    synth_ofi = np.random.normal(0.0, 50.0, n_ticks)
    synth_d_mid = 0.002 * synth_ofi + np.random.normal(0.0, 0.02, n_ticks)
    synth_mid = 100.0 + np.cumsum(synth_d_mid)

    s_ofi = pd.Series(synth_ofi)
    s_mid = pd.Series(synth_mid)

    impact = estimate_ofi_price_impact(s_ofi, s_mid)
    assert impact["correlation"] > 0.85, f"OFI 与价格变化应高度正相关, 实际: {impact['correlation']}"
    assert 0.0015 <= impact["beta"] <= 0.0025, f"Beta 冲击系数应接近 0.002, 实际: {impact['beta']}"
    assert impact["r_squared"] > 0.70, f"R^2 应高于 0.70, 实际: {impact['r_squared']}"

    print("Lesson 03 Exercise Passed!")
