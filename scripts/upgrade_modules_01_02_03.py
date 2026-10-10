#!/usr/bin/env python3
"""
InvestLearning Institutional Upgrader for Modules 01, 02, and 03.
Applies:
  1. Cold, first-principles Investment Committee tone.
  2. Labeled structure (- **[核心标签]**：...).
  3. Triadic visual layout (Anchor sentence -> SVG Diagram Card -> 1/2/3 Breakdown).
  4. Quarto Callout containers (.callout-note / .callout-warning).
  5. KaTeX math formulas with explicit domains.
  6. In-depth Q1~Q3 thought question answers.
  7. Full web database sync (web/js/data-curriculum.js).
"""

import os
import re
import sys
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY_BIN = sys.executable

print(f"Starting upgrade script in {BASE_DIR} using {PY_BIN}...")
