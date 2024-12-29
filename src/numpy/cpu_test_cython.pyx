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
    
    Args:
        n: Upper bound for prime number calculation
        
    Returns:
        np.ndarray: Boolean array where True indicates prime numbers
    """
    if n < 2:
        return np.array([], dtype=bool)
    
    # Initialize boolean array
    cdef np.ndarray[np.uint8_t, ndim=1] sieve = np.ones(n + 1, dtype=np.uint8)
    sieve[0] = sieve[1] = 0
    
    cdef int i, j
    cdef int limit = int(sqrt(n)) + 1
    
    # Optimized sieving with direct memory access
    for i in range(2, limit):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = 0
                
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


def run_cpu_test(int limit = 10000) -> List[int]:
    """
    Run CPU-bound test to calculate prime numbers using Cython-optimized NumPy.
    
    Args:
        limit: Upper bound for prime number calculation (default: 10000)
        
    Returns:
        List[int]: List of calculated prime numbers
    """
    return calculate_primes(limit) 