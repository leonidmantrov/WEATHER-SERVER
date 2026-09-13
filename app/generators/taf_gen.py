import random
from datetime import datetime, timezone, timedelta
from .climate_zones import get_climate
from ..utils.time_utils import get_unix_timestamp, generate_valid_period


def generate_taf(aerodrome):
    """Генерирует реалистичный прогноз TAF с учётом климатической зоны"""
    climate = get_climate(aerodrome.icao_code)

    # Период действия
    now = datetime.now(timezone.utc)
    valid_start = now - timedelta(hours=1)
    valid_end = now + timedelta(hours=23)

    # Базовый ветер
    wind_dir = random.choice([0, 45, 90, 135, 180, 225, 270, 315])
    wind_speed = random.randint(climate['wind_range'][0], climate['wind_range'][1])

    # Базовые видимость и облачность
    visibility = random.choice([5000, 8000, 10000])
    visibility = max(visibility, climate['visibility_range'][0])
    visibility = min(visibility, climate['visibility_range'][1])

    clouds = []
    if visibility < 5000:
        clouds.append({"amount": "BKN", "base": random.choice([300, 600, 1000])})
    else:
        clouds.append({"amount": random.choice(["FEW", "SCT"]), "base": random.choice([1000, 1500, 2000, 3000])})

    # Максимальная/минимальная температура
    max_temp = random.randint(climate['temp_range'][0], climate['temp_range'][1])
    min_temp = max_temp - random.randint(5, 12)
    max_time = get_unix_timestamp(now + timedelta(hours=12))
    min_time = get_unix_timestamp(now + timedelta(hours=3))

    # Периоды изменений TEMPO
    changes = []
    for _ in range(random.randint(1, 2)):
        ch_start, ch_end = generate_valid_period(
            base_time=now,
            min_start_hours=2,
            max_start_hours=6,
            min_duration_hours=2,
            max_duration_hours=4
        )

        changes.append({
            "changeIndicator": "TEMPORARY_FLUCTUATIONS",
            "validPeriod": {
                "begin": get_unix_timestamp(ch_start),
                "end": get_unix_timestamp(ch_end)
            },
            "surfaceWind": {
                "speed": wind_speed + random.randint(2, 6),
                "direction": (wind_dir + random.choice([-30, 0, 30])) % 360,
                "gustSpeed": wind_speed + random.randint(5, 10)
            }
        })

    # Формируем raw TAF
    taf = f"TAF {aerodrome.icao_code} "
    taf += f"{valid_start.strftime('%d%H%M')}Z {valid_start.strftime('%d%H')}/{valid_end.strftime('%d%H')} "
    taf += f"{wind_dir:03d}{wind_speed:02d}MPS "

    if visibility >= 10000:
        taf += "9999 "
    else:
        taf += f"{visibility} "

    for c in clouds:
        taf += f"{c['amount']}{c['base']:03d} "

    taf += f"TX{max_temp:02d}/{max_time // 3600 % 24:02d}Z "
    taf += f"TN{min_temp:02d}/{min_time // 3600 % 24:02d}Z "

    for ch in changes:
        taf += "TEMPO "
        begin = ch['validPeriod']['begin']
        end = ch['validPeriod']['end']
        taf += f"{begin // 3600 % 24:02d}{begin // 60 % 60:02d}/{end // 3600 % 24:02d}{end // 60 % 60:02d} "
        wind = ch['surfaceWind']
        taf += f"{wind['direction']:03d}{wind['speed']:02d}G{wind['gustSpeed']:02d}MPS "

    taf = taf.rstrip() + "="

    # Структурированный ответ
    properties = {
        "raw": taf,
        "kind": "TAF",
        "aerodrome": {
            "icao": aerodrome.icao_code,
            "name": aerodrome.name,
            "point": [aerodrome.longitude, aerodrome.latitude],
            "elevation": aerodrome.elevation
        },
        "issueTime": get_unix_timestamp(now),
        "validPeriod": {
            "begin": get_unix_timestamp(valid_start),
            "end": get_unix_timestamp(valid_end)
        },
        "surfaceWind": {
            "speed": wind_speed,
            "direction": wind_dir
        },
        "visibility": {
            "prevailing": visibility,
            "above": visibility >= 10000
        },
        "clouds": clouds,
        "temperatures": [
            {
                "maxTemp": str(max_temp),
                "maxTime": max_time,
                "minTemp": str(min_temp),
                "minTime": min_time
            }
        ],
        "changes": changes,
        "vfr": _calculate_vfr(visibility, clouds)
    }

    return properties


def _calculate_vfr(visibility, clouds):
    """Расчёт категории полётов по NOAA и ICAO"""
    bases = [c['base'] for c in clouds if c.get('base')]
    cloud_base = min(bases) if bases else 10000

    # ICAO
    if visibility >= 5000 and cloud_base >= 1500:
        icao = "VMC"
    else:
        icao = "IMC"

    # NOAA
    if visibility < 1600 or cloud_base < 500:
        noaa = "LIFR"
    elif visibility < 5000 or cloud_base < 1000:
        noaa = "IFR"
    elif visibility < 8000 or cloud_base < 3000:
        noaa = "MVFR"
    else:
        noaa = "VFR"

    return {"icao": icao, "noaa": noaa}