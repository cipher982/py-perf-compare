def fibonacci_memoized(n, memo=None):
    """Calculate Fibonacci number with memoization."""
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def run_mixed_test(n):
    """Run mixed test calculating Fibonacci sequence with memoization."""
    return [fibonacci_memoized(i) for i in range(n)]


if __name__ == "__main__":
    fib_sequence = run_mixed_test(35)
    print(f"Fibonacci sequence: {fib_sequence}")
    print(f"Length of sequence: {len(fib_sequence)}")
