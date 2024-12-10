# Python Performance Comparison Guide

## Overview
This project provides a comprehensive performance comparison of different Python implementations across various computational tasks.

## Project Structure
```
python-tests/
│
├── src/
│   ├── cpu_test.py             # Pure Python CPU-bound test
│   ├── memory_test.py          # Pure Python memory-bound test
│   ├── mixed_test.py           # Pure Python mixed test
│   ├── cython_cpu_test.pyx     # Cython CPU-bound test
│   ├── cython_memory_test.pyx  # Cython memory-bound test
│   └── cython_mixed_test.pyx   # Cython mixed test
│
├── benchmarks/
│   └── performance_runner.py   # Performance measurement script
│
├── pyproject.toml              # Project configuration and dependencies
├── setup.py                    # Cython extension build configuration
└── README.md                   # Project documentation
```

## Test Cases
1. **CPU-bound Test**: Calculate prime numbers
2. **Memory-bound Test**: Matrix multiplication
3. **Mixed Test**: Fibonacci sequence with memoization

## Implementation Methods
- Pure Python (CPython)
- Cython-optimized
- (Optional) PyPy
- (Optional) Nuitka compilation

## Prerequisites
- Python 3.8+
- UV package manager (recommended)
- Cython
- NumPy

## Setup and Installation

### Using UV (Recommended)
1. Install UV package manager
```bash
pip install uv
```

2. Install project dependencies
```bash
uv pip install -e . --compile
```

### Manual Setup
1. Install dependencies
```bash
pip install numpy cython memory-profiler psutil matplotlib nuitka
```

2. Compile Cython extensions
```bash
python setup.py build_ext --inplace
```

## Running Performance Tests
```bash
python benchmarks/performance_runner.py
```

### Expected Outputs
- Console output with performance metrics
- Performance comparison graph in `results/performance_comparison.png`

## Performance Metrics
- Execution time
- Memory usage
- Comparative analysis across different implementations

## Troubleshooting
- Ensure all dependencies are correctly installed
- Check Python and NumPy versions compatibility
- Verify Cython extension compilation

## Contributing
Contributions, issues, and feature requests are welcome!
