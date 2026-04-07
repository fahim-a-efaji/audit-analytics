# Audit Analytics Dashboard

> End-to-end analytics engineering project — Python · DuckDB · dbt Core · Streamlit · OpenAI

Built to demonstrate a production-grade analytics pipeline using 100% free, local tools. Showcases the same skills used in enterprise audit analytics work: ETL pipelines, data modeling, anomaly detection, dashboarding, and AI-assisted data exploration.

---

## Architecture

```
Raw Data (Python/Faker)
      ↓
DuckDB (local warehouse)
      ↓
dbt Core (staging → intermediate → marts)
      ↓
Streamlit Dashboard + OpenAI GPT Chat
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data generation | Python + Faker | Synthetic financial transactions |
| Warehouse | DuckDB | Local OLAP database — no server needed |
| Transformation | dbt Core + dbt-duckdb | Staging, intermediate, and mart models |
| Anomaly detection | Python / SQL (Z-score) | Statistical outlier flagging |
| Dashboard | Streamlit + Plotly | Interactive KPI dashboard |
| AI layer | OpenAI GPT-3.5 | Natural language Q&A on data |

---

## Features

- **5,000 synthetic financial transactions** across 5 vendors, 5 categories, 2 years
- **Automated anomaly detection** using Z-score (flags transactions > 3 standard deviations from category mean)
- **Risk scoring** — HIGH / MEDIUM / LOW / NORMAL per transaction
- **dbt pipeline** with staging → intermediate → marts pattern, including data tests
- **Interactive dashboard** with KPI cards, bar charts, box plots, time series, and flagged transaction table
- **AI chat assistant** — ask questions in plain English, powered by OpenAI

---

## Setup & Run

### 1. Clone and install
```bash
git clone https://github.com/YOUR_USERNAME/audit-analytics-dashboard
cd audit-analytics-dashboard
pip install -r requirements.txt
```

### 2. Add OpenAI API key (optional — dashboard works without it)
```bash
# Get free key at https://platform.openai.com/api-keys
# Edit .streamlit/secrets.toml
OPENAI_API_KEY = "sk-your-key-here"
```

### 3. Run everything with one command
```bash
bash run.sh
```

### Or run step by step
```bash
# Step 1 — generate data
python data/generate_data.py

# Step 2 — run dbt transformations
cd dbt_project
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..

# Step 3 — launch dashboard
streamlit run app/dashboard.py
```

Dashboard opens at **http://localhost:8501**

---

## dbt Models

```
models/
├── staging/
│   └── stg_transactions.sql       — clean and standardise raw data
├── intermediate/
│   └── int_anomaly_flags.sql      — Z-score calculation and anomaly flagging
└── marts/
    ├── fct_transactions.sql       — final transaction fact table with risk levels
    └── fct_anomaly_summary.sql    — aggregated KPIs by vendor and category
```

---

## Dashboard Screenshots

![Screenshot 2](data/Screenshot%202.JPG)
![Screenshot 3](data/Screenshot%203.JPG)
![Screenshot 4](data/Screenshot%204.JPG)
![Screenshot 5](data/Screenshot%205.JPG)

---

## About

Built by **Md Fahim Al Efaji** — Analytics Engineer  
[LinkedIn](https://www.linkedin.com/in/fahim-al-efaji) · [Portfolio](https://fahim-a-efaji.github.io/portfolio/)
