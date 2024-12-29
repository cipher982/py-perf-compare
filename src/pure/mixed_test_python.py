"""Pure Python implementation of mixed CPU/memory test."""

from typing import Dict
from typing import List


def fibonacci_memoized(n: int, memo: Dict[int, int] = None) -> int:
    """
    Calculate Fibonacci number with memoization.

    Args:
        n: The index of the Fibonacci number to calculate
        memo: Memoization dictionary to store computed values

    Returns:
        int: The nth Fibonacci number
    """
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def run_mixed_test(n: int = 35) -> List[int]:
    """
    Run mixed test calculating Fibonacci sequence with memoization.

    Args:
        n: Length of the Fibonacci sequence to calculate (default: 35)

    Returns:
        List[int]: List of Fibonacci numbers
    """
    return [fibonacci_memoized(i) for i in range(n)]


if __name__ == "__main__":
    fib_sequence = run_mixed_test()
    print(f"Fibonacci sequence: {fib_sequence}")
    print(f"Length of sequence: {len(fib_sequence)}")
