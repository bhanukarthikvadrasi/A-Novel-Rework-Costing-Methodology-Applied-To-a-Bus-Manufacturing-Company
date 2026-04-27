"""
costing_model.py
----------------
Implements three costing approaches for bus manufacturing rework:

  1. Traditional Cost   — Simple sum of visible, direct cost components.
  2. Rework Cost        — Adds hidden costs often ignored by traditional methods
                          (overhead allocation, scrap recycling recovery).
  3. Novel Cost         — Integrates a stage-position penalty that captures the
                          compounding financial impact of late-stage defect
                          discovery (Prevention–Appraisal–Failure framework).

Novel methodology insight
-------------------------
In traditional costing, all rework events of equal monetary value are treated
identically regardless of *where* in the production sequence they occur.
However, a defect found during Final Finishing has already accumulated the full
value of every preceding operation. Fixing it at that point means re-doing or
protecting work that was done correctly — an opportunity cost not captured by
summing direct costs alone.

The Novel Cost formula introduces a Stage Position Factor (SPF) drawn from the
PAF (Prevention–Appraisal–Failure) quality-cost model, which penalises
downstream failure costs more heavily. This enables management to:
  • Prioritise upstream defect prevention investments.
  • Compare rework ROI across stages on a like-for-like basis.
  • Identify which defect types generate disproportionate downstream losses.
"""

import pandas as pd
import numpy as np

# ── Stage Position Factor (SPF) ────────────────────────────────────────────────
# Reflects the compounding opportunity cost of discovering a defect late.
# Stage 1 (Body Fabrication) has the lowest SPF; Stage 6 (Final Finishing)
# has the highest, because all upstream value-added work is at risk.
STAGE_POSITION_FACTOR = {
    "Body Fabrication":              1.00,
    "Painting & Surface Treatment":  1.15,
    "Electrical Wiring":             1.30,
    "Mechanical Assembly":           1.50,
    "Quality Inspection":            1.70,
    "Final Finishing":               1.90,
}

# Overhead recovery rate applied in the novel model (fraction of labor cost)
OVERHEAD_RATE = 0.18   # 18 % overhead burden on rework labor

# Scrap recovery rate — fraction of material loss partially recovered
SCRAP_RECOVERY_RATE = 0.05   # 5 % of material can be salvaged / recycled


# ──────────────────────────────────────────────────────────────────────────────
# 1. TRADITIONAL COSTING
# ──────────────────────────────────────────────────────────────────────────────

def calculate_traditional_cost(df: pd.DataFrame) -> pd.Series:
    """
    Traditional rework cost = Labor_Cost + Material_Loss + Delay_Cost.

    This is the simplest and most widely used approach. It sums only the
    three directly observable cost buckets without any stage adjustment.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing Labor_Cost, Material_Loss, Delay_Cost columns.

    Returns
    -------
    pd.Series
        Row-level traditional cost for each rework event.
    """
    traditional_cost = df["Labor_Cost"] + df["Material_Loss"] + df["Delay_Cost"]
    return traditional_cost.rename("Traditional_Cost")


# ──────────────────────────────────────────────────────────────────────────────
# 2. REWORK COST (enhanced direct cost)
# ──────────────────────────────────────────────────────────────────────────────

def calculate_rework_cost(df: pd.DataFrame) -> pd.Series:
    """
    Enhanced rework cost = Traditional_Cost
                         + Overhead_Burden
                         - Scrap_Recovery

    This intermediate model adds the indirect overhead allocated to rework
    activities and subtracts any scrap material that can be partially recovered,
    giving a more accurate picture of net rework expenditure.

    Formula
    -------
    Overhead_Burden  = Labor_Cost × OVERHEAD_RATE
    Scrap_Recovery   = Material_Loss × SCRAP_RECOVERY_RATE
    Rework_Cost      = Labor_Cost + Material_Loss + Delay_Cost
                       + Overhead_Burden - Scrap_Recovery

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing Labor_Cost, Material_Loss, Delay_Cost columns.

    Returns
    -------
    pd.Series
        Row-level enhanced rework cost for each event.
    """
    overhead_burden  = df["Labor_Cost"]   * OVERHEAD_RATE
    scrap_recovery   = df["Material_Loss"] * SCRAP_RECOVERY_RATE

    rework_cost = (
        df["Labor_Cost"]
        + df["Material_Loss"]
        + df["Delay_Cost"]
        + overhead_burden
        - scrap_recovery
    )
    return rework_cost.rename("Rework_Cost")


# ──────────────────────────────────────────────────────────────────────────────
# 3. NOVEL COSTING (stage-position-adjusted)
# ──────────────────────────────────────────────────────────────────────────────

def calculate_novel_cost(df: pd.DataFrame) -> pd.Series:
    """
    Novel rework cost = Rework_Cost × Stage_Position_Factor (SPF)

    The SPF captures the compounding financial impact of late defect discovery
    based on the Prevention–Appraisal–Failure (PAF) quality-cost framework.

    A defect corrected at Body Fabrication (SPF = 1.00) costs baseline price.
    The same defect corrected at Final Finishing (SPF = 1.90) costs 90 % more
    because all intermediate value-added work is implicitly at risk and must
    be re-verified or protected during the repair.

    Formula
    -------
    Novel_Cost = Rework_Cost × SPF(Production_Stage)

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing Labor_Cost, Material_Loss, Delay_Cost,
        and Production_Stage columns.

    Returns
    -------
    pd.Series
        Row-level novel (PAF-adjusted) cost for each rework event.
    """
    rework_cost = calculate_rework_cost(df)

    # Map each row's stage to its corresponding SPF value
    spf = df["Production_Stage"].map(STAGE_POSITION_FACTOR)

    novel_cost = rework_cost * spf
    return novel_cost.rename("Novel_Cost")


# ──────────────────────────────────────────────────────────────────────────────
# SUMMARY STATISTICS
# ──────────────────────────────────────────────────────────────────────────────

def compute_summary(df: pd.DataFrame) -> dict:
    """
    Compute high-level summary metrics comparing all three costing models.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset enriched with Traditional_Cost, Rework_Cost, Novel_Cost columns.

    Returns
    -------
    dict
        Dictionary of key financial metrics used for reporting.
    """
    total_traditional = df["Traditional_Cost"].sum()
    total_rework      = df["Rework_Cost"].sum()
    total_novel       = df["Novel_Cost"].sum()

    # Assumed baseline production cost per bus × number of unique buses
    n_buses              = df["Bus_ID"].nunique()
    base_production_cost = 2_500_000 * n_buses  # INR 25 lakh per bus (illustrative)
    total_production     = base_production_cost + total_traditional

    # Rework cost as a percentage of total production cost
    rework_pct = (total_traditional / total_production) * 100

    # Cost saving: novel model reveals additional hidden costs vs traditional
    novel_vs_traditional_gap = total_novel - total_traditional
    savings_if_prevented     = total_novel * 0.40  # 40 % addressable via upstream prevention

    return {
        "n_buses":                   n_buses,
        "n_rework_events":           len(df),
        "base_production_cost":      base_production_cost,
        "total_traditional_cost":    total_traditional,
        "total_rework_cost":         total_rework,
        "total_novel_cost":          total_novel,
        "total_production_cost":     total_production,
        "rework_pct_of_production":  rework_pct,
        "novel_vs_traditional_gap":  novel_vs_traditional_gap,
        "potential_savings":         savings_if_prevented,
    }
