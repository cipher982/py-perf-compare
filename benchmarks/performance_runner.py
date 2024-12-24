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


def measure_performance(func, *args, num_runs=30):
    """Measure performance metrics for a given function."""
    logging.info(f"Starting performance measurement for {func.__module__}.{func.__name__}")
    logging.info(f"Arguments: {args}")

    times = []
    memory_usages = []

    for run in range(num_runs):
        logging.debug(f"Run {run + 1}/{num_runs}")

        # Time measurement
        start_time = timeit.default_timer()
        func(*args)
        end_time = timeit.default_timer()
        run_time = end_time - start_time
        times.append(run_time)

        logging.debug(f"Run time: {run_time:.4f} seconds")

        # Memory measurement
        memory_usage = memory_profiler.memory_usage((func, args), max_iterations=1)
        memory_usages.append(memory_usage[0])
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


def run_benchmarks(implementation="cpython"):
    """Run performance benchmarks for all test cases."""
    logging.info(f"Running benchmarks with {implementation} implementation...")
    logging.info(f"Using executable: {sys.executable}")
    logging.info("Building Cython extensions...")

    # Determine which test modules to use based on implementation
    if implementation == "cpython":
        test_modules = [
            (cpu_test.run_cpu_test, "CPU Test"),
            (memory_test.run_memory_test, "Memory Test"),
            (mixed_test.run_mixed_test, "Mixed Test"),
        ]
        if cython_cpu_test:
            test_modules.append((cython_cpu_test.run_cpu_test, "Cython CPU Test"))
        if cython_memory_test:
            test_modules.append((cython_memory_test.run_memory_test, "Cython Memory Test"))
        if cython_mixed_test:
            test_modules.append((cython_mixed_test.run_mixed_test, "Cython Mixed Test"))
    elif implementation == "pypy":
        test_modules = [
            (pypy_cpu_test.run_cpu_test, "PyPy CPU Test"),
            (pypy_memory_test.run_memory_test, "PyPy Memory Test"),
            (pypy_mixed_test.run_mixed_test, "PyPy Mixed Test"),
        ]
    else:
        logging.error(f"Invalid implementation: {implementation}")
        return

    # Create results directory
    results_dir = f"/app/results/{implementation}"
    shutil.rmtree(results_dir, ignore_errors=True)
    shutil.os.makedirs(results_dir, exist_ok=True)

    # Run benchmarks
    for test_func, test_name in test_modules:
        try:
            logging.info(f"Running {test_name}")
            avg_time, std_time, avg_memory, std_memory = measure_performance(test_func, 10000)

            # Save results to CSV
            results_file = f"{results_dir}/{test_name.lower().replace(' ', '_')}_results.csv"
            with open(results_file, "w") as f:
                f.write("Metric,Value,Std Dev\n")
                f.write(f"Time (seconds),{avg_time},{std_time}\n")
                f.write(f"Memory (MiB),{avg_memory},{std_memory}\n")

        except Exception as e:
            logging.error(f"Error running {test_name}: {e}")


def main():
    """Main function to run benchmarks."""
    implementation = sys.argv[1] if len(sys.argv) > 1 else "cpython"
    run_benchmarks(implementation)


if __name__ == "__main__":
    main()
