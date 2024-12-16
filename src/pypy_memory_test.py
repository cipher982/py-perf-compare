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


def run_memory_test(n):
    """
    Pure Python implementation for memory test.
    No numpy dependency required.
    """
    # Create a list of lists to consume memory
    matrix = []
    for i in range(n):
        row = [j * j for j in range(n)]
        matrix.append(row)

    # Do some operations
    result = 0
    for i in range(n):
        for j in range(n):
            result += matrix[i][j]

    return result


if __name__ == "__main__":
    result = run_memory_test(500)
    print(f"Memory test completed. Result: {result}")
