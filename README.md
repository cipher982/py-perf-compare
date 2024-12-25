# Python Performance Comparison

## Project Goals
A benchmarking suite that compares performance across different Python implementations (CPython, Cython, PyPy) for various computational tasks. The project uses Docker to ensure consistent testing environments and reproducible results.

## Overview
This project provides performance comparisons across three types of computational tasks:
- CPU-bound operations (prime number calculations)
- Memory-bound operations (matrix multiplication)
- Mixed operations (Fibonacci sequence with memoization)

Each task is implemented in:
- Pure Python (CPython)
- Cython-optimized code
- PyPy-compatible implementations

## Project Structure
```
.
├── benchmarks/
│   └── performance_runner.py    # Performance measurement script
├── src/
│   ├── cpu_test.py             # Pure Python CPU-bound test
│   ├── memory_test.py          # Pure Python memory-bound test
│   ├── mixed_test.py           # Pure Python mixed test
│   ├── cython_cpu_test.pyx     # Cython CPU-bound test
│   ├── cython_memory_test.pyx  # Cython memory-bound test
│   ├── cython_mixed_test.pyx   # Cython mixed test
│   ├── pypy_cpu_test.py        # PyPy-compatible CPU-bound test
│   ├── pypy_memory_test.py     # PyPy-compatible memory-bound test
│   └── pypy_mixed_test.py      # PyPy-compatible mixed test
├── docker/
│   ├── Dockerfile.cpython      # CPython environment
│   └── Dockerfile.pypy         # PyPy environment
├── docker-compose.yml          # Docker services configuration
├── docker-entrypoint.sh        # Container startup script
├── pyproject.toml             # Project configuration
├── requirements-pypy.txt      # PyPy-specific dependencies
├── run_benchmarks.py          # Main benchmark runner
└── .gitignore                # Git ignore patterns
```

## Prerequisites
- Docker
- Docker Compose

That's it! All other dependencies are handled by Docker.

## Running Benchmarks

### Quick Start with Docker (Recommended)
```bash
# Build and run all benchmarks
docker compose up --build

# View results in ./results directory
```

The benchmarks will run in parallel across two containers:
- `cpython`: Running CPython and Cython tests
- `pypy`: Running PyPy tests

Results will be saved to:
- `./results/cpython/` - CPython and Cython results
- `./results/pypy/` - PyPy results

### Benchmark Types

#### CPU-bound Test
Measures pure computational performance through prime number calculations.
- Implementation: Sieve of Eratosthenes algorithm
- Metrics: Raw computation speed
- Expected results: [Placeholder for typical performance patterns]

#### Memory-bound Test
Evaluates memory handling through matrix operations.
- Implementation: Matrix multiplication without NumPy
- Metrics: Memory usage and operation speed
- Expected results: [Placeholder for typical performance patterns]

#### Mixed Test
Tests both CPU and memory performance using Fibonacci sequence.
- Implementation: Fibonacci with memoization
- Metrics: Combined CPU and memory performance
- Expected results: [Placeholder for typical performance patterns]

## Results Interpretation
[Placeholder for how to interpret benchmark results]
