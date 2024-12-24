#!/bin/bash

# Argument is the implementation to run (cpython or pypy)
IMPLEMENTATION=${1:-cpython}

# Activate the appropriate virtual environment
if [ "$IMPLEMENTATION" = "cpython" ]; then
    . /venv/bin/activate
    PYTHON_CMD="python"
elif [ "$IMPLEMENTATION" = "pypy" ]; then
    . /venv/bin/activate
    PYTHON_CMD="pypy3"
else
    echo "Invalid implementation. Use 'cpython' or 'pypy'."
    exit 1
fi

# Create results directory
mkdir -p /app/results

# Run the benchmarks
echo "Running benchmarks with $IMPLEMENTATION..."
cd /app/benchmarks
$PYTHON_CMD performance_runner.py "$IMPLEMENTATION"

# Copy results to mounted volume
cp -r /app/results/* /results/ 2>/dev/null || echo "Error: Failed to copy results"
