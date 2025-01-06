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
    if [ "$IMPLEMENTATION" = "cython" ]; then
        log "INFO" "Compiling Cython files..."
        cd /app
        python setup.py build_ext --inplace
        cd - > /dev/null
    fi
}

# Ensure results directory exists with proper permissions
mkdir -p /results/{cpython,cython,pypy}/{pure,numpy}
chmod -R 777 /results

# List of valid implementations
VALID_IMPLEMENTATIONS=("cpython" "cython" "pypy" "all")

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

# Build the common arguments string
ARGS="--runs ${RUNS} --prime-upper-bound ${PRIME_UPPER_BOUND} --matrix-dimension ${MATRIX_DIMENSION} --fibonacci-length ${FIBONACCI_LENGTH}"

case "$IMPLEMENTATION" in
    "all")
        log "INFO" "Running benchmarks for all implementations..."
        for impl in "cpython" "cython" "pypy"; do
            log "INFO" "Starting benchmarks for $impl"
            python /app/benchmarks/performance_runner.py "$impl" $ARGS
        done
        
        # Only process results in benchmark-controller
        log "INFO" "Processing results..."
        python /app/benchmarks/results_processor.py /results/
        ;;
    *)
        log "INFO" "Running benchmarks for $IMPLEMENTATION"
        python /app/benchmarks/performance_runner.py "$IMPLEMENTATION" $ARGS
        ;;
esac

# End timestamp and calculate total duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

log "INFO" "All benchmarks completed for $IMPLEMENTATION"
log "INFO" "Total benchmark duration: $DURATION seconds"

# Display results structure
log "INFO" "Results saved in /results/"
ls -R /results/
