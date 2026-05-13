def detect_fvg(df):

    bullish_fvg = []
    bearish_fvg = []

    for i in range(2, len(df)):

        # Bullish FVG
        if df['low'].iloc[i] > df['high'].iloc[i - 2]:

            bullish_fvg.append({
                "index": i,
                "top": df['low'].iloc[i],
                "bottom": df['high'].iloc[i - 2]
            })

        # Bearish FVG
        if df['high'].iloc[i] < df['low'].iloc[i - 2]:

            bearish_fvg.append({
                "index": i,
                "top": df['low'].iloc[i - 2],
                "bottom": df['high'].iloc[i]
            })

    return bullish_fvg, bearish_fvg

def check_fvg_retrace(df, bullish_fvg, bearish_fvg):

    current_price = df['close'].iloc[-1]

    # Bullish retrace
    for fvg in bullish_fvg:

        if fvg['bottom'] <= current_price <= fvg['top']:
            return "BULLISH_FVG_RETRACE"

    # Bearish retrace
    for fvg in bearish_fvg:

        if fvg['bottom'] <= current_price <= fvg['top']:
            return "BEARISH_FVG_RETRACE"

    return "NO_FVG_RETRACE"


def fvg_engine(df):

    bullish_fvg, bearish_fvg = detect_fvg(df)

    retrace = check_fvg_retrace(
        df,
        bullish_fvg,
        bearish_fvg
    )

    return {
        "bullish_fvg": bullish_fvg,
        "bearish_fvg": bearish_fvg,
        "retrace": retrace
    }