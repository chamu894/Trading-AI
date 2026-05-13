def calculate_metrics(trades):

    total_trades = len(trades)

    if total_trades == 0:

        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "winrate": 0
        }

    wins = 0
    losses = 0

    for t in trades:

        # SAFE result access
        result = t.get("result", "")

        # WIN CHECK
        if result in ["WIN", "PROFIT", "TP_HIT"]:
            wins += 1

        # LOSS CHECK
        elif result in ["LOSS", "SL_HIT"]:
            losses += 1

    # WINRATE
    winrate = (wins / total_trades) * 100

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "winrate": round(winrate, 2)
    }