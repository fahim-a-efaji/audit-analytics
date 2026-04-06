#!/bin/bash
# run.sh — runs the full pipeline end to end
# Usage: bash run.sh

set -e

echo ""
echo "=== Step 1: Generate synthetic data ==="
python data/generate_data.py

echo ""
echo "=== Step 2: Run dbt transformations ==="
cd dbt_project
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..

echo ""
echo "=== Step 3: Launch dashboard ==="
echo "Opening http://localhost:8501"
streamlit run app/dashboard.py
