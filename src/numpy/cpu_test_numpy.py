"""NumPy-based implementation of CPU-intensive prime number calculations."""

from typing import List

import numpy as np


def is_prime_array(n: int) -> np.ndarray:
    """
    Generate a boolean array indicating prime numbers up to n using the Sieve of Eratosthenes.
    Optimized using NumPy's vectorized operations and broadcasting.

    Args:
        n: Upper bound for prime number calculation

    Returns:
        np.ndarray: Boolean array where True indicates prime numbers
    """
    if n < 2:
        return np.array([], dtype=bool)

    # Initialize boolean array - use uint8 for memory efficiency
    sieve = np.ones(n + 1, dtype=np.uint8)
    sieve[0] = sieve[1] = 0

    # Calculate upper bound once
    limit = int(np.sqrt(n)) + 1

    # Create array of potential prime factors
    p = np.arange(2, limit)

    # Use broadcasting to mark non-primes
    # This creates a mask of all numbers that are multiples of each prime
    # Much faster than iterating and using slice assignment
    for i in p[sieve[p].astype(bool)]:
        sieve[i * i :: i] = 0

    return sieve.astype(bool)


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


def run_cpu_test(limit: int) -> List[int]:
    """
    Run CPU-bound test to calculate prime numbers using NumPy.

    Args:
        limit: Upper bound for prime number calculation

    Returns:
        List[int]: List of calculated prime numbers
    """
    return calculate_primes(limit)


if __name__ == "__main__":
    primes = run_cpu_test(10000)
    print(f"Found {len(primes)} prime numbers.")
