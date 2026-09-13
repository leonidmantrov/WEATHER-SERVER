import random
from datetime import datetime, timezone, timedelta


def generate_airep(fir_code):
    """Генерирует сообщение AIREP (с борта воздушного судна)"""
    phenomena = [
        'MOD TURB',
        'SEV TURB',
        'MOD ICE',
        'SEV ICE',
        'WS',
        'MOD CAT',
        'SEV CAT'
    ]

    phenomenon = random.choice(phenomena)
    intensity = random.choice(['OBS', 'FCST'])

    lat = random.uniform(45, 75)
    lon = random.uniform(30, 150)

    flight_level = random.randint(50, 400) * 10

    now = datetime.now(timezone.utc)
    report_time = now - timedelta(minutes=random.randint(5, 60))

    callsign = f"AFL{random.randint(100, 999)}"

    raw = f"{callsign} {phenomenon} {intensity} AT "
    raw += f"{report_time.strftime('%H%M')}Z "
    raw += f"N{lat:.1f}E{lon:.1f} "
    raw += f"FL{flight_level}"

    return {
        'raw': raw,
        'latitude': lat,
        'longitude': lon
    }