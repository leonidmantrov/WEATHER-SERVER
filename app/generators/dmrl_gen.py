import random
from datetime import datetime, timezone


def generate_dmrl_polygon(radar, phenomenon_type='wdmrl'):
    """Генерирует данные ДМРЛ для радара"""
    # Создаем несколько полигонов вокруг радара
    polygons = []
    num_polygons = random.randint(1, 5)

    for i in range(num_polygons):
        # Центр полигона (в пределах радиуса радара)
        angle = random.uniform(0, 360)
        distance = random.uniform(10, radar.range_km * 0.8)

        # Приблизительный перевод км в градусы
        lat_offset = (distance * 0.009)  # 1 км ≈ 0.009 градуса
        lon_offset = (distance * 0.009) / 0.7  # Поправка на широту

        center_lat = radar.latitude + lat_offset * (1 if angle < 180 else -1)
        center_lon = radar.longitude + lon_offset * (1 if angle < 270 and angle > 90 else -1)

        # Размер полигона
        size = random.uniform(0.1, 0.5)

        polygon = [
            [center_lon - size, center_lat - size],
            [center_lon + size, center_lat - size],
            [center_lon + size, center_lat + size],
            [center_lon - size, center_lat + size],
            [center_lon - size, center_lat - size]
        ]

        if phenomenon_type == 'wdmrl':
            properties = {
                'phenomenon': random.randint(1, 5)
            }
        elif phenomenon_type == 'pdmrl':
            properties = {
                'intensity': round(random.uniform(0.5, 20), 1)
            }
        elif phenomenon_type == 'tdmrl':
            properties = {
                'height': random.randint(200, 10000)
            }

        polygons.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [polygon]
            },
            'properties': properties
        })

    return polygons