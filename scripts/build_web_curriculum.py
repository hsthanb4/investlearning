#!/usr/bin/env python3
"""
InvestLearning Web Curriculum Builder
Generates rich institutional HTML for Modules 01, 02, and 03 with:
  - Anthropic minimalism styling
  - Quarto callouts (.callout-note / .callout-warning)
  - Inline Anthropic SVGs from SVGS dictionary
  - Math blocks
  - Triadic layout (Anchor -> Card -> 1/2/3 Breakdown)
  - Q&A with hints and solutions
"""

import os
import re
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from generate_curriculum_svgs import SVGS
from curriculum_content_m01 import M01_LESSONS
from curriculum_content_m02 import M02_LESSONS
from curriculum_content_m03 import M03_LESSONS

def extract_code_body(py_path):
    with open(py_path, "r", encoding="utf-8") as f:
        content = f.read()
    trimmed = content.lstrip()
    if trimmed.startswith('r"""') or trimmed.startswith('"""'):
        parts = trimmed.split('"""', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()

def build_lesson_html(lesson_id, title, math_formula, svg_key_1, svg_key_2, breakdown_1, breakdown_2, note_text, warning_text):
    svg_1 = SVGS.get(svg_key_1, "")
    svg_2 = SVGS.get(svg_key_2, "")
    
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
    <span class="diagram-title">{title} · 核心传导拓扑</span>
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

print("Web Curriculum Builder loaded successfully.")
