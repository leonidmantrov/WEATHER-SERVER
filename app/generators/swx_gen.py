import random
from datetime import datetime, timezone


def generate_swx():
    """Генерирует сообщение SWX (космическая погода)"""
    effects = [
        'GNSS MOD',
        'HF COM MOD',
        'RAD SAT MOD',
        'GNSS SEV',
        'HF COM SEV'
    ]

    effect = random.choice(effects)

    now = datetime.now(timezone.utc)

    raw = f"SWX ADVISORY\n"
    raw += f"DTG: {now.strftime('%Y%m%d/%H%MZ')}\n"
    raw += f"SWXC: ACFJ\n"
    raw += f"SWX EFFECT: {effect}\n"
    raw += f"FCST SWX +6 HR: {now.strftime('%d/%H%MZ')} NOT AVBL\n"
    raw += f"RMK: END OF EVENT"

    # Случайный полигон (область воздействия)
    center_lat = random.uniform(50, 80)
    center_lon = random.uniform(0, 180)

    polygon = []
    for i in range(6):
        angle = i * 60
        lat = center_lat + random.uniform(-5, 5)
        lon = center_lon + random.uniform(-10, 10)
        polygon.append([lon, lat])

    return {
        'code': 'ACFJ',
        'raw': raw,
        'effect': effect,
        'polygon': polygon
    }