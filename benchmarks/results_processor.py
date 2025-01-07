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

        # Process pure and numpy subdirectories
        for subdir in ["pure", "numpy"]:
            subdir_path = os.path.join(impl_dir, subdir)
            if not os.path.exists(subdir_path):
                continue

            # Process each CSV file in the subdirectory
            for csv_file in glob.glob(os.path.join(subdir_path, "*.csv")):
                try:
                    df = pd.read_csv(csv_file)
                    if not df.empty:
                        rows.extend(df.to_dict("records"))
                except pd.errors.EmptyDataError:
                    print(f"Warning: Empty CSV file found: {csv_file}")
                    continue

    if not rows:
        raise ValueError("No valid data found in any CSV files")

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
    df["Type"] = df["Test Name"].apply(lambda x: "NumPy" if "NumPy" in x else "Pure")

    # Create 2x2 subplot grid
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # Plot each subset
    for data, ax, title in [
        (df[df["Type"] == "Pure"], ax1, "Pure - Time"),
        (df[df["Type"] == "NumPy"], ax2, "NumPy - Time"),
        (df[df["Type"] == "Pure"], ax3, "Pure - Memory"),
        (df[df["Type"] == "NumPy"], ax4, "NumPy - Memory"),
    ]:
        sns.barplot(
            data=data,
            x="Test Type",
            y="Time (seconds)" if "Time" in title else "Memory (MiB)",
            hue="Implementation",
            ax=ax,
        )
        ax.set_title(title)
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2g")

    # Clean up
    for ax in [ax2, ax3, ax4]:
        ax.get_legend().remove()

    plt.suptitle("Performance Comparison", fontsize=14)
    plt.tight_layout()
    plt.savefig(
        os.path.join(os.path.dirname(combined_csv), f'comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
    )
    plt.close()


def main():
    """Process results and generate plots."""
    import sys

    if len(sys.argv) > 1:
        results_dir = sys.argv[1]
    else:
        results_dir = "/results"

    try:
        combined_csv = process_results_directory(results_dir)
        plot_results(combined_csv)
        print("Results processed and plots generated in results/")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
