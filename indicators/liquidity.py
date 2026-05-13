import pandas as pd

def find_equal_highs_lows(df, threshold=0.0005):

    highs = df['high']
    lows = df['low']

    equal_highs = []
    equal_lows = []

    # Equal highs
    for i in range(len(df)-1):

        if abs(highs.iloc[i] - highs.iloc[i+1]) < threshold:
            equal_highs.append(i)

        if abs(lows.iloc[i] - lows.iloc[i+1]) < threshold:
            equal_lows.append(i)

    return equal_highs, equal_lows

def detect_liquidity_sweep(df, equal_highs, equal_lows):

    last_price = df['close'].iloc[-1]

    last_high = df['high'].iloc[-1]
    last_low = df['low'].iloc[-1]

    # Sweep buy-side liquidity (highs taken)
    for i in equal_highs:
        if last_high > df['high'].iloc[i]:
            return "BUY_SIDE_SWEEP"

    # Sweep sell-side liquidity (lows taken)
    for i in equal_lows:
        if last_low < df['low'].iloc[i]:
            return "SELL_SIDE_SWEEP"

    return "NO_SWEEP"

def liquidity_zones(df, equal_highs, equal_lows):

    zones = []

    for i in equal_highs:
        zones.append({
            "type": "BUY_SIDE_LIQUIDITY",
            "price": df['high'].iloc[i]
        })

    for i in equal_lows:
        zones.append({
            "type": "SELL_SIDE_LIQUIDITY",
            "price": df['low'].iloc[i]
        })

    return zones

def liquidity_engine(df):

    equal_highs, equal_lows = find_equal_highs_lows(df)

    sweep = detect_liquidity_sweep(df, equal_highs, equal_lows)

    zones = liquidity_zones(df, equal_highs, equal_lows)

    return {
        "equal_highs": equal_highs,
        "equal_lows": equal_lows,
        "sweep": sweep,
        "zones": zones
    }