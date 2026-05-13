import MetaTrader5 as mt5

mt5.initialize()


def place_order(symbol, order_type, lot, sl, tp):

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        print("❌ Symbol tick error")
        return None

    price = tick.ask if order_type == "BUY" else tick.bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 10001,
        "comment": "AI TRADE",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result is None:
        print("❌ Order send failed")
        return None

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Trade failed: {result.retcode}")
        return None

    print("✅ Trade executed successfully")

    return result