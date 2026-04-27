"""
main.py
-------
Entry point for the Novel Rework Costing Methodology project.

Run:
    python main.py

What it does:
    1. Generates (or loads) a realistic rework dataset
    2. Applies three costing models to the data
    3. Prints a cost comparison report to the terminal
    4. Produces three analysis charts as PNG files
    5. Saves the enriched dataset to CSV
"""

import os
import pandas as pd

from data_generator import generate_dataset, save_dataset
from costing_model   import build_cost_summary, print_cost_report
from visualization   import generate_all_plots


# ── Configuration ────────────────────────────────────────────────────────────
DATA_PATH        = "sample_data.csv"
ENRICHED_PATH    = "rework_costing_results.csv"
N_ROWS           = 150          # number of synthetic incidents to generate


def load_or_generate(path: str, n: int) -> pd.DataFrame:
    """
    Load existing CSV if present, otherwise generate a fresh dataset.

    Parameters
    ----------
    path : str  – file path to look for / write to
    n    : int  – number of rows to generate if file is missing

    Returns
    -------
    pd.DataFrame
    """
    if os.path.exists(path):
        print(f"[main] Loading existing dataset from '{path}' …")
        return pd.read_csv(path)
    else:
        print(f"[main] No dataset found – generating {n} synthetic rows …")
        df = generate_dataset(n_rows=n)
        save_dataset(df, path=path)
        return df


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all three costing models and return the enriched dataframe.

    Parameters
    ----------
    df : pd.DataFrame  – raw rework log

    Returns
    -------
    pd.DataFrame  – same data with Traditional_Cost, Rework_Cost,
                    Novel_Cost, SWDSI columns added
    """
    print("[main] Running costing models …")
    enriched = build_cost_summary(df)
    return enriched


def save_results(df: pd.DataFrame, path: str) -> None:
    """Save the enriched dataframe (with all cost columns) to CSV."""
    df.to_csv(path, index=False)
    print(f"[main] Results saved → '{path}'")


def main() -> None:
    print("\n" + "=" * 58)
    print("  Novel Rework Costing Methodology")
    print("  Applied to a Bus Manufacturing Company")
    print("=" * 58)

    # Step 1 – Data
    df = load_or_generate(DATA_PATH, N_ROWS)

    # Step 2 – Costing
    enriched = run_pipeline(df)

    # Step 3 – Report
    print_cost_report(enriched)

    # Step 4 – Visualisations
    print("[main] Generating visualisation charts …")
    generate_all_plots(enriched)

    # Step 5 – Save enriched CSV
    save_results(enriched, ENRICHED_PATH)

    print("\n[main] ✓  Pipeline complete.  Check the PNG files for charts.\n")


if __name__ == "__main__":
    main()
