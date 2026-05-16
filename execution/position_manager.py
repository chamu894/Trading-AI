import MetaTrader5 as mt5


class PositionManager:

    # -------------------------
    # GET OPEN POSITIONS
    # -------------------------
    def get_open_positions(self, symbol):

        positions = mt5.positions_get(symbol=symbol)

        if positions is None:
            return []

        return positions
    
        # -------------------------
    # MOVE SL TO BREAK EVEN
    # -------------------------
    def break_even(self, position):

        entry = position.price_open
        current_sl = position.sl
        current_tp = position.tp

        # BUY
        if position.type == 0:

            if position.price_current > entry + 50:

                if current_sl < entry:

                    self.modify_sl(
                        position.ticket,
                        entry,
                        current_tp
                    )

        # SELL
        else:

            if position.price_current < entry - 50:

                if current_sl > entry:

                    self.modify_sl(
                        position.ticket,
                        entry,
                        current_tp
                    )


        # -------------------------
    # TRAILING STOP
    # -------------------------
    def trailing_stop(self, position):

        current_tp = position.tp

        # BUY
        if position.type == 0:

            new_sl = position.price_current - 30

            if new_sl > position.sl:

                self.modify_sl(
                    position.ticket,
                    new_sl,
                    current_tp
                )

        # SELL
        else:

            new_sl = position.price_current + 30

            if new_sl < position.sl:

                self.modify_sl(
                    position.ticket,
                    new_sl,
                    current_tp
                )  


        # -------------------------
    # MODIFY SL/TP
    # -------------------------
    def modify_sl(self, ticket, sl, tp):

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "sl": sl,
            "tp": tp
        }

        result = mt5.order_send(request)

        return result


         # -------------------------
    # PARTIAL CLOSE
    # -------------------------
    def partial_close(self, position):

        volume = position.volume / 2

        tick = mt5.symbol_info_tick(position.symbol)

        # BUY
        if position.type == 0:
            price = tick.bid
            order_type = mt5.ORDER_TYPE_SELL

        # SELL
        else:
            price = tick.ask
            order_type = mt5.ORDER_TYPE_BUY

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": volume,
            "type": order_type,
            "position": position.ticket,
            "price": price,
            "deviation": 20,
            "magic": 999999,
            "comment": "AI Partial Close"
        }

        result = mt5.order_send(request)

        return result                         