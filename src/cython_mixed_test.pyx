# cython: boundscheck=False, wraparound=False, nonecheck=False

def fibonacci_memoized(int n, dict memo=None):
    """Cython-optimized Fibonacci with memoization."""
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n-1, memo) + fibonacci_memoized(n-2, memo)
    return memo[n]

def run_mixed_test(int n=35):
    """Run mixed test calculating Fibonacci sequence with memoization."""
    return [fibonacci_memoized(i) for i in range(n)]
