import random
from datetime import datetime, timezone, timedelta
from ..utils.time_utils import get_unix_timestamp


def generate_sigmet(fir_code):
    """Генерирует структурированный SIGMET"""
    phenomena_types = [
        'SEV TURB',
        'SEV ICE',
        'SEV MTW',
        'HVY DS',
        'HVY SS',
        'RDOACT CLD'
    ]

    phenomenon = random.choice(phenomena_types)
    intensity = random.choice(['OBS', 'FCST'])
    number = random.randint(1, 99)

    now = datetime.now(timezone.utc)
    valid_start = now
    valid_end = now + timedelta(hours=4)

    lat = random.uniform(50, 70)
    lon = random.uniform(30, 150)

    polygon = [
        [lon, lat],
        [lon + 2, lat],
        [lon + 2, lat + 1],
        [lon, lat + 1],
        [lon, lat]
    ]

    raw = f"{fir_code} SIGMET {number} VALID "
    raw += f"{valid_start.strftime('%d%H%M')}/{valid_end.strftime('%d%H%M')} "
    raw += f"{fir_code}-\n"
    raw += f"{fir_code} FIR {intensity} {phenomenon} "
    raw += f"AT {lat:.1f}N {lon:.1f}E "
    raw += f"MOV E {random.randint(10, 40)}KMH NC="

    properties = {
        "raw": raw,
        "validPeriod": {
            "begin": get_unix_timestamp(valid_start),
            "end": get_unix_timestamp(valid_end)
        },
        "number": str(number),
        "indexFir": fir_code,
        "phenomen": phenomenon,
        "intensiv": intensity,
        "mov": {
            "speed": random.randint(10, 40),
            "direct": random.choice([0, 45, 90, 135, 180, 225, 270, 315])
        },
        "cnl": False,
        "cnlNum": None
    }

    geometry = {
        "type": "Polygon",
        "coordinates": [polygon]
    }

    return {
        "properties": properties,
        "geometry": geometry
    }