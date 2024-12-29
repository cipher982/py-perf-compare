#!/bin/bash
set -e

# Enhanced logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$level] $message"
}

# Function to compile Cython files
compile_cython() {
    log "INFO" "Compiling Cython files..."
    cd /app
    python setup.py build_ext --inplace
    cd - > /dev/null
}

# Get the implementation name (first argument)
IMPLEMENTATION=$1
shift  # Remove first argument, leaving remaining args

# Ensure results directory exists
mkdir -p /results/cpython /results/cython /results/pypy

# List of valid implementations
VALID_IMPLEMENTATIONS=("cpython" "cython" "pypy" "all")

# Check if the implementation is valid
if [[ ! " ${VALID_IMPLEMENTATIONS[@]} " =~ " ${IMPLEMENTATION} " ]]; then
    log "ERROR" "Invalid implementation. Must be one of: ${VALID_IMPLEMENTATIONS[*]}"
    exit 1
fi

# Compile Cython files if needed
if [ "$IMPLEMENTATION" = "cython" ] || [ "$IMPLEMENTATION" = "all" ]; then
    compile_cython
fi

# Start timestamp for entire benchmark run
START_TIME=$(date +%s)
log "INFO" "Starting benchmark suite for implementation: $IMPLEMENTATION"

case "$IMPLEMENTATION" in
  "all")
    log "INFO" "Running benchmarks for all implementations..."
    for impl in "cpython" "cython" "pypy"; do
      log "INFO" "Starting benchmarks for $impl"
      python /app/benchmarks/performance_runner.py "$impl" "$@"
      log "INFO" "Completed benchmarks for $impl"
    done
    ;;
    
  *)
    log "INFO" "Running benchmarks for $IMPLEMENTATION"
    python /app/benchmarks/performance_runner.py "$IMPLEMENTATION" "$@"
    ;;
esac

# End timestamp and calculate total duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

log "INFO" "All benchmarks completed for $IMPLEMENTATION"
log "INFO" "Total benchmark duration: $DURATION seconds"

# Combine and display results
log "INFO" "Results saved in /results/"
ls -l /results/
