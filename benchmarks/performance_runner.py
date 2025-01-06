import argparse
import logging
import logging.handlers
import os
import statistics
import sys
import timeit
import traceback
from datetime import datetime

import memory_profiler
from tqdm import tqdm


# Conditional imports based on implementation
def get_imports(implementation):
    if implementation == "cpython":
        from src.numpy.cpu_test_cython import run_cpu_test as numpy_cython_cpu_test
        from src.numpy.memory_test_cython import run_memory_test as numpy_cython_memory_test
        from src.pure.cpu_test_cython import run_cpu_test as pure_cython_cpu_test
        from src.pure.memory_test_cython import run_memory_test as pure_cython_memory_test
        from src.pure.mixed_test_cython import run_mixed_test as pure_cython_mixed_test
    else:
        # Placeholder for no Cython tests
        numpy_cython_cpu_test = None
        numpy_cython_memory_test = None
        pure_cython_cpu_test = None
        pure_cython_memory_test = None
        pure_cython_mixed_test = None

    # Common imports
    from src.numpy.cpu_test_numpy import run_cpu_test as numpy_python_cpu_test
    from src.numpy.memory_test_python import run_memory_test as numpy_python_memory_test
    from src.pure.cpu_test_python import run_cpu_test as pure_python_cpu_test
    from src.pure.memory_test_python import run_memory_test as pure_python_memory_test
    from src.pure.mixed_test_python import run_mixed_test as pure_python_mixed_test

    return {
        "numpy_cython_cpu_test": numpy_cython_cpu_test,
        "numpy_cython_memory_test": numpy_cython_memory_test,
        "pure_cython_cpu_test": pure_cython_cpu_test,
        "pure_cython_memory_test": pure_cython_memory_test,
        "pure_cython_mixed_test": pure_cython_mixed_test,
        "numpy_python_cpu_test": numpy_python_cpu_test,
        "numpy_python_memory_test": numpy_python_memory_test,
        "pure_python_cpu_test": pure_python_cpu_test,
        "pure_python_memory_test": pure_python_memory_test,
        "pure_python_mixed_test": pure_python_mixed_test,
    }


sys.set_int_max_str_digits(0)

DIVIDER = "=" * 50
SUBDIV = "-" * 20


def setup_logging(implementation):
    """
    Set up comprehensive logging with multiple handlers and detailed formatting.

    Args:
        implementation (str): The implementation being benchmarked (cpython, cython, pypy)
    """
    # Create results and logs directories if they don't exist
    results_dir = "/results"
    logs_dir = os.path.join(results_dir, "logs")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    # Create a unique log filename with timestamp and implementation
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"{implementation}_benchmark_{timestamp}.log")

    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console Handler - for real-time output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("[%(asctime)s][%(levelname).4s] %(message)s", datefmt="%H:%M:%S")
    console_handler.setFormatter(console_formatter)

    # File Handler - for detailed logging
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "[%(asctime)s][%(levelname).4s][%(filename)s:%(lineno)d] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Rotate File Handler - to manage log file sizes
    rotate_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
    )
    rotate_handler.setLevel(logging.DEBUG)
    rotate_handler.setFormatter(file_formatter)

    # Clear any existing handlers
    logger.handlers.clear()

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(rotate_handler)

    return log_filename


def measure_performance(func, *args, num_runs=30, verbose=False):
    """Measure performance metrics for a given function."""
    logging.info(f"Starting performance measurement for {func.__module__}.{func.__name__}")
    logging.info(f"Arguments: {args}")

    times = []
    memory_usages = []

    progress_bar = tqdm(range(num_runs), desc="Running tests", leave=False)
    for run in progress_bar:
        try:
            # Time measurement
            start_time = timeit.default_timer()
            result = func(*args)
            end_time = timeit.default_timer()
            run_time = end_time - start_time
            times.append(run_time)

            if verbose:
                logging.debug(f"Run time: {run_time:.4f} seconds")
                logging.debug(f"Result length/value: {len(result) if hasattr(result, '__len__') else type(result)}")

            # Memory measurement
            memory_usage = memory_profiler.memory_usage((func, args), max_iterations=1)
            memory_usages.append(memory_usage[0])

            if verbose:
                logging.debug(f"Memory usage: {memory_usage[0]:.4f} MiB")

        except Exception as e:
            logging.error(f"Error in run {run + 1}/{num_runs}: {e}")
            import traceback

            traceback.print_exc()
            continue

    # Compute statistics
    if not times:
        logging.error("No successful runs completed!")
        return 0, 0, 0, 0

    avg_time = statistics.mean(times)
    std_time = statistics.stdev(times) if len(times) > 1 else 0
    avg_memory = statistics.mean(memory_usages)
    std_memory = statistics.stdev(memory_usages) if len(memory_usages) > 1 else 0

    logging.info(f"{SUBDIV}")
    logging.info("Performance Summary:")
    logging.info(f"  Average Time: {avg_time:.4f} ± {std_time:.4f} seconds")
    logging.info(f"  Average Memory: {avg_memory:.4f} ± {std_memory:.4f} MiB")
    logging.info(f"{SUBDIV}")

    return avg_time, std_time, avg_memory, std_memory


def run_benchmarks(implementation, num_runs, cpu_limit, memory_size, mixed_size, verbose=False):
    """
    Run performance benchmarks for specified implementation.

    Args:
        implementation (str): Target implementation (cpython, pypy, cython)
        num_runs (int): Number of times to run each test
        cpu_limit (int): Limit for CPU-bound tests
        memory_size (int): Size for memory-bound tests
        mixed_size (int): Size for mixed tests
        verbose (bool): Enable verbose logging
    """
    logging.info(f"Number of runs: {num_runs}")
    logging.info(f"CPU test limit: {cpu_limit}")
    logging.info(f"Memory test size: {memory_size}")
    logging.info(f"Mixed test size: {mixed_size}\n")

    imports = get_imports(implementation)

    # Determine which test modules to use based on implementation
    if implementation == "cpython":
        test_modules = [
            (imports["pure_python_cpu_test"], "CPU Test (Pure Python)", (cpu_limit,)),
            (imports["numpy_python_cpu_test"], "CPU Test (NumPy Python)", (cpu_limit,)),
            (imports["pure_python_memory_test"], "Memory Test (Pure Python)", (memory_size,)),
            (imports["numpy_python_memory_test"], "Memory Test (NumPy Python)", (memory_size,)),
            (imports["pure_python_mixed_test"], "Mixed Test (Pure Python)", (mixed_size,)),
            (imports["pure_cython_cpu_test"], "CPU Test (Pure Cython)", (cpu_limit,)),
            (imports["numpy_cython_cpu_test"], "CPU Test (NumPy Cython)", (cpu_limit,)),
            (imports["pure_cython_memory_test"], "Memory Test (Pure Cython)", (memory_size,)),
            (imports["numpy_cython_memory_test"], "Memory Test (NumPy Cython)", (memory_size,)),
            (imports["pure_cython_mixed_test"], "Mixed Test (Pure Cython)", (mixed_size,)),
        ]
    elif implementation == "cython":
        test_modules = [
            (imports["pure_python_cpu_test"], "CPU Test (Pure Python)", (cpu_limit,)),
            (imports["numpy_python_cpu_test"], "CPU Test (NumPy Python)", (cpu_limit,)),
            (imports["pure_python_memory_test"], "Memory Test (Pure Python)", (memory_size,)),
            (imports["numpy_python_memory_test"], "Memory Test (NumPy Python)", (memory_size,)),
            (imports["pure_python_mixed_test"], "Mixed Test (Pure Python)", (mixed_size,)),
            (imports["pure_cython_cpu_test"], "CPU Test (Pure Cython)", (cpu_limit,)),
            (imports["numpy_cython_cpu_test"], "CPU Test (NumPy Cython)", (cpu_limit,)),
            (imports["pure_cython_memory_test"], "Memory Test (Pure Cython)", (memory_size,)),
            (imports["numpy_cython_memory_test"], "Memory Test (NumPy Cython)", (memory_size,)),
            (imports["pure_cython_mixed_test"], "Mixed Test (Pure Cython)", (mixed_size,)),
        ]
    elif implementation == "pypy":
        test_modules = [
            (imports["pure_python_cpu_test"], "CPU Test (Pure PyPy)", (cpu_limit,)),
            (imports["numpy_python_cpu_test"], "CPU Test (NumPy PyPy)", (cpu_limit,)),
            (imports["pure_python_memory_test"], "Memory Test (Pure PyPy)", (memory_size,)),
            (imports["numpy_python_memory_test"], "Memory Test (NumPy PyPy)", (memory_size,)),
            (imports["pure_python_mixed_test"], "Mixed Test (Pure PyPy)", (mixed_size,)),
        ]
    else:
        logging.error(f"Invalid implementation: {implementation}")
        return

    # Run benchmarks
    for test_func, test_name, test_args in test_modules:
        if test_func is None:
            logging.warning(f"Skipping {test_name} - Not available for this implementation")
            continue

        logging.info("\n--------------------")
        logging.info(f"Running {test_name}")
        logging.info("--------------------")

        try:
            avg_time, std_time, avg_memory, std_memory = measure_performance(
                test_func, *test_args, num_runs=num_runs, verbose=verbose
            )

            logging.info("--------------------")
            logging.info("Performance Summary:")
            logging.info(f"  Average Time: {avg_time:.4f} ± {std_time:.4f} seconds")
            logging.info(f"  Average Memory: {avg_memory:.4f} ± {std_memory:.4f} MiB")
            logging.info("--------------------\n")

        except Exception as e:
            logging.error(f"Error running {test_name}: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")


def main():
    parser = argparse.ArgumentParser(description="Run performance benchmarks")
    parser.add_argument(
        "implementations",
        nargs="+",  # Accept one or more values
        choices=["cpython", "cython", "pypy", "all"],
        help="Implementation(s) to benchmark. Use 'all' for all implementations or specify one or more.",
    )
    parser.add_argument("--runs", type=int, required=True, help="Number of runs for each benchmark")
    parser.add_argument("--cpu-limit", type=int, required=True, help="Limit for CPU benchmark")
    parser.add_argument("--memory-size", type=int, required=True, help="Size for memory benchmark")
    parser.add_argument("--mixed-size", type=int, required=True, help="Size for mixed benchmark")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Set up logging for the first implementation
    setup_logging(args.implementations[0])

    # Determine which implementations to run
    implementations_to_run = []
    if "all" in args.implementations:
        implementations_to_run = ["cpython", "cython", "pypy"]
    else:
        implementations_to_run = args.implementations

    # Run benchmarks for specified implementations
    for impl in implementations_to_run:
        run_benchmarks(
            implementation=impl,
            num_runs=args.runs,
            cpu_limit=args.cpu_limit,
            memory_size=args.memory_size,
            mixed_size=args.mixed_size,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
