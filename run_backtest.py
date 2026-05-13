import MetaTrader5 as mt5

from market_engine.data_stream import get_data

from ai_engine.xgboost_model import (
    train_model,
    create_features,
    create_labels
)

from backtesting.engine import BacktestEngine
from backtesting.metrics import calculate_metrics

# NEW IMPORT
from backtesting.equity_curve import analyze_equity

# =========================
# MT5 INIT
# =========================
mt5.initialize()

# =========================
# GET DATA
# =========================
df = get_data(
    "GOLD",
    mt5.TIMEFRAME_M1,
    1000
)

# =========================
# FEATURE ENGINEERING
# =========================
df = create_features(df)

df = create_labels(df)

# =========================
# TRAIN MODEL
# =========================
model = train_model(df)

# =========================
# RUN BACKTEST
# =========================
engine = BacktestEngine(
    df,
    model
)

trades = engine.run()

# =========================
# BASIC RESULTS
# =========================
results = calculate_metrics(trades)

print("\n========================")
print("BACKTEST RESULTS")
print("========================")

print(results)

# =========================
# EQUITY ANALYSIS
# =========================
equity_results = analyze_equity(
    trades
)

print("\n========================")
print("EQUITY ANALYSIS")
print("========================")

print(equity_results)

# =========================
# MT5 SHUTDOWN
# =========================
mt5.shutdown()