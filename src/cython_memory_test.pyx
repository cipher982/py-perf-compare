# cython: boundscheck=False, wraparound=False, nonecheck=False

import numpy as np
cimport numpy as np
cimport cython

def matrix_multiply(np.ndarray[double, ndim=2] A, np.ndarray[double, ndim=2] B):
    """Cython-optimized matrix multiplication."""
    cdef int rows_A = A.shape[0]
    cdef int cols_A = A.shape[1]
    cdef int cols_B = B.shape[1]
    
    # Create result matrix
    cdef np.ndarray[double, ndim=2] result = np.zeros((rows_A, cols_B), dtype=np.float64)
    
    # Perform matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i, j] += A[i, k] * B[k, j]
    
    return result

def generate_matrix(int rows, int cols):
    """Generate a random matrix using NumPy."""
    return np.random.rand(rows, cols)

def run_memory_test(int matrix_size=500):
    """Run memory-bound test with matrix multiplication."""
    A = generate_matrix(matrix_size, matrix_size)
    B = generate_matrix(matrix_size, matrix_size)
    return matrix_multiply(A, B)
