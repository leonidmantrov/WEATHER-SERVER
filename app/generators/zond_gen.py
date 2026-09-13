import random
from datetime import datetime, timezone, timedelta


def generate_zond(fir_code):
    """Генерирует траекторию радиозонда"""
    # Случайная точка запуска
    start_lat = random.uniform(45, 75)
    start_lon = random.uniform(30, 150)

    # Время запуска (в пределах последних 2 часов)
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=random.randint(30, 120))

    # Генерация траектории
    path = []
    num_points = random.randint(10, 20)

    current_lat = start_lat
    current_lon = start_lon
    current_height = 0

    for i in range(num_points):
        # Высота увеличивается
        current_height += random.randint(500, 2000)

        # Смещение по горизонтали (зонд дрейфует)
        current_lat += random.uniform(-0.05, 0.05)
        current_lon += random.uniform(-0.05, 0.05)

        path.append({
            'lat': round(current_lat, 4),
            'lon': round(current_lon, 4),
            'height': current_height
        })

    return {
        'code': fir_code,
        'start': int(start_time.timestamp()),
        'end': int(start_time.timestamp() + num_points * 60),
        'path': path
    }