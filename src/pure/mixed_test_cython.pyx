"""Cython implementation of mixed CPU/memory test."""
from typing import Dict, List
from cpython.dict cimport PyDict_GetItem, PyDict_SetItem


cdef long long fibonacci_memoized_cy(int n, dict memo) nogil except -1:
    """Optimized Cython implementation of memoized Fibonacci."""
    cdef long long result
    cdef long long prev1, prev2
    
    with gil:
        if n in memo:
            return memo[n]
        
        if n <= 1:
            memo[n] = n
            return n
            
        prev1 = fibonacci_memoized_cy(n - 1, memo)
        prev2 = fibonacci_memoized_cy(n - 2, memo)
        result = prev1 + prev2
        memo[n] = result
        
    return result


def run_mixed_test(int n = 35) -> List[int]:
    """
    Run mixed test calculating Fibonacci sequence with memoization.
    
    Args:
        n: Length of the Fibonacci sequence to calculate (default: 35)
        
    Returns:
        List[int]: List of Fibonacci numbers
    """
    cdef dict memo = {}
    cdef int i
    cdef list result = []
    
    for i in range(n):
        result.append(fibonacci_memoized_cy(i, memo))
        
    return result


if __name__ == "__main__":
    fib_sequence = run_mixed_test()
    print(f"Fibonacci sequence: {fib_sequence}")
    print(f"Length of sequence: {len(fib_sequence)}") 