def confluence_engine(structure, liquidity, fvg):

    score = 0
    signals = []

    # -------------------------
    # 1. MARKET STRUCTURE
    # -------------------------

    # Bullish BOS
    if structure["bos"] == "BULLISH_BOS":
        score += 2
        signals.append("BULLISH_STRUCTURE")

    # Bearish BOS
    if structure["bos"] == "BEARISH_BOS":
        score -= 2
        signals.append("BEARISH_STRUCTURE")

    # Bullish CHOCH
    if structure["choch"] == "BULLISH_CHOCH":
        score += 3
        signals.append("BULLISH_REVERSAL")

    # Bearish CHOCH
    if structure["choch"] == "BEARISH_CHOCH":
        score -= 3
        signals.append("BEARISH_REVERSAL")


    # -------------------------
    # 2. LIQUIDITY
    # -------------------------

    # Buy-side liquidity taken
    if liquidity["sweep"] == "BUY_SIDE_SWEEP":
        score -= 3
        signals.append("LIQUIDITY_TAKEN_BUY_SIDE")

    # Sell-side liquidity taken
    if liquidity["sweep"] == "SELL_SIDE_SWEEP":
        score += 3
        signals.append("LIQUIDITY_TAKEN_SELL_SIDE")


    # -------------------------
    # 3. FAIR VALUE GAP (FVG)
    # -------------------------

    # Bullish FVG retrace
    if fvg["retrace"] == "BULLISH_FVG_RETRACE":
        score += 2
        signals.append("BULLISH_FVG")

    # Bearish FVG retrace
    if fvg["retrace"] == "BEARISH_FVG_RETRACE":
        score -= 2
        signals.append("BEARISH_FVG")


    # -------------------------
    # FINAL DECISION
    # -------------------------

    if score >= 4:
        decision = "BUY"

    elif score <= -4:
        decision = "SELL"

    else:
        decision = "NO_TRADE"


    # -------------------------
    # RETURN RESULT
    # -------------------------

    return {
        "score": score,
        "signals": signals,
        "decision": decision
    }