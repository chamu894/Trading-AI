import json
import os
from datetime import datetime

FILE = "memory/trades.json"

def log_trade(data):

    data["time"] = str(datetime.now())

    # file exists check
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)

    # load existing
    with open(FILE, "r") as f:
        trades = json.load(f)

    trades.append(data)

    with open(FILE, "w") as f:
        json.dump(trades, f, indent=4)