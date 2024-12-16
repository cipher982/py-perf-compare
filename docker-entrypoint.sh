#!/bin/bash
set -e

# Function to run benchmarks with specific Python implementation
run_benchmarks() {
    implementation=$1
    venv_path=$2
    echo "Running benchmarks with $implementation..."
    
    # Set up environment variables
    export PATH="$venv_path/bin:$PATH"
    export PYTHONPATH=/app
    
    # Run benchmarks
    if [ "$implementation" = "pypy" ]; then
        pypy3 run_benchmarks.py "$implementation"
    else
        python run_benchmarks.py "$implementation"
    fi
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
