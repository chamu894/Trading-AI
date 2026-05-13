import pandas as pd

# =========================
# SWING DETECTION
# =========================
def detect_swings(df, window=2):

    highs = df['high']
    lows = df['low']

    swing_highs = []
    swing_lows = []

    for i in range(window, len(df) - window):

        is_swing_high = True
        is_swing_low = True

        for j in range(1, window + 1):

            # FIXED iloc indexing
            if (
                highs.iloc[i] <= highs.iloc[i - j]
                or highs.iloc[i] <= highs.iloc[i + j]
            ):
                is_swing_high = False

            if (
                lows.iloc[i] >= lows.iloc[i - j]
                or lows.iloc[i] >= lows.iloc[i + j]
            ):
                is_swing_low = False

        if is_swing_high:
            swing_highs.append(i)

        if is_swing_low:
            swing_lows.append(i)

    return swing_highs, swing_lows


# =========================
# BOS DETECTION
# =========================
def detect_bos(df, swing_highs, swing_lows):

    if len(swing_highs) == 0 or len(swing_lows) == 0:
        return "NO_BOS"

    last_high = df['high'].iloc[swing_highs[-1]]
    last_low = df['low'].iloc[swing_lows[-1]]

    current_price = df['close'].iloc[-1]

    if current_price > last_high:
        return "BULLISH_BOS"

    if current_price < last_low:
        return "BEARISH_BOS"

    return "NO_BOS"


# =========================
# CHOCH DETECTION
# =========================
def detect_choch(df, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "NO_CHOCH"

    recent_high = df['high'].iloc[swing_highs[-1]]
    prev_high = df['high'].iloc[swing_highs[-2]]

    recent_low = df['low'].iloc[swing_lows[-1]]
    prev_low = df['low'].iloc[swing_lows[-2]]

    current_price = df['close'].iloc[-1]

    # Bullish reversal
    if current_price > prev_high:
        return "BULLISH_CHOCH"

    # Bearish reversal
    if current_price < prev_low:
        return "BEARISH_CHOCH"

    return "NO_CHOCH"


# =========================
# MAIN STRUCTURE ENGINE
# =========================
def market_structure(df):

    swing_highs, swing_lows = detect_swings(df)

    bos = detect_bos(
        df,
        swing_highs,
        swing_lows
    )

    choch = detect_choch(
        df,
        swing_highs,
        swing_lows
    )

    return {
        "bos": bos,
        "choch": choch,
        "swing_highs": swing_highs,
        "swing_lows": swing_lows
    }