import pandas as pd

def calculate_atr(df, period=14):

    df = df.copy()

    # True Range calculations
    df['high_low'] = df['high'] - df['low']

    df['high_close'] = abs(
        df['high'] - df['close'].shift(1)
    )

    df['low_close'] = abs(
        df['low'] - df['close'].shift(1)
    )

    # True Range
    df['true_range'] = df[
        ['high_low', 'high_close', 'low_close']
    ].max(axis=1)

    # ATR
    df['atr'] = df['true_range'].rolling(period).mean()

    return df

def volatility_state(df):

    latest_atr = df['atr'].iloc[-1]

    if latest_atr < 1:
        return "LOW_VOLATILITY"

    elif latest_atr > 5:
        return "HIGH_VOLATILITY"

    else:
        return "NORMAL_VOLATILITY"
    
def trade_allowed_by_volatility(state):

    blocked = [
        "LOW_VOLATILITY"
    ]

    return state not in blocked

def dynamic_sl_tp(price, atr, direction):

    if direction == "BUY":

        sl = price - (atr * 2)
        tp = price + (atr * 3)

    else:

        sl = price + (atr * 2)
        tp = price - (atr * 3)

    return sl, tp