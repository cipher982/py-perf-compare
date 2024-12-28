#!/usr/bin/env python3
import glob
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def process_results_directory(results_dir="/results"):
    """Process all results from the directory structure and combine them."""
    implementations = ["cpython", "cython", "pypy"]
    rows = []

    for impl in implementations:
        impl_dir = os.path.join(results_dir, impl)
        if not os.path.exists(impl_dir):
            continue

        # Process each CSV file in the implementation directory
        for csv_file in glob.glob(os.path.join(impl_dir, "*_results.csv")):
            test_name = os.path.basename(csv_file).replace("_results.csv", "")

            # Read the CSV file
            df = pd.read_csv(csv_file)
            rows.append(
                {
                    "test_type": test_name.replace("_test", "").upper(),
                    "implementation": impl,
                    "mean_time": df.loc[df["Metric"] == "Time (seconds)", "Value"].iloc[0],
                    "std_time": df.loc[df["Metric"] == "Time (seconds)", "Std Dev"].iloc[0],
                    "mean_memory": df.loc[df["Metric"] == "Memory (MiB)", "Value"].iloc[0],
                    "std_memory": df.loc[df["Metric"] == "Memory (MiB)", "Std Dev"].iloc[0],
                }
            )

    # Create DataFrame from all results
    df = pd.DataFrame(rows)

    # Save combined results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_csv = os.path.join(results_dir, f"combined_results_{timestamp}.csv")
    df.to_csv(combined_csv, index=False)

    return combined_csv


def plot_results(combined_csv):
    """Generate performance visualization from combined results."""
    df = pd.read_csv(combined_csv)
    df["implementation"] = df["implementation"].str.upper()

    # Create single figure with two columns: Time and Memory
    fig, (ax_time, ax_mem) = plt.subplots(1, 2, figsize=(15, 8))

    # Plot execution times
    sns.barplot(
        data=df,
        x="test_type",
        y="mean_time",
        hue="implementation",
        ax=ax_time,
        palette="Set2",
        capsize=0.05,
        err_kws={"linewidth": 2},
    )

    # Format time axis and labels
    ax_time.set_yscale("log")  # Use log scale for better visibility of small differences
    ax_time.set_title("Execution Time by Test", pad=20, fontsize=12, fontweight="bold")
    ax_time.set_xlabel("Test Type", fontsize=10)
    ax_time.set_ylabel("Time (seconds)", fontsize=10)

    # Add value labels on bars for time
    for container in ax_time.containers:
        for bar in container:
            height = bar.get_height()
            if height < 0.001:
                label = f"{height:.2e}"
            else:
                label = f"{height:.3f}"
            ax_time.text(
                bar.get_x() + bar.get_width() / 2, height, label, ha="center", va="bottom", fontsize=8, rotation=45
            )

    # Plot memory usage
    sns.barplot(
        data=df,
        x="test_type",
        y="mean_memory",
        hue="implementation",
        ax=ax_mem,
        palette="Set2",
        capsize=0.05,
        err_kws={"linewidth": 2},
    )

    # Format memory axis and labels
    ax_mem.set_title("Memory Usage by Test", pad=20, fontsize=12, fontweight="bold")
    ax_mem.set_xlabel("Test Type", fontsize=10)
    ax_mem.set_ylabel("Memory (MB)", fontsize=10)

    # Add value labels on bars for memory
    for container in ax_mem.containers:
        for bar in container:
            height = bar.get_height()
            ax_mem.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=45,
            )

    # Adjust layout and labels
    for ax in [ax_time, ax_mem]:
        ax.grid(True, alpha=0.3, linestyle="--")
        # Move legend to top
        ax.legend(
            title="Implementation",
            bbox_to_anchor=(0.5, 1.15),
            loc="center",
            ncol=3,
            fontsize=9,
        )
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # Add overall title
    fig.suptitle(
        "Performance Comparison: CPython vs Cython vs PyPy",
        y=1.1,
        fontsize=14,
        fontweight="bold",
    )

    # Adjust layout to prevent overlapping
    plt.tight_layout()

    # Save plot
    plot_dir = os.path.dirname(combined_csv)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = os.path.join(plot_dir, f"performance_comparison_{timestamp}.png")
    fig.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    return plot_path


if __name__ == "__main__":
    import sys

    # Use provided results directory or default to /results
    results_dir = sys.argv[1] if len(sys.argv) > 1 else "/results"

    if os.path.exists(results_dir):
        combined_csv = process_results_directory(results_dir)
        plot_results(combined_csv)
        print(f"Results processed and plots generated in {results_dir}")
    else:
        print(f"Results directory not found: {results_dir}")
