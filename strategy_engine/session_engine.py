from datetime import datetime
import pytz


def get_current_session():

    utc_now = datetime.now(pytz.utc)

    hour = utc_now.hour

    # London Open
    if 7 <= hour < 12:
        return "LONDON_OPEN"

    # Overlap Session
    elif 12 <= hour < 16:
        return "OVERLAP"

    # New York
    elif 16 <= hour < 20:
        return "NEWYORK_OPEN"

    else:
        return "OFF_SESSION"


def session_trade_allowed(session):

    allowed = [
        "LONDON_OPEN",
        "NEWYORK_OPEN",
        "OVERLAP"
    ]

    return session in allowed