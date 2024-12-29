# cython: boundscheck=False, wraparound=False, nonecheck=False
import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free

def matrix_multiply_pure(double[:, :] A, double[:, :] B):
    """Cython-optimized pure matrix multiplication."""
    cdef int rows_A = A.shape[0]
    cdef int cols_A = A.shape[1]
    cdef int cols_B = B.shape[1]
    
    # Create result matrix
    cdef double[:, :] result = np.zeros((rows_A, cols_B))
    
    cdef int i, j, k
    cdef double temp
    
    # Perform matrix multiplication with static typing
    for i in range(rows_A):
        for j in range(cols_B):
            temp = 0
            for k in range(cols_A):
                temp += A[i, k] * B[k, j]
            result[i, j] = temp
    
    return np.asarray(result)

def matrix_multiply_numpy(np.ndarray[double, ndim=2] A, np.ndarray[double, ndim=2] B):
    """Cython-optimized NumPy matrix multiplication."""
    return np.dot(A, B)

def generate_matrix_pure(int rows, int cols):
    """Generate a random matrix using Cython optimizations."""
    return np.random.rand(rows, cols)

def generate_matrix_numpy(int rows, int cols):
    """Generate a random matrix using NumPy."""
    return np.random.rand(rows, cols)

def run_memory_test_pure(int matrix_size=500):
    """Run memory-bound test with Cython-optimized pure multiplication."""
    cdef np.ndarray[double, ndim=2] A = generate_matrix_pure(matrix_size, matrix_size)
    cdef np.ndarray[double, ndim=2] B = generate_matrix_pure(matrix_size, matrix_size)
    return matrix_multiply_pure(A, B)

def run_memory_test_numpy(int matrix_size=500):
    """Run memory-bound test with NumPy matrix multiplication."""
    cdef np.ndarray[double, ndim=2] A = generate_matrix_numpy(matrix_size, matrix_size)
    cdef np.ndarray[double, ndim=2] B = generate_matrix_numpy(matrix_size, matrix_size)
    return matrix_multiply_numpy(A, B)

def run_memory_test(int matrix_size=500, bint use_numpy=False):
    """Run memory-bound test with configurable backend."""
    return run_memory_test_numpy(matrix_size) if use_numpy else run_memory_test_pure(matrix_size)
