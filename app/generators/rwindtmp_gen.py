import random
from datetime import datetime, timezone, timedelta


def generate_wind_temp(lat, lon, fl, point_time):
    """Генерирует ветер и температуру для точки маршрута"""
    # Температура зависит от эшелона (высоты)
    # На уровне моря ~15°C, каждый километр -6.5°C
    height_km = fl * 30.48 / 1000  # Переводим футы в км (приблизительно)
    base_temp = 15 - (6.5 * height_km)

    # Добавляем случайные вариации
    temperature = base_temp + random.uniform(-3, 3)
    temperature = round(temperature, 1)

    # Ветер зависит от высоты
    if fl < 100:
        wind_speed = random.randint(3, 10)
    elif fl < 200:
        wind_speed = random.randint(8, 20)
    elif fl < 300:
        wind_speed = random.randint(15, 30)
    else:
        wind_speed = random.randint(20, 40)

    # Направление ветра
    wind_dir = random.choice([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])

    return {
        'pointFl': int(fl),
        'pointTime': int(point_time),
        'tmp': float(temperature),
        'wdir': int(wind_dir),
        'wind': int(wind_speed)
    }