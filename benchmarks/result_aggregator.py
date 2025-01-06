"""
Result aggregator for benchmark results. This script runs in the controller container
and aggregates results from all benchmark runs.
"""

import json
from pathlib import Path

import pandas as pd

RESULTS_DIR = Path("/results")


def aggregate_results():
    """Aggregate all benchmark results into a single report."""
    results = {"cpython": {"pure": {}, "numpy": {}}, "pypy": {"pure": {}, "numpy": {}}}

    # Collect all results
    for impl in ["cpython", "pypy"]:
        for variant in ["pure", "numpy"]:
            result_dir = RESULTS_DIR / impl / variant
            if not result_dir.exists():
                continue

            for result_file in result_dir.glob("*.json"):
                with open(result_file) as f:
                    results[impl][variant][result_file.stem] = json.load(f)

    # Convert to DataFrame for analysis
    rows = []
    for impl in results:
        for variant in results[impl]:
            for test_name, metrics in results[impl][variant].items():
                rows.append({"implementation": impl, "variant": variant, "test": test_name, **metrics})

    df = pd.DataFrame(rows)

    # Generate summary report
    report_path = RESULTS_DIR / "benchmark_summary.md"
    with open(report_path, "w") as f:
        f.write("# Benchmark Results Summary\n\n")

        # Overall statistics
        f.write("## Overall Statistics\n")
        f.write(f"Total tests run: {len(df)}\n")
        f.write(f"Implementations: {', '.join(df['implementation'].unique())}\n")
        f.write(f"Test variants: {', '.join(df['variant'].unique())}\n\n")

        # Performance comparison tables
        f.write("## Performance Comparisons\n")
        for test in df["test"].unique():
            f.write(f"\n### {test}\n")
            test_df = df[df["test"] == test]
            f.write(test_df.to_markdown())
            f.write("\n")


if __name__ == "__main__":
    aggregate_results()
