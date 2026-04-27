# Novel Rework Costing Methodology Applied to a Bus Manufacturing Company

> A Python-based analytical framework that reveals the **true cost of manufacturing rework** using a stage-position-adjusted costing model grounded in the Prevention–Appraisal–Failure (PAF) quality-cost framework.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [What is Rework Costing?](#what-is-rework-costing)
3. [Problems with Traditional Methods](#problems-with-traditional-methods)
4. [The Novel Methodology](#the-novel-methodology)
5. [Project Structure](#project-structure)
6. [Installation](#installation)
7. [How to Run](#how-to-run)
8. [Example Terminal Output](#example-terminal-output)
9. [Charts Generated](#charts-generated)
10. [Key Results](#key-results)
11. [Methodology Reference](#methodology-reference)

---

## Project Overview

Bus manufacturing is a multi-stage, labour-intensive process spanning body fabrication, painting, electrical wiring, mechanical assembly, quality inspection, and final finishing. When a defect occurs at any stage, the unit must undergo **rework** — additional labour, material, and time to bring it back to specification.

This project implements and compares **three costing models** applied to a realistic synthetic dataset of 150 rework events across a bus manufacturing facility:

| Model | Description |
|---|---|
| **Traditional** | Simple sum of Labor + Material + Delay costs |
| **Rework Cost** | Adds overhead burden and subtracts scrap recovery |
| **Novel (PAF-Adjusted)** | Multiplies rework cost by a Stage Position Factor reflecting downstream compounding impact |

---

## What is Rework Costing?

**Rework** refers to corrective work performed on a bus unit that has failed to meet quality specifications during production. This includes re-welding cracked joints, re-painting blistered surfaces, re-routing wiring, or re-aligning misassembled components.

**Rework costing** is the discipline of quantifying the full financial impact of this corrective activity — not just the visible, direct costs, but also the hidden opportunity costs embedded in the production system.

---

## Problems with Traditional Methods

Traditional costing simply adds up three buckets:

```
Traditional Cost = Labor Cost + Material Loss + Delay Cost
```

This approach has three critical blind spots:

1. **Stage blindness** — A defect caught at Final Finishing is treated the same as one caught at Body Fabrication, even though the former has consumed far more value-added work.
2. **Overhead omission** — Factory overhead allocated to rework activities is not included.
3. **No prevention incentive** — Because all defects look equally costly regardless of when they are caught, there is no financial signal to motivate upstream quality investment.

---

## The Novel Methodology

The novel approach introduces a **Stage Position Factor (SPF)** derived from the PAF quality-cost model:

```
Novel Cost = Rework_Cost × Stage_Position_Factor(stage)
```

Where:

```
Rework_Cost = Labor_Cost + Material_Loss + Delay_Cost
              + (Labor_Cost × 0.18 overhead)
              - (Material_Loss × 0.05 scrap_recovery)
```

And the SPF values are:

| Production Stage | SPF |
|---|---|
| Body Fabrication | 1.00 |
| Painting & Surface Treatment | 1.15 |
| Electrical Wiring | 1.30 |
| Mechanical Assembly | 1.50 |
| Quality Inspection | 1.70 |
| Final Finishing | 1.90 |

**Why does this matter?** A weld crack repaired at Final Finishing (SPF = 1.90) effectively costs 90% more than the same repair at Body Fabrication (SPF = 1.00), because all intermediate production value is at risk and must be re-verified. The novel model exposes this hidden burden and creates a measurable financial case for **upstream defect prevention**.

---

## Project Structure

```
rework_costing/
│
├── main.py               # Entry point — runs the full analysis pipeline
├── data_generator.py     # Generates synthetic rework dataset (150 rows)
├── costing_model.py      # Implements the three costing models + summary metrics
├── visualization.py      # Produces 4 matplotlib charts
│
├── sample_data.csv       # Auto-generated dataset (created on first run)
├── requirements.txt      # Python dependencies
├── README.md             # This file
│
└── charts/               # Auto-created directory for output charts
    ├── 01_rework_vs_total.png
    ├── 02_stage_defect_frequency.png
    ├── 03_traditional_vs_novel.png
    └── 04_defect_heatmap.png
```

---

## Installation

**Prerequisites:** Python 3.8 or higher.

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/rework-costing-bus-manufacturing.git
cd rework-costing-bus-manufacturing

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run

```bash
python main.py
```

This single command will:
- Generate the 150-row synthetic dataset and save it as `sample_data.csv`
- Apply all three costing models to every row
- Print a formatted financial summary to the terminal
- Save four charts inside the `charts/` directory

---

## Example Terminal Output

```
══════════════════════════════════════════════════════════════
  Novel Rework Costing Methodology
  Applied to a Bus Manufacturing Company
══════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────
  Step 3 — Summary Financial Metrics
──────────────────────────────────────────────────────────────

  Metric                                                Value
  ────────────────────────────────────────  ──────────────────
  Number of Buses                                         150
  Number of Rework Events                                 150
  Baseline Production Cost                 ₹ 375,000,000.00
  Total Traditional Rework Cost            ₹   1,243,832.39
  Total Rework Cost (with overhead)        ₹   1,278,492.05
  Total Novel Cost (PAF-Adjusted)          ₹   1,696,561.84
  Total Production Cost (Trad.)            ₹ 376,243,832.39
  Rework as % of Production Cost                        0.33%
  Hidden Cost Gap (Novel − Traditional)    ₹     452,729.45
  Potential Savings (40% prevention)       ₹     678,624.74

──────────────────────────────────────────────────────────────
  Step 4 — Stage-Wise Cost Breakdown
──────────────────────────────────────────────────────────────

  Stage                            Events  Avg Hrs  Traditional      Novel Cost
  ────────────────────────────────  ──────  ───────  ──────────────  ────────────
  Mechanical Assembly                  22     8.46  ₹     272,485  ₹   419,215
  Body Fabrication                     24    12.52  ₹     359,429  ₹   370,755
  Painting & Surface Treatment         26     6.68  ₹     215,965  ₹   256,056
  Final Finishing                      23     3.19  ₹     128,578  ₹   249,711
  Electrical Wiring                    22     5.23  ₹     158,894  ₹   212,141
  Quality Inspection                   33     2.04  ₹     108,481  ₹   188,683

══════════════════════════════════════════════════════════════
  Analysis complete. Key takeaway:
  The novel PAF-adjusted model reveals 36.4% more cost
  than traditional methods — hidden in late-stage defects.
  Upstream prevention could save up to ₹     678,624.74.
══════════════════════════════════════════════════════════════
```

---

## Charts Generated

Four charts are automatically saved to the `charts/` directory:

### Chart 1 — Rework Cost vs Total Production Cost
**File:** `charts/01_rework_vs_total.png`

Stacked bar chart comparing baseline production cost against novel rework cost for each manufacturing stage. Shows which stage carries the largest rework burden relative to its productive output.

### Chart 2 — Stage-Wise Defect Frequency
**File:** `charts/02_stage_defect_frequency.png`

Horizontal bar chart showing how many rework events were recorded at each stage. Identifies the highest-frequency problem areas and directs process improvement focus.

### Chart 3 — Traditional vs Novel Cost Comparison
**File:** `charts/03_traditional_vs_novel.png`

Grouped bar chart overlaying traditional and novel costs side by side for each stage. The percentage gap labels above each pair quantify the hidden cost that traditional methods leave undetected.

### Chart 4 — Defect-Type Cost Heatmap
**File:** `charts/04_defect_heatmap.png`

Matrix heatmap of average novel cost across all combinations of defect type (rows) and production stage (columns). Reveals which specific defect-stage combinations are most financially damaging — directly informing targeted prevention spend.

---

## Key Results

Based on the 150-event simulation:

- Traditional costing **understates** true rework cost by **36.4%** compared to the novel PAF-adjusted model.
- The hidden cost gap between models is **₹4.53 lakh** across a 150-bus production run.
- Redirecting just 40% of that gap into upstream prevention programmes could yield savings of **₹6.79 lakh**.
- **Mechanical Assembly** and **Final Finishing** generate disproportionately high novel costs relative to their event counts, pointing to the highest-ROI stages for quality investment.

---

## Methodology Reference

This project is grounded in the following quality-cost frameworks:

- **PAF Model (Prevention–Appraisal–Failure):** Categorises quality costs into proactive prevention, inspection/appraisal, and reactive failure costs.
- **Taguchi Loss Function:** Conceptual basis for the compounding cost of quality deviation as production progresses.
- **Stage-Position Factor (SPF):** Novel contribution of this work — a stage-indexed multiplier that translates PAF theory into a practical, row-level cost adjustment applicable to production datasets.

---

*This project was developed as an academic and analytical demonstration of novel rework costing methodology. All data is synthetically generated.*
