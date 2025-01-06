import random

import numpy as np


def matrix_multiply_pure(A, B):
    """Perform matrix multiplication without NumPy."""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("Incompatible matrix dimensions")

    # Initialize result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Perform matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result


def matrix_multiply_numpy(A, B):
    """Perform matrix multiplication using NumPy."""
    return np.dot(A, B)


def generate_matrix_pure(rows, cols):
    """Generate a random matrix without NumPy."""
    return [[random.uniform(0, 1) for _ in range(cols)] for _ in range(rows)]


def generate_matrix_numpy(rows, cols):
    """Generate a random matrix using NumPy."""
    return np.random.rand(rows, cols)


def run_memory_test_pure(matrix_size):
    """Run memory test using pure Python implementation."""
    A = generate_matrix_pure(matrix_size, matrix_size)
    B = generate_matrix_pure(matrix_size, matrix_size)
    return matrix_multiply_pure(A, B)


def run_memory_test_numpy(matrix_size):
    """Run memory test using NumPy implementation."""
    A = generate_matrix_numpy(matrix_size, matrix_size)
    B = generate_matrix_numpy(matrix_size, matrix_size)
    return matrix_multiply_numpy(A, B)


def run_memory_test(matrix_size, use_numpy):
    """Run memory test with specified implementation."""
    if use_numpy:
        return run_memory_test_numpy(matrix_size)
    return run_memory_test_pure(matrix_size)


if __name__ == "__main__":
    result = run_memory_test(500, False)
    print(f"Matrix multiplication completed. Result matrix size: {len(result)}x{len(result[0])}")
