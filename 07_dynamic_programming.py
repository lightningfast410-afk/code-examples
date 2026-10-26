"""07_dynamic_programming.py — Memoized Fibonacci and minimum coin change.

Demonstrates: dynamic programming — solve each subproblem once,
store it, and reuse it. The naive Fibonacci recursion is
exponential; the memoized version is linear.
Run: python3 07_dynamic_programming.py
"""

from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def min_coins(coins, amount):
    """Fewest coins summing to amount, or -1 when impossible."""
    INF = float("inf")
    best = [0] + [INF] * amount
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value and best[value - coin] != INF:
                best[value] = min(best[value], best[value - coin] + 1)
    return -1 if best[amount] == INF else best[amount]


def main():
    assert fib(30) == 832040
    assert fib(0) == 0 and fib(1) == 1
    assert min_coins([1, 5, 10, 25], 63) == 6  # 25+25+10+1+1+1
    assert min_coins([3], 7) == -1
    print(f"PROOF: fib(30) = {fib(30)}, min_coins(63) = 6, impossible -> -1")


if __name__ == "__main__":
    main()
