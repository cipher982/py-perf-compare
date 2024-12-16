#!/bin/bash
set -e

# Function to run benchmarks with specific Python implementation
run_benchmarks() {
    implementation=$1
    venv_path=$2
    echo "Running benchmarks with $implementation..."
    
    # Activate virtual environment
    source $venv_path/bin/activate
    
    # Run benchmarks
    python run_benchmarks.py "$implementation"
    
    # Deactivate virtual environment
    deactivate
}

# Run benchmarks for each implementation
run_benchmarks "cpython" "/venv/cpython"
run_benchmarks "pypy" "/venv/pypy"

# Copy results to mounted volume if it exists
if [ -d "/results" ]; then
    cp -r results/* /results/
fi
