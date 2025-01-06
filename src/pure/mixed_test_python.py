"""Pure Python implementation of mixed CPU/memory test."""

from typing import Dict
from typing import List


def fibonacci_memoized(n: int, memo: Dict[int, int] = None) -> int:
    """
    Calculate Fibonacci number iteratively with memoization.

    Args:
        n: The index of the Fibonacci number to calculate
        memo: Memoization dictionary to store computed values (not used in iterative version)

    Returns:
        int: The nth Fibonacci number
    """
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def run_mixed_test(n: int) -> List[int]:
    """
    Run mixed CPU and memory test.

    Args:
        n: Size parameter for the test

    Returns:
        List[int]: List of Fibonacci numbers
    """
    return [fibonacci_memoized(i) for i in range(n)]


if __name__ == "__main__":
    fib_sequence = run_mixed_test(35)
    print(f"Fibonacci sequence: {fib_sequence}")
    print(f"Length of sequence: {len(fib_sequence)}")
