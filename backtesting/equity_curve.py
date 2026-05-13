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

        if trade["result"] == "WIN":

            profit = risk * risk_reward

            balance += profit

        else:

            balance -= risk

        equity.append(balance)

    return equity

def calculate_drawdown(equity):

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

        if trade["result"] == "WIN":
            gross_profit += 2

        else:
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

