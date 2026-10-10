"""
模块 06 · 第 4 课参考答案
"""
import numpy as np

def calculate_historical_var_cvar(returns: np.ndarray, confidence: float = 0.95) -> tuple:
    alpha = 1.0 - confidence
    cutoff = np.percentile(returns, alpha * 100.0)
    var = -cutoff
    tail_losses = -returns[returns <= cutoff]
    cvar = float(np.mean(tail_losses)) if len(tail_losses) > 0 else var
    return var, cvar

if __name__ == "__main__":
    rets = np.array([-0.10, -0.06, -0.05, -0.02, 0.01, 0.02, 0.03, 0.04, 0.05, 0.08])
    var90, cvar90 = calculate_historical_var_cvar(rets, confidence=0.90)
    assert cvar90 >= var90
    print("Lesson 04 (VaR/CVaR) Answer Verified!")
