"""
generate_data.py
Generates 5,000 synthetic financial transactions and loads them into DuckDB.
Run once before dbt: python data/generate_data.py
"""

import pandas as pd
from faker import Faker
import random
import duckdb
import os

fake = Faker()
random.seed(42)
Faker.seed(42)

VENDORS    = ["Acme Corp", "GlobalTech", "FastSupply", "PrimeSolutions", "NovaBuild"]
CATEGORIES = ["Travel", "IT Equipment", "Consulting", "Facilities", "Marketing"]
N_ROWS     = 5000
ANOMALY_RATE = 0.05   # 5% of rows will be anomalies

rows = []
for i in range(N_ROWS):
    amount = round(random.uniform(100, 50_000), 2)
    # inject anomalies — extreme high values
    if random.random() < ANOMALY_RATE:
        amount = round(random.uniform(200_000, 999_999), 2)

    rows.append({
        "transaction_id" : f"TXN-{i+1:05d}",
        "date"           : fake.date_between(start_date="-2y", end_date="today").isoformat(),
        "vendor"         : random.choice(VENDORS),
        "category"       : random.choice(CATEGORIES),
        "amount"         : amount,
        "submitted_by"   : fake.name(),
        "department"     : random.choice(["Finance", "HR", "IT", "Operations", "Legal"]),
        "approved"       : random.choices([True, False], weights=[85, 15])[0],
        "currency"       : "EUR",
    })

df = pd.DataFrame(rows)

# Always write to project root so dbt can find it
db_path = os.path.join(os.path.dirname(__file__), "..", "audit_analytics.duckdb")
db_path = os.path.normpath(db_path)

con = duckdb.connect(db_path)
con.execute("CREATE OR REPLACE TABLE raw_transactions AS SELECT * FROM df")
row_count = con.execute("SELECT COUNT(*) FROM raw_transactions").fetchone()[0]
con.close()

print(f"✅ Generated {row_count:,} transactions → {db_path}")
print(f"   Anomalies injected: ~{int(N_ROWS * ANOMALY_RATE)}")
