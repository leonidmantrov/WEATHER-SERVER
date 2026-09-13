import random
from datetime import datetime, timezone, timedelta
from ..utils.time_utils import get_unix_timestamp


def generate_gamet(fir_code, area_name, area_number):
    """Генерирует структурированный GAMET"""
    now = datetime.now(timezone.utc)
    valid_start = now
    valid_end = now + timedelta(hours=6)

    raw = f"{fir_code} GAMET VALID {valid_start.strftime('%d%H%M')}/{valid_end.strftime('%d%H%M')} "
    raw += f"{fir_code}-\n"
    raw += f"{fir_code} {area_name} {area_number} BLW FL100\n\n"
    raw += "SECN I\n"
    raw += f"SFC VIS: {random.choice(['5000', '8000', '10000'])} M\n"
    raw += f"SIG CLD: BKN {random.choice(['300', '600', '1000'])} M AGL\n"
    raw += "\nSECN II\n"
    raw += f"WIND/T: {random.randint(200, 300)}/{random.randint(3, 10)}MPS\n"
    raw += f"CLD: BKN SC {random.choice(['450', '600', '800'])} M AGL\n"
    raw += f"FZLVL: {random.choice(['0200', '0300', '0400'])} M AMSL\n"
    raw += f"MNM QNH: {random.randint(1015, 1030)} HPA="

    properties = {
        "raw": raw,
        "kind": "GAMET",
        "fir": fir_code,
        "areaName": area_name,
        "areaNumbers": [area_number],
        "validPeriod": {
            "begin": get_unix_timestamp(valid_start),
            "end": get_unix_timestamp(valid_end)
        }
    }

    return properties