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
    """
    Pure Python implementation for mixed CPU/memory test.
    No numpy dependency required.
    """
    # Memory-intensive part
    data = []
    for i in range(n):
        data.append([j * j for j in range(n)])

    # CPU-intensive part
    result = 0
    for i in range(n):
        for j in range(n):
            if i % 2 == 0:
                result += data[i][j]
            else:
                result *= data[i][j] + 1

    return result


if __name__ == "__main__":
    result = run_mixed_test(35)
    print(f"Result of mixed test: {result}")
