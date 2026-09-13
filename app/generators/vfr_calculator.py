def calculate_vfr(visibility, cloud_base):
    """Рассчитывает категорию полетов по NOAA и ICAO"""
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

    return icao, noaa