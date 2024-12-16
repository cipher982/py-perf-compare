# Python Performance Comparison Guide

## Overview
This project provides a comprehensive performance comparison of different Python implementations across various computational tasks, including:
- Pure Python (CPython)
- Cython-optimized
- PyPy-compatible implementations

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
│   ├── cython_mixed_test.pyx   # Cython mixed test
│   ├── pypy_cpu_test.py        # PyPy-compatible CPU-bound test
│   ├── pypy_memory_test.py     # PyPy-compatible memory-bound test
│   └── pypy_mixed_test.py      # PyPy-compatible mixed test
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
- PyPy-compatible

## Prerequisites
- Python 3.8+ (recommended 3.11+)
- UV package manager
- Cython
- NumPy
- PyPy (optional)

## Setup and Installation

### 1. Install UV Package Manager
```bash
pip install uv
```

### 2. Create Virtual Environment
```bash
# Create a new virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install Project Dependencies
```bash
# Install dependencies with UV
uv pip install -e . --system
```

### 4. Install PyPy (Optional)
#### macOS (Homebrew)
```bash
brew install pypy3
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install pypy3
```

### 5. Compile Cython Extensions
```bash
# Compile Cython extensions
python setup.py build_ext --inplace
```

## Running with Docker (Recommended)

The easiest way to run the benchmarks is using Docker, which ensures consistent environments across different Python implementations.

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

This will:
- Create separate environments for CPython and PyPy
- Run all benchmarks
- Save results to the `./results` directory

## Manual Setup (Alternative)

If you prefer not to use Docker, you can set up the environments manually:

### 1. CPython/Cython Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. PyPy Setup
```bash
# Create PyPy virtual environment
pypy3 -m venv .venv-pypy

# Activate PyPy environment
source .venv-pypy/bin/activate  # On Windows: .venv-pypy\Scripts\activate

# Install PyPy-specific dependencies
pip install -r requirements-pypy.txt
pip install -e .
```

### Running Benchmarks
```bash
# Make sure you're in the project root
python run_benchmarks.py
```

## Running Performance Tests

### Comprehensive Benchmark
```bash
python run_benchmarks.py
```

### Specific Implementation Benchmarks
```bash
# Run CPython and PyPy benchmarks
python run_benchmarks.py cpython pypy

# Run only Cython benchmarks
python run_benchmarks.py cython
```

## Available Implementations
- `cpython`: Standard Python implementation
- `cython`: Cython-optimized tests
- `pypy`: PyPy JIT-compiled implementation

### Expected Outputs
- Console output with performance metrics
- Performance comparison graph in `results/performance_comparison_{timestamp}.png`
- Detailed performance log in `performance_test.log`

## Performance Metrics
- Execution time
- Memory usage
- Comparative analysis across implementations

## Troubleshooting

### Cython Compilation Errors
- Ensure C compiler is installed (gcc, clang)
- Install Python development headers:
  ```bash
  # macOS
  brew install python-dev

  # Ubuntu/Debian
  sudo apt-get install python3-dev
  ```

### PyPy Compatibility
- Some libraries may not be fully compatible with PyPy
- Test and verify library support before benchmarking

### Performance Variations
Results may vary based on:
- Hardware specifications
- Python version
- Cython version
- System load

## Contributing
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Run tests and benchmarks
5. Submit a pull request

## License
[Insert License Information]
