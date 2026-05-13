def calculate_metrics(trades):

    wins = 0
    losses = 0

    filtered_trades = []

    # =========================
    # FILTER OPEN TRADES
    # =========================
    for t in trades:

        if t["result"] == "OPEN":
            continue

        filtered_trades.append(t)

        if t["result"] == "WIN":
            wins += 1

        elif t["result"] == "LOSS":
            losses += 1

    # =========================
    # TOTAL TRADES
    # =========================
    total = wins + losses

    # =========================
    # WINRATE
    # =========================
    if total > 0:

        winrate = (wins / total) * 100

    else:

        winrate = 0

    # =========================
    # RETURN RESULTS
    # =========================
    return {

        "total_trades": total,

        "wins": wins,

        "losses": losses,

        "winrate": round(winrate, 2)
    }