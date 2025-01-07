"""Cython implementation of CPU-intensive prime number calculations using NumPy."""
from typing import List
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt

# Initialize NumPy C API
np.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
def is_prime_array(int n) -> np.ndarray:
    """
    Generate a boolean array indicating prime numbers up to n using optimized Sieve of Eratosthenes.
    Optimized using NumPy's vectorized operations and broadcasting with Cython enhancements.
    
    Args:
        n: Upper bound for prime number calculation
        
    Returns:
        np.ndarray: Boolean array where True indicates prime numbers
    """
    if n < 2:
        return np.array([], dtype=bool)
    
    # Initialize boolean array with direct memory access
    cdef np.ndarray[np.uint8_t, ndim=1] sieve = np.ones(n + 1, dtype=np.uint8)
    sieve[0] = sieve[1] = 0
    
    # Calculate upper bound once
    cdef int limit = int(sqrt(n)) + 1
    
    # Create array of potential prime factors
    cdef np.ndarray[np.int64_t, ndim=1] p = np.arange(2, limit, dtype=np.int64)
    
    # Use broadcasting with Cython-optimized loop
    cdef int i
    cdef np.ndarray[np.uint8_t, ndim=1] prime_mask = sieve[p].astype(np.uint8)
    for i in p[prime_mask > 0]:
        sieve[i * i::i] = 0
                
    return sieve.astype(bool)


def calculate_primes(int limit) -> List[int]:
    """
    Calculate all prime numbers up to the given limit using Cython-optimized NumPy.
    
    Args:
        limit: Upper bound for prime number calculation
        
    Returns:
        List[int]: List of prime numbers up to the limit
    """
    sieve = is_prime_array(limit)
    return list(np.nonzero(sieve)[0])


def run_cpu_test(limit: int) -> List[int]:
    """
    Run CPU-bound test to calculate prime numbers using NumPy with Cython optimizations.
    
    Args:
        limit: Upper bound for prime number calculation
        
    Returns:
        List[int]: List of calculated prime numbers
    """
    return calculate_primes(limit)


if __name__ == "__main__":
    primes = run_cpu_test(10000)
    print(f"Found {len(primes)} prime numbers.")