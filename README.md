# Audit Analytics Dashboard

> End-to-end analytics engineering project — Python · DuckDB · dbt Core · Streamlit · OpenAI

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit)](https://fahim-audit-analytics.streamlit.app/)

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
| AI layer | OpenAI GPT-4o-mini | Natural language Q&A on data |

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
git clone https://github.com/YOUR_USERNAME/audit-analytics
cd audit-analytics
pip install -r requirements.txt
```

### 2. Add OpenAI API key (optional — dashboard works without it)

**Mac / Linux / Git Bash:**
```bash
mkdir .streamlit
echo 'OPENAI_API_KEY = "sk-your-key-here"' > .streamlit/secrets.toml
```

**Windows PowerShell:**
```powershell
New-Item -ItemType Directory -Force .streamlit
'OPENAI_API_KEY = "sk-your-key-here"' | Out-File .streamlit\secrets.toml -Encoding utf8
```

Get a free key at https://platform.openai.com/api-keys

### 3. Run everything

**Mac / Linux / Git Bash (one command):**
```bash
bash run.sh
```

**Windows PowerShell (step by step):**
```powershell
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

![Screenshot 1](data/Screenshot%201.JPG)
![Screenshot 2](data/Screenshot%202.JPG)
![Screenshot 3](data/Screenshot%203.JPG)
![Screenshot 4](data/Screenshot%204.JPG)
![Screenshot 5](data/Screenshot%205.JPG)

---

## Deploying Online (GitHub Pages + Streamlit Cloud)

### Live App — Streamlit Community Cloud (free)
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app** → select this repo → branch: `main` → main file: `app/dashboard.py`
3. Under **Advanced settings → Secrets**, add: `OPENAI_API_KEY = "sk-..."`
4. Click **Deploy** — you'll get a public URL to share

### Project Page — GitHub Pages
1. Go to your repo on GitHub → **Settings → Pages**
2. Source: **Deploy from a branch** → branch: `main`, folder: `/ (root)`
3. Click **Save** — your README becomes a public project page at:
   `https://YOUR_USERNAME.github.io/audit-analytics/`

---

## About

Built by **Md Fahim Al Efaji** — Analytics Engineer  
[LinkedIn](https://www.linkedin.com/in/fahim-al-efaji) · [Portfolio](https://fahim-a-efaji.github.io/portfolio/)
