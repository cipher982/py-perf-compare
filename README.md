# Python Performance Comparison

## Project Goals
A benchmarking suite that compares performance across different Python implementations (CPython, Cython, PyPy) for various computational tasks. The project uses Docker to ensure consistent testing environments and reproducible results.

## Overview
This project provides performance comparisons across three types of computational tasks:
- CPU-bound operations (prime number calculations)
- Memory-bound operations (matrix multiplication)
- Mixed operations (Fibonacci sequence with memoization)

## Project Structure
```
.
├── benchmarks/
│   ├── performance_runner.py    # Performance measurement script
│   └── results_processor.py     # Results processing and visualization
├── src/
│   ├── pure/                    # Pure Python implementations
│   │   ├── cpu_test_python.py   # Pure Python CPU-bound test
│   │   ├── cpu_test_cython.pyx  # Cython CPU-bound test
│   │   ├── memory_test_python.py # Pure Python memory-bound test
│   │   ├── memory_test_cython.pyx # Cython memory-bound test
│   │   ├── mixed_test_python.py  # Pure Python mixed test
│   │   └── mixed_test_cython.pyx # Cython mixed test
│   └── numpy/                   # NumPy-optimized implementations
│       ├── cpu_test_numpy.py    # NumPy CPU-bound test
│       ├── cpu_test_cython.pyx  # Cython+NumPy CPU-bound test
│       ├── memory_test_python.py # NumPy memory-bound test
│       └── memory_test_cython.pyx # Cython+NumPy memory-bound test
├── docker/
│   ├── Dockerfile.base         # Base Docker configuration
│   ├── Dockerfile.cpython      # CPython environment
│   └── Dockerfile.pypy         # PyPy environment
├── results/                    # Benchmark results
│   ├── cpython/                # CPython test results
│   ├── pypy/                   # PyPy test results
│   ├── logs/                   # Benchmark run logs
│   └── performance_comparison.png  # Visualization of results
├── docker-compose.yml          # Docker services configuration
├── docker-entrypoint.sh        # Container startup script
├── pyproject.toml             # Project configuration and dependency management
├── setup.py                   # Additional build and setup configurations
├── uv.lock                    # Dependency lock file
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── .env                       # Default benchmark parameters
└── requirements-pypy.txt      # PyPy-specific dependencies
```

## Project Dependencies and Configuration
- **Dependency Management**: 
  - `pyproject.toml`: Primary configuration for project dependencies
  - `uv.lock`: Ensures consistent dependency versions across environments
  - `setup.py`: Additional build and packaging configurations

- **Code Quality**:
  - Pre-commit hooks configured in `.pre-commit-config.yaml`
  - Ensures code style and quality standards

## Benchmark Implementations

### Test Variations
Each computational task is implemented in multiple variations:
- Pure Python implementations
- NumPy-optimized implementations
- Cython-optimized implementations
- PyPy-compatible implementations

### Benchmark Types

#### CPU-bound Test
Measures pure computational performance through prime number calculations.
- Implementation: Sieve of Eratosthenes algorithm
- Metrics: Raw computation speed
- Variations:
  - Pure Python implementation
  - NumPy-accelerated implementation
  - Cython-optimized implementation
  - PyPy-compatible implementation

#### Memory-bound Test
Evaluates memory handling through matrix operations.
- Implementation: Matrix multiplication 
- Metrics: Memory usage and operation speed
- Variations:
  - Pure Python implementation
  - NumPy-accelerated implementation
  - Cython-optimized implementation
  - PyPy-compatible implementation

#### Mixed Test
Tests both CPU and memory performance using Fibonacci sequence.
- Implementation: Iterative Fibonacci calculation
- Metrics: Combined CPU and memory performance
- Variations:
  - Pure Python implementation
  - Cython-optimized implementation
  - PyPy-compatible implementation

## Prerequisites
- Docker
- Docker Compose
- Python 3.11+

## Running Benchmarks

### Quick Start with Docker (Recommended)
```bash
# Run all implementations
IMPLEMENTATION=all RUNS=3 PRIME_UPPER_BOUND=1000000 MATRIX_DIMENSION=200 FIBONACCI_LENGTH=500 docker compose up

# Or run specific implementation
IMPLEMENTATION=cpython RUNS=3 PRIME_UPPER_BOUND=1000000 MATRIX_DIMENSION=200 FIBONACCI_LENGTH=500 docker compose up
```

### Configuration
Default values for all parameters are provided in `.env`. You can override them using environment variables:
- `IMPLEMENTATION`: Target implementation (all, cpython, cython, pypy)
- `RUNS`: Number of test iterations
- `PRIME_UPPER_BOUND`: Upper limit for prime number calculations
- `MATRIX_DIMENSION`: Size of matrices (NxN) for multiplication
- `FIBONACCI_LENGTH`: Number of Fibonacci numbers to calculate

Results will be saved to:
- `./results/cpython/` - CPython and Cython results
- `./results/pypy/` - PyPy results
- `./results/logs/` - Detailed benchmark logs

## Results Interpretation
- Detailed CSV results available for each test type and implementation
- Performance comparison visualizations generated in `results/`
- Comprehensive logging provides in-depth insights into benchmark performance

## License
See the `LICENSE` file for details about project licensing.

## Contributing
Contributions are welcome! Please refer to project guidelines and code of conduct.
