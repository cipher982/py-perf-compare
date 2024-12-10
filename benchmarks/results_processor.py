#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def save_results_to_csv(results, timestamp):
    """Save benchmark results to CSV file."""
    # Restructure results for DataFrame
    rows = []
    for test_name, metrics in results.items():
        # Parse test name into components
        test_type = test_name.split(' Test')[0]  # CPU, Memory, or Mixed
        implementation = test_name.split('(')[-1].strip(')')  # Python, Cython, or PyPy
        
        rows.append({
            'test_type': test_type,
            'implementation': implementation,
            'mean_time': metrics['mean_time'],
            'std_time': metrics['std_time'],
            'mean_memory': metrics['mean_memory'],
            'std_memory': metrics['std_memory']
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows)
    os.makedirs('results', exist_ok=True)
    csv_path = f'results/benchmark_results_{timestamp}.csv'
    df.to_csv(csv_path, index=False)
    return csv_path

def plot_results(csv_path):
    """Generate improved performance visualization."""
    # Read results
    df = pd.read_csv(csv_path)
    
    # Set style
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Create figure with subplots for each test type
    test_types = df['test_type'].unique()
    fig, axes = plt.subplots(len(test_types), 2, figsize=(15, 5*len(test_types)))
    
    for idx, test_type in enumerate(test_types):
        test_data = df[df['test_type'] == test_type]
        
        # Plot execution time
        sns.barplot(
            data=test_data,
            x='implementation',
            y='mean_time',
            ax=axes[idx, 0],
            capsize=0.05,
            errwidth=2
        )
        axes[idx, 0].set_title(f'{test_type} Test - Execution Time')
        axes[idx, 0].set_ylabel('Time (seconds)')
        axes[idx, 0].grid(True, alpha=0.3)
        
        # Plot memory usage
        sns.barplot(
            data=test_data,
            x='implementation',
            y='mean_memory',
            ax=axes[idx, 1],
            capsize=0.05,
            errwidth=2
        )
        axes[idx, 1].set_title(f'{test_type} Test - Memory Usage')
        axes[idx, 1].set_ylabel('Memory (MB)')
        axes[idx, 1].grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        axes[idx, 0].tick_params(axis='x', rotation=45)
        axes[idx, 1].tick_params(axis='x', rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'results/performance_comparison_{timestamp}.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return plot_path

if __name__ == '__main__':
    # This can be used to regenerate plots from existing CSV files
    import sys
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        if os.path.exists(csv_path):
            plot_results(csv_path)
        else:
            print(f"CSV file not found: {csv_path}")
