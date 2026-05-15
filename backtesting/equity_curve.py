def build_equity_curve(
    trades,
    starting_balance=1000,
    risk_reward=2
):

    equity = [starting_balance]

    balance = starting_balance

    for trade in trades:

        # Risk 1%
        risk = balance * 0.01

        # SAFE result access
        result = trade.get("result", "")

        # WIN
        if result in ["WIN", "PROFIT", "TP_HIT"]:

            profit = risk * risk_reward

            balance += profit

        # LOSS
        elif result in ["LOSS", "SL_HIT"]:

            balance -= risk

        # UNKNOWN RESULT
        else:
            pass

        equity.append(balance)

    return equity


def calculate_drawdown(equity):

    if len(equity) == 0:
        return 0

    peak = equity[0]

    max_drawdown = 0

    for value in equity:

        if value > peak:
            peak = value

        drawdown = (peak - value) / peak

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return round(max_drawdown * 100, 2)


def profit_factor(trades):

    gross_profit = 0
    gross_loss = 0

    for trade in trades:

        result = trade.get("result", "")

        if result in ["WIN", "PROFIT", "TP_HIT"]:
            gross_profit += 2

        elif result in ["LOSS", "SL_HIT"]:
            gross_loss += 1

    if gross_loss == 0:
        return 0

    return round(gross_profit / gross_loss, 2)


def analyze_equity(trades):

    equity = build_equity_curve(trades)

    dd = calculate_drawdown(equity)

    pf = profit_factor(trades)

    return {
        "equity_curve": equity,
        "max_drawdown": dd,
        "profit_factor": pf
    }