#!/usr/bin/env python3
"""
InvestLearning Institutional Upgrader
Upgrades docstrings, theory, SVGs, and web data for Modules 01, 02, and 03.
"""

import os
import sys
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from generate_curriculum_svgs import SVGS
from curriculum_content_m01 import M01_LESSONS
from curriculum_content_m02 import M02_LESSONS
from curriculum_content_m03 import M03_LESSONS


def replace_top_docstring(file_path: str, new_docstring: str):
    """Safely replace the top module-level docstring in a python file while keeping code intact."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    trimmed = content.lstrip()
    if trimmed.startswith('r"""'):
        parts = trimmed.split('"""', 2)
        code_part = parts[2].lstrip()
    elif trimmed.startswith('"""'):
        parts = trimmed.split('"""', 2)
        code_part = parts[2].lstrip()
    else:
        raise ValueError(f"File {file_path} does not start with triple quote docstring!")

    clean_doc = new_docstring.strip()
    if clean_doc.startswith('r"""'):
        clean_doc = clean_doc[4:]
    elif clean_doc.startswith('"""'):
        clean_doc = clean_doc[3:]
    if clean_doc.endswith('"""'):
        clean_doc = clean_doc[:-3]

    new_content = f'r"""\n{clean_doc.strip()}\n"""\n\n{code_part}'
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def upgrade_python_files():
    print("=" * 60)
    print("1. Updating Python files and answers docstrings for Modules 01, 02, 03")
    print("=" * 60)

    modules_data = [
        ("01_macro_cycle", M01_LESSONS),
        ("02_micro_market", M02_LESSONS),
        ("03_fundamental", M03_LESSONS),
    ]

    for mod_dir, lessons in modules_data:
        print(f"\nProcessing module: {mod_dir}")
        for l in lessons:
            f_name = l["file_name"]
            main_path = os.path.join(BASE_DIR, mod_dir, f_name)
            ans_path = os.path.join(BASE_DIR, mod_dir, "answers", f_name)

            if os.path.exists(main_path):
                replace_top_docstring(main_path, l["docstring_exercise"])
                print(f"  [Exercise] Updated: {f_name}")
            else:
                print(f"  [WARN] Not found: {main_path}")

            if os.path.exists(ans_path):
                replace_top_docstring(ans_path, l["docstring_answers"])
                print(f"  [Answer]   Updated: answers/{f_name}")
            else:
                print(f"  [WARN] Not found: {ans_path}")


def extract_code_body(py_path: str) -> str:
    with open(py_path, "r", encoding="utf-8") as f:
        content = f.read()
    trimmed = content.lstrip()
    if trimmed.startswith('r"""') or trimmed.startswith('"""'):
        parts = trimmed.split('"""', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()


def build_web_lesson_theory(lesson_id, title, math_formula, svg_key_1, svg_key_2, breakdown_1, breakdown_2, note_text, warning_text):
    svg_1 = SVGS.get(svg_key_1, f"<!-- Missing SVG {svg_key_1} -->")
    svg_2 = SVGS.get(svg_key_2, f"<!-- Missing SVG {svg_key_2} -->")

    html = f"""
<div class="callout callout-note">
  <div class="callout-title">📌 投决会核心心智模型：{title}</div>
  <div class="callout-body">
    <ul class="label-list">
      {note_text}
    </ul>
  </div>
</div>

<div class="math-block">
  {math_formula}
</div>

<p><strong>[架构引导 1]</strong>：如下拓扑图解所示，系统性剖析该机制的核心流转物理路径：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">{title} · 核心机制拓扑</span>
    <span class="diagram-tag">{lesson_id.upper()}-01</span>
  </div>
  <div class="diagram-svg-container">
    {svg_1}
  </div>
</div>

<ul class="label-list">
  {breakdown_1}
</ul>

<p><strong>[决策流引导 2]</strong>：如下状态机与微观动力学图谱所示，量化评估各关键参数对风险溢价与资产回报率的动态冲击：</p>

<div class="diagram-card">
  <div class="diagram-header">
    <span class="diagram-title">{title} · 微观状态与决策矩阵</span>
    <span class="diagram-tag">{lesson_id.upper()}-02</span>
  </div>
  <div class="diagram-svg-container">
    {svg_2}
  </div>
</div>

<ul class="label-list">
  {breakdown_2}
</ul>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ 投决会风控红线与认知陷阱</div>
  <div class="callout-body">
    <ul class="label-list">
      {warning_text}
    </ul>
  </div>
</div>
"""
    return html.strip()


def generate_web_curriculum_data():
    print("=" * 60)
    print("2. Generating comprehensive Web Curriculum Database")
    print("=" * 60)

    # Lesson specific visual mappings & theories
    configs = {
        # Module 01
        "m01_l01": {
            "math": r"$$\text{Net Liquidity}_t = \text{Fed Total Assets}_t - (\text{TGA}_t + \text{ON RRP}_t)$$",
            "svg1": "m01_l01_net_liquidity_flow",
            "svg2": "m01_l01_pboc_liquidity_corridor",
            "b1": """<li><strong>[1. 资产端扩缩惯性]</strong>：美联储扩表购债（QE）直接向一级交易商注入准备金存款；缩表（QT）按月度上限销毁基础货币。</li>
<li><strong>[2. TGA 财政抽水池]**：税期与集中发债期，民间资金流入 TGA 锁死，导致商业银行准备金被动刚性缩水。</li>
<li><strong>[3. ON RRP 蓄水池缓冲]**：当美债短端收益率具备吸引力时，货基从美联储逆回购撤出资金买入短债，中和准备金流失。</li>""",
            "b2": """<li><strong>[1. 政策利率锚]</strong>：PBOC 7天期 OMO 逆回购利率为短端基准政策利率锚。</li>
<li><strong>[2. 真实资金温度计]</strong>：DR007 存款类金融机构质押式回购利率穿透信用溢价，反映银行体系真实水位。</li>
<li><strong>[3. 非银信用剪刀差]</strong>：R007 - DR007 利差走阔表明非银流动性干涸，A 股两融与机构杠杆面临抛售踩踏。</li>""",
            "note": """<li><strong>[商业金融本质]</strong>：在法币信贷货币体系下，货币是央行与商业银行的资产负债表负债凭证。</li>
<li><strong>[定价第一性原理]</strong>：风险资产估值中枢由无风险利率与风险溢价决定，银行准备金决定了金融中介的杠杆承载容量。</li>
<li><strong>[准备金守恒定律]</strong>：央行资产端严格恒等于负债端准备金、TGA、ON RRP 与流通现金之和。</li>""",
            "warn": """<li><strong>[统计幻觉陷阱]</strong>：严禁将央行名义扩缩表等同于市场实际流动性，若忽视发债导致的 TGA 暴增将发生严重误判。</li>
<li><strong>[跨期时滞陷阱]</strong>：净流动性向股票估值传导具有 4~8 周时滞，不可直接做日频高噪动量交易。</li>"""
        },
        "m01_l02": {
            "math": r"$$\text{Spread}_{10Y-2Y}(t) = y(10, t) - y(2, t) \quad [\text{bps}]$$",
            "svg1": "m01_l02_yield_curve_regimes",
            "svg2": "m01_l02_estrella_mishkin_curve",
            "b1": """<li><strong>[1. 常态正斜率]</strong>：健康扩张期，长端收益率包含合理的期限溢价（Term Premium），曲线向上倾斜。</li>
<li><strong>[2. 平坦化警报]</strong>：央行持续加息收紧短端，远期经济放缓预期压制长端，利差收敛至零。</li>
<li><strong>[3. 深度倒挂]</strong>：短端借贷成本高于长期投资收益，对商业银行信贷供给形成负反馈挤压。</li>""",
            "b2": """<li><strong>[1. 零轴分水岭]</strong>：Estrella-Mishkin 模型中，利差跌破 0 bps 时未来 12 个月衰退概率突破 30% 警戒线。</li>
<li><strong>[2. 非线性加速]</strong>：倒挂深度超过 -100 bps 时，模型预测衰退发生概率超过 65%，历史预测置信度极高。</li>
<li><strong>[3. 投决会规则]</strong>：利差深度倒挂期间，必须强制压缩多头组合的高 Beta 敞口并储备高息现金。</li>""",
            "note": """<li><strong>[定价基石公理]</strong>：国债收益率曲线是全市场固定收益投资者对经济增长、通胀中枢与利率路径的无套利预期概率分布。</li>
<li><strong>[期限溢价规律]</strong>：持有长久期国债承担更高的再投资与通胀波动风险，理应享有正向期限溢价补偿。</li>
<li><strong>[商业银行脆弱性]</strong>：倒挂直接压缩银行借短贷长的净息差（NIM），迫使信贷标准急剧紧缩，引发实体违约螺旋。</li>""",
            "warn": """<li><strong>[牛市陡峭化杀跌陷阱]</strong>：历史暴跌几乎全部发生在“倒挂解除、曲线重新变陡（Bull Steepening）”的阶段，而非初次倒挂期。</li>
<li><strong>[确诊降息陷阱]**：央行紧急降息意味着经济衰退与信用危机被确诊，企业盈利 EPS 断崖式下修速度远超降息带来的折现修复。</li>"""
        },
        "m01_l03": {
            "math": r"$$\text{Phase}_t = f(\Delta \text{Sales}_t, \Delta \text{Inventory}_t) \in \{\text{被动去}, \text{主动补}, \text{被动补}, \text{主动去}\}$$",
            "svg1": "m01_l03_merrill_clock_quadrants",
            "svg2": "m01_l03_kitchin_inventory_cycle",
            "b1": """<li><strong>[1. 复苏期 (Recovery)]</strong>：增长上行叠加通胀下行，企业盈利修复而贴现率保持低位，股票资产夏普比率最高。</li>
<li><strong>[2. 过热期 (Overheat)]</strong>：工业产能利用率见顶，大宗商品涨幅领先，央行加息紧缩压制长久期债券。</li>
<li><strong>[3. 滞胀期 (Stagflation)]</strong>：原材料成本高企吞噬利润，央行无法降息，股债双杀，现金为王。</li>""",
            "b2": """<li><strong>[1. 被动去库存]</strong>：需求率先回暖而存货被动消耗，企业毛利与现金流爆发，股票权益最强买点。</li>
<li><strong>[2. 主动补库存]</strong>：产销两旺开工扩产，资本开支加速，上游大宗商品与周期股迎来主升浪。</li>
<li><strong>[3. 主动去库存]</strong>：全行业减产降价甩卖资产，宽松政策推动长久期利率债迎来波澜壮阔大牛市。</li>""",
            "note": """<li><strong>[资产配置公理]</strong>：大类资产期望收益率是宏观总需求（增长）与价格中枢（通胀）二阶导的数学投影。</li>
<li><strong>[微观财务传导]</strong>：经济增长驱动营收与毛利，通胀决定成本侵蚀与折现率，库存周期主导企业现金流演变。</li>
<li><strong>[动态轮动原则]</strong>：不存在永远战胜通胀的单一资产，宏观对冲的本质是动态重配与当前周期最兼容的标的。</li>""",
            "warn": """<li><strong>[美林电风扇现象]</strong>：中国宏观调控逆周期干预果断，象限跳跃频繁。严禁按海外静态周期进行机械长线轮动。</li>
<li><strong>[滞胀股债负相关失效]</strong>：通胀主导时股债相关性由负转正，经典 60/40 组合将遭受系统性双杀，必须强制配置大宗商品或现金对冲。</li>"""
        },
        "m01_l04": {
            "math": r"$$\text{CFSI}_t = 0.6 \cdot (y^{\text{US}}_{10Y} - y^{\text{CN}}_{10Y}) + 0.2 \cdot \% \Delta \text{DXY} + 0.2 \cdot \% \Delta \text{USDCNH}$$",
            "svg1": "m01_l04_dollar_tide_mechanism",
            "svg2": "m01_l04_capital_flow_shock_index",
            "b1": """<li><strong>[1. 美债高息虹吸]</strong>：美联储维持高基准利率，美债无风险资产收益吸引全球跨国流动性回流美国。</li>
<li><strong>[2. 汇率承压贬值]</strong>：离岸人民币（USD/CNH）面临外生抛压，外币折算损耗增加。</li>
<li><strong>[3. 白马权重抛压]</strong>：北向陆股通资金被迫被动减仓，茅台、宁德等核心白马面临跨期折现估值收缩。</li>""",
            "b2": """<li><strong>[1. 常态顺差 (CFSI ≤ 1.0)]</strong>：外资保持稳定净流入，权益白马资产享受估值溢价。</li>
<li><strong>[2. 预警状态 (1.0 < CFSI ≤ 2.0)]</strong>：汇率波动加大，暂停盲目加仓，收窄外资持股比例过高标的。</li>
<li><strong>[3. 极度冲击 (CFSI > 2.0)]</strong>：外资系统性流出，坚决启动外汇风险对冲，配置防御资产。</li>""",
            "note": """<li><strong>[全球储备锚定本质]</strong>：美元是全球国际贸易结算、大宗商品计价与离岸借贷的底层锚定资产，美联储主导全球资本潮汐。</li>
<li><strong>[抛补利率平价守恒]</strong>：利差深度倒挂必然驱动套息交易（Carry Trade）资金回流高息货币。</li>
<li><strong>[跨国资产折现压制]</strong>：全球配置基金按美元核算 NAV，人民币快速贬值会带来严重外币折算亏损，触发 VaR 被动减仓。</li>""",
            "warn": """<li><strong>[外币 NAV 估值盲区]</strong>：境内投资者以人民币看待标的估值，忽视外币折算亏损对海外长线机构的强平风控约束。</li>
<li><strong>[优先抛售流动性资产]</strong>：外资被动降仓时，首先遭到清算的是成交额最大、流动性最好的大市值白马龙头。</li>"""
        },
        "m01_l05": {
            "math": r"$$\omega^{\text{Equity}}_t = f(\text{Liquidity Trend}_t, \text{VIX}_t) \in \{0.20, 0.50, 0.90\}$$",
            "svg1": "m01_l05_all_weather_framework",
            "svg2": "m01_l05_regime_state_machine",
            "b1": """<li><strong>[1. 四象限风险平分]</strong>：增长与通胀的四种可能情景各分配 25% 风险预算。</li>
<li><strong>[2. 资产风险正交化]</strong>：挑选在特定宏观环境下具备高确定性超额收益的底层资产进行对冲。</li>
<li><strong>[3. 长期复利抗通胀]</strong>：组合穿越 50 年美联储加息与衰退周期，实现稳健向上的净值曲线。</li>""",
            "b2": """<li><strong>[1. 扩张期积极进攻]</strong>：流动性宽松且低波动时，股票敞口升至 90%，享受估值膨胀。</li>
<li><strong>[2. 中性防御过渡]</strong>：流动性收紧但未发生恐慌时，股票降至 50%，平衡回撤。</li>
<li><strong>[3. 危机硬断路器]</strong>：VIX 突破 30 时，无论流动性如何，股票敞口强制压缩至 20%，现金为王。</li>""",
            "note": """<li><strong>[全天候公理]</strong>：资产多样化与风险平价的前提是宏观因子风险的正交暴露。</li>
<li><strong>[多稳态状态机]</strong>：宏观市场由流动性环境与波动率风险溢价构成的多稳态非线性马尔可夫状态机驱动。</li>
<li><strong>[尾部收敛风险]</strong>：在流动性冻结与恐慌飙升的危机体制下，股债负相关关系可能彻底失效并收敛为 1.0。</li>""",
            "warn": """<li><strong>[协方差矩阵崩溃]</strong>：在极端黑天鹅时刻，资产间非线性杠杆清算会瞬间摧毁过去三年建立的统计相关性假设。</li>
<li><strong>[外生宏观断路器优先]</strong>：风控系统必须优先遵循外生硬规则（如 VIX 阈值、隔夜拆借冻结），严禁完全依赖统计内生止损。</li>"""
        },

        # Module 02
        "m02_l01": {
            "math": r"$$P^{\text{micro}}_t = \frac{q^b_1 \cdot P^a_1 + q^a_1 \cdot P^b_1}{q^b_1 + q^a_1} = P^b_1 + \frac{q^b_1}{q^b_1 + q^a_1}(P^a_1 - P^b_1)$$",
            "svg1": "m02_l01_lob_structure",
            "svg2": "m02_l01_matching_engine_flow",
            "b1": """<li><strong>[1. 价格优先公理]</strong>：出价更高的买单优先于出价更低的买单；出价更低的卖单优先于出价更高的卖单。</li>
<li><strong>[2. 时间优先公理 (FIFO)]</strong>：在同一价格档位上，先到达交易所服务器的订单排在队首，享受最优成交权。</li>
<li><strong>[3. 价差动态弹性]</strong>：平时做市商提供充沛挂单使 Spread 极窄；一旦突发重大冲击，做市商撤单导致 Spread 瞬间放大数十倍。</li>""",
            "b2": """<li><strong>[1. 交叉即撮合]</strong>：限价单买价若 ≥ 卖一价，立即按卖一价撮合成交；未完全吃完部分按原限价挂入买方队首。</li>
<li><strong>[2. 市价单扫盘风险]</strong>：大单以市价单形式打出将连续吃空各档深度，使自身在不利的高价位非线性成交。</li>
<li><strong>[3. 撤单流信息含量]</strong>：高频撤单占全市场委托的 80% 以上，撤单的微观空间分布反映了知情交易者的撤退意图。</li>""",
            "note": """<li><strong>[微观物理本质]</strong>：价格不是连续函数，而是离散挂单在交易所内存中的碰撞残差。</li>
<li><strong>[买卖队列拓扑]</strong>：买方按价格降序排列，卖方按价格升序排列，中间为无套利价差（Spread）。</li>
<li><strong>[微观价格先行]</strong>：考虑盘口委托量不对称性的 Micro-Price 能够无偏预测下一跳价格变动方向。</li>""",
            "warn": """<li><strong>[市价单穿仓陷阱]</strong>：严禁在集合竞价尾盘、涨跌停开板或黑天鹅突发时使用市价单交易。做市商撤单会导致 5%~10% 的即时滑点穿仓。</li>
<li><strong>[虚假挂单撤单 (Spoofing)]</strong>：深度远端挂出的巨额买单往往是主力资金制造的支撑假象，一旦上方卖单成交完毕该假单将在数毫秒内撤销。</li>"""
        },
        "m02_l02": {
            "math": r"$$N_{\text{Futures}} = \text{round}\left( \frac{\text{Equity Notional} \times \beta_{\text{Stock}}}{P_{\text{Futures}} \times \text{Multiplier}} \right)$$",
            "svg1": "m02_l02_limit_lock_liquidity_freeze",
            "svg2": "m02_l02_cross_market_hedge_ic",
            "b1": """<li><strong>[1. 现货通道封死]</strong>：一字跌停时买一挂单量为 0，卖一封单数十万手，散户排在队尾成交概率几乎为零。</li>
<li><strong>[2. 衍生品流动性替换]</strong>：股指期货市场具备连续 T+0 交易与双向多空机制，流动性充裕，可瞬间承接对冲敞口。</li>
<li><strong>[3. 下行风险锁死]</strong>：对冲组合在连环跌停期间，期货空头浮盈对冲现货资产缩水，锁死组合最大回撤。</li>""",
            "b2": """<li><strong>[1. Beta 中性对冲]</strong>：根据被困个股的行业与市值属性精确测算股指 Beta，计算对应期货做空手数。</li>
<li><strong>[2. 负基差摩擦]</strong>：股指期货贴水年化 8%~15%，对冲持有存在展期负基差摩擦损耗。</li>
<li><strong>[3. 损耗熔断]</strong>：若连续多日跌停且期货空头贴水走阔超阈值，系统必须执行对冲头寸损耗熔断。</li>""",
            "note": """<li><strong>[交易制度公理]</strong>：制度摩擦直接剥夺流动性退出期权，制造非对称尾部风险。</li>
<li><strong>[T+1 单边暴露]</strong>：A 股 T+1 剥夺了日内买入者的即时平仓止损权，迫使其承受 4 小时日内暴跌与 15 小时隔夜外生冲击。</li>
<li><strong>[流动性归零黑洞]</strong>：一字跌停板将公允估值与可撮合成交完全割裂，流动性降为绝对零度。</li>""",
            "warn": """<li><strong>[基差贴水走阔风险 (Basis Bleed)]</strong>：股指期货深幅贴水使得做空对冲承担不可忽视的移仓成本。</li>
<li><strong>[Alpha-Beta 解耦风险]</strong>：若跌停属于个股特质爆雷而大盘指数上涨，期货做空端将出现亏损，引发现货期货双向失血。</li>"""
        },
        "m02_l03": {
            "math": r"$$\text{OFI}_t = I^b_t - I^a_t, \quad \Delta P^{\text{mid}}_t = \beta \cdot \text{OFI}_t + \epsilon_t$$",
            "svg1": "m02_l03_ofi_flux_calculation",
            "svg2": "m02_l03_kyle_lambda_impact",
            "b1": """<li><strong>[1. 三态判定完备]</strong>：价格上跳、维持与破位三态严格覆盖了订单簿最优档位的所有微观事件组合。</li>
<li><strong>[2. 物理净通量对冲]</strong>：买方新增挂单与卖方撤销挂单在代数上统一整合为推升价格的正向驱动力。</li>
<li><strong>[3. 高信噪比领先]</strong>：相比仅记录成交历史的事后主动成交量，OFI 包含了做市商挂撤单意图，预测能量显著提高。</li>""",
            "b2": """<li><strong>[1. 微观 Kyle's Lambda]</strong>：OFI 与中间价跳跃的回归斜率 β 纯粹反映了盘口价格冲击弹性。</li>
<li><strong>[2. 多档加权衰减]</strong>：针对 Level 2 至 Level 10 深度档位，引入指数衰减权重 $w_k = \exp(-\alpha (k-1))$。</li>
<li><strong>[3. 虚假挂单过滤]</strong>：深档虚假挂单撤单（Spoofing）通过指数衰减被快速过滤，保留浅层真实供需信号。</li>""",
            "note": """<li><strong>[高频第一性原理]</strong>：价格跳跃不是成交量的线性函数，而是挂单簿净通量的不平衡释放。</li>
<li><strong>[代数守恒公理]</strong>：OFI 将买卖双边挂单、吃单与撤单的净通量差分，输出纯净的微观价格跳跃先行信号。</li>
<li><strong>[微观冲击映射]</strong>：在秒级与 Tick 级窗口内，中间价变动量与 OFI 存在极高的线性决定系数（$R^2$ 常达 60%~80%）。</li>""",
            "warn": """<li><strong>[因子半衰期极短]</strong>：单步 OFI 的预测能量呈指数级衰减，有效半衰期仅有数十毫秒至数秒，严禁在低频级别直接套用。</li>
<li><strong>[深档虚假诱骗污染]</strong>：未加权的多档 OFI 极易被买五/卖五以外的远端虚假挂单操纵，必须施加严格的距离指数衰减。</li>"""
        },
        "m02_l04": {
            "math": r"$$x_j = \frac{\sinh(\kappa (T - t_j))}{\sinh(\kappa T)} \cdot X, \quad \kappa \approx \sqrt{\frac{\lambda \sigma^2}{\eta}}$$",
            "svg1": "m02_l04_impact_decomposition",
            "svg2": "m02_l04_almgren_chriss_curves",
            "b1": """<li><strong>[1. 永久市场冲击]</strong>：由母单向市场透露知情信息引发，促使对手盘上修公允价值，该冲击不可逆。</li>
<li><strong>[2. 临时市场冲击]</strong>：由单笔子单在微观瞬间消耗盘口局部深度引发，随后随做市商回补挂单而迅速均值回归。</li>
<li><strong>[3. 正交物理分解]</strong>：总冲击严格等于永久冲击与临时冲击之和，拆单优化主要平抑临时冲击的非线性放大。</li>""",
            "b2": """<li><strong>[1. 风险中性 TWAP]</strong>：当风险厌恶系数 λ = 0 时，最优拆单退化为线性匀速 TWAP，临时冲击平方和全局最小。</li>
<li><strong>[2. 风险厌恶前置加速]</strong>：当 λ > 0 时，持仓轨迹呈双曲正弦曲线，前期快速卖出以规避漫长执行中的价格方差风险。</li>
<li><strong>[3. VWAP 契合微笑]</strong>：依据全市场日内成交量 U 型微笑曲线分配子单规模，避免在午盘清淡期产生剧烈冲击。</li>""",
            "note": """<li><strong>[算法执行公理]</strong>：回测与实盘的巨大鸿沟在于未计提市场冲击与非线性滑点。</li>
<li><strong>[平方根法则经验公理]</strong>：总冲击成本与交易量占日均成交量（ADV）的平方根成正比：$I \propto \sigma \sqrt{Q/V}$。</li>
<li><strong>[Almgren-Chriss 效用权衡]</strong>：在执行冲击滑点期望成本与未执行持仓波动方差之间建立拉格朗日最优变分平衡。</li>""",
            "warn": """<li><strong>[盲目套用 TWAP 惩罚]</strong>：在开盘与收盘成交量剧烈放大时若机械匀速执行，将在局部清淡期承受非线性滑点重创。</li>
<li><strong>[冰山单被嗅探陷阱]</strong>：固定时间间隔和固定股数的拆单将被高频嗅探算法（Sniffer Algos）秒级识别并招致掠夺性抢跑。</li>"""
        },
        "m02_l05": {
            "math": r"$$\text{Score} = \text{clip}(50.0 + 0.3 \cdot \text{Flow}_{\text{North}} + 2.5 \cdot (\text{MarginRatio} - 8.0) + 0.5 \cdot \text{Flow}_{\text{Inst}} + \Delta \text{Score}_{\text{Seats}}, 0.0, 100.0)$$",
            "svg1": "m02_l05_capital_taxonomy",
            "svg2": "m02_l05_sentiment_gauge_score",
            "b1": """<li><strong>[1. 外资长线 (Long-only)]</strong>：托管于汇丰、花旗等外资行，持仓久期长，重仓高 ROIC 白马龙头。</li>
<li><strong>[2. 机构专用席位]</strong>：公募、险资与社保专用席位，持仓溢价具备中长期持续性，是真正的“基本面底牌”。</li>
<li><strong>[3. 顶级知名游资]</strong>：热点题材情绪点火，极限 T+1 隔夜博弈，次日开盘极易抢跑平仓收割流动性。</li>""",
            "b2": """<li><strong>[1. 强力多头 (Score > 75)]</strong>：机构集体大单买入共振，两融积极加仓，筹码高度集中，顺势做多。</li>
<li><strong>[2. 震荡博弈 (45 ≤ Score ≤ 75)]</strong>：资金多空拉锯轮动较快，控制杠杆水平，等待明确方向。</li>
<li><strong>[3. 高危派发 (Score < 45)]</strong>：拉萨天团霸榜接盘，主力机构成功出逃，坚决一票否决清仓避险。</li>""",
            "note": """<li><strong>[资金博弈公理]</strong>：资金性质决定持仓久期，筹码结构决定极端行情的脆弱性边界。</li>
<li><strong>[席位标签穿透]</strong>：单一价格形态极易被虚假诱骗，穿透龙虎榜席位与托管行是看清主力底牌的终极放大镜。</li>
<li><strong>[拉萨天团反向指标]</strong>：东财散户集中地霸榜买入往往意味着筹码发散、散户接盘，属于强烈的筹码崩塌信号。</li>""",
            "warn": """<li><strong>[盲目跟风游资席位陷阱]</strong>：知名游资买入溢价在次日开盘 15 分钟内即被抢跑出逃耗尽，散户开盘追入极易被核按钮深套。</li>
<li><strong>[虚假假外资障眼法]</strong>：未穿透托管行的北向资金存在大量境内配资离岸套壳，必须结合 CCASS 席位明细剔除投机热钱噪音。</li>"""
        },

        # Module 03
        "m03_l01": {
            "math": r"$$\text{ROE} = \left(\frac{\text{NI}}{\text{EBT}}\right) \times \left(\frac{\text{EBT}}{\text{EBIT}}\right) \times \left(\frac{\text{EBIT}}{\text{Rev}}\right) \times \left(\frac{\text{Rev}}{\text{Assets}}\right) \times \left(\frac{\text{Assets}}{\text{Equity}}\right)$$",
            "svg1": "m03_l01_three_statements_articulation",
            "svg2": "m03_l01_dupont_five_factor_tree",
            "b1": """<li><strong>[1. 资产负债表绝对平衡]</strong>：资产总计严格恒等于负债总计与股东权益之和，任何虚假资产均需对应科目配平。</li>
<li><strong>[2. 留存收益跨期桥梁]</strong>：期末留存收益严格等于期初留存收益加当期净利润扣除现金分红。</li>
<li><strong>[3. 现金流真金白银]</strong>：通过间接法扣减存货和应收账款占用（ΔNWC），揭示企业不依赖外部输血的自主造血能力。</li>""",
            "b2": """<li><strong>[1. 护城河定价权]</strong>：顶级白马凭借极高的 EBIT 利润率（>50%）单引擎驱动卓越 ROE，完全无需杠杆。</li>
<li><strong>[2. 极致周转效率]</strong>：Costco 等零售企业虽然利润率微薄，但通过高达 3.5 次以上的资产周转率同样创造 20%+ ROE。</li>
<li><strong>[3. 脆弱杠杆陷阱]</strong>：传统房企通过高达 6~8 倍的权益乘数虚构高 ROE 假象，下行期利息直接将净利润清零。</li>""",
            "note": """<li><strong>[财务第一性原理]</strong>：商业本质必然锚定企业创造自由现金流的长期能力，三张表是透视资本配置效率的事实底册。</li>
<li><strong>[收付实现制试金石]</strong>：权责发生制下的净利润充斥着会计估计，收付实现制下的真金白银现金流无法伪造。</li>
<li><strong>[五因子正交解构]</strong>：现代杜邦分析将 ROE 解构为税收负担、利息负担、经营利润率、资产周转率与权益乘数。</li>""",
            "warn": """<li><strong>[经营现金流持续小于净利润红线]</strong>：连续两年 CFO < 净利润且应收账款大幅跑赢营收，是上市公司业绩造假塞货的头号警报。</li>
<li><strong>[商誉沉没与减值炸弹]</strong>：商誉本质为并购历史溢价不产生经营现金流，测算真实回报率时必须强制扣除商誉（Tangible ROIC）。</li>"""
        },
        "m03_l02": {
            "math": r"$$M = -4.84 + 0.920 \cdot \text{DSRI} + 0.528 \cdot \text{GMI} + 0.404 \cdot \text{AQI} + 0.892 \cdot \text{SGI} + 0.115 \cdot \text{DEPI} - 0.172 \cdot \text{SGAI} + 4.037 \cdot \text{TATA} + 0.0327 \cdot \text{LVGI}$$",
            "svg1": "m03_l02_beneish_eight_pillars",
            "svg2": "m03_l02_deposit_loan_paradox",
            "b1": """<li><strong>[1. 应计项权重绝对压倒]</strong>：TATA 的回归系数（4.037）权重最高，表明现金流与利润背离是财务操纵的决定性证据。</li>
<li><strong>[2. 跨表自洽印证]</strong>：资产质量恶化（AQI）与折旧放缓（DEPI）相互印证，揭开研发违规资本化的包装面具。</li>
<li><strong>[3. 严格阈值判定]</strong>：M-Score > -1.78 触发高舞弊概率预警，安然在暴雷前一年评分为 -1.49。</li>""",
            "b2": """<li><strong>[1. 商业逻辑反常]</strong>：账面躺着百亿存款却同时借入数十亿高息短贷并承担数亿利息支出，违背商业常理。</li>
<li><strong>[2. 虚假流水伪造]</strong>：所谓百亿存款实质属于伪造对账单，或早已被控股股东违规质押担保处于完全受限冻结状态。</li>
<li><strong>[3. 终局暴雷必然]</strong>：缺乏真实流动性的造假公司在债务到期无法续借时，资金链断裂将瞬间引爆违约。</li>""",
            "note": """<li><strong>[法务会计哲学]</strong>：业务逻辑有印证，资产质量显端倪，应计粉饰看现金。</li>
<li><strong>[操纵动机识别]</strong>：在业绩承诺、股权质押与再融资考核压力下，管理层拥有强烈的会计粉饰寻租动机。</li>
<li><strong>[Beneish 八维雷达]</strong>：通过应收账款、毛利率、资产质量、营收成长、折旧率、费用率、总应计项与杠杆率全景扫描。</li>""",
            "warn": """<li><strong>[存贷双高典型地雷]</strong>：大存大贷是 A 股最具杀伤力的财务造假形态，必须通过利息收入率与净财务费用进行自动化交叉验证。</li>
<li><strong>[存货与毛利率逆势背离]</strong>：存货周转天数飙升而毛利率反常走高，确证企业少结转营业成本、囤积成本虚增利润的手法。</li>"""
        },
        "m03_l03": {
            "math": r"$$\text{ROIC} = \frac{\text{EBIT}(1 - t)}{\text{Invested Capital}}, \quad \text{EVA} = \text{Invested Capital} \times (\text{ROIC} - \text{WACC})$$",
            "svg1": "m03_l03_roic_wacc_spread_eva",
            "svg2": "m03_l03_moat_decay_curves",
            "b1": """<li><strong>[1. 价值创造真实引擎]</strong>：ROIC 持续显著高于 WACC（EVA > 0），企业每追加一元投资均在复合放大股东财富。</li>
<li><strong>[2. 价值毁灭黑洞]</strong>：ROIC < WACC（EVA < 0），企业看似有利润实则无法覆盖资本成本，扩产等同于加速自杀。</li>
<li><strong>[3. 剔除财务杠杆噪音]</strong>：ROIC 将债权人与股东资本统一核算，彻底消除了负债率高低对盈利能力的虚假掩盖。</li>""",
            "b2": """<li><strong>[1. 宽护城河持久度 (Wide Moat)]</strong>：衰减率 λ 极小（0.03），半衰期长达 15~20 年，超额资本回报长期维持。</li>
<li><strong>[2. 窄护城河过渡期]</strong>：衰减率 λ 约为 0.10，超额收益在 8~10 年内逐步收敛至行业平均水平。</li>
<li><strong>[3. 无壁垒代工陷阱]</strong>：衰减率 λ > 0.30，超额利润在 3~5 年内被新进入对手竞争抹平。</li>""",
            "note": """<li><strong>[商业护城河量化公理]</strong>：ROIC 持续高于 WACC 是商业护城河存在的唯一数学真理。</li>
<li><strong>[投入资本会计守恒]</strong>：资产端（NWC + PP&E + 无形资产 - 超额现金）与融资端（权益 + 有息负债 - 现金）严格恒等。</li>
<li><strong>[资本配置决策基石]</strong>：只有当企业投入资本回报率超越机会成本时，留存收益再投资才能产生真实的复利雪球。</li>""",
            "warn": """<li><strong>[规模不经济与扩产陷阱]</strong>：在 ROIC < WACC 时，管理层追求“营收翻倍”的大规模资本开支是对股东财富的毁灭性打击。</li>
<li><strong>[高 ROE 虚假繁荣]</strong>：依靠 80% 负债率高杠杆或者炒股理财非经常性损益堆砌的高 ROE，在 ROIC 显微镜下一览无余。</li>"""
        },
        "m03_l04": {
            "math": r"$$\text{EV} = \sum_{t=1}^N \frac{\text{FCFF}_t}{(1 + \text{WACC})^t} + \frac{\text{FCFF}_N (1 + g)}{(\text{WACC} - g)(1 + \text{WACC})^N}, \quad \text{Value per Share} = \frac{\text{EV} - \text{Net Debt}}{\text{Shares}}$$ ",
            "svg1": "m03_l04_two_stage_dcf_timeline",
            "svg2": "m03_l04_wacc_sensitivity_matrix",
            "b1": """<li><strong>[1. 显性预测期现值]</strong>：逐年测算营收、毛利、EBIT、CapEx 与营运资本，通常占企业价值的 25%~35%。</li>
<li><strong>[2. 永续终值期现值 (TV)]</strong>：基于戈登增长模型折现，终值通常占据企业价值的 65%~80%，对贴现率极其敏感。</li>
<li><strong>[3. 净负债股权桥梁]</strong>：企业价值 EV 扣除有息负债并加回多余现金，得出归属于普通股股东的每股内在价值。</li>""",
            "b2": """<li><strong>[1. 贴现率非线性放大]</strong>：WACC 变动 ±1% 将引起每股内在价值 ±20% 的巨幅摇摆，必须进行双变量网格测算。</li>
<li><strong>[2. 蒙特卡洛随机模拟]</strong>：将 WACC 与 g 设定为随机分布进行 10,000 次抽样，输出内在价值概率密度分布。</li>
<li><strong>[3. 安全边际决策]</strong>：以 5% 分位数的悲观现值作为下行安全边际（Margin of Safety）买入红线。</li>""",
            "note": """<li><strong>[绝对估值第一性原理]</strong>：资产内在价值等于未来存续期全部自由现金流的现值总和。</li>
<li><strong>[FCFF 与 FCFE 适用边界]</strong>：非金融企业使用 FCFF 与 WACC 贴现；高杠杆金融机构必须采用股利折现模型（DDM）。</li>
<li><strong>[反向 DCF 逆推逻辑]</strong>：将当前市价代入模型，倒推市场隐含的未来营收复合增速与现金流转化率是否符合商业常识。</li>""",
            "warn": """<li><strong>[参数倒推迎合市价陷阱]**：微调 WACC 或终值增长率 g 就能随意得出任何目标价，单一点位预测在投决会中毫无信度。</li>
<li><strong>[资本开支与折旧永久错配]</strong>：在永续期假设中，严禁假设资本开支长期低于折旧，必须保持资产重置的资本守恒。</li>"""
        },
        "m03_l05": {
            "math": r"$$\frac{P}{B} = \frac{\text{ROE} - g}{K_e - g}, \quad \text{Score} = \text{clip}(50.0 - 20.0 \cdot Z_{\text{PE}} + 30.0 \cdot (\text{ROIC} - 0.10), 0.0, 100.0)$$",
            "svg1": "m03_l05_multiples_decision_tree",
            "svg2": "m03_l05_cyclical_pe_inversion",
            "b1": """<li><strong>[1. P/E 市盈率]</strong>：适用于盈利平稳持续的成熟消费与蓝筹股，必须结合盈利复合增速观察 PEG < 1.0。</li>
<li><strong>[2. P/B 市净率]</strong>：适用于银行金融与重资产制造，核心纽带是 PB-ROE 框架：高 ROE 理应享受高 PB 溢价。</li>
<li><strong>[3. EV/EBITDA]</strong>：剔除资本结构与折旧政策干扰，是高杠杆重资产行业与跨国并购估值的标准工具。</li>""",
            "b2": """<li><strong>[1. 景气顶峰低 PE 陷阱]</strong>：周期股在利润最高点静态 PE 仅 2~3 倍，看似低估实为历史大顶，随后利润必将雪崩。</li>
<li><strong>[2. 景气冰点高/负 PE 黄金坑]</strong>：全行业巨亏出清时 PE 畸高或为负数，股价跌穿重置成本，反而是周期大底买点。</li>
<li><strong>[3. 估值工具切换]</strong>：周期股景气高位看周期归一化利润（Through-the-Cycle Earnings），低谷看 PB 与重置成本。</li>""",
            "note": """<li><strong>[相对估值乘数公理]</strong>：乘数是一价定律下的相对投影，本质是增长率、风险溢价与资产回报率的压缩表象。</li>
<li><strong>[横截面偏离度评价]</strong>：在细分行业内部计算标准化 Z-Score，寻找相对估值洼地。</li>
<li><strong>[价值陷阱量化防御]</strong>：便宜的股票往往因质次而便宜，必须结合 ROIC 门槛与利息保障倍数过滤僵尸企业。</li>""",
            "warn": """<li><strong>[强周期股低市盈率自杀陷阱]</strong>：在周期顶峰误将 PE=2 倍当作捡便宜买入，将承受 60%~80% 的股价腰斩惨剧。</li>
<li><strong>[质次价廉价值陷阱]</strong>：长期低于 0.5 倍 PB 往往反映了未确认坏账与资产减值的悲观折价，缺乏 ROIC 支撑的低估是长期死水。</li>"""
        }
    }

    # Extract starter/solutions from Python files
    all_curriculum_modules = [
        ("m01", "01", "01_macro_cycle", "宏观经济与流动性周期", "Macroeconomics & Liquidity Cycles", 
         "以第一性原理拆解央行资产负债表扩张收缩、利率期限结构、通胀动力学与美林投资时钟大类资产配置框架。", "🌐", M01_LESSONS),
        ("m02", "02", "02_micro_market", "市场微观结构与订单流", "Market Microstructure & Order Flow",
         "深入交易所限价订单簿（LOB）撮合物理现实、买卖点差动力学、OFI 订单流不平衡与 Almgren-Chriss 算法拆单。", "⚡", M02_LESSONS),
        ("m03", "03", "03_fundamental", "公司财务分析与估值", "Fundamental Analysis & Valuation",
         "三表动态勾稽平衡校验、杜邦五因子拆解、Beneish M-Score 8维法务舞弊排雷与两阶段自由现金流折现（DCF）。", "💎", M03_LESSONS)
    ]

    upgraded_modules_json = []

    for mod_id, mod_num, folder, title, title_en, desc, icon, lessons in all_curriculum_modules:
        mod_dict = {
            "id": mod_id,
            "num": mod_num,
            "folder": folder,
            "title": title,
            "title_en": title_en,
            "desc": desc,
            "icon": icon,
            "lessons_count": len(lessons),
            "lessons": []
        }

        for l in lessons:
            lid = l["id"]
            cfg = configs.get(lid, {})
            py_ans_file = os.path.join(BASE_DIR, folder, "answers", l["file_name"])
            code_body = ""
            if os.path.exists(py_ans_file):
                code_body = extract_code_body(py_ans_file)

            theory_html = build_web_lesson_theory(
                lid,
                l["title"],
                cfg.get("math", "$$E = mc^2$$"),
                cfg.get("svg1", ""),
                cfg.get("svg2", ""),
                cfg.get("b1", ""),
                cfg.get("b2", ""),
                cfg.get("note", ""),
                cfg.get("warn", "")
            )

            # Build QA list
            qa_items = [
                {
                    "q": "Q1: 投决会核心机制思考题",
                    "hint": "从资产负债表借贷平衡与风险定价公式出发思考。",
                    "ans": "详见课程 docstring 与 answers/ 参考实现中的详细投决会推导。"
                },
                {
                    "q": "Q2: 工业界实战与风险传导思考题",
                    "hint": "注意区分名义指标与实际微观流动性的背离。",
                    "ans": "详见课程 docstring 与 answers/ 参考实现中的详细投决会推导。"
                },
                {
                    "q": "Q3: 制度约束与量化模型边界思考题",
                    "hint": "结合交易制度微观摩擦与宏观跨周期调节进行剖析。",
                    "ans": "详见课程 docstring 与 answers/ 参考实现中的详细投决会推导。"
                }
            ]

            lesson_dict = {
                "id": lid,
                "num": l["num"],
                "title": l["title"],
                "difficulty": l["difficulty"],
                "time": l["time"],
                "status": "completed",
                "objectives": l["objectives"],
                "theory": theory_html,
                "code": code_body[:3000] if len(code_body) > 3000 else code_body,
                "qa": qa_items,
                "exercise": {
                    "title": f"量化实现与断言测试：{l['title']}",
                    "starter": f"# {l['title']} 实战工作台\nimport numpy as np\nimport pandas as pd\n\ndef run_pipeline():\n    # TODO: 实现算法逻辑\n    return True\n",
                    "solution": f"# 参考实现请运行 answers/{l['file_name']}"
                }
            }
            mod_dict["lessons"].append(lesson_dict)

        upgraded_modules_json.append(mod_dict)

    # Now read web/js/data-curriculum.js, find where m04 starts, and replace m01-m03
    curriculum_js_path = os.path.join(BASE_DIR, "web", "js", "data-curriculum.js")
    with open(curriculum_js_path, "r", encoding="utf-8") as f:
        curr_text = f.read()

    # Find the start of m04
    m04_match = re.search(r'\{\s*"id":\s*"m04"', curr_text)
    if not m04_match:
        m04_match = re.search(r'\{\s*id:\s*"m04"', curr_text)

    if not m04_match:
        print("❌ Could not find m04 in data-curriculum.js!")
        return

    m04_idx = m04_match.start()
    tail_text = curr_text[m04_idx:]

    # Construct the upgraded m01-m03 javascript array text
    header = """/**
 * InvestLearning Curriculum Database (Anthropic & Quarto Enhanced)
 * Institutional Grade Syllabus, Cold Tone, KaTeX Math & Pure SVG Vector Topologies
 */

const CURRICULUM_DATA = [
"""
    m01_03_text = json.dumps(upgraded_modules_json, ensure_ascii=False, indent=2)
    # Strip opening '[' and closing ']'
    m01_03_text = m01_03_text.strip()
    if m01_03_text.startswith("["):
        m01_03_text = m01_03_text[1:].strip()
    if m01_03_text.endswith("]"):
        m01_03_text = m01_03_text[:-1].strip()

    full_new_js = f"{header}{m01_03_text},\n  {tail_text}"

    with open(curriculum_js_path, "w", encoding="utf-8") as f:
        f.write(full_new_js)

    print(f"✅ Successfully updated {curriculum_js_path} with all 15 lessons for Modules 01, 02, 03!")


def upgrade_notebook_converter():
    print("=" * 60)
    print("3. Updating convert_to_notebooks.py to properly support r\"\"\" docstrings")
    print("=" * 60)

    conv_path = os.path.join(BASE_DIR, "scripts", "convert_to_notebooks.py")
    with open(conv_path, "r", encoding="utf-8") as f:
        conv_code = f.read()

    # Enhance docstring splitting
    old_snippet = """    # 拆分顶层 docstring (理论精讲) 与 Python 代码
    if content.strip().startswith('\"\"\"'):
        parts = content.strip().split('\"\"\"', 2)
        if len(parts) >= 3:
            docstring = parts[1].strip()
            code_body = parts[2].strip()"""

    new_snippet = """    # 拆分顶层 docstring (理论精讲) 与 Python 代码
    stripped = content.strip()
    if stripped.startswith('r\"\"\"') or stripped.startswith('\"\"\"'):
        parts = stripped.split('\"\"\"', 2)
        if len(parts) >= 3:
            docstring = parts[1].strip()
            code_body = parts[2].strip()"""

    if old_snippet in conv_code:
        conv_code = conv_code.replace(old_snippet, new_snippet)
        with open(conv_path, "w", encoding="utf-8") as f:
            f.write(conv_code)
        print("  Updated convert_to_notebooks.py with r\"\"\" support!")
    else:
        print("  convert_to_notebooks.py already updated or snippet not matched.")


def main():
    upgrade_python_files()
    generate_web_curriculum_data()
    upgrade_notebook_converter()
    print("\n🎉 Upgrade scripts successfully completed!")


if __name__ == "__main__":
    main()
