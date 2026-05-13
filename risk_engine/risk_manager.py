class RiskManager:

    def __init__(self, balance=1000):

        self.balance = balance

        self.start_balance = balance
        self.daily_loss = 0

        self.consecutive_losses = 0
        self.equity_peak = balance

    # -------------------------
    # LOT SIZE
    # -------------------------
    def calculate_lot(self, risk_percent=1):

        risk_amount = self.balance * (risk_percent / 100)

        lot = risk_amount / 100

        return max(round(lot, 2), 0.01)

    # -------------------------
    # TRADE ALLOWED
    # -------------------------
    def can_trade(self):

        # consecutive losses
        if self.consecutive_losses >= 5:
            return False

        # daily loss
        if self.daily_loss >= self.start_balance * 0.05:
            return False

        # drawdown
        if self.balance < self.equity_peak * 0.85:
            return False

        return True

    # -------------------------
    # UPDATE AFTER TRADE
    # -------------------------
    def update_trade(self, profit_loss):

        self.balance += profit_loss

        if self.balance > self.equity_peak:
            self.equity_peak = self.balance

        if profit_loss < 0:
            self.daily_loss += abs(profit_loss)
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0