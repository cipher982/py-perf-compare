# cython: boundscheck=False, wraparound=False, nonecheck=False
import numpy as np
cimport numpy as np

def matrix_multiply(np.ndarray[double, ndim=2] A, np.ndarray[double, ndim=2] B):
    """Cython-optimized NumPy matrix multiplication."""
    return np.dot(A, B)

def generate_matrix(int rows, int cols):
    """Generate a random matrix using NumPy."""
    return np.random.rand(rows, cols)

def run_memory_test(int matrix_size=500):
    """Run memory-bound test with NumPy matrix multiplication."""
    cdef np.ndarray[double, ndim=2] A = generate_matrix(matrix_size, matrix_size)
    cdef np.ndarray[double, ndim=2] B = generate_matrix(matrix_size, matrix_size)
    return matrix_multiply(A, B) 