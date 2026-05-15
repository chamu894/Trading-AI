import sys
import os

# 🔥 MUST be FIRST
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd

from backtesting.metrics import calculate_metrics
from backtesting.equity_curve import analyze_equity

st.set_page_config(
    page_title="AI Trading Dashboard",
    layout="wide"
)

st.title("📊 AI Trading Performance Dashboard")

# =========================
# CSV PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(BASE_DIR, "data", "trades.csv")

# =========================
# LOAD DATA
# =========================
try:

    df = pd.read_csv(csv_path)

    # fill empty values
    df = df.fillna("")

except Exception as e:

    st.error(f"CSV LOAD ERROR: {e}")

    st.stop()

# =========================
# EMPTY FILE CHECK
# =========================
if df.empty:

    st.warning("No trade data found yet.")

    st.stop()

# =========================
# SHOW TABLE
# =========================
st.subheader("📋 Raw Trades Data")

st.dataframe(df)

# =========================
# CONVERT TO RECORDS
# =========================
trades = df.to_dict(orient="records")

# =========================
# METRICS
# =========================
metrics = calculate_metrics(trades)

equity = analyze_equity(trades)

# =========================
# DASHBOARD METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Trades",
    metrics["total_trades"]
)

col2.metric(
    "Winrate %",
    round(metrics["winrate"], 2)
)

col3.metric(
    "Profit Factor",
    equity["profit_factor"]
)

# =========================
# EQUITY CURVE
# =========================
st.subheader("📉 Equity Curve")

st.line_chart(equity["equity_curve"])

# =========================
# DRAWDOWN
# =========================
st.subheader("📉 Drawdown")

st.write(
    "Max Drawdown %:",
    equity["max_drawdown"]
)