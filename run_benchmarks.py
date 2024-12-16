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


def run_benchmark(implementation):
    """Run benchmarks for a specific Python implementation."""
    executable = find_executable(implementation)

    if not executable:
        logging.error(f"No {implementation} executable found.")
        return False

    logging.info(f"Running benchmarks with {implementation.capitalize()} implementation...")
    logging.info(f"Using executable: {executable}")

    # Set up environment variables for PyPy
    env = os.environ.copy()
    if implementation == "pypy":
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv-pypy")
        if sys.platform == "win32":
            env["PATH"] = os.path.join(venv_path, "Scripts") + os.pathsep + env["PATH"]
            env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
        else:
            env["PATH"] = os.path.join(venv_path, "bin") + os.pathsep + env["PATH"]
            env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))

    # Ensure Cython extensions are built for CPython
    if implementation in ["cpython", "cython"]:
        try:
            logging.info("Building Cython extensions...")
            subprocess.run(
                ["python3", "setup.py", "build_ext", "--inplace"],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to build Cython extensions: {e.stderr}")
            return False

    try:
        result = subprocess.run(
            [executable, "benchmarks/performance_runner.py"], check=True, capture_output=True, text=True, env=env
        )
        for line in result.stdout.splitlines():
            logging.info(f"{implementation.upper()} STDOUT: {line}")
        return True
    except subprocess.CalledProcessError as e:
        if e.stderr:
            for line in e.stderr.splitlines():
                logging.warning(f"{implementation.upper()} STDERR: {line}")
        logging.error(f"{implementation.capitalize()} benchmarks failed with return code {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Python Performance Benchmarks")
    parser.add_argument(
        "implementations",
        nargs="*",
        default=["cpython", "cython", "pypy"],
        help="Specify which implementations to benchmark (cpython, cython, pypy)",
    )

    args = parser.parse_args()

    # Validate implementations
    valid_impls = ["cpython", "cython", "pypy"]
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


if __name__ == "__main__":
    main()
