"""Pure Python implementation of CPU-intensive prime number calculations."""

from typing import List


def is_prime(n: int) -> bool:
    """
    Determine if a number is prime using 6k ± 1 optimization.

    Args:
        n: The number to test for primality

    Returns:
        bool: True if the number is prime, False otherwise
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def calculate_primes(limit: int) -> List[int]:
    """
    Calculate all prime numbers up to the given limit.

    Args:
        limit: Upper bound for prime number calculation

    Returns:
        List[int]: List of prime numbers up to the limit
    """
    return [num for num in range(2, limit + 1) if is_prime(num)]


def run_cpu_test(limit: int) -> List[int]:
    """
    Run CPU-bound test to calculate prime numbers.

    Args:
        limit: Upper bound for prime number calculation

    Returns:
        List[int]: List of calculated prime numbers
    """
    return calculate_primes(limit)


if __name__ == "__main__":
    primes = run_cpu_test(10000)
    print(f"Found {len(primes)} prime numbers.")
