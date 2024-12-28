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
    # Read results
    df = pd.read_csv(combined_csv)

    # Capitalize implementation names
    df["implementation"] = df["implementation"].str.upper()

    # Set style with better visibility
    plt.style.use("seaborn")

    # Create figure with subplots for each test type
    test_types = sorted(df["test_type"].unique())
    fig, axes = plt.subplots(len(test_types), 2, figsize=(15, 5 * len(test_types)))

    # Color palette for better distinction
    colors = ["#2ecc71", "#3498db", "#e74c3c"]

    # Find max memory usage for consistent y-axis
    max_memory = df["mean_memory"].max() * 1.2  # Add 20% padding

    for idx, test_type in enumerate(test_types):
        test_data = df[df["test_type"] == test_type].copy()

        # Plot execution time
        ax_time = axes[idx, 0] if len(test_types) > 1 else axes[0]
        sns.barplot(
            data=test_data,
            x="implementation",
            y="mean_time",
            hue="implementation",
            ax=ax_time,
            palette=colors,
            capsize=0.05,
            err_kws={"linewidth": 2},
            legend=False,
        )

        # Always use log scale for time to handle small values better
        ax_time.set_yscale("log")
        ax_time.set_title(f"{test_type} Test - Execution Time", pad=20, fontsize=12, fontweight="bold")
        ax_time.set_ylabel("Time (seconds)", fontsize=10)

        # Plot memory usage
        ax_mem = axes[idx, 1] if len(test_types) > 1 else axes[1]
        sns.barplot(
            data=test_data,
            x="implementation",
            y="mean_memory",
            hue="implementation",
            ax=ax_mem,
            palette=colors,
            capsize=0.05,
            err_kws={"linewidth": 2},
            legend=False,
        )
        ax_mem.set_title(f"{test_type} Test - Memory Usage", pad=20, fontsize=12, fontweight="bold")
        ax_mem.set_ylabel("Memory (MB)", fontsize=10)

        # Set consistent y-axis for memory plots
        ax_mem.set_ylim(0, max_memory)

        # Rotate labels and adjust layout
        for ax in [ax_time, ax_mem]:
            ax.tick_params(axis="x", rotation=45)
            ax.grid(True, alpha=0.3, linestyle="--")

            # Add value labels on top of bars with appropriate formatting
            for p in ax.patches:
                height = p.get_height()
                if ax == ax_time:
                    # Format time with scientific notation for very small values
                    if height < 0.001:
                        value_text = f"{height:.2e}"
                    else:
                        value_text = f"{height:.3f}"
                else:
                    # Format memory with 1 decimal place
                    value_text = f"{height:.1f}"

                ax.text(p.get_x() + p.get_width() / 2.0, height, value_text, ha="center", va="bottom", fontsize=9)

    # Add a title for the entire figure
    fig.suptitle("Performance Comparison: Time and Memory Usage", y=1.02, fontsize=14, fontweight="bold")

    # Adjust layout
    plt.tight_layout()

    # Save plot
    plot_dir = os.path.dirname(combined_csv)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = os.path.join(plot_dir, f"performance_comparison_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
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
