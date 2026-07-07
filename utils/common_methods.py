import time
import re

def create_saucedemo_session_cookie(context, expires_in_seconds=600, username="standard_user") -> None:
    future_expiration_time = int(time.time()) + expires_in_seconds

    context.add_cookies([{
        "name": "session-username",
        "value": username,
        "domain": "www.saucedemo.com",
        "path": "/",
        "expires": future_expiration_time,
        "httpOnly": False,
        "secure": False,
        "sameSite": "Lax"
    }])

def parse_currency_string_to_float(input_str: str) -> float:
    cleaned = re.sub(r"[^0-9.]", "", input_str)
    return float(cleaned) if cleaned else 0.0
    