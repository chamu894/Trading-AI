import MetaTrader5 as mt5
from datetime import datetime, timedelta


class PnLTracker:

    def __init__(self):

        self.last_ticket = None

    # -------------------------
    # GET LATEST CLOSED TRADE
    # -------------------------
    def get_latest_closed_trade(self):

        date_to = datetime.now()
        date_from = date_to - timedelta(days=1)

        deals = mt5.history_deals_get(date_from, date_to)

        if deals is None:
            return None

        if len(deals) == 0:
            return None

        latest = deals[-1]

        # avoid duplicate processing
        if latest.ticket == self.last_ticket:
            return None

        self.last_ticket = latest.ticket

        return {
            "ticket": latest.ticket,
            "profit": latest.profit,
            "symbol": latest.symbol,
            "type": latest.type
        }