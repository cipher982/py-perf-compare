import numpy as np


def matrix_multiply(A, B):
    """Perform matrix multiplication using NumPy."""
    return np.dot(A, B)


def generate_matrix(rows, cols):
    """Generate a random matrix using NumPy."""
    return np.random.rand(rows, cols)


def run_memory_test(matrix_size=500):
    """Run memory-bound test with NumPy matrix multiplication."""
    A = generate_matrix(matrix_size, matrix_size)
    B = generate_matrix(matrix_size, matrix_size)
    return matrix_multiply(A, B)


if __name__ == "__main__":
    result = run_memory_test()
    print(f"Matrix multiplication completed. Result matrix shape: {result.shape}")
