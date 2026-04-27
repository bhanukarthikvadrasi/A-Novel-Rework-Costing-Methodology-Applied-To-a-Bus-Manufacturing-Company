"""
data_generator.py
-----------------
Generates a realistic synthetic dataset simulating rework events
in a bus manufacturing facility.

Columns:
    Bus_ID           : Unique identifier for each bus unit
    Production_Stage : Manufacturing stage where the defect occurred
    Defect_Type      : Category of defect detected
    Rework_Time      : Hours spent on the rework activity
    Labor_Cost       : Direct labor cost incurred (INR)
    Material_Loss    : Cost of scrapped or wasted material (INR)
    Delay_Cost       : Cost attributed to production schedule delay (INR)
"""

import numpy as np
import pandas as pd

# ── Seed for reproducibility ───────────────────────────────────────────────────
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# ── Domain constants ───────────────────────────────────────────────────────────
PRODUCTION_STAGES = [
    "Body Fabrication",
    "Painting & Surface Treatment",
    "Electrical Wiring",
    "Mechanical Assembly",
    "Quality Inspection",
    "Final Finishing",
]

DEFECT_TYPES = [
    "Welding Crack",
    "Paint Blister",
    "Wire Short Circuit",
    "Misaligned Component",
    "Dimensional Deviation",
    "Surface Scratch",
    "Loose Fastener",
    "Fluid Leak",
]

# Stage-specific rework-time ranges in hours [min, max]
STAGE_REWORK_TIME = {
    "Body Fabrication":              (4.0, 20.0),
    "Painting & Surface Treatment":  (2.0, 10.0),
    "Electrical Wiring":             (1.5,  8.0),
    "Mechanical Assembly":           (3.0, 15.0),
    "Quality Inspection":            (0.5,  4.0),
    "Final Finishing":               (1.0,  6.0),
}

# Labor rate per hour (INR)
LABOR_RATE_PER_HOUR = 350.0

# Material loss base rate per rework-hour (INR)
MATERIAL_LOSS_BASE = 500.0

# Delay cost multiplier — later stages carry higher schedule penalties
DELAY_MULTIPLIER = {
    "Body Fabrication":              1.0,
    "Painting & Surface Treatment":  1.2,
    "Electrical Wiring":             1.5,
    "Mechanical Assembly":           1.8,
    "Quality Inspection":            2.2,
    "Final Finishing":               2.5,
}


def generate_dataset(n_records: int = 150) -> pd.DataFrame:
    """
    Generate a synthetic rework event dataset for bus manufacturing.

    Each row represents one rework incident on a specific bus unit at a
    specific production stage.

    Parameters
    ----------
    n_records : int
        Number of rework event rows to generate (default 150).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Bus_ID, Production_Stage, Defect_Type,
        Rework_Time, Labor_Cost, Material_Loss, Delay_Cost.
    """
    records = []

    for i in range(1, n_records + 1):
        # Randomly assign a production stage and defect type
        stage  = np.random.choice(PRODUCTION_STAGES)
        defect = np.random.choice(DEFECT_TYPES)

        # Rework time drawn from stage-specific range with slight noise
        t_min, t_max = STAGE_REWORK_TIME[stage]
        rework_time  = round(np.random.uniform(t_min, t_max), 2)

        # Labor cost = time × hourly rate (±10 % stochastic noise)
        labor_cost = round(
            rework_time * LABOR_RATE_PER_HOUR * np.random.uniform(0.90, 1.10), 2
        )

        # Material loss = base rate × rework time (±20 % stochastic noise)
        material_loss = round(
            MATERIAL_LOSS_BASE * rework_time * np.random.uniform(0.80, 1.20), 2
        )

        # Delay cost increases with how far downstream the defect was caught
        delay_cost = round(
            rework_time
            * LABOR_RATE_PER_HOUR
            * DELAY_MULTIPLIER[stage]
            * np.random.uniform(0.85, 1.15),
            2,
        )

        records.append(
            {
                "Bus_ID":           f"BUS-{i:04d}",
                "Production_Stage": stage,
                "Defect_Type":      defect,
                "Rework_Time":      rework_time,
                "Labor_Cost":       labor_cost,
                "Material_Loss":    material_loss,
                "Delay_Cost":       delay_cost,
            }
        )

    df = pd.DataFrame(records)
    return df


def save_sample_csv(df: pd.DataFrame, path: str = "sample_data.csv") -> None:
    """
    Persist the generated dataset to a CSV file.

    Parameters
    ----------
    df   : pd.DataFrame — Dataset to save.
    path : str          — Output file path (default: sample_data.csv).
    """
    df.to_csv(path, index=False)
    print(f"[data_generator] Dataset saved → {path}  ({len(df)} rows)")


if __name__ == "__main__":
    df = generate_dataset()
    save_sample_csv(df)
    print(df.head())
