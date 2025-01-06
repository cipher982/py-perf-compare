#!/bin/bash
set -e

# Enhanced logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$level] $message"
}

# Function to compile Cython files if needed
compile_cython() {
    if [ "$IMPLEMENTATION" = "cpython" ]; then
        log "INFO" "Compiling Cython files..."
        cd /app
        python setup.py build_ext --inplace
        cd - > /dev/null
    fi
}

# Get the implementation name (first argument)
IMPLEMENTATION=$1
shift  # Remove first argument, leaving remaining args

# Ensure results directory exists with proper permissions
mkdir -p /results/{cpython,pypy}/pure /results/{cpython,pypy}/numpy
chmod -R 777 /results

# List of valid implementations
VALID_IMPLEMENTATIONS=("cpython" "pypy" "all")

# Check if the implementation is valid
if [[ ! " ${VALID_IMPLEMENTATIONS[@]} " =~ " ${IMPLEMENTATION} " ]]; then
    log "ERROR" "Invalid implementation. Must be one of: ${VALID_IMPLEMENTATIONS[*]}"
    exit 1
fi

# Compile Cython files if needed
compile_cython

# Start timestamp for entire benchmark run
START_TIME=$(date +%s)
log "INFO" "Starting benchmark suite for implementation: $IMPLEMENTATION"

case "$IMPLEMENTATION" in
    "all")
        log "INFO" "Running benchmarks for all implementations..."
        for impl in "cpython" "pypy"; do
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

# Process results
log "INFO" "Processing results..."
python /app/benchmarks/results_processor.py /results/

# Display results structure
log "INFO" "Results saved in /results/"
ls -R /results/
