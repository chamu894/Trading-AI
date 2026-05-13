def calculate_lot(balance, risk_percent=1):

    risk_amount = balance * (risk_percent / 100)

    lot = risk_amount / 100  # simplified model

    return round(lot, 2)

def set_sl_tp(entry_price, direction, atr):

    if direction == "BUY":

        sl = entry_price - (atr * 2)
        tp = entry_price + (atr * 3)

    else:

        sl = entry_price + (atr * 2)
        tp = entry_price - (atr * 3)

    return sl, tp