import MetaTrader5 as mt5

from market_engine.data_stream import get_data
from indicators.market_structure import market_structure

TIMEFRAMES = {

    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M10": mt5.TIMEFRAME_M10,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,

    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,

    "D1": mt5.TIMEFRAME_D1,

    "W1": mt5.TIMEFRAME_W1,

    "MN1": mt5.TIMEFRAME_MN1
}

def get_tf_bias(symbol, timeframe):

    df = get_data(
        symbol,
        timeframe,
        200
    )

    structure = market_structure(df)

    bos = structure["bos"]

    if bos == "BULLISH_BOS":
        return "BULLISH"

    elif bos == "BEARISH_BOS":
        return "BEARISH"

    return "NEUTRAL"

def multi_timeframe_bias(symbol):

    biases = {}

    for name, tf in TIMEFRAMES.items():

        bias = get_tf_bias(symbol, tf)

        biases[name] = bias

    return biases

def overall_market_bias(biases):

    bullish = 0
    bearish = 0

    for tf, bias in biases.items():

        if bias == "BULLISH":
            bullish += 1

        elif bias == "BEARISH":
            bearish += 1

    if bullish > bearish:
        return "OVERALL_BULLISH"

    elif bearish > bullish:
        return "OVERALL_BEARISH"

    return "MIXED"

