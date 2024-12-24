#!/bin/bash
set -e

# Get the implementation name (first argument)
IMPLEMENTATION=$1
shift  # Remove first argument, leaving remaining args

case "$IMPLEMENTATION" in
  "all")
    echo "Running CPython benchmarks..."
    python /app/run_benchmarks.py "cpython" "$@"
    
    echo "Running Cython benchmarks..."
    python /app/run_benchmarks.py "cython" "$@"
    ;;
    
  *)
    echo "Running benchmarks for $IMPLEMENTATION..."
    python /app/run_benchmarks.py "$IMPLEMENTATION" "$@"
    ;;
esac

# Combine and display results
echo "All benchmarks completed. Results saved in /app/results/"
