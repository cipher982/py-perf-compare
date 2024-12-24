#!/bin/bash
set -e

# Get the implementation name (first argument)
IMPLEMENTATION=$1
shift  # Remove first argument, leaving remaining args

# Ensure results directory exists
mkdir -p /results/cpython /results/cython /results/pypy

# List of valid implementations
VALID_IMPLEMENTATIONS=("cpython" "cython" "pypy" "all")

# Check if the implementation is valid
if [[ ! " ${VALID_IMPLEMENTATIONS[@]} " =~ " ${IMPLEMENTATION} " ]]; then
    echo "Error: Invalid implementation. Must be one of: ${VALID_IMPLEMENTATIONS[*]}"
    exit 1
fi

case "$IMPLEMENTATION" in
  "all")
    echo "Running all benchmarks..."
    python /app/run_benchmarks.py "cpython" "$@"
    python /app/run_benchmarks.py "cython" "$@"
    python /app/run_benchmarks.py "pypy" "$@"
    ;;
    
  *)
    echo "Running benchmarks for $IMPLEMENTATION..."
    python /app/run_benchmarks.py "$IMPLEMENTATION" "$@"
    ;;
esac

# Combine and display results
echo "All benchmarks completed. Results saved in /results/"
ls -l /results/
