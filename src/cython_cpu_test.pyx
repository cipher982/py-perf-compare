# cython: boundscheck=False, wraparound=False, nonecheck=False

def is_prime(int n):
    """Cython-optimized prime number check."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def calculate_primes(int limit):
    """Cython-optimized prime calculation."""
    return [num for num in range(2, limit + 1) if is_prime(num)]

def run_cpu_test(int limit=10000):
    """Run CPU-bound test to calculate primes."""
    return calculate_primes(limit)
