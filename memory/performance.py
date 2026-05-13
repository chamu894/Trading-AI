import json
import os

FILE = "memory/trades.json"

def analyze_performance():

    if not os.path.exists(FILE):

        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "winrate": 0
        }

    with open(FILE, "r") as f:
        trades = json.load(f)

    wins = 0
    losses = 0

    for t in trades:

        if t.get("result") == "WIN":
            wins += 1
        else:
            losses += 1

    total = wins + losses

    winrate = (
        (wins / total) * 100
        if total > 0 else 0
    )

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "winrate": winrate
    }