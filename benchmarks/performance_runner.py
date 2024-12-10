import timeit
import statistics
import memory_profiler
import psutil
import matplotlib.pyplot as plt
import sys
import os
import logging
from datetime import datetime

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

from src import cpu_test, memory_test, mixed_test

def measure_performance(func, *args, num_runs=100):
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
        mem_usage = memory_profiler.memory_usage((func, args), max_iterations=1)[0]
        memory_usages.append(mem_usage)
        
        logging.debug(f"Memory usage: {mem_usage:.2f} MB")
    
    return {
        'mean_time': statistics.mean(times),
        'std_time': statistics.stdev(times),
        'mean_memory': statistics.mean(memory_usages),
        'std_memory': statistics.stdev(memory_usages)
    }

def run_benchmarks():
    """Run performance benchmarks for all test cases."""
    logging.info("Starting performance benchmarks")
    
    benchmarks = {
        'CPU Test (Primes)': (cpu_test.run_cpu_test, 5000),  # Reduced from 10000
        'Memory Test (Matrix)': (memory_test.run_memory_test, 250),  # Reduced from 500
        'Mixed Test (Fibonacci)': (mixed_test.run_mixed_test, 30)
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
    
    plt.figure(figsize=(15, 5))
    
    # Time performance
    plt.subplot(1, 2, 1)
    names = list(results.keys())
    mean_times = [result['mean_time'] for result in results.values()]
    plt.bar(names, mean_times)
    plt.title('Mean Execution Time')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45)
    
    # Memory performance
    plt.subplot(1, 2, 2)
    mean_memories = [result['mean_memory'] for result in results.values()]
    plt.bar(names, mean_memories)
    plt.title('Mean Memory Usage')
    plt.ylabel('Memory (MB)')
    plt.xticks(rotation=45)
    
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
