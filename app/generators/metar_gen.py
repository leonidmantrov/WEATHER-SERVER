import random
from datetime import datetime, timezone
from .climate_zones import get_climate


def generate_metar(aerodrome):
    """Генерирует реалистичную сводку METAR с учётом климатической зоны"""
    climate = get_climate(aerodrome.icao_code)

    # Ветер
    wind_dir = random.choice([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])
    wind_speed = random.randint(climate['wind_range'][0], climate['wind_range'][1])

    # Видимость
    visibility = random.choice([3000, 5000, 8000, 10000])
    visibility = max(visibility, climate['visibility_range'][0])
    visibility = min(visibility, climate['visibility_range'][1])

    # Температура и точка росы
    temperature = random.randint(climate['temp_range'][0], climate['temp_range'][1])
    dew_point = temperature - random.randint(0, 15)
    if dew_point < -50:
        dew_point = -50

    # Давление
    qnh = random.randint(climate['pressure_range'][0], climate['pressure_range'][1])

    # Облачность
    cloud_amounts = ['FEW', 'SCT', 'BKN', 'OVC']
    cloud_bases = [300, 600, 1000, 1500, 2000, 3000, 2700]
    amount = random.choice(cloud_amounts)
    base = random.choice(cloud_bases)

    clouds = [{
        "amount": amount,
        "base": base
    }]

    # Состояние ВПП
    runway_state = [{
        "direction": random.choice([6, 24, 18, 36]),
        "depositType": random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        "contamination": random.randint(0, 25),
        "depthOfDeposit": random.randint(0, 50),
        "estimatedSurfaceFrictionOrBrakingAction": random.randint(0, 95)
    }]

    # Время выпуска
    issue_time = datetime.now(timezone.utc)
    issue_time_str = issue_time.strftime('%d%H%M')

    # Формирование raw METAR
    metar = f"METAR {aerodrome.icao_code} {issue_time_str}Z "
    metar += f"{wind_dir:03d}{wind_speed:02d}MPS "

    if visibility >= 10000:
        metar += "9999 "
    else:
        metar += f"{visibility} "

    metar += f"{amount}{base:03d} "

    # Температура (отрицательные с M)
    if temperature < 0:
        temp_str = f"M{abs(temperature):02d}"
    else:
        temp_str = f"{temperature:02d}"

    if dew_point < 0:
        dew_str = f"M{abs(dew_point):02d}"
    else:
        dew_str = f"{dew_point:02d}"

    metar += f"{temp_str}/{dew_str} "
    metar += f"Q{qnh} "

    # Добавляем состояние ВПП в raw
    rwy_dir = runway_state[0]['direction']
    rwy_dep = runway_state[0]['depositType']
    rwy_cont = runway_state[0]['contamination']
    rwy_depth = runway_state[0]['depthOfDeposit']
    rwy_frict = runway_state[0]['estimatedSurfaceFrictionOrBrakingAction']
    metar += f"R{rwy_dir:02d}/{rwy_dep}{rwy_cont:02d}{rwy_depth:02d}{rwy_frict:02d} "

    metar += "NOSIG="

    # Формируем структурированный ответ
    properties = {
        "raw": metar,
        "kind": "METAR",
        "aerodrome": {
            "icao": aerodrome.icao_code,
            "name": aerodrome.name,
            "point": [aerodrome.longitude, aerodrome.latitude],
            "elevation": aerodrome.elevation
        },
        "issueTime": int(issue_time.timestamp()),
        "surfaceWind": {
            "speed": wind_speed,
            "direction": wind_dir
        },
        "visibility": {
            "prevailing": visibility,
            "above": visibility >= 10000
        },
        "clouds": clouds,
        "temperatureAir": str(temperature),
        "temperatureDew": str(dew_point),
        "pressureQnh": qnh,
        "runwayState": runway_state,
        "trendNosig": True,
        "vfr": _calculate_vfr(visibility, clouds)
    }

    return properties


def _calculate_vfr(visibility, clouds):
    """Расчёт категории полётов по NOAA и ICAO"""
    bases = [c['base'] for c in clouds if c.get('base')]
    if bases:
        cloud_base = min(bases)
    else:
        cloud_base = 10000

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

    return {
        "icao": icao,
        "noaa": noaa
    }