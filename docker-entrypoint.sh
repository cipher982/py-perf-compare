#!/bin/bash

# Install dependencies in both environments if not already installed
setup_environment() {
    echo "Setting up $1 environment..."
    source $2/bin/activate
    pip install -e .
    python setup.py build_ext --inplace
    deactivate
}

# Debug function to show Python executables
debug_python_env() {
    echo "=== Debugging Python environment ==="
    echo "PATH: $PATH"
    echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
    echo "Contents of /venv/pypy/bin:"
    ls -la /venv/pypy/bin
    echo "Contents of /venv/cpython/bin:"
    ls -la /venv/cpython/bin
    echo "Contents of /usr/local/bin:"
    ls -la /usr/local/bin/python* /usr/local/bin/pypy* 2>/dev/null || true
    echo "Contents of /usr/local/lib:"
    ls -la /usr/local/lib/pypy* 2>/dev/null || true
    echo "==========================="
}

# Function to run benchmarks with specific Python implementation
run_benchmarks() {
    implementation=$1
    venv_path=$2
    echo "Running benchmarks with $implementation..."
    
    # Debug before running
    debug_python_env
    
    # Set up environment variables
    export PATH="$venv_path/bin:$PATH"
    
    if [ "$implementation" = "pypy" ]; then
        # For PyPy, use the system PyPy
        PYTHON_CMD="pypy3"
    else
        # For CPython, use the copied executable
        PYTHON_CMD="/usr/local/bin/python"
    fi
    
    echo "Using Python command: $PYTHON_CMD"
    echo "Implementation check:"
    $PYTHON_CMD -c "import sys; print(f'Running with {sys.implementation.name}')"
    
    # Run benchmarks with error handling
    if ! $PYTHON_CMD run_benchmarks.py "$implementation"; then
        echo "Error: Benchmarks for $implementation failed"
    fi
}

# Set up environments if needed
setup_environment "CPython" "/venv/cpython"
setup_environment "PyPy" "/venv/pypy"

# Create results directory if it doesn't exist
mkdir -p /app/results

# Run benchmarks for each implementation
run_benchmarks "cpython" "/venv/cpython"
run_benchmarks "pypy" "/venv/pypy"

# Copy results to mounted volume
cp /app/results/* /results/ || echo "Error: Failed to copy results"
