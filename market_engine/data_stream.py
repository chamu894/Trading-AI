import MetaTrader5 as mt5
import pandas as pd

# MT5 initialize
mt5.initialize()

# Get market data
def get_data(symbol, timeframe, candles):

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        candles
    )

    # Safety check
    if rates is None:
        print("ERROR: Could not fetch market data")
        return pd.DataFrame()

    df = pd.DataFrame(rates)

    # Convert time
    df['time'] = pd.to_datetime(
        df['time'],
        unit='s'
    )

    return df