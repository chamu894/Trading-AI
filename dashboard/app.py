import sys
import os

# 🔥 MUST be FIRST (before any project imports)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd

from backtesting.engine import BacktestEngine
from backtesting.metrics import calculate_metrics
from backtesting.equity_curve import analyze_equity

st.set_page_config(page_title="AI Trading Dashboard", layout="wide")

st.title("📊 AI Trading Performance Dashboard")

# Load data
df = pd.read_csv("data/trades.csv")

st.subheader("Raw Trades Data")
st.dataframe(df)

# Convert trades
trades = df.to_dict(orient="records")

# Metrics
metrics = calculate_metrics(trades)
equity = analyze_equity(trades)

col1, col2, col3 = st.columns(3)

col1.metric("Total Trades", metrics["total_trades"])
col2.metric("Winrate %", round(metrics["winrate"], 2))
col3.metric("Profit Factor", equity["profit_factor"])

st.subheader("📉 Equity Curve")
st.line_chart(equity["equity_curve"])

st.subheader("📉 Drawdown")
st.write("Max Drawdown %:", equity["max_drawdown"])