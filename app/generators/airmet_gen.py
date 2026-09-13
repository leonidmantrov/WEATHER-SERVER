import random
from datetime import datetime, timezone, timedelta
from ..utils.time_utils import get_unix_timestamp


def generate_airmet(fir_code):
    """Генерирует структурированный AIRMET"""
    phenomena_types = ['MOD TURB', 'MOD ICE', 'MOD MTW']
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
        [lon + 1.5, lat],
        [lon + 1.5, lat + 1],
        [lon, lat + 1],
        [lon, lat]
    ]

    raw = f"{fir_code} AIRMET {number} VALID "
    raw += f"{valid_start.strftime('%d%H%M')}/{valid_end.strftime('%d%H%M')} "
    raw += f"{fir_code}-\n"
    raw += f"{fir_code} {phenomenon} {intensity} "
    raw += f"AT {lat:.1f}N {lon:.1f}E "
    raw += f"BLW FL100 MOV E {random.randint(10, 40)}KMH NC="

    properties = {
        "raw": raw,
        "validPeriod": {
            "begin": get_unix_timestamp(valid_start),
            "end": get_unix_timestamp(valid_end)
        },
        "number": str(number),
        "indexFir": fir_code,
        "phenomen": phenomenon,
        "intensiv": intensity
    }

    geometry = {
        "type": "Polygon",
        "coordinates": [polygon]
    }

    return {
        "properties": properties,
        "geometry": geometry
    }