import logging
import shutil
import statistics
import sys
import timeit
from datetime import datetime

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
        try:
            logging.debug(f"Profiling function: {func.__name__}, args: {args}")

            # Create a proper function call tuple for memory_profiler
            func_tuple = (func, args, {})  # (function, args, kwargs)
            mem_usage = memory_profiler.memory_usage(proc=func_tuple, interval=0.1, max_iterations=1)[0]
            memory_usages.append(mem_usage)
            logging.debug(f"Memory usage: {mem_usage:.2f} MB")
        except Exception as e:
            logging.warning(f"Memory profiling failed: {e}", exc_info=True)
            memory_usages.append(0)

    return {
        "mean_time": statistics.mean(times),
        "std_time": statistics.stdev(times) if len(times) > 1 else 0,
        "mean_memory": statistics.mean(memory_usages),
        "std_memory": statistics.stdev(memory_usages) if len(memory_usages) > 1 else 0,
    }


def run_benchmarks():
    """Run performance benchmarks for all test cases and implementations."""
    logging.info("Starting performance benchmarks")

    # Validate PyPy executable
    pypy_executable = shutil.which("pypy3.10")
    if not pypy_executable:
        logging.warning("PyPy executable not found. Skipping PyPy benchmarks.")
        benchmarks = {
            "CPU Test (Python)": (cpu_test.run_cpu_test, 10000),  # Prime number calculation
            "CPU Test (Cython)": (cython_cpu_test.run_cpu_test, 10000),
            "Memory Test (Python)": (memory_test.run_memory_test, 200),  # Matrix size increased for better measurement
            "Memory Test (Cython)": (cython_memory_test.run_memory_test, 200),
            "Mixed Test (Python)": (mixed_test.run_mixed_test, 35),  # Fibonacci sequence
            "Mixed Test (Cython)": (cython_mixed_test.run_mixed_test, 35),
        }
    else:
        benchmarks = {
            "CPU Test (Python)": (cpu_test.run_cpu_test, 10000),  # Prime number calculation
            "CPU Test (Cython)": (cython_cpu_test.run_cpu_test, 10000),
            "CPU Test (PyPy)": (pypy_cpu_test.run_cpu_test, 10000),
            "Memory Test (Python)": (memory_test.run_memory_test, 200),  # Matrix size increased for better measurement
            "Memory Test (Cython)": (cython_memory_test.run_memory_test, 200),
            "Memory Test (PyPy)": (pypy_memory_test.run_memory_test, 200),
            "Mixed Test (Python)": (mixed_test.run_mixed_test, 35),  # Fibonacci sequence
            "Mixed Test (Cython)": (cython_mixed_test.run_mixed_test, 35),
            "Mixed Test (PyPy)": (pypy_mixed_test.run_mixed_test, 35),
        }

    results = {}
    for name, (func, arg) in benchmarks.items():
        logging.info(f"Running benchmark: {name}")
        results[name] = measure_performance(func, arg)

    return results


def main():
    try:
        results = run_benchmarks()

        # Print detailed results
        for name, metrics in results.items():
            logging.info(f"\n{name}:")
            logging.info(f"  Mean Time: {metrics['mean_time']:.4f} ± {metrics['std_time']:.4f} seconds")
            logging.info(f"  Mean Memory: {metrics['mean_memory']:.2f} ± {metrics['std_memory']:.2f} MB")

        # Save results and generate plots
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        from benchmarks.results_processor import plot_results  # type: ignore
        from benchmarks.results_processor import save_results_to_csv  # type: ignore

        # Save to CSV
        csv_path = save_results_to_csv(results, timestamp)
        logging.info(f"\nResults saved to: {csv_path}")

        # Generate plot
        plot_path = plot_results(csv_path)
        logging.info(f"Performance plot saved to: {plot_path}")

        logging.info("Performance benchmarks completed successfully")

    except Exception as e:
        logging.error(f"An error occurred during benchmarking: {e}", exc_info=True)


if __name__ == "__main__":
    import shutil

    main()
