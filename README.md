# DSAN 6000 Final Project — Reddit Cost-of-Living & Economic Stress

## 🧭 Project Overview

This project analyzes how Reddit users discuss the **cost of living, inflation, wages, debt, and related economic stress** using a large-scale Reddit dataset.

We focus on activity between **January 2022 and March 2023**, a period marked by elevated inflation and financial pressure in many countries.

The work is organized into four cumulative milestones:

- **Milestone 1 (v0.1-eda):** Define questions, set up infrastructure, and perform Exploratory Data Analysis (EDA)
- **Milestone 2 (v0.2-nlp):** NLP cleaning, topic modeling, and external data overlay
- **Milestone 3 (v0.3-ml):** Predictive / classification / clustering models
- **Milestone 4 (v1.0-final):** Integrated analysis, final narrative, and public-facing deliverables

All development follows the course constraints: **no large data files in the repo**, clear structure, modular code, and reproducible analysis.

---

## 📦 Data Description

### 1. Primary Reddit Dataset

You will work with a preprocessed subset of the Reddit Archive:

- **Time window:** **Jan 2022 – Mar 2023**
- **Sources:**
  - Submissions parquet (~14 GB)
  - Comments parquet (~95 GB)
- **Preprocessing provided (by instructors):**
  - Reduced set of relevant fields
  - Unix timestamps converted to readable timestamps
  - Stored as **parquet** for efficient Spark processing

The full data is hosted in **Azure Blob Storage** and accessed from the class AzureML workspace.  
A typical layout (exact path provided in course materials) is:

```text
wasbs://reddit-project@dsan6000fall2024.blob.core.windows.net/202101-202303/submissions/
wasbs://reddit-project@dsan6000fall2024.blob.core.windows.net/202101-202303/comments/
```

with partitions like:

```text
.../submissions/year=YYYY/month=MM/*.parquet
.../comments/year=YYYY/month=MM/*.parquet
```

> ⚠️ **Do NOT commit** these parquet files or any other large datasets to the repo.

### 2. Local Sample Data (for Milestone 1)

For local development and debugging (no cluster required), we use:

```text
data/raw/submissions-sample.json
data/raw/comments-sample.json
```

These small samples:

- Mirror the schema of the full dataset sufficiently for testing
- Are used by `project_eda.ipynb` when `USE_SAMPLE = True`
- Ensure that all Spark logic is correct before scaling up in Azure

---

## 🌐 External Data: Stock Prices

To satisfy the **external data overlay** requirement and enable richer analysis, we include:

`code/stock_price_downloader.py`

This module:

- Uses `yfinance` to download daily historical stock prices
- Supports individual and multiple tickers
- Writes small CSV files to `data/raw/` (or returns DataFrames directly)
- Is designed to be imported and reused in notebooks

Example usage in a notebook:

```python
import stock_price_downloader as spd

# Download single stock for project window
nvda = spd.download_stock('NVDA', '2022-01-01', '2023-03-31', save_csv=True)

# Download multiple tech/market tickers
tickers = ['NVDA', 'AAPL', 'MSFT', 'SPY']
prices = spd.download_multiple_stocks(
    tickers,
    '2022-01-01',
    '2023-03-31',
    save_combined=True,
    save_individual=False
)
```

These stock price series can be:

- Aggregated to weekly/monthly levels
- Joined with Reddit-derived metrics (e.g., volume of cost-of-living posts, sentiment proxies)
- Used to explore relationships between **market behavior** and **public economic anxiety**

All downloaded CSVs must remain **small** and live under `data/raw/` or `data/external/`.

---

## 🧩 Analysis Theme

**Core theme:** *Reddit & the Cost of Living Crisis (2022–2023)*

Representative questions:

1. How frequently do Reddit users mention inflation, prices, rent, wages, and debt between Jan 2022 and Mar 2023?
2. Which communities (subreddits) host the most cost-of-living conversations?
3. How do engagement patterns (upvotes, comments) differ for economic-stress posts vs. other content?
4. Are there visible temporal patterns in cost-of-living posts that align with major economic events?
5. How can external data (e.g., stock prices, CPI) be overlaid with Reddit activity to contextualize public sentiment?

Milestone 1 focuses on:

- Defining at least **10 business goals** and **matching technical proposals**
- Verifying access to Reddit data via Spark (locally on samples; at scale in Azure)
- Conducting basic EDA, transformations, and visualizations
- Establishing a clean, reproducible project structure

---

## ⚙️ Environment & Tools

### Local Development (Sample Only)

1. Create/activate environment:
   ```bash
   conda activate dsan6000
   pip install pyspark pandas matplotlib yfinance
   ```

2. Run starter script (connectivity + sample check):
   ```bash
   python code/project_starter_script.py
   ```

3. Launch the EDA notebook:
   ```bash
   jupyter notebook code/project_eda.ipynb
   ```

In this mode, the notebook should use:
```python
USE_SAMPLE = True
```
to ensure only the JSON samples are read.

### AzureML + Serverless Spark (Full Reddit Parquet)

For big-data EDA (and later milestones):

1. Log into `https://ml.azure.com`, open your **group workspace**.
2. Use your **Compute Instance** for git operations.
3. Attach `project_eda.ipynb` to a **Serverless Spark** compute for Spark execution.
4. Set:
   ```python
   USE_SAMPLE = False
   ```
5. Load from the provided Azure Blob paths for `202101-202303`, then filter to **2022-01–2023-03**.
6. Write only **small aggregated outputs** (CSV/parquet) to:
   ```text
   azureml://datastores/workspaceblobstore/paths/<team-subdir>/
   ```
   and/or `data/processed/` in this repo.

---

## 📊 Notebook: `code/project_eda.ipynb`

Milestone 1 notebook includes:

1. **Project framing**
   - 10 business goals (non-technical)
   - 10 technical proposals (EDA, NLP, ML directions)

2. **Data loading & schema**
   - Configurable local vs Azure paths
   - Print schema and record counts
   - Explanation of key fields

3. **Data quality checks**
   - Missing value summaries
   - Simple filters (valid subreddits, non-deleted authors)

4. **Feature engineering**
   - Economic keyword flags (e.g., inflation, rent, mortgage, wage, price, loan, debt)
   - Text length metrics + bucketization
   - Time-based features where timestamps are available

5. **Summary tables**
   - Top subreddits for cost-of-living-related posts
   - Distribution of post lengths
   - Engagement comparison (flagged vs non-flagged)

6. **Visualizations**
   - Subreddit-level keyword activity
   - Length distributions
   - Economic vs non-economic post counts
   - Engagement distributions
   - Share of economic posts by subreddit

7. **External data hook**
   - Documentation on using `stock_price_downloader.py`
   - Plan to overlay stock trends with Reddit activity in later milestones

---

## 📁 Repository Structure

Aligned with course guidelines:

```text
dsan6000-final-project/
├── README.md
├── code/
│   ├── project_eda.ipynb
│   ├── project_starter_script.py
│   └── stock_price_downloader.py
├── data/
│   ├── raw/
│   │   ├── submissions-sample.json
│   │   ├── comments-sample.json
│   │   └── <small external CSVs e.g., stock prices>
│   └── processed/
│       └── <small summary tables for EDA>
├── docs/
│   └── <Milestone reports / rendered notebooks / website-ready artifacts>
└── website-source/
    └── <static site source for final presentation>
```

✅ No large parquet files or massive CSVs are tracked in git.

---

## ✅ Milestone 1 Submission Checklist

By tag **`v0.1-eda`**, this repo should contain:

- Updated `README.md` (this file)
- `code/project_eda.ipynb`:
  - 10 business goals & technical plans
  - EDA, cleaning, new features, tables, and plots
- `code/project_starter_script.py`
- `code/stock_price_downloader.py` (external stock data utility)
- `data/raw/` with only tiny sample & downloaded external CSVs
- `data/processed/` with small aggregated outputs
- Clean repo structure, no large data, no absolute paths, clear comments