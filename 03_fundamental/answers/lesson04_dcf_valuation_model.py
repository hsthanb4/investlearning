r"""
================================================================================
模块 03：财务报表深度分析与估值建模 · 第 4/5 课
第 4 课：自由现金流折现 (DCF) 估值引擎与蒙特卡洛敏感性分析 (参考答案版)
================================================================================

【Q1 投决会深度解析】
为什么华尔街常说“DCF 是理论上最完美、实践中最容易被操纵的估值模型”？贴现率 WACC 变动 1% 对终值（Terminal Value）会产生多大程度的放大效应？分析师该如何防范“为了迎合市价而倒推输入参数”的估值造假？
- **[终值敏感性放大效应与估值防御准则]**：
  - **[1. 终值分母的非线性凸性]**：戈登增长模型的终值为 $\text{TV} = \frac{\text{FCFF}_{N+1}}{\text{WACC} - g}$。分母是一个极小的数值（例如 $9.0\% - 2.5\% = 6.5\%$）。若分析师主观将 WACC 从 9.0% 微调至 8.0%，分母直接收窄至 $8.0\% - 2.5\% = 5.5\%$，终值将被动暴增：
    $$\frac{6.5\% - 5.5\%}{5.5\%} \approx +18.2\%$$
    由于终值现值占整体企业价值（EV）的 70% 以上，贴现率变动 1% 将引起最终每股内在价值 20%~30% 的巨幅摆动。
  - **[2. 倒推参数的操纵心理]**：卖方分析师为了给予买入评级或配合承销项目，往往先看当前股票市价（如 100 元），然后倒推调高长期营收增速、压低资本开支、调低贝塔值以降低 WACC，炮制出“目标价 130 元”的伪 DCF 报告。
  - **[3. 买方投决会防范准则]**：
    - 绝不允许使用单一确定性点位估值，必须输出 **WACC-g 双变量敏感性网格矩阵**；
    - 执行 10,000 次蒙特卡洛模拟，输出概率密度分布带，以 5% 分位数的悲观现值作为下行安全边际（Margin of Safety）。

【Q2 投决会深度解析】
区分 FCFF 与 FCFE 的适用边界。对于高杠杆金融机构（如商业银行、证券公司），为什么无法使用常规 FCFF 模型，而必须采用股利折现模型（DDM）或超额收益模型？
- **[资本结构与金融机构资产负债表特质]**：
  - **[1. 非金融企业 vs 金融机构的负债本质]**：对于制造业或科技公司，有息债务（借款、债券）属于外生融资资本结构选择，与日常经营商品生产严格分离。因此可以计算剔除利息影响的 FCFF，并使用 WACC 贴现。
  - **[2. 商业银行的负债就是其“原材料”]**：商业银行的客户存款与同业拆借虽然在会计上属于负债，但实质上是银行借以发放贷款、购买债券的“经营性原材料”。对银行而言，无法清晰分离什么是“经营活动现金流”、什么是“融资活动债务”，营运资本变动（ΔNWC）在金融资产规模膨胀时失去实体物理意义，常规 FCFF 计算公式完全失效。
  - **[3. 监管资本约束下的折现模型]**：商业银行的扩张受巴塞尔协议与央行核心一级资本充足率（CAR）的刚性约束。只有扣除维持法定资本充足率所需留存后的多余现金，才能作为真实股利分配给股东。因此金融机构的黄金估值模型是**股利折现模型（DDM）**或**剩余收益模型（Residual Income Model）**，折现率直接使用股权资本成本 $K_e$。

【Q3 投决会深度解析】
什么是“反向 DCF”（Reverse DCF）？在对高估值成长股（如英伟达 Nvidia、特斯拉 Tesla）进行投研时，如何通过当前市价反推市场隐含的长期营收增速与自由现金流转化率？
- **[反向逆推逻辑与成长幻觉检验]**：
  - **[1. 反向 DCF 的核心哲学]**：不主动主观预测公司未来能赚多少钱，而是将当前市场上狂热的“实际交易市值”作为已知输入，假定合理的 WACC（如 9%）与永续增长率（如 2.5%），通过优化算法逆向求解：**为了支撑当前的高市值，公司在未来 10 年必须实现怎样惊人的营收复合增速（CAGR）与自由现金流净利率（FCF Margin）？**
  - **[2. 现实锚定与常识检验]**：以某千亿美元市值的 AI 芯片巨头为例，若当前股价隐含其未来 10 年营收必须保持年化 45% 的复利增长，且 10 年后其年自由现金流将超越全美所有科技巨头自由现金流之和，或者其隐含的市场规模（TAM）将超过全球半导体总产值的 80%，分析师即可凭借商业常识确证该资产已进入严重泡沫化与过度透支阶段。
  - **[3. 投决会决策应用]**：反向 DCF 将抽象的玄学多空争论，转化为极其具体的“市场隐含成长假设是否具备现实可行性”的实证概率问题，是防范高位追高被套的终极定量滤网。
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
