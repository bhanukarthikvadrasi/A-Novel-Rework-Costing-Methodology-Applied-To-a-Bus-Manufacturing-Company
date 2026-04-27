"""
main.py
-------
Entry point for the Novel Rework Costing Methodology project.

Execution flow
--------------
1. Generate synthetic rework dataset via data_generator.
2. Apply three costing models via costing_model.
3. Compute summary financial metrics.
4. Print a formatted results table to the terminal.
5. Generate and save all charts via visualization.

Run
---
    python main.py
"""

import pandas as pd

from data_generator import generate_dataset, save_sample_csv
from costing_model  import (
    calculate_traditional_cost,
    calculate_rework_cost,
    calculate_novel_cost,
    compute_summary,
)
from visualization import generate_all_charts


# ── Formatting helpers ─────────────────────────────────────────────────────────

def fmt_inr(value: float) -> str:
    """Format a float as an Indian Rupee string with comma grouping."""
    return f"₹{value:>15,.2f}"


def section(title: str, width: int = 62) -> None:
    """Print a titled section separator."""
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")


# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n" + "═" * 62)
    print("  Novel Rework Costing Methodology")
    print("  Applied to a Bus Manufacturing Company")
    print("═" * 62)

    # ── Step 1: Data generation ────────────────────────────────────────────────
    section("Step 1 — Generating Dataset")
    df = generate_dataset(n_records=150)
    save_sample_csv(df, path="sample_data.csv")
    print(f"  Records generated : {len(df)}")
    print(f"  Unique buses      : {df['Bus_ID'].nunique()}")
    print(f"  Production stages : {df['Production_Stage'].nunique()}")
    print(f"  Defect types      : {df['Defect_Type'].nunique()}")

    # ── Step 2: Apply costing models ──────────────────────────────────────────
    section("Step 2 — Applying Costing Models")
    df["Traditional_Cost"] = calculate_traditional_cost(df)
    df["Rework_Cost"]      = calculate_rework_cost(df)
    df["Novel_Cost"]       = calculate_novel_cost(df)
    print("  Traditional Cost, Rework Cost, and Novel Cost columns added.")

    # ── Step 3: Compute summary metrics ───────────────────────────────────────
    section("Step 3 — Summary Financial Metrics")
    s = compute_summary(df)

    print(f"\n  {'Metric':<40} {'Value':>18}")
    print(f"  {'─'*40}  {'─'*18}")
    print(f"  {'Number of Buses':<40} {s['n_buses']:>18,}")
    print(f"  {'Number of Rework Events':<40} {s['n_rework_events']:>18,}")
    print(f"  {'Baseline Production Cost':<40} {fmt_inr(s['base_production_cost'])}")
    print(f"  {'Total Traditional Rework Cost':<40} {fmt_inr(s['total_traditional_cost'])}")
    print(f"  {'Total Rework Cost (with overhead)':<40} {fmt_inr(s['total_rework_cost'])}")
    print(f"  {'Total Novel Cost (PAF-Adjusted)':<40} {fmt_inr(s['total_novel_cost'])}")
    print(f"  {'Total Production Cost (Trad.)':<40} {fmt_inr(s['total_production_cost'])}")
    print(f"  {'Rework as % of Production Cost':<40} {s['rework_pct_of_production']:>17.2f}%")
    print(f"  {'Hidden Cost Gap (Novel − Traditional)':<40} {fmt_inr(s['novel_vs_traditional_gap'])}")
    print(f"  {'Potential Savings (40% prevention)':<40} {fmt_inr(s['potential_savings'])}")

    # ── Step 4: Stage-wise breakdown ──────────────────────────────────────────
    section("Step 4 — Stage-Wise Cost Breakdown")
    stage_summary = (
        df.groupby("Production_Stage")
        .agg(
            Events          = ("Bus_ID",            "count"),
            Avg_Rework_Hrs  = ("Rework_Time",        "mean"),
            Traditional_INR = ("Traditional_Cost",   "sum"),
            Novel_INR       = ("Novel_Cost",         "sum"),
        )
        .round(2)
        .sort_values("Novel_INR", ascending=False)
    )

    print(f"\n  {'Stage':<32} {'Events':>6}  {'Avg Hrs':>7}  "
          f"{'Traditional':>14}  {'Novel Cost':>14}")
    print(f"  {'─'*32}  {'─'*6}  {'─'*7}  {'─'*14}  {'─'*14}")
    for stage, row in stage_summary.iterrows():
        abbr = stage[:30]
        print(
            f"  {abbr:<32} {int(row['Events']):>6}  "
            f"{row['Avg_Rework_Hrs']:>7.2f}  "
            f"₹{row['Traditional_INR']:>12,.0f}  "
            f"₹{row['Novel_INR']:>12,.0f}"
        )

    # ── Step 5: Generate charts ────────────────────────────────────────────────
    section("Step 5 — Generating Charts")
    chart_paths = generate_all_charts(df, s)
    print(f"\n  {len(chart_paths)} charts saved to the 'charts/' directory:")
    for p in chart_paths:
        print(f"    • {p}")

    # ── Final banner ───────────────────────────────────────────────────────────
    print("\n" + "═" * 62)
    print("  Analysis complete. Key takeaway:")
    gap_pct = (s["novel_vs_traditional_gap"] / s["total_traditional_cost"]) * 100
    print(f"  The novel PAF-adjusted model reveals {gap_pct:.1f}% more cost")
    print("  than traditional methods — hidden in late-stage defects.")
    print(f"  Upstream prevention could save up to {fmt_inr(s['potential_savings'])}.")
    print("═" * 62 + "\n")


if __name__ == "__main__":
    main()
