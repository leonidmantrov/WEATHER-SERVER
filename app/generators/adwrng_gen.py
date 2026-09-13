import random
from datetime import datetime, timezone, timedelta

from app.utils.time_utils import get_unix_timestamp


def generate_adwrng(aerodrome):
    """Генерирует предупреждение по аэродрому"""
    warnings = [
        'TS FCST',
        'SFC WIND SPD 15MPS FCST',
        'FOG FCST',
        'HVY SNOW FCST',
        'ICE FCST',
        'WS FCST'
    ]

    warning_type = random.choice(warnings)

    now = datetime.now(timezone.utc)
    start = now
    end = now + timedelta(hours=random.randint(2, 6))

    number = random.randint(1, 99)

    raw = f"{aerodrome.icao_code} AD WRNG {number} "
    raw += f"{start.strftime('%d%H%M')} VALID {start.strftime('%d%H%M')}/{end.strftime('%d%H%M')} "
    raw += warning_type

    properties = {
        "icao": aerodrome.icao_code,
        "corrected": False,
        "number": number,
        "issueTime": get_unix_timestamp(now),
        "validPeriod": {
            "begin": get_unix_timestamp(start),
            "end": get_unix_timestamp(end)
        },
        "cancellation": False,
        "cancelled": None,
        "msg": warning_type,
        "raw": raw
    }

    return properties