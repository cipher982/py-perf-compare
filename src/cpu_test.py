def is_prime(n):
    """Efficient primality test using 6k ± 1 optimization."""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check for prime using 6k ± 1 optimization
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def calculate_primes(limit):
    """Calculate all prime numbers up to the given limit."""
    return [num for num in range(2, limit + 1) if is_prime(num)]


def run_cpu_test(limit):
    """Run CPU-bound test to calculate primes."""
    return calculate_primes(limit)


if __name__ == "__main__":
    primes = run_cpu_test(10000)
    print(f"Found {len(primes)} prime numbers.")
