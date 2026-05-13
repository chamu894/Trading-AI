from indicators.market_structure import market_structure
from indicators.liquidity import liquidity_engine
from indicators.fvg import fvg_engine

# ATR IMPORT
from indicators.atr_engine import calculate_atr

from strategy_engine.confluence import confluence_engine

from ai_engine.xgboost_model import predict

from backtesting.simulator import simulate_trade


class BacktestEngine:

    def __init__(self, df, model, threshold=0.65):

        self.df = df
        self.model = model
        self.threshold = threshold

        self.trades = []
        self.balance = 1000

    def run(self):

        # =========================
        # MAIN LOOP
        # =========================
        for i in range(100, len(self.df) - 20):

            # =========================
            # PAST DATA
            # =========================
            data = self.df.iloc[:i].copy()

            # =========================
            # CALCULATE ATR
            # =========================
            data = calculate_atr(data)

            # =========================
            # MARKET ANALYSIS
            # =========================
            structure = market_structure(data)

            liquidity = liquidity_engine(data)

            fvg = fvg_engine(data)

            # =========================
            # CONFLUENCE DECISION
            # =========================
            decision = confluence_engine(
                structure,
                liquidity,
                fvg
            )

            # =========================
            # CURRENT CANDLE
            # =========================
            latest = data.iloc[-1]

            # =========================
            # AI PROBABILITY
            # =========================
            prob = predict(
                self.model,
                latest
            )

            # =========================
            # FUTURE DATA
            # =========================
            future_data = self.df.iloc[i:i + 20]

            # =========================
            # CURRENT ATR
            # =========================
            atr = data["atr"].iloc[-1]

            # Skip if ATR invalid
            if atr != atr:
                continue

            # =========================
            # BUY TRADE
            # =========================
            if (
                prob > self.threshold and
                decision["decision"] == "BUY"
            ):

                trade = simulate_trade(
                    direction="BUY",
                    entry=latest["close"],
                    future_data=future_data,
                    atr=atr
                )

                self.trades.append(trade)

            # =========================
            # SELL TRADE
            # =========================
            elif (
                prob < (1 - self.threshold) and
                decision["decision"] == "SELL"
            ):

                trade = simulate_trade(
                    direction="SELL",
                    entry=latest["close"],
                    future_data=future_data,
                    atr=atr
                )

                self.trades.append(trade)

        return self.trades