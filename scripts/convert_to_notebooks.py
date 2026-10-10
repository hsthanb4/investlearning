"""
StockLearning 自动转换脚本：将所有 .py 课程与答案转换为标准 Jupyter Notebook (.ipynb)
================================================================================
"""

import os
import glob
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def py_to_notebook(py_path: str, ipynb_path: str):
    with open(py_path, "r", encoding="utf-8") as f:
        content = f.read()

    cells = []
    # 拆分顶层 docstring (理论精讲) 与 Python 代码
    if content.strip().startswith('"""'):
        parts = content.strip().split('"""', 2)
        if len(parts) >= 3:
            docstring = parts[1].strip()
            code_body = parts[2].strip()

            # Markdown cell
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + "\n" for line in docstring.split("\n")]
            })
            # Code cell
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [line + "\n" for line in code_body.split("\n")]
            })
        else:
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [line + "\n" for line in content.split("\n")]
            })
    else:
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in content.split("\n")]
        })

    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.12"},
            "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    with open(ipynb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

def main():
    py_files = glob.glob(os.path.join(BASE_DIR, "[0-1][0-9]_*/*.py"))
    py_files += glob.glob(os.path.join(BASE_DIR, "[0-1][0-9]_*/answers/*.py"))
    
    count = 0
    for p in py_files:
        if p.endswith(".py"):
            nb_path = p[:-3] + ".ipynb"
            py_to_notebook(p, nb_path)
            count += 1
            
    print(f"🎉 成功生成 {count} 个 Jupyter Notebook (.ipynb) 交互式课件！")

if __name__ == "__main__":
    main()
