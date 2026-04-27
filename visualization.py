"""
visualization.py
----------------
Generates four publication-quality charts for the rework costing analysis.

Charts produced
---------------
1. Rework Cost vs Total Production Cost  — Stacked bar by production stage
2. Stage-Wise Defect Frequency           — Horizontal bar chart
3. Traditional vs Novel Cost Comparison  — Grouped bar by stage
4. Defect-Type Cost Heatmap              — Average novel cost per defect per stage
"""

import matplotlib
matplotlib.use("Agg")           # Non-interactive backend (safe for all environments)

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import os

# ── Output directory ───────────────────────────────────────────────────────────
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Shared colour palette ──────────────────────────────────────────────────────
COLOR_TRADITIONAL = "#4C72B0"
COLOR_REWORK      = "#DD8452"
COLOR_NOVEL       = "#55A868"
COLOR_ACCENT      = "#C44E52"
STAGE_COLORS      = [
    "#4C72B0", "#DD8452", "#55A868",
    "#C44E52", "#8172B2", "#937860",
]

INR_FMT = mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.1f}L")  # lakhs


def _save(fig: plt.Figure, filename: str) -> str:
    """Save figure to charts/ directory and return file path."""
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[visualization] Saved → {path}")
    return path


# ──────────────────────────────────────────────────────────────────────────────
# CHART 1 — Rework Cost vs Total Production Cost (stacked bar by stage)
# ──────────────────────────────────────────────────────────────────────────────

def plot_rework_vs_total(df: pd.DataFrame, summary: dict) -> str:
    """
    Stacked bar chart showing how rework cost (novel model) and baseline
    production cost are distributed across each manufacturing stage.

    This helps management see *which* stage carries the largest rework burden
    relative to its baseline output value.

    Parameters
    ----------
    df      : enriched DataFrame with Novel_Cost and Production_Stage.
    summary : dict from costing_model.compute_summary().

    Returns
    -------
    str — File path of saved chart.
    """
    stage_novel  = df.groupby("Production_Stage")["Novel_Cost"].sum().sort_index()
    n_stages     = len(stage_novel)
    base_per_stg = summary["base_production_cost"] / n_stages  # equal split (illustrative)

    stages = stage_novel.index.tolist()
    x      = np.arange(len(stages))
    base_v = [base_per_stg] * len(stages)
    rew_v  = stage_novel.values

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(x, base_v, label="Baseline Production Cost", color="#AEC6E8", zorder=2)
    ax.bar(x, rew_v,  bottom=base_v, label="Rework Cost (Novel)", color=COLOR_NOVEL,
           alpha=0.88, zorder=2)

    ax.set_xticks(x)
    ax.set_xticklabels(stages, rotation=20, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(INR_FMT)
    ax.set_ylabel("Cost (INR, Lakhs)", fontsize=10)
    ax.set_title("Rework Cost vs Total Production Cost by Stage", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
    ax.set_axisbelow(True)

    fig.tight_layout()
    return _save(fig, "01_rework_vs_total.png")


# ──────────────────────────────────────────────────────────────────────────────
# CHART 2 — Stage-Wise Defect Frequency
# ──────────────────────────────────────────────────────────────────────────────

def plot_stage_defects(df: pd.DataFrame) -> str:
    """
    Horizontal bar chart showing how many rework events occurred at each stage.

    Identifies the highest-frequency defect stages — valuable for prioritising
    process improvement resources.

    Parameters
    ----------
    df : enriched DataFrame with Production_Stage column.

    Returns
    -------
    str — File path of saved chart.
    """
    counts = (
        df["Production_Stage"]
        .value_counts()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(counts.index, counts.values, color=STAGE_COLORS[::-1],
                   edgecolor="white", linewidth=0.6, zorder=2)

    # Annotate bar values
    for bar, val in zip(bars, counts.values):
        ax.text(
            val + 0.4, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=9, color="#333333"
        )

    ax.set_xlabel("Number of Rework Events", fontsize=10)
    ax.set_title("Stage-Wise Defect Frequency", fontsize=13, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.4, zorder=1)
    ax.set_axisbelow(True)

    fig.tight_layout()
    return _save(fig, "02_stage_defect_frequency.png")


# ──────────────────────────────────────────────────────────────────────────────
# CHART 3 — Traditional vs Novel Cost Comparison (grouped bar by stage)
# ──────────────────────────────────────────────────────────────────────────────

def plot_traditional_vs_novel(df: pd.DataFrame) -> str:
    """
    Grouped bar chart comparing total Traditional Cost vs Novel Cost per stage.

    The gap between bars shows the *additional hidden cost* uncovered by the
    novel stage-position-adjusted methodology — cost that traditional models
    simply miss.

    Parameters
    ----------
    df : enriched DataFrame with Traditional_Cost, Novel_Cost, Production_Stage.

    Returns
    -------
    str — File path of saved chart.
    """
    grp = df.groupby("Production_Stage").agg(
        Traditional_Cost=("Traditional_Cost", "sum"),
        Novel_Cost=("Novel_Cost", "sum"),
    ).sort_index()

    stages = grp.index.tolist()
    x      = np.arange(len(stages))
    width  = 0.38

    fig, ax = plt.subplots(figsize=(11, 6))
    b1 = ax.bar(x - width / 2, grp["Traditional_Cost"], width,
                label="Traditional Cost", color=COLOR_TRADITIONAL, zorder=2)
    b2 = ax.bar(x + width / 2, grp["Novel_Cost"], width,
                label="Novel Cost (PAF-Adjusted)", color=COLOR_NOVEL, zorder=2)

    ax.set_xticks(x)
    ax.set_xticklabels(stages, rotation=20, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(INR_FMT)
    ax.set_ylabel("Total Cost (INR, Lakhs)", fontsize=10)
    ax.set_title("Traditional vs Novel Cost by Production Stage", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
    ax.set_axisbelow(True)

    # Annotate percentage gap above each novel bar
    for rect_t, rect_n in zip(b1, b2):
        trad = rect_t.get_height()
        nov  = rect_n.get_height()
        gap_pct = ((nov - trad) / trad) * 100 if trad > 0 else 0
        ax.text(
            rect_n.get_x() + rect_n.get_width() / 2,
            nov + nov * 0.01,
            f"+{gap_pct:.0f}%",
            ha="center", va="bottom", fontsize=7.5, color=COLOR_ACCENT, fontweight="bold"
        )

    fig.tight_layout()
    return _save(fig, "03_traditional_vs_novel.png")


# ──────────────────────────────────────────────────────────────────────────────
# CHART 4 — Defect-Type Cost Heatmap
# ──────────────────────────────────────────────────────────────────────────────

def plot_defect_heatmap(df: pd.DataFrame) -> str:
    """
    Heatmap of average Novel Cost across Defect Types (rows) × Production
    Stages (columns).

    Reveals which defect-stage combinations are most costly — enabling targeted
    defect-prevention programmes.

    Parameters
    ----------
    df : enriched DataFrame with Defect_Type, Production_Stage, Novel_Cost.

    Returns
    -------
    str — File path of saved chart.
    """
    pivot = (
        df.pivot_table(
            index="Defect_Type",
            columns="Production_Stage",
            values="Novel_Cost",
            aggfunc="mean",
        )
        .fillna(0)
    )

    fig, ax = plt.subplots(figsize=(13, 6))
    cax = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=25, ha="right", fontsize=8.5)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)

    # Annotate cells with INR values in thousands
    for r in range(pivot.shape[0]):
        for c in range(pivot.shape[1]):
            val = pivot.values[r, c]
            if val > 0:
                ax.text(c, r, f"₹{val/1000:.1f}K",
                        ha="center", va="center", fontsize=7, color="black")

    cbar = fig.colorbar(cax, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("Avg Novel Cost (INR)", fontsize=9)
    cbar.ax.yaxis.set_major_formatter(INR_FMT)

    ax.set_title("Average Novel Cost Heatmap: Defect Type × Production Stage",
                 fontsize=12, fontweight="bold")

    fig.tight_layout()
    return _save(fig, "04_defect_heatmap.png")


# ──────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────

def generate_all_charts(df: pd.DataFrame, summary: dict) -> list:
    """
    Run all four chart functions and return a list of saved file paths.

    Parameters
    ----------
    df      : Enriched DataFrame (must already contain cost columns).
    summary : Summary dict from costing_model.compute_summary().

    Returns
    -------
    list of str — File paths of all saved charts.
    """
    paths = [
        plot_rework_vs_total(df, summary),
        plot_stage_defects(df),
        plot_traditional_vs_novel(df),
        plot_defect_heatmap(df),
    ]
    return paths
