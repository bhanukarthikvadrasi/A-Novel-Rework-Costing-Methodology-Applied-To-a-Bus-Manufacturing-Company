# Novel Rework Costing Methodology Applied To a Bus Manufacturing Company

> A Python-based analytical framework that reveals the **hidden costs of manufacturing defects** using a Stage-Weighted Defect Severity Index (SWDSI) — a novel improvement over traditional costing practices.

---

## 📖 Background

### What is Rework Costing?

In bus manufacturing, **rework** refers to any corrective action taken after a defect is identified on the production line — rewelding a cracked chassis joint, rewiring an incorrectly routed harness, or repainting a blistered body panel. Every rework event consumes additional labour, wastes materials, and stalls downstream assembly.

**Rework costing** is the practice of quantifying exactly how much each of these events costs the plant, so that management can prioritise quality improvement investment.

### The Problem with Traditional Methods

Traditional costing simply adds up **Labour + Material** and calls it the rework cost. This approach has two blind spots:

| What it misses | Why it matters |
|---|---|
| **Downstream delay cost** | A rework at engine integration can stall three downstream stations simultaneously |
| **Stage & severity weighting** | A paint blister found at final inspection costs far more than the same defect at the body shop, because all upstream work must be redone |

As a result, traditional methods can **underestimate true rework costs by 20–30%**, leading to under-investment in quality control at the most critical stages.

### What is Novel in This Methodology?

This project introduces the **Stage-Weighted Defect Severity Index (SWDSI)**:

```
SWDSI  = stage_weight(Production_Stage) × defect_weight(Defect_Type)

C_novel = (Labour + Material + Delay) × (1 + SWDSI)
```

- **`stage_weight`** — increases as defects appear later in production (0.10 at Chassis Fabrication → 0.50 at Quality Inspection), reflecting the compounding cost of reworking near-complete buses.
- **`defect_weight`** — higher for structurally or safety-critical defect types (welding, dimensional mismatch).
- The **(1 + SWDSI)** multiplier scales total direct costs upward, surfacing the hidden economic burden that traditional methods ignore.

---

## 📁 Project Structure

```
rework_costing/
│
├── main.py                      # Entry point — runs the full pipeline
├── data_generator.py            # Synthetic rework dataset (150 rows)
├── costing_model.py             # Three costing functions + report printer
├── visualization.py             # Three matplotlib charts
│
├── sample_data.csv              # Raw generated dataset (auto-created)
├── rework_costing_results.csv   # Enriched dataset with cost columns (auto-created)
│
├── plot1_rework_vs_total.png    # Chart 1 (auto-created)
├── plot2_stage_defects.png      # Chart 2 (auto-created)
├── plot3_trad_vs_novel.png      # Chart 3 (auto-created)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

**Prerequisites:** Python 3.8 or higher

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/rework-costing-bus-manufacturing.git
cd rework-costing-bus-manufacturing

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python main.py
```

On first run, this will:
1. Generate a synthetic dataset of 150 rework incidents → `sample_data.csv`
2. Apply all three costing models
3. Print the cost comparison report to the terminal
4. Save three charts as PNG files
5. Save the enriched results → `rework_costing_results.csv`

On subsequent runs, the existing `sample_data.csv` is loaded instead of regenerated.

---

##  Example Terminal Output

```
══════════════════════════════════════════════════════════
  REWORK COSTING REPORT – BUS MANUFACTURING PLANT
══════════════════════════════════════════════════════════
  Total incidents analysed  : 150
──────────────────────────────────────────────────────────
  Method                         Total Cost (USD)
──────────────────────────────────────────────────────────
  Traditional (Labour+Material)  $     18,194.34
  Standard Rework (+Delay)       $     23,398.90
  Novel SWDSI-Adjusted           $     24,790.55
──────────────────────────────────────────────────────────
  Rework cost as % of production : 56.3%
  Hidden cost revealed by novel  : $6,596.21
  Hidden cost as % of novel total: 26.6%
══════════════════════════════════════════════════════════
```

**Key insight:** The novel method reveals **$6,596** in hidden costs (26.6% of the true rework total) that traditional costing leaves unaccounted.

---

## 📈 Chart Explanations

### Chart 1 — `plot1_rework_vs_total.png`
**Rework Cost vs Total Cost by Production Stage**

A stacked bar chart showing, for each production stage, how much of the total cost is baseline labour vs rework overhead. Stages with a large amber (rework) segment are the plant's costliest quality failure points and should receive priority process improvement attention.

### Chart 2 — `plot2_stage_defects.png`
**Stage-Wise Defect Frequency**

A horizontal bar chart ranking each stage by the number of recorded defect incidents. Combine this with Chart 1 to distinguish between *high-frequency, low-cost* stages and *low-frequency, high-cost* stages — they require different management responses.

### Chart 3 — `plot3_trad_vs_novel.png`
**Traditional vs Novel (SWDSI) Cost Comparison by Stage**

A grouped bar chart placing traditional and novel cost estimates side-by-side for every stage. The percentage annotations on each novel bar show how much more the SWDSI method attributes to that stage relative to the traditional estimate. Shaded bands highlight the hidden-cost gap.

---

## 🔢 Costing Formulas

| Method | Formula |
|---|---|
| Traditional | `Labour_Cost + Material_Loss` |
| Standard Rework | `Labour_Cost + Material_Loss + Delay_Cost` |
| Novel (SWDSI) | `(Labour + Material + Delay) × (1 + stage_weight × defect_weight)` |

---

## 🗂️ Dataset Columns

| Column | Description |
|---|---|
| `Bus_ID` | Unique bus identifier (e.g. BUS-1042) |
| `Production_Stage` | Where in the line the defect was found |
| `Defect_Type` | Nature of the defect |
| `Rework_Time` | Hours spent on corrective action |
| `Labor_Cost` | Direct labour cost of rework (USD) |
| `Material_Loss` | Scrapped / wasted material cost (USD) |
| `Delay_Cost` | Downstream production delay cost (USD) |

---

## 🛠️ Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
```

---

## 📄 License

MIT License — free for academic and commercial use.

---

## 👤 Author

Developed as an academic/research project demonstrating quantitative cost engineering methods applied to heavy vehicle manufacturing.
