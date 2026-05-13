import os
import csv
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "data", "trades.csv")


class TradeLogger:

    def __init__(self):

        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

        # create file if not exists
        if not os.path.exists(FILE_PATH):

            with open(FILE_PATH, "w", newline="", encoding="utf-8") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "time",
                    "type",
                    "entry",
                    "sl",
                    "tp",
                    "lot",
                    "profit",
                    "probability",
                    "regime",
                    "session",
                    "result"
                ])

    # -------------------------
    # LOG TRADE
    # -------------------------
    def log(self, trade: dict):

        with open(FILE_PATH, "a", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now(),
                trade.get("type"),
                trade.get("entry"),
                trade.get("sl"),
                trade.get("tp"),
                trade.get("lot"),
                trade.get("profit"),
                trade.get("probability"),
                trade.get("regime"),
                trade.get("session"),
                trade.get("result")
            ])

        print("✅ Trade logged successfully")