#!/usr/bin/env python3
import argparse
import logging
import os
import shutil
import subprocess
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("benchmark_runner.log", mode="w"),
    ],
)


def find_executable(name):
    """Find executable path for different Python implementations."""
    executables = {
        "cpython": ["python3", "python"],
        "pypy": ["pypy3", "pypy"],
        "cython": ["python3", "python"],  # Cython runs through CPython
    }

    for exe in executables.get(name, []):
        path = shutil.which(exe)
        if path:
            return path
    return None


def run_benchmark(implementation, runs=30, cpu_limit=10000, memory_size=1000, mixed_size=1000, verbose=False):
    """Run benchmarks for a specific Python implementation."""
    executable = find_executable(implementation)

    if not executable:
        logging.error(f"No {implementation} executable found.")
        return False

    logging.info(f"Running benchmarks with {implementation.capitalize()} implementation...")
    logging.info(f"Using executable: {executable}")

    # Construct command with all arguments
    cmd = [
        executable,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmarks", "performance_runner.py"),
        implementation,
        "--runs",
        str(runs),
        "--cpu-limit",
        str(cpu_limit),
        "--memory-size",
        str(memory_size),
        "--mixed-size",
        str(mixed_size),
    ]

    # Add verbose flag if specified
    if verbose:
        cmd.append("-v")

    try:
        # Run the benchmark with a timeout of 1 hour (3600 seconds)
        logging.info(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=3600)

        # Log output
        logging.info("Benchmark Output:")
        logging.info(result.stdout)

        if result.stderr:
            logging.warning("Benchmark Errors:")
            logging.warning(result.stderr)

        return True

    except subprocess.TimeoutExpired:
        logging.error("Benchmark timed out after 1 hour")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Benchmark failed with exit code {e.returncode}")
        logging.error("STDOUT:")
        logging.error(e.stdout)
        logging.error("STDERR:")
        logging.error(e.stderr)
        return False
    except Exception as e:
        logging.error(f"Unexpected error during benchmark: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main function to run benchmarks."""
    parser = argparse.ArgumentParser(
        description="Python Performance Benchmarks", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "implementation",
        nargs="?",
        default="cpython",
        help="""Python implementation to benchmark
Choices: 
- cpython (Standard Python)
- pypy (PyPy JIT-compiled implementation)""",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=30,
        help="""Number of times to run each benchmark
Default: 30
Recommended for quick test: 3-5
Example: --runs 5 (faster, less statistically significant)""",
    )
    parser.add_argument(
        "--cpu-limit",
        type=int,
        default=10000,
        help="""Limit for CPU-bound test (prime number calculation)
- Determines the upper bound for prime number calculation
- Smaller number = faster test
- Default: 10000
- Quick test example: --cpu-limit 100""",
    )
    parser.add_argument(
        "--memory-size",
        type=int,
        default=1000,
        help="""Size for memory-bound test
- Controls matrix size or memory allocation
- Smaller number = less memory and faster test
- Default: 1000
- Quick test example: --memory-size 10""",
    )
    parser.add_argument(
        "--mixed-size",
        type=int,
        default=1000,
        help="""Size for mixed test (Fibonacci with memoization)
- Controls the Fibonacci sequence length
- Smaller number = faster test
- Default: 1000
- Quick test example: --mixed-size 10""",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed logging and debug information")

    args = parser.parse_args()

    # Run the benchmark
    success = run_benchmark(
        implementation=args.implementation,
        runs=args.runs,
        cpu_limit=args.cpu_limit,
        memory_size=args.memory_size,
        mixed_size=args.mixed_size,
        verbose=args.verbose,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
