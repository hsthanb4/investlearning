"""
模块 09 · 第 4 课参考答案
"""
def calculate_net_net_working_capital(cash_and_equiv: float, receivables: float, inventory: float, total_liabilities: float) -> float:
    adjusted_assets = cash_and_equiv + 0.75 * receivables + 0.50 * inventory
    return adjusted_assets - total_liabilities

if __name__ == "__main__":
    nn = calculate_net_net_working_capital(100.0, 80.0, 60.0, 110.0)
    assert abs(nn - 80.0) < 1e-4
    print("Lesson 04 (Spinoff & Net-Net) Answer Verified!")
