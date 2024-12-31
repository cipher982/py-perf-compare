# cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt
from libc.time cimport time
from libc.stdlib cimport rand, RAND_MAX, srand

cdef double** create_matrix(int rows, int cols):
    """Create a 2D matrix using C arrays."""
    cdef double** matrix = <double**>malloc(rows * sizeof(double*))
    cdef int i
    for i in range(rows):
        matrix[i] = <double*>malloc(cols * sizeof(double))
    return matrix

cdef void free_matrix(double** matrix, int rows):
    """Free a 2D matrix."""
    cdef int i
    for i in range(rows):
        free(matrix[i])
    free(matrix)

cdef double** matrix_multiply(double** A, double** B, int rows_A, int cols_A, int cols_B):
    """Perform matrix multiplication using C arrays."""
    cdef double** result = create_matrix(rows_A, cols_B)
    cdef int i, j, k
    cdef double temp
    
    for i in range(rows_A):
        for j in range(cols_B):
            temp = 0
            for k in range(cols_A):
                temp += A[i][k] * B[k][j]
            result[i][j] = temp
    
    return result

cdef double** generate_matrix(int rows, int cols):
    """Generate a random matrix using C random number generator."""
    cdef double** matrix = create_matrix(rows, cols)
    cdef int i, j
    
    # Seed random number generator
    srand(time(NULL))
    
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = rand() / float(RAND_MAX)
    
    return matrix

def run_memory_test(int matrix_size=500):
    """Run memory-bound test with pure C matrix multiplication."""
    # Generate matrices
    cdef double** A = generate_matrix(matrix_size, matrix_size)
    cdef double** B = generate_matrix(matrix_size, matrix_size)
    
    # Perform multiplication
    cdef double** result = matrix_multiply(A, B, matrix_size, matrix_size, matrix_size)
    
    # Convert result to Python list before freeing memory
    cdef int i, j
    python_result = [[result[i][j] for j in range(matrix_size)] for i in range(matrix_size)]
    
    # Free all matrices
    free_matrix(A, matrix_size)
    free_matrix(B, matrix_size)
    free_matrix(result, matrix_size)
    
    return python_result 