"""
dashboard.py
Audit Analytics Dashboard — Streamlit + DuckDB + OpenAI

Run: streamlit run app/dashboard.py
Requires: OPENAI_API_KEY in .streamlit/secrets.toml  OR  set as env var
"""

import os
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Audit Analytics Dashboard",
    page_icon="🔍",
    layout="wide",
)

# ── DB path ───────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "audit_analytics.duckdb")
DB_PATH = os.path.normpath(DB_PATH)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    con = duckdb.connect(DB_PATH, read_only=True)
    df      = con.execute("SELECT * FROM fct_transactions").df()
    summary = con.execute("SELECT * FROM fct_anomaly_summary").df()
    con.close()
    return df, summary


df, summary = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🔍 Audit Analytics Dashboard")
st.caption("Pipeline: Python → DuckDB → dbt Core → Streamlit + OpenAI | Built by Fahim Al Efaji")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Transactions",  f"{len(df):,}")
c2.metric("Total Amount",        f"€{df['amount'].sum():,.0f}")
c3.metric("Anomalies Detected",  f"{df['is_anomaly'].sum():,}")
c4.metric("Anomaly Rate",        f"{df['is_anomaly'].mean()*100:.1f}%")
c5.metric("High Risk",           f"{(df['risk_level']=='HIGH').sum():,}")

st.divider()

# ── Charts row 1 ─────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Anomalies by Vendor")
    vendor_anom = summary.groupby("vendor")["anomaly_count"].sum().reset_index()
    fig = px.bar(vendor_anom, x="vendor", y="anomaly_count",
                 color="anomaly_count", color_continuous_scale="Reds",
                 labels={"anomaly_count": "Anomalies", "vendor": "Vendor"})
    fig.update_layout(showlegend=False, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Risk Level Distribution")
    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]
    color_map = {"HIGH": "#E24B4A", "MEDIUM": "#BA7517", "LOW": "#1D9E75", "NORMAL": "#888"}
    fig2 = px.pie(risk_counts, names="risk_level", values="count",
                  color="risk_level", color_discrete_map=color_map)
    fig2.update_layout(margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts row 2 ─────────────────────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Monthly Transaction Volume")
    monthly = df.groupby(["year", "month"])["amount"].sum().reset_index()
    monthly["period"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)
    monthly = monthly.sort_values("period")
    fig3 = px.line(monthly, x="period", y="amount",
                   labels={"period": "Month", "amount": "Total Amount (€)"})
    fig3.update_layout(margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("Amount Distribution by Category")
    fig4 = px.box(df, x="category", y="amount", color="category",
                  points="outliers",
                  labels={"amount": "Amount (€)", "category": "Category"})
    fig4.update_layout(showlegend=False, margin=dict(t=10))
    st.plotly_chart(fig4, use_container_width=True)

# ── Anomaly table ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🚨 Flagged Transactions")

flagged = df[df["is_anomaly"]].sort_values("z_score", ascending=False)[[
    "transaction_id", "transaction_date", "vendor",
    "category", "amount", "z_score", "risk_level", "approved"
]].head(50)

st.dataframe(
    flagged.style.apply(
        lambda row: ["background-color: #fde8e8" if row["risk_level"] == "HIGH" else "" for _ in row],
        axis=1
    ),
    use_container_width=True
)

# ── AI Chat ───────────────────────────────────────────────────────────────────
st.divider()
st.subheader("🤖 AI Audit Assistant")
st.caption("Ask questions about the data in plain English — powered by OpenAI GPT")

# Get API key from Streamlit secrets or env var
api_key = None
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.warning("⚠️ No OpenAI API key found. Add OPENAI_API_KEY to .streamlit/secrets.toml to enable AI chat.")
    st.code("""
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-..."
    """)
else:
    from openai import OpenAI
    openai_client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("e.g. Which vendor has the most high-risk transactions?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        context = f"""
You are a senior audit data analyst. Answer concisely based on this dataset summary:

- Total transactions: {len(df):,}
- Total amount: €{df['amount'].sum():,.0f}
- Anomaly count: {df['is_anomaly'].sum():,} ({df['is_anomaly'].mean()*100:.1f}% rate)
- High risk transactions: {(df['risk_level']=='HIGH').sum():,}
- Vendors: {', '.join(df['vendor'].unique())}
- Categories: {', '.join(df['category'].unique())}
- Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}
- Top anomaly vendor: {summary.iloc[0]['vendor']} ({int(summary.iloc[0]['anomaly_count'])} anomalies)

Anomaly summary (top 5 rows):
{summary.head(5).to_string(index=False)}

Answer the question clearly. If you cannot answer from this data, say so.
        """

        with st.chat_message("assistant"):
            with st.spinner("Analysing..."):
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": context},
                        {"role": "user",   "content": prompt},
                    ],
                    max_tokens=300,
                )
                answer = response.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
