import json

def update_last_trade(result):

    with open("memory/trades.json", "r") as f:
        trades = json.load(f)

    trades[-1]["result"] = result

    with open("memory/trades.json", "w") as f:
        json.dump(trades, f, indent=4)