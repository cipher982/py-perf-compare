def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def calculate_primes(limit):
    """Calculate all prime numbers up to the given limit."""
    return [num for num in range(2, limit + 1) if is_prime(num)]


def run_cpu_test(n):
    """
    Pure Python implementation for CPU test.
    No numpy dependency required.
    """
    result = 0
    for i in range(n):
        result += i * i
    return result


if __name__ == "__main__":
    result = run_cpu_test(10000)
    print(f"Result: {result}")
