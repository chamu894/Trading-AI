from memory.performance import analyze_performance

def adjust_threshold():

    stats = analyze_performance()

    winrate = stats["winrate"]

    # adaptive threshold logic
    if winrate < 50:
        threshold = 0.75  # stricter trading
    elif winrate > 65:
        threshold = 0.60  # more aggressive
    else:
        threshold = 0.65

    return threshold