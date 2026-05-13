class RiskManager:

    def __init__(self, balance=1000):

        self.balance = balance

        self.start_balance = balance
        self.daily_loss = 0
        self.max_drawdown = 0

        self.consecutive_losses = 0
        self.equity_peak = balance

    # -------------------------
    # LOT SIZE CALCULATION
    # -------------------------
    def calculate_lot(self, risk_percent=1):

        risk_amount = self.balance * (risk_percent / 100)

        # simplified pip value model
        lot = risk_amount / 100

        return round(lot, 2)

    # -------------------------
    # SL / TP CALCULATION
    # -------------------------
    def set_sl_tp(self, entry_price, direction, atr):

        if direction == "BUY":

            sl = entry_price - (atr * 2)
            tp = entry_price + (atr * 3)

        else:

            sl = entry_price + (atr * 2)
            tp = entry_price - (atr * 3)

        return sl, tp

    # -------------------------
    # RISK CHECK BEFORE TRADE
    # -------------------------
    def can_trade(self):

        # stop if too many losses
        if self.consecutive_losses >= 3:
            return False

        # stop if daily loss too high
        if self.daily_loss >= self.start_balance * 0.03:
            return False

        # stop if drawdown too high
        if self.balance < self.equity_peak * 0.9:
            return False

        return True

    # -------------------------
    # AFTER TRADE UPDATE
    # -------------------------
    def update_trade(self, profit_loss):

        self.balance += profit_loss

        if self.balance > self.equity_peak:
            self.equity_peak = self.balance

        # loss tracking
        if profit_loss < 0:
            self.daily_loss += abs(profit_loss)
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0