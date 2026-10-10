"""
模块 06 · 第 5 课参考答案
"""
import numpy as np

def calculate_kurtosis(returns: np.ndarray) -> float:
    n = len(returns)
    mean = np.mean(returns)
    std = np.std(returns, ddof=0)
    if std == 0:
        return 0.0
    m4 = np.mean((returns - mean) ** 4)
    return float(m4 / (std ** 4) - 3.0)

if __name__ == "__main__":
    normal_like = np.array([-0.02, -0.01, 0.0, 0.01, 0.02])
    fat_tail = np.array([-0.15, -0.01, 0.0, 0.01, 0.20])
    k_fat = calculate_kurtosis(fat_tail)
    k_norm = calculate_kurtosis(normal_like)
    assert k_fat > k_norm
    print("Lesson 05 (Tail Risk) Answer Verified!")
