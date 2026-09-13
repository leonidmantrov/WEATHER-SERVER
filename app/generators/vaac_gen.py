import random
from datetime import datetime, timezone, timedelta


def generate_vaac(code):
    """Генерирует сообщение VAAC (вулканический пепел)"""
    volcanoes = [
        {'name': 'SHEVELUCH', 'lat': 56.65, 'lon': 161.36},
        {'name': 'KLYUCHEVSKOY', 'lat': 56.05, 'lon': 160.64},
        {'name': 'BEZYMIANNY', 'lat': 55.97, 'lon': 160.59},
        {'name': 'KARYMSKY', 'lat': 54.05, 'lon': 159.44}
    ]

    volcano = random.choice(volcanoes)

    now = datetime.now(timezone.utc)

    # Случайный полигон облака пепла
    center_lat = volcano['lat'] + random.uniform(-2, 2)
    center_lon = volcano['lon'] + random.uniform(-2, 2)

    polygon = []
    for i in range(6):
        angle = i * 60
        lat = center_lat + random.uniform(-0.5, 0.5)
        lon = center_lon + random.uniform(-0.5, 0.5)
        polygon.append([lon, lat])

    raw = f"VA ADVISORY\n"
    raw += f"DTG: {now.strftime('%Y%m%d/%H%MZ')}\n"
    raw += f"VAAC: {code}\n"
    raw += f"VOLCANO: {volcano['name']}\n"
    raw += f"PSN: N{volcano['lat']:.2f} E{volcano['lon']:.2f}\n"
    raw += f"OBS VA CLD: SFC/FL{random.randint(100, 300)} "
    raw += f"N{center_lat:.1f} E{center_lon:.1f}\n"
    raw += f"FCST VA CLD +6 HR: {random.randint(50, 300)}FT"

    return {
        'code': code,
        'raw': raw,
        'volcano': volcano['name'],
        'polygon': polygon
    }