import random


def matrix_multiply(A, B):
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


def generate_matrix(rows, cols):
    """Generate a random matrix."""
    return [[random.uniform(0, 1) for _ in range(cols)] for _ in range(rows)]


def run_memory_test(matrix_size=500):
    """Run memory-bound test with matrix multiplication."""
    A = generate_matrix(matrix_size, matrix_size)
    B = generate_matrix(matrix_size, matrix_size)
    return matrix_multiply(A, B)


if __name__ == "__main__":
    result = run_memory_test()
    print(f"Matrix multiplication completed. Result matrix size: {len(result)}x{len(result[0])}")
