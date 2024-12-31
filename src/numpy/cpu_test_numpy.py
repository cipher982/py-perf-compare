"""NumPy-based implementation of CPU-intensive prime number calculations."""

from typing import List

import numpy as np


def is_prime_array(n: int) -> np.ndarray:
    """
    Generate a boolean array indicating prime numbers up to n using the Sieve of Eratosthenes.

    Args:
        n: Upper bound for prime number calculation

    Returns:
        np.ndarray: Boolean array where True indicates prime numbers
    """
    if n < 2:
        return np.array([], dtype=bool)

    # Initialize boolean array
    sieve = np.ones(n + 1, dtype=bool)
    sieve[0] = sieve[1] = False

    # Use vectorized operations for sieving
    for i in range(2, int(np.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False

    return sieve


def calculate_primes(limit: int) -> List[int]:
    """
    Calculate all prime numbers up to the given limit using NumPy.

    Args:
        limit: Upper bound for prime number calculation

    Returns:
        List[int]: List of prime numbers up to the limit
    """
    sieve = is_prime_array(limit)
    return list(np.nonzero(sieve)[0])


def run_cpu_test(limit: int = 10000) -> List[int]:
    """
    Run CPU-bound test to calculate prime numbers using NumPy.

    Args:
        limit: Upper bound for prime number calculation (default: 10000)

    Returns:
        List[int]: List of calculated prime numbers
    """
    return calculate_primes(limit)


if __name__ == "__main__":
    primes = run_cpu_test()
    print(f"Found {len(primes)} prime numbers.")
