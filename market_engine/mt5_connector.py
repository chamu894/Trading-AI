import MetaTrader5 as mt5
import pandas as pd

# MT5 initialize
mt5.initialize()

# Get market data
rates = mt5.copy_rates_from_pos(
    "GOLD",
    mt5.TIMEFRAME_M1,
    0,
    10
)

# Convert to dataframe
df = pd.DataFrame(rates)

# Print data
print(df)