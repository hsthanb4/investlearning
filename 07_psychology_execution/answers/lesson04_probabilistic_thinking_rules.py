"""
模块 07 · 第 4 课参考答案
"""
def should_take_trade(expected_payoff_ratio: float, win_probability: float, min_expectancy_ratio: float = 0.20) -> bool:
    score = win_probability * expected_payoff_ratio - (1.0 - win_probability)
    return score >= min_expectancy_ratio

if __name__ == "__main__":
    assert should_take_trade(2.5, 0.40) == True
    assert should_take_trade(1.5, 0.40) == False
    print("Lesson 04 (Probabilistic Thinking) Answer Verified!")
