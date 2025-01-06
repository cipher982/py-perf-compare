import argparse
import logging
import statistics
import sys
import timeit
import traceback

import memory_profiler
from tqdm import tqdm


# Conditional imports based on implementation
def get_imports(implementation: str):
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


def setup_logging(implementation: str):
    """Basic logging setup for benchmark output."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Single console handler with simple formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname).4s] %(message)s", datefmt="%H:%M:%S"))

    logger.handlers.clear()
    logger.addHandler(handler)


def measure_performance(func, *args, num_runs: int = 30, verbose: bool = False):
    """Measure performance metrics for a given function."""
    logging.info(f"Starting performance measurement for {func.__module__}.{func.__name__}")
    logging.info(f"Arguments: {args}")

    times = []
    memory_usages = []

    progress_bar = tqdm(range(num_runs), desc="Running tests", leave=False)
    for _ in progress_bar:
        try:
            # Time measurement
            start_time = timeit.default_timer()
            func(*args)
            end_time = timeit.default_timer()
            run_time = end_time - start_time
            times.append(run_time)

            # Memory measurement
            memory_usage = memory_profiler.memory_usage((func, args), max_iterations=1)
            memory_usages.append(memory_usage[0])

        except Exception as e:
            logging.error(f"Error in run: {e}")
            traceback.print_exc()
            continue

    if not times:
        logging.error("No successful runs completed!")
        return

    avg_time = statistics.mean(times)
    std_time = statistics.stdev(times) if len(times) > 1 else 0
    avg_memory = statistics.mean(memory_usages)
    std_memory = statistics.stdev(memory_usages) if len(memory_usages) > 1 else 0

    logging.info("--------------------")
    logging.info("Performance Summary:")
    logging.info(f"  Average Time: {avg_time:.4f} ± {std_time:.4f} seconds")
    logging.info(f"  Average Memory: {avg_memory:.4f} ± {std_memory:.4f} MiB")
    logging.info("--------------------\n")


def run_benchmarks(
    implementation: str,
    num_runs: int,
    prime_upper_bound: int,
    matrix_dimension: int,
    fibonacci_length: int,
    verbose: bool = False,
):
    """
    Run performance benchmarks for specified implementation.

    Args:
        implementation (str): Target implementation (cpython, pypy, cython)
        num_runs (int): Number of times to run each test
        prime_upper_bound (int): Upper bound for prime number calculations
        matrix_dimension (int): Size of NxN matrices for multiplication
        fibonacci_length (int): Number of Fibonacci numbers to calculate
        verbose (bool): Enable verbose logging
    """
    logging.info(f"\n{DIVIDER}\nRunning {implementation} benchmarks\n{DIVIDER}")
    logging.info(f"Number of runs: {num_runs}")
    logging.info(f"Prime number upper bound: {prime_upper_bound}")
    logging.info(f"Matrix dimension: {matrix_dimension}")
    logging.info(f"Fibonacci sequence length: {fibonacci_length}\n")

    imports = get_imports(implementation)

    # Determine which test modules to use based on implementation
    if implementation == "cpython":
        test_cases = [
            (imports["pure_python_cpu_test"], "CPU Test (Pure Python)", (prime_upper_bound,)),
            (imports["numpy_python_cpu_test"], "CPU Test (NumPy Python)", (prime_upper_bound,)),
            (imports["pure_python_memory_test"], "Memory Test (Pure Python)", (matrix_dimension,)),
            (imports["numpy_python_memory_test"], "Memory Test (NumPy Python)", (matrix_dimension,)),
            (imports["pure_python_mixed_test"], "Mixed Test (Pure Python)", (fibonacci_length,)),
            (imports["pure_cython_cpu_test"], "CPU Test (Pure Cython)", (prime_upper_bound,)),
            (imports["numpy_cython_cpu_test"], "CPU Test (NumPy Cython)", (prime_upper_bound,)),
            (imports["pure_cython_memory_test"], "Memory Test (Pure Cython)", (matrix_dimension,)),
            (imports["numpy_cython_memory_test"], "Memory Test (NumPy Cython)", (matrix_dimension,)),
            (imports["pure_cython_mixed_test"], "Mixed Test (Pure Cython)", (fibonacci_length,)),
        ]
    elif implementation == "cython":
        test_cases = [
            (imports["pure_python_cpu_test"], "CPU Test (Pure Python)", (prime_upper_bound,)),
            (imports["numpy_python_cpu_test"], "CPU Test (NumPy Python)", (prime_upper_bound,)),
            (imports["pure_python_memory_test"], "Memory Test (Pure Python)", (matrix_dimension,)),
            (imports["numpy_python_memory_test"], "Memory Test (NumPy Python)", (matrix_dimension,)),
            (imports["pure_python_mixed_test"], "Mixed Test (Pure Python)", (fibonacci_length,)),
            (imports["pure_cython_cpu_test"], "CPU Test (Pure Cython)", (prime_upper_bound,)),
            (imports["numpy_cython_cpu_test"], "CPU Test (NumPy Cython)", (prime_upper_bound,)),
            (imports["pure_cython_memory_test"], "Memory Test (Pure Cython)", (matrix_dimension,)),
            (imports["numpy_cython_memory_test"], "Memory Test (NumPy Cython)", (matrix_dimension,)),
            (imports["pure_cython_mixed_test"], "Mixed Test (Pure Cython)", (fibonacci_length,)),
        ]
    else:  # pypy
        test_cases = [
            (imports["pure_python_cpu_test"], "CPU Test (Pure PyPy)", (prime_upper_bound,)),
            (imports["numpy_python_cpu_test"], "CPU Test (NumPy PyPy)", (prime_upper_bound,)),
            (imports["pure_python_memory_test"], "Memory Test (Pure PyPy)", (matrix_dimension,)),
            (imports["numpy_python_memory_test"], "Memory Test (NumPy PyPy)", (matrix_dimension,)),
            (imports["pure_python_mixed_test"], "Mixed Test (Pure PyPy)", (fibonacci_length,)),
        ]
    # Run benchmarks
    for test_func, test_name, test_args in test_cases:
        if test_func is None:
            logging.warning(f"Skipping {test_name} - Not available for this implementation")
            continue

        logging.info("\n--------------------")
        logging.info(f"Running {test_name}")
        logging.info("--------------------")

        try:
            measure_performance(test_func, *test_args, num_runs=num_runs, verbose=verbose)
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
    parser.add_argument(
        "--prime-upper-bound", type=int, required=True, help="Upper bound for prime number calculations"
    )
    parser.add_argument("--matrix-dimension", type=int, required=True, help="Size of NxN matrices for multiplication")
    parser.add_argument("--fibonacci-length", type=int, required=True, help="Number of Fibonacci numbers to calculate")
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
            prime_upper_bound=args.prime_upper_bound,
            matrix_dimension=args.matrix_dimension,
            fibonacci_length=args.fibonacci_length,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
