#!/usr/bin/env python3
import sys
import subprocess
import platform
import argparse
import shutil
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('benchmark_runner.log', mode='w')
    ]
)

def find_executable(name):
    """Find executable path for different Python implementations."""
    executables = {
        'cpython': ['python3', 'python'],
        'pypy': ['pypy3', 'pypy'],
        'cython': ['python3', 'python']  # Cython runs through CPython
    }
    
    for exe in executables.get(name, []):
        path = shutil.which(exe)
        if path:
            return path
    return None

def run_benchmark(implementation):
    """Run benchmarks for a specific Python implementation."""
    executable = find_executable(implementation)
    
    if not executable:
        logging.error(f"No {implementation} executable found.")
        return False
    
    logging.info(f"Running benchmarks with {implementation.capitalize()} implementation...")
    logging.info(f"Using executable: {executable}")
    
    # Ensure Cython extensions are built for CPython
    if implementation in ['cpython', 'cython']:
        try:
            logging.info("Building Cython extensions...")
            subprocess.run(['python3', 'setup.py', 'build_ext', '--inplace'], 
                           check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to build Cython extensions: {e.stderr.decode()}")
            return False
    
    try:
        # Run performance runner with real-time logging
        process = subprocess.Popen(
            [executable, 'benchmarks/performance_runner.py'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        
        # Real-time logging of stdout and stderr
        if process.stdout:
            for line in process.stdout:
                logging.info(f"{implementation.upper()} STDOUT: {line.strip()}")
        if process.stderr:
            for line in process.stderr:
                logging.warning(f"{implementation.upper()} STDERR: {line.strip()}")
        
        # Wait for process to complete
        process.wait()
        
        if process.returncode != 0:
            logging.error(f"{implementation.capitalize()} benchmarks failed with return code {process.returncode}")
            return False
        
        return True
    
    except Exception as e:
        logging.error(f"Error running {implementation} benchmarks: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run Python Performance Benchmarks')
    parser.add_argument(
        'implementations', 
        nargs='*', 
        default=['cpython', 'cython', 'pypy'],
        help='Specify which implementations to benchmark (cpython, cython, pypy)'
    )
    
    args = parser.parse_args()
    
    # Validate implementations
    valid_impls = ['cpython', 'cython', 'pypy']
    implementations = [impl for impl in args.implementations if impl in valid_impls]
    
    if not implementations:
        logging.error("No valid implementations specified.")
        sys.exit(1)
    
    # Run benchmarks for specified implementations
    results = {}
    for impl in implementations:
        results[impl] = run_benchmark(impl)
    
    # Summary
    logging.info("\nBenchmark Summary:")
    for impl, success in results.items():
        logging.info(f"{impl.capitalize()}: {'✓ Completed' if success else '✗ Failed'}")
    
    # Check if any benchmarks failed
    if not all(results.values()):
        sys.exit(1)

if __name__ == '__main__':
    main()
