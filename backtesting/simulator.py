def simulate_trade(
    direction,
    entry,
    future_data,
    atr
):

    # =========================
    # DYNAMIC SL / TP
    # =========================
    if direction == "BUY":

        sl = entry - (atr * 2)
        tp = entry + (atr * 3)

    else:

        sl = entry + (atr * 2)
        tp = entry - (atr * 3)

    # =========================
    # CHECK FUTURE CANDLES
    # =========================
    for i in range(len(future_data)):

        candle = future_data.iloc[i]

        high = candle["high"]
        low = candle["low"]

        # =========================
        # BUY TRADE
        # =========================
        if direction == "BUY":

            # STOP LOSS HIT
            if low <= sl:

                return {
                    "direction": direction,
                    "entry": entry,
                    "sl": sl,
                    "tp": tp,
                    "result": "LOSS"
                }

            # TAKE PROFIT HIT
            if high >= tp:

                return {
                    "direction": direction,
                    "entry": entry,
                    "sl": sl,
                    "tp": tp,
                    "result": "WIN"
                }

        # =========================
        # SELL TRADE
        # =========================
        else:

            # STOP LOSS HIT
            if high >= sl:

                return {
                    "direction": direction,
                    "entry": entry,
                    "sl": sl,
                    "tp": tp,
                    "result": "LOSS"
                }

            # TAKE PROFIT HIT
            if low <= tp:

                return {
                    "direction": direction,
                    "entry": entry,
                    "sl": sl,
                    "tp": tp,
                    "result": "WIN"
                }

    # =========================
    # TRADE STILL OPEN
    # =========================
    return {
        "direction": direction,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "result": "OPEN"
    }