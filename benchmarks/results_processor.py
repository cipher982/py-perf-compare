#!/usr/bin/env python3
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def save_results_to_csv(results, timestamp):
    """Save benchmark results to CSV file."""
    # Restructure results for DataFrame
    rows = []
    for test_name, metrics in results.items():
        # Parse test name into components
        test_type = test_name.split(" Test")[0]  # CPU, Memory, or Mixed
        implementation = test_name.split("(")[-1].strip(")")  # Python, Cython, or PyPy

        rows.append(
            {
                "test_type": test_type,
                "implementation": implementation,
                "mean_time": metrics["mean_time"],
                "std_time": metrics["std_time"],
                "mean_memory": metrics["mean_memory"],
                "std_memory": metrics["std_memory"],
            }
        )

    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows)
    os.makedirs("results", exist_ok=True)
    csv_path = f"results/benchmark_results_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    return csv_path


def plot_results(csv_path):
    """Generate improved performance visualization."""
    # Read results
    df = pd.read_csv(csv_path)

    # Set style with better visibility
    plt.style.use("fivethirtyeight")

    # Create figure with subplots for each test type
    test_types = df["test_type"].unique()
    fig, axes = plt.subplots(len(test_types), 2, figsize=(15, 5 * len(test_types)))

    # Color palette for better distinction
    colors = ["#2ecc71", "#3498db", "#e74c3c"]

    for idx, test_type in enumerate(test_types):
        test_data = df[df["test_type"] == test_type].copy()

        # Plot execution time with log scale if values vary significantly
        time_data = test_data["mean_time"]
        use_log_time = max(time_data) / (min(time_data) + 1e-10) > 100

        ax_time = axes[idx, 0] if len(test_types) > 1 else axes[0]
        sns.barplot(
            x="implementation", y="mean_time", data=test_data, ax=ax_time, palette=colors, capsize=0.05, errwidth=2
        )
        if use_log_time:
            ax_time.set_yscale("log")
        ax_time.set_title(f"{test_type} Test - Execution Time")
        ax_time.set_ylabel("Time (seconds)")

        # Plot memory usage
        ax_mem = axes[idx, 1] if len(test_types) > 1 else axes[1]
        sns.barplot(
            x="implementation", y="mean_memory", data=test_data, ax=ax_mem, palette=colors, capsize=0.05, errwidth=2
        )
        ax_mem.set_title(f"{test_type} Test - Memory Usage")
        ax_mem.set_ylabel("Memory (MB)")

        # Rotate labels and adjust layout
        for ax in [ax_time, ax_mem]:
            ax.tick_params(axis="x", rotation=45)
            ax.grid(True, alpha=0.3, linestyle="--")

            # Add value labels on top of bars
            for p in ax.patches:
                height = p.get_height()
                ax.text(p.get_x() + p.get_width() / 2.0, height, f"{height:.2f}", ha="center", va="bottom")

    # Adjust layout
    plt.tight_layout()

    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f"results/performance_comparison_{timestamp}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    return plot_path


if __name__ == "__main__":
    # This can be used to regenerate plots from existing CSV files
    import sys

    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        if os.path.exists(csv_path):
            plot_results(csv_path)
        else:
            print(f"CSV file not found: {csv_path}")
