from datetime import datetime
import pytz

def get_current_session():

    # UTC time
    utc_now = datetime.now(pytz.utc)

    hour = utc_now.hour

    # London Session
    if 7 <= hour < 10:
        return "LONDON_OPEN"

    # New York Session
    elif 12 <= hour < 15:
        return "NEWYORK_OPEN"

    # London + NY overlap
    elif 12 <= hour < 16:
        return "OVERLAP"

    else:
        return "OFF_SESSION"
    

def session_trade_allowed(session):

    allowed = [
        "LONDON_OPEN",
        "NEWYORK_OPEN",
        "OVERLAP"
    ]

    return session in allowed