import timeit
import statistics
import memory_profiler
import psutil
import matplotlib.pyplot as plt
import sys
import os
import logging
from datetime import datetime
import importlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('performance_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dynamically import test modules
from src import cpu_test, memory_test, mixed_test
import src.cython_cpu_test as cython_cpu_test
import src.cython_memory_test as cython_memory_test
import src.cython_mixed_test as cython_mixed_test
import src.pypy_cpu_test as pypy_cpu_test
import src.pypy_memory_test as pypy_memory_test
import src.pypy_mixed_test as pypy_mixed_test

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
        result = func(*args)
        end_time = timeit.default_timer()
        run_time = end_time - start_time
        times.append(run_time)
        
        logging.debug(f"Run time: {run_time:.4f} seconds")
        
        # Memory measurement
        try:
            mem_usage = memory_profiler.memory_usage((func, args), max_iterations=1)[0]
            memory_usages.append(mem_usage)
            logging.debug(f"Memory usage: {mem_usage:.2f} MB")
        except Exception as e:
            logging.warning(f"Memory profiling failed: {e}")
            memory_usages.append(0)
    
    return {
        'mean_time': statistics.mean(times),
        'std_time': statistics.stdev(times) if len(times) > 1 else 0,
        'mean_memory': statistics.mean(memory_usages),
        'std_memory': statistics.stdev(memory_usages) if len(memory_usages) > 1 else 0
    }

def run_benchmarks():
    """Run performance benchmarks for all test cases and implementations."""
    logging.info("Starting performance benchmarks")
    
    # Define test configurations
    benchmarks = {
        'CPU Test (Python)': (cpu_test.run_cpu_test, 3000),
        'CPU Test (Cython)': (cython_cpu_test.run_cpu_test, 3000),
        'CPU Test (PyPy)': (pypy_cpu_test.run_cpu_test, 3000),
        
        'Memory Test (Python)': (memory_test.run_memory_test, 200),
        'Memory Test (Cython)': (cython_memory_test.run_memory_test, 200),
        'Memory Test (PyPy)': (pypy_memory_test.run_memory_test, 200),
        
        'Mixed Test (Python)': (mixed_test.run_mixed_test, 25),
        'Mixed Test (Cython)': (cython_mixed_test.run_mixed_test, 25),
        'Mixed Test (PyPy)': (pypy_mixed_test.run_mixed_test, 25)
    }
    
    results = {}
    for name, (func, arg) in benchmarks.items():
        logging.info(f"Running benchmark: {name}")
        results[name] = measure_performance(func, arg)
    
    return results

def plot_results(results):
    """Generate performance graphs."""
    logging.info("Generating performance graphs")
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    plt.figure(figsize=(16, 6))
    
    # Time performance
    plt.subplot(1, 2, 1)
    names = list(results.keys())
    mean_times = [result['mean_time'] for result in results.values()]
    std_times = [result['std_time'] for result in results.values()]
    
    plt.bar(names, mean_times, yerr=std_times, capsize=5)
    plt.title('Mean Execution Time with Standard Deviation')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45, ha='right')
    
    # Memory performance
    plt.subplot(1, 2, 2)
    mean_memories = [result['mean_memory'] for result in results.values()]
    std_memories = [result['std_memory'] for result in results.values()]
    
    plt.bar(names, mean_memories, yerr=std_memories, capsize=5)
    plt.title('Mean Memory Usage with Standard Deviation')
    plt.ylabel('Memory (MB)')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    graph_filename = f'results/performance_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(graph_filename)
    plt.close()
    
    logging.info(f"Performance graph saved to {graph_filename}")

def main():
    try:
        results = run_benchmarks()
        
        # Print detailed results
        for name, metrics in results.items():
            logging.info(f"\n{name}:")
            logging.info(f"  Mean Time: {metrics['mean_time']:.4f} ± {metrics['std_time']:.4f} seconds")
            logging.info(f"  Mean Memory: {metrics['mean_memory']:.2f} ± {metrics['std_memory']:.2f} MB")
        
        plot_results(results)
        logging.info("Performance benchmarks completed successfully")
    
    except Exception as e:
        logging.error(f"An error occurred during benchmarking: {e}", exc_info=True)

if __name__ == "__main__":
    main()
