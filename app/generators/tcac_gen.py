import random
from datetime import datetime, timezone, timedelta


def generate_tcac(code):
    """Генерирует сообщение TCAC (тропический циклон)"""
    names = ['NIGEL', 'OPHELIA', 'PHILIPPE', 'RINA', 'SEAN', 'TAMMY']
    cyclone_name = random.choice(names)

    now = datetime.now(timezone.utc)

    # Случайная позиция циклона
    center_lat = random.uniform(10, 30)
    center_lon = random.uniform(140, 180)

    # Полигон циклона
    polygon = []
    for i in range(8):
        angle = i * 45
        lat = center_lat + random.uniform(-1, 1)
        lon = center_lon + random.uniform(-1, 1)
        polygon.append([lon, lat])

    raw = f"TC ADVISORY\n"
    raw += f"DTG: {now.strftime('%Y%m%d/%H%MZ')}\n"
    raw += f"TCAC: {code}\n"
    raw += f"TC: {cyclone_name}\n"
    raw += f"OBS PSN: {now.strftime('%d/%H%MZ')} "
    raw += f"N{center_lat:.1f} W{center_lon:.1f}\n"
    raw += f"MAX WIND: {random.randint(30, 120)}KT"

    return {
        'code': code,
        'raw': raw,
        'cyclone': cyclone_name,
        'polygon': polygon
    }