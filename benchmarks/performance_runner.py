import argparse
import logging
import shutil
import statistics
import sys
import timeit

import memory_profiler

from src import cpu_test
from src import cython_cpu_test
from src import cython_memory_test
from src import cython_mixed_test
from src import memory_test
from src import mixed_test
from src import pypy_cpu_test
from src import pypy_memory_test
from src import pypy_mixed_test

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("performance_test.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def measure_performance(func, *args, num_runs=30, verbose=False):
    """Measure performance metrics for a given function."""
    logging.info(f"Starting performance measurement for {func.__module__}.{func.__name__}")
    logging.info(f"Arguments: {args}")

    times = []
    memory_usages = []

    for run in range(num_runs):
        if verbose:
            logging.debug(f"Run {run + 1}/{num_runs}")

        # Time measurement
        start_time = timeit.default_timer()
        result = func(*args)
        end_time = timeit.default_timer()
        run_time = end_time - start_time
        times.append(run_time)

        if verbose:
            logging.debug(f"Run time: {run_time:.4f} seconds")
            logging.debug(f"Result length/value: {len(result) if hasattr(result, '__len__') else result}")

        # Memory measurement
        memory_usage = memory_profiler.memory_usage((func, args), max_iterations=1)
        memory_usages.append(memory_usage[0])

        if verbose:
            logging.debug(f"Memory usage: {memory_usage[0]:.4f} MiB")

    # Compute statistics
    avg_time = statistics.mean(times)
    std_time = statistics.stdev(times) if len(times) > 1 else 0
    avg_memory = statistics.mean(memory_usages)
    std_memory = statistics.stdev(memory_usages) if len(memory_usages) > 1 else 0

    logging.info("Performance Summary:")
    logging.info(f"  Average Time: {avg_time:.4f} ± {std_time:.4f} seconds")
    logging.info(f"  Average Memory: {avg_memory:.4f} ± {std_memory:.4f} MiB")

    return avg_time, std_time, avg_memory, std_memory


def run_benchmarks(
    implementation="cpython", num_runs=30, cpu_limit=10000, memory_size=1000, mixed_size=1000, verbose=False
):
    """Run performance benchmarks for all test cases."""
    logging.info(f"Running benchmarks with {implementation} implementation...")
    logging.info(f"Using executable: {sys.executable}")
    logging.info(f"Number of runs: {num_runs}")
    logging.info(f"CPU test limit: {cpu_limit}")
    logging.info(f"Memory test size: {memory_size}")
    logging.info(f"Mixed test size: {mixed_size}")

    # Determine which test modules to use based on implementation
    if implementation == "cpython":
        test_modules = [
            (cpu_test.run_cpu_test, "CPU Test", (cpu_limit,)),
            (memory_test.run_memory_test, "Memory Test", (memory_size,)),
            (mixed_test.run_mixed_test, "Mixed Test", (mixed_size,)),
        ]
        if cython_cpu_test:
            test_modules.append((cython_cpu_test.run_cpu_test, "Cython CPU Test", (cpu_limit,)))
        if cython_memory_test:
            test_modules.append((cython_memory_test.run_memory_test, "Cython Memory Test", (memory_size,)))
        if cython_mixed_test:
            test_modules.append((cython_mixed_test.run_mixed_test, "Cython Mixed Test", (mixed_size,)))
    elif implementation == "pypy":
        test_modules = [
            (pypy_cpu_test.run_cpu_test, "PyPy CPU Test", (cpu_limit,)),
            (pypy_memory_test.run_memory_test, "PyPy Memory Test", (memory_size,)),
            (pypy_mixed_test.run_mixed_test, "PyPy Mixed Test", (mixed_size,)),
        ]
    else:
        logging.error(f"Invalid implementation: {implementation}")
        return

    # Create results directory
    results_dir = f"/app/results/{implementation}"
    shutil.rmtree(results_dir, ignore_errors=True)
    shutil.os.makedirs(results_dir, exist_ok=True)

    # Run benchmarks
    for test_func, test_name, test_args in test_modules:
        try:
            logging.info(f"Running {test_name}")
            avg_time, std_time, avg_memory, std_memory = measure_performance(
                test_func, *test_args, num_runs=num_runs, verbose=verbose
            )

            # Save results to CSV
            results_file = f"{results_dir}/{test_name.lower().replace(' ', '_')}_results.csv"
            with open(results_file, "w") as f:
                f.write("Metric,Value,Std Dev\n")
                f.write(f"Time (seconds),{avg_time},{std_time}\n")
                f.write(f"Memory (MiB),{avg_memory},{std_memory}\n")

        except Exception as e:
            logging.error(f"Error running {test_name}: {e}")
            import traceback

            traceback.print_exc()


def main():
    """Main function to run benchmarks."""
    parser = argparse.ArgumentParser(description="Python Performance Benchmarks")
    parser.add_argument(
        "implementation", nargs="?", default="cpython", help="Python implementation to benchmark (cpython or pypy)"
    )
    parser.add_argument("--runs", type=int, default=30, help="Number of benchmark runs")
    parser.add_argument("--cpu-limit", type=int, default=10000, help="Limit for CPU-bound test (prime calculation)")
    parser.add_argument("--memory-size", type=int, default=1000, help="Size for memory-bound test")
    parser.add_argument("--mixed-size", type=int, default=1000, help="Size for mixed test")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    # Parse known args to handle potential extra arguments
    args, unknown = parser.parse_known_args()

    # Configure logging level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate implementation if provided
    if args.implementation not in ["cpython", "pypy"]:
        logging.warning(f"Invalid implementation '{args.implementation}'. Defaulting to cpython.")
        args.implementation = "cpython"

    run_benchmarks(
        implementation=args.implementation,
        num_runs=args.runs,
        cpu_limit=args.cpu_limit,
        memory_size=args.memory_size,
        mixed_size=args.mixed_size,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
