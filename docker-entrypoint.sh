#!/bin/bash
set -e

# Function to verify Python implementation
verify_implementation() {
    implementation=$1
    venv_path=$2
    python_path="$venv_path/bin/python"
    
    # Check if Python exists in the virtual environment
    if [ ! -f "$python_path" ]; then
        echo "Error: Python not found at $python_path"
        exit 1
    }
    
    # Verify Python implementation
    implementation_info=$($python_path -c "import sys; print(sys.implementation.name)")
    
    if [ "$implementation" = "pypy" ] && [ "$implementation_info" != "pypy" ]; then
        echo "Error: Expected PyPy but got $implementation_info implementation"
        exit 1
    elif [ "$implementation" = "cpython" ] && [ "$implementation_info" != "cpython" ]; then
        echo "Error: Expected CPython but got $implementation_info implementation"
        exit 1
    fi
    
    echo "Verified $implementation implementation: $implementation_info"
}

# Function to run benchmarks with specific Python implementation
run_benchmarks() {
    implementation=$1
    venv_path=$2
    echo "Running benchmarks with $implementation..."
    
    # Verify correct implementation before running
    verify_implementation "$implementation" "$venv_path"
    
    # Set up environment variables
    export PATH="$venv_path/bin:$PATH"
    export PYTHONPATH=/app:$PYTHONPATH
    
    # Run benchmarks using python from the virtual environment
    $venv_path/bin/python run_benchmarks.py "$implementation"
}

# Create results directory if it doesn't exist
mkdir -p /app/results

# Run benchmarks for each implementation
run_benchmarks "cpython" "/venv/cpython"
run_benchmarks "pypy" "/venv/pypy"

# Copy results to mounted volume if it exists
if [ -d "/results" ]; then
    cp -r /app/results/* /results/
fi
