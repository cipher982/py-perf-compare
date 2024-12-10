def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def calculate_primes(limit):
    """Calculate all prime numbers up to the given limit."""
    return [num for num in range(2, limit + 1) if is_prime(num)]

def run_cpu_test(limit=10000):
    """Run CPU-bound test to calculate primes."""
    return calculate_primes(limit)

if __name__ == "__main__":
    primes = run_cpu_test()
    print(f"Found {len(primes)} prime numbers.")
