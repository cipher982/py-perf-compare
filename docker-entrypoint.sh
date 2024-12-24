#!/bin/bash
set -e

# Default implementations if none provided
IMPLEMENTATIONS=${@:-cpython pypy cython}

# Run benchmarks for each implementation
for IMPLEMENTATION in $IMPLEMENTATIONS; do
    echo "Running benchmarks for $IMPLEMENTATION..."
    python /app/run_benchmarks.py "$IMPLEMENTATION"
done
