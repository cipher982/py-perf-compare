#!/usr/bin/env python3
import glob
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def process_results_directory(results_dir):
    """Process all results from the directory structure and combine them."""
    implementations = ["cpython", "cython", "pypy"]
    rows = []

    for impl in implementations:
        impl_dir = os.path.join(results_dir, impl)
        if not os.path.exists(impl_dir):
            continue

        # Process each CSV file in the implementation directory
        for csv_file in glob.glob(os.path.join(impl_dir, "*_results.csv")):
            # Read the CSV file
            df = pd.read_csv(csv_file)
            rows.extend(df.to_dict("records"))

    # Create DataFrame from all results
    df = pd.DataFrame(rows)

    # Save combined results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_csv = os.path.join(results_dir, f"combined_results_{timestamp}.csv")
    df.to_csv(combined_csv, index=False)

    return combined_csv


def plot_results(combined_csv):
    """Create detailed performance comparison plots."""
    df = pd.read_csv(combined_csv)

    # Create figure with subplots for time and memory
    fig, (ax_time, ax_mem) = plt.subplots(2, 1, figsize=(12, 16))

    # Color palette for different implementations
    colors = sns.color_palette("husl", n_colors=3)

    # Plot execution times
    time_data = df[df["Metric"] == "Time (seconds)"]
    sns.barplot(
        data=time_data,
        x="Test Type",
        y="Value",
        hue="Implementation",
        ax=ax_time,
        palette=colors,
    )

    # Format time axis and labels
    ax_time.set_title("Execution Time by Test", pad=20, fontsize=12, fontweight="bold")
    ax_time.set_xlabel("Test Type", fontsize=10)
    ax_time.set_ylabel("Time (seconds)", fontsize=10)

    # Add value labels on bars for time
    for container in ax_time.containers:
        ax_time.bar_label(container, fmt="%.3f", padding=3, rotation=45)

    # Plot memory usage
    memory_data = df[df["Metric"] == "Memory (MiB)"]
    sns.barplot(
        data=memory_data,
        x="Test Type",
        y="Value",
        hue="Implementation",
        ax=ax_mem,
        palette=colors,
    )

    # Format memory axis and labels
    ax_mem.set_title("Memory Usage by Test", pad=20, fontsize=12, fontweight="bold")
    ax_mem.set_xlabel("Test Type", fontsize=10)
    ax_mem.set_ylabel("Memory (MiB)", fontsize=10)

    # Add value labels on bars for memory
    for container in ax_mem.containers:
        ax_mem.bar_label(container, fmt="%.1f", padding=3, rotation=45)

    # Adjust layout and labels
    for ax in [ax_time, ax_mem]:
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(
            title="Implementation",
            bbox_to_anchor=(0.5, 1.15),
            loc="center",
            ncol=3,
            fontsize=9,
        )
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # Add overall title
    fig.suptitle(
        "Performance Comparison: Pure vs NumPy Implementations",
        y=1.05,
        fontsize=14,
        fontweight="bold",
    )

    # Save plots
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_file = os.path.join(os.path.dirname(combined_csv), f"performance_comparison_{timestamp}.png")
    plt.savefig(plot_file, bbox_inches="tight", dpi=300)
    plt.close()


def main():
    """Process results and generate plots."""
    import sys

    if len(sys.argv) > 1:
        results_dir = sys.argv[1]
    else:
        results_dir = "/results"

    combined_csv = process_results_directory(results_dir)
    plot_results(combined_csv)
    print("Results processed and plots generated in results/")


if __name__ == "__main__":
    main()
