"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 4/5 课
参考实现与标准问答解析
第 4 课：自由现金流折现 (DCF) 估值引擎与蒙特卡洛敏感性分析
================================================================================
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any


def two_stage_dcf_valuation(
    fcff_forecast: List[float],
    wacc: float,
    terminal_g: float,
    net_debt: float,
    shares_outstanding: float
) -> Dict[str, float]:
    """
    两阶段 DCF 估值引擎
    """
    if wacc <= terminal_g:
        raise ValueError("WACC 必须严格大于永续增长率 terminal_g")

    n = len(fcff_forecast)
    pv_forecast = 0.0
    for t, cf in enumerate(fcff_forecast, start=1):
        pv_forecast += cf / ((1.0 + wacc) ** t)

    last_cf = fcff_forecast[-1]
    terminal_val = (last_cf * (1.0 + terminal_g)) / (wacc - terminal_g)
    pv_terminal = terminal_val / ((1.0 + wacc) ** n)

    enterprise_value = pv_forecast + pv_terminal
    equity_value = enterprise_value - net_debt
    per_share_value = equity_value / shares_outstanding

    return {
        "pv_forecast": float(pv_forecast),
        "terminal_value": float(terminal_val),
        "pv_terminal": float(pv_terminal),
        "enterprise_value": float(enterprise_value),
        "equity_value": float(equity_value),
        "per_share_value": float(per_share_value)
    }


def dcf_sensitivity_matrix(
    fcff_forecast: List[float],
    wacc_list: List[float],
    g_list: List[float],
    net_debt: float,
    shares_outstanding: float
) -> pd.DataFrame:
    """
    构建 WACC 与 永续增长率 g 的二维每股内在价值敏感性矩阵
    """
    matrix_data = []
    for w in wacc_list:
        row = []
        for g in g_list:
            if w <= g:
                row.append(np.nan)
            else:
                res = two_stage_dcf_valuation(fcff_forecast, w, g, net_debt, shares_outstanding)
                row.append(res["per_share_value"])
        matrix_data.append(row)

    df = pd.DataFrame(matrix_data, index=wacc_list, columns=g_list)
    df.index.name = "WACC"
    df.columns.name = "Terminal_g"
    return df


def monte_carlo_dcf(
    fcff_forecast: List[float],
    base_wacc: float,
    wacc_std: float,
    base_g: float,
    g_std: float,
    net_debt: float,
    shares_outstanding: float,
    n_simulations: int = 1000,
    random_seed: int = 42
) -> Dict[str, float]:
    """
    基于蒙特卡洛模拟生成 DCF 每股内在价值置信分布
    """
    rng = np.random.RandomState(random_seed)
    wacc_samples = rng.normal(base_wacc, wacc_std, n_simulations)
    g_samples = rng.normal(base_g, g_std, n_simulations)

    per_share_list = []
    for w, g in zip(wacc_samples, g_samples):
        # 保证资本成本与永续增长利差至少 0.5%，防止分母奇异
        if w - g < 0.005:
            g = w - 0.005
        res = two_stage_dcf_valuation(fcff_forecast, w, g, net_debt, shares_outstanding)
        per_share_list.append(res["per_share_value"])

    arr = np.array(per_share_list)
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "p5": float(np.percentile(arr, 5)),
        "p95": float(np.percentile(arr, 95)),
        "std": float(np.std(arr))
    }


if __name__ == "__main__":
    print("=" * 60)
    print("运行 Lesson 04 参考实现与测试")
    print("=" * 60)

    forecast = [100.0, 115.0, 130.0, 145.0, 160.0]
    wacc_val = 0.09
    g_val = 0.025
    net_debt_val = 200.0
    shares_val = 10.0

    dcf_res = two_stage_dcf_valuation(forecast, wacc_val, g_val, net_debt_val, shares_val)
    print("两阶段 DCF 估值结果:", dcf_res)

    assert abs(dcf_res["pv_forecast"] - 495.62) < 1.0
    assert abs(dcf_res["terminal_value"] - 2523.08) < 1.0
    assert abs(dcf_res["pv_terminal"] - 1639.81) < 1.0
    assert abs(dcf_res["enterprise_value"] - 2135.43) < 1.5
    assert abs(dcf_res["equity_value"] - 1935.43) < 1.5
    assert abs(dcf_res["per_share_value"] - 193.54) < 0.2

    wacc_grid = [0.08, 0.09, 0.10]
    g_grid = [0.02, 0.025, 0.03]
    matrix = dcf_sensitivity_matrix(forecast, wacc_grid, g_grid, net_debt_val, shares_val)
    print("敏感性矩阵 (每股价值):\n", matrix)

    assert matrix.loc[0.08, 0.03] > matrix.loc[0.09, 0.025] > matrix.loc[0.10, 0.02]

    mc_res = monte_carlo_dcf(
        forecast, base_wacc=0.09, wacc_std=0.005,
        base_g=0.025, g_std=0.003,
        net_debt=net_debt_val, shares_outstanding=shares_val,
        n_simulations=1000, random_seed=42
    )
    print("蒙特卡洛估值区间:", mc_res)

    assert mc_res["p5"] < mc_res["median"] < mc_res["p95"]
    assert abs(mc_res["median"] - dcf_res["per_share_value"]) < 15.0

    print("Lesson 04 参考答案全部断言通过！\n")

    print("=" * 60)
    print("【思考题标准答案与评分基准】")
    print("=" * 60)
    print("""
Q1 标准解析（得分要点：终值高占比带来的杠杆敏感性、输入参数的主观调节与防范机制）：
1. 终值杠杆放大效应：
   在常规两阶段 DCF 模型中，终值现值（PV of Terminal Value）通常占据企业总价值 EV 的 65% ~ 80% 以上！
   由于终值公式 TV = FCFF_N * (1+g) / (WACC - g)，分母是利差 (WACC - g)。
   若原 WACC 为 9%，g 为 2.5%，分母为 6.5%；若 WACC 下调 1% 至 8%，分母缩小至 5.5%，直接导致终值激增 18.2%！加上贴现因子变大，每股内在价值涨幅可达 25%~35%。
2. 防范“倒推输入”的造假：
   - 严禁分析师为匹配现价反向调试 WACC 或 g；
   - 设定终值增长率上限：g 绝不能超过长期宏观真实 GDP 潜在增速（一般 2%~3%）；
   - 使用退出乘数法（Exit Multiple，如预测期末 EV/EBITDA）进行双重锚定交叉验证；
   - 采用敏感性矩阵与蒙特卡洛分布（输出 10%~90% 置信区间）取代单一静态点估计。

Q2 标准解析（得分要点：金融机构资本结构与经营模式的特殊性、债务对银行业的特殊意义）：
1. 为什么不能用 FCFF 估值金融机构（银行/券商）：
   - 在非金融实体企业中，债务是“外生融资工具”，EBIT 是不含债务成本的经营成果；
   - 但在商业银行和券商中，“负债（存款、拆借）是核心经营原材料”！利息支出是直接营业成本，无法清晰剥离经营活动与筹资活动；
   - 银行的营运资本（NWC）与固定资产 CapEx 极少，资本开支主要是监管资本金（核心一级资本充足率要求）。因此 FCFF = EBIT(1-t) + D&A - CapEx - ΔNWC 彻底失效。
2. 适用模型：
   必须使用股权自由现金流（FCFE = 净利润 - 满足监管资本充足率所需留存资本）或股利折现模型（DDM），折现率使用股权资本成本 Ke。

Q3 标准解析（得分要点：反向 DCF 的工程实现与估值预期差度量）：
1. 反向 DCF（Reverse DCF）原理：
   正向 DCF 是“输入预测假设 -> 计算合理股价”；而反向 DCF 则是“以当前市场真实股价为 EV 输入 -> 反解模型参数（隐含复合增长率 CAGR、稳态 FCF 利润率）”。
2. 实战应用（以高估值科技股为例）：
   - 将当前市值代入两阶段 DCF 方程；
   - 固定合理的 WACC（如 9%）与永续 g（如 3%）；
   - 反求未来 5~10 年企业需要维持多少的营收年化复合增速（如 45% CAGR）以及多高的稳态 FCF Margin（如 35%）；
   - 分析师将该隐含指标与潜在全市场空间（TAM，Total Addressable Market）对比。若反推结果要求该公司 5 年后占据全球 120% 的市场份额，则表明当前股价已彻底脱离地心引力，泡沫极度显著，反之若反推隐含增速远低于行业真实景气度，则存在巨大预期差买点。
""")
