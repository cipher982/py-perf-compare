"""Cython implementation of CPU-intensive prime number calculations."""
from typing import List
from cpython cimport array
import array

# Declare C-level types for better performance
cdef bint is_prime_cy(int n) nogil:
    """Optimized Cython implementation of primality test."""
    cdef int i
    
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


def calculate_primes(int limit) -> List[int]:
    """
    Calculate all prime numbers up to the given limit using Cython optimizations.
    
    Args:
        limit: Upper bound for prime number calculation
        
    Returns:
        List[int]: List of prime numbers up to the limit
    """
    # Create array for collecting primes
    cdef array.array result = array.array('i', [])
    cdef int num
    cdef int prime
    cdef list primes = []
    
    with nogil:
        for num in range(2, limit + 1):
            if is_prime_cy(num):
                with gil:
                    primes.append(num)
                    
    return primes


def run_cpu_test(int limit = 10000) -> List[int]:
    """
    Run CPU-bound test to calculate prime numbers using Cython.
    
    Args:
        limit: Upper bound for prime number calculation (default: 10000)
        
    Returns:
        List[int]: List of calculated prime numbers
    """
    return calculate_primes(limit) 