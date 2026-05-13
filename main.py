import MetaTrader5 as mt5
import time

# =========================
# MARKET DATA
# =========================
from market_engine.data_stream import get_data

# =========================
# STRUCTURE + LIQUIDITY
# =========================
from indicators.market_structure import market_structure
from indicators.liquidity import liquidity_engine

# =========================
# FVG ENGINE
# =========================
from indicators.fvg import fvg_engine

# =========================
# ATR VOLATILITY ENGINE
# =========================
from indicators.atr_engine import (
    calculate_atr,
    volatility_state,
    trade_allowed_by_volatility,
    dynamic_sl_tp
)

# =========================
# CONFLUENCE ENGINE
# =========================
from strategy_engine.confluence import confluence_engine

# =========================
# SESSION ENGINE
# =========================
from strategy_engine.session_engine import (
    get_current_session,
    session_trade_allowed
)

# =========================
# MULTI TIMEFRAME ENGINE
# =========================
from strategy_engine.multi_timeframe import (
    multi_timeframe_bias,
    overall_market_bias
)

# =========================
# 📊 MARKET REGIME ENGINE (NEW)
# =========================
from strategy_engine.market_regime import (
    detect_market_regime,
    trade_allowed_by_regime
)

# =========================
# AI ENGINE
# =========================
from ai_engine.xgboost_model import (
    create_features,
    create_labels,
    train_model,
    predict
)

# =========================
# EXECUTION + RISK
# =========================
from execution.trade_executor import place_order
from risk_engine.risk_manager import calculate_lot

# =========================
# MEMORY SYSTEM
# =========================
from memory.learning_loop import adjust_threshold
from memory.trade_journal import log_trade

# =========================
# CONFIG
# =========================
SYMBOL = "GOLD"
INITIAL_BALANCE = 1000

# =========================
# MT5 INIT
# =========================
mt5.initialize()

# =========================
# TRAIN AI MODEL FIRST
# =========================
print("TRAINING AI MODEL...")

train_df = get_data(
    SYMBOL,
    mt5.TIMEFRAME_M1,
    500
)

if train_df.empty:
    print("NO TRAINING DATA FOUND")
    quit()

# -------------------------
# ATR
# -------------------------
train_df = calculate_atr(train_df)

# -------------------------
# FVG
# -------------------------
fvg = fvg_engine(train_df)

print("\nFVG DATA")
print(fvg)

# -------------------------
# SESSION
# -------------------------
session = get_current_session()
allowed = session_trade_allowed(session)

print("\nSESSION:", session)

# -------------------------
# MULTI TF BIAS
# -------------------------
biases = multi_timeframe_bias(SYMBOL)
overall_bias = overall_market_bias(biases)

print("\nMULTI TF BIAS")
print(biases)

print("\nOVERALL BIAS:", overall_bias)

# -------------------------
# FEATURE ENGINEERING
# -------------------------
train_df = create_features(train_df)
train_df = create_labels(train_df)

# -------------------------
# TRAIN MODEL
# -------------------------
model = train_model(train_df)

print("MODEL TRAINED SUCCESSFULLY")

# =========================
# MAIN LOOP
# =========================
while True:

    try:

        # =========================
        # 1. GET DATA
        # =========================
        df = get_data(
            SYMBOL,
            mt5.TIMEFRAME_M1,
            100
        )

        if df.empty:
            print("No market data")
            time.sleep(5)
            continue

        # =========================
        # 2. ATR
        # =========================
        df = calculate_atr(df)

        volatility = volatility_state(df)
        volatility_allowed = trade_allowed_by_volatility(volatility)

        # =========================
        # 3. FEATURES
        # =========================
        df = create_features(df)
        latest = df.iloc[-1]

        # =========================
        # 4. STRUCTURE
        # =========================
        structure = market_structure(df)

        # =========================
        # 5. LIQUIDITY
        # =========================
        liquidity = liquidity_engine(df)

        # =========================
        # 6. FVG
        # =========================
        fvg = fvg_engine(df)

        # =========================
        # 7. REGIME (NEW 🔥)
        # =========================
        regime = detect_market_regime(df)
        regime_allowed = trade_allowed_by_regime(regime)

        # =========================
        # 8. CONFLUENCE
        # =========================
        decision = confluence_engine(
            structure,
            liquidity,
            fvg
        )

        # =========================
        # 9. AI PROBABILITY
        # =========================
        probability = predict(model, latest)

        # =========================
        # 10. SESSION
        # =========================
        session = get_current_session()
        allowed = session_trade_allowed(session)

        # =========================
        # 11. MULTI TF BIAS
        # =========================
        biases = multi_timeframe_bias(SYMBOL)
        overall_bias = overall_market_bias(biases)

        # =========================
        # 12. THRESHOLD
        # =========================
        threshold = adjust_threshold()

        # =========================
        # LOG OUTPUT
        # =========================
        print("\n========================")
        print("AI TRADING SYSTEM")
        print("========================")

        print("SESSION:", session)
        print("REGIME:", regime)

        print("VOLATILITY:", volatility)

        print("\nMULTI TF BIAS")
        print(biases)

        print("\nOVERALL BIAS:", overall_bias)

        print("\nBOS:", structure["bos"])
        print("CHOCH:", structure["choch"])
        print("SWEEP:", liquidity["sweep"])
        print("FVG:", fvg["retrace"])

        print("\nREGIME ALLOWED:", regime_allowed)

        print("SCORE:", decision["score"])
        print("DECISION:", decision["decision"])

        print("\nPROBABILITY:", round(probability, 2))
        print("THRESHOLD:", threshold)

        # =========================
        # BUY LOGIC
        # =========================
        if (
            probability > threshold and
            decision["decision"] == "BUY" and
            allowed and
            volatility_allowed and
            regime_allowed and   # 🔥 NEW FILTER
            overall_bias == "OVERALL_BULLISH"
        ):

            lot = calculate_lot(INITIAL_BALANCE, 1)
            entry = latest["close"]
            atr = df['atr'].iloc[-1]

            sl, tp = dynamic_sl_tp(entry, atr, "BUY")

            result = place_order(
                SYMBOL,
                "BUY",
                lot,
                sl,
                tp
            )

            print("\nBUY TRADE EXECUTED")

            log_trade({
                "type": "BUY",
                "entry": float(entry),
                "sl": float(sl),
                "tp": float(tp),
                "probability": float(probability),
                "score": decision["score"],
                "volatility": volatility,
                "regime": regime,
                "session": session,
                "overall_bias": overall_bias,
                "result": str(result)
            })

        # =========================
        # SELL LOGIC
        # =========================
        elif (
            probability < (1 - threshold) and
            decision["decision"] == "SELL" and
            allowed and
            volatility_allowed and
            regime_allowed and   # 🔥 NEW FILTER
            overall_bias == "OVERALL_BEARISH"
        ):

            lot = calculate_lot(INITIAL_BALANCE, 1)
            entry = latest["close"]
            atr = df['atr'].iloc[-1]

            sl, tp = dynamic_sl_tp(entry, atr, "SELL")

            result = place_order(
                SYMBOL,
                "SELL",
                lot,
                sl,
                tp
            )

            print("\nSELL TRADE EXECUTED")

            log_trade({
                "type": "SELL",
                "entry": float(entry),
                "sl": float(sl),
                "tp": float(tp),
                "probability": float(probability),
                "score": decision["score"],
                "volatility": volatility,
                "regime": regime,
                "session": session,
                "overall_bias": overall_bias,
                "result": str(result)
            })

        else:
            print("\nNO TRADE")

        time.sleep(5)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)