import pandas as pd

def trend_strength(df):

    latest_close = df['close'].iloc[-1]

    sma_20 = df['close'].rolling(20).mean().iloc[-1]
    sma_50 = df['close'].rolling(50).mean().iloc[-1]

    distance = abs(sma_20 - sma_50)

    return distance

def volatility_strength(df):

    atr = df['atr'].iloc[-1]

    return atr

def choppy_market(df):

    recent_high = df['high'].rolling(20).max().iloc[-1]

    recent_low = df['low'].rolling(20).min().iloc[-1]

    range_size = recent_high - recent_low

    atr = df['atr'].iloc[-1]

    # small range + high noise
    if range_size < (atr * 3):
        return True

    return False

def detect_market_regime(df):

    trend = trend_strength(df)

    volatility = volatility_strength(df)

    choppy = choppy_market(df)

    # Trending market
    if trend > 5 and volatility > 2:
        return "TRENDING"

    # Volatile market
    elif volatility > 8:
        return "VOLATILE"

    # Choppy market
    elif choppy:
        return "CHOPPY"

    # Sideways market
    else:
        return "RANGING"
    

def trade_allowed_by_regime(regime):

    blocked = [
        "CHOPPY"
    ]

    return regime not in blocked

