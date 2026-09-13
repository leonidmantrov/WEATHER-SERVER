"""
Климатические зоны для аэродромов.
Определяет диапазоны температур и погодных условий для каждого аэродрома.
"""

# Климатические данные для каждого аэродрома (ICAO код)
CLIMATE_ZONES = {
    # === РОССИЯ: Московский узел ===
    'UUEE': {
        'temp_range': (-15, 25),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1030),
        'description': 'Умеренный'
    },
    'UUWW': {
        'temp_range': (-15, 25),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1030),
        'description': 'Умеренный'
    },
    'UUDD': {
        'temp_range': (-15, 25),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1030),
        'description': 'Умеренный'
    },
    'UUBW': {
        'temp_range': (-15, 25),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1030),
        'description': 'Умеренный'
    },

    # === РОССИЯ: Крупные хабы и миллионники ===
    'ULLI': {
        'temp_range': (-10, 22),
        'wind_range': (2, 15),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Прохладный'
    },
    'UNNT': {
        'temp_range': (-25, 25),
        'wind_range': (1, 13),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'UNKL': {
        'temp_range': (-25, 25),
        'wind_range': (1, 13),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'USSS': {
        'temp_range': (-22, 25),
        'wind_range': (1, 13),
        'visibility_range': (800, 10000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'UWWW': {
        'temp_range': (-18, 26),
        'wind_range': (1, 13),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'URRP': {
        'temp_range': (-10, 30),
        'wind_range': (2, 15),
        'visibility_range': (1000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Континентальный'
    },
    'URKK': {
        'temp_range': (-5, 32),
        'wind_range': (2, 14),
        'visibility_range': (1500, 10000),
        'pressure_range': (985, 1025),
        'description': 'Тёплый'
    },
    'URSS': {
        'temp_range': (5, 30),
        'wind_range': (1, 10),
        'visibility_range': (3000, 10000),
        'pressure_range': (995, 1020),
        'description': 'Субтропики'
    },
    'UWGG': {
        'temp_range': (-15, 25),
        'wind_range': (1, 12),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Умеренный'
    },
    'UWKD': {
        'temp_range': (-20, 27),
        'wind_range': (1, 13),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'USTR': {
        'temp_range': (-22, 24),
        'wind_range': (1, 13),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'USCC': {
        'temp_range': (-22, 25),
        'wind_range': (1, 13),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'UNOO': {
        'temp_range': (-25, 25),
        'wind_range': (1, 13),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'USPP': {
        'temp_range': (-25, 22),
        'wind_range': (1, 12),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1020),
        'description': 'Холодный'
    },
    'URMM': {
        'temp_range': (-5, 30),
        'wind_range': (2, 14),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Тёплый'
    },
    'URWW': {
        'temp_range': (-12, 30),
        'wind_range': (2, 15),
        'visibility_range': (1000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Континентальный'
    },
    'UWUU': {
        'temp_range': (-20, 27),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'UWPS': {
        'temp_range': (-18, 25),
        'wind_range': (1, 12),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'UWOO': {
        'temp_range': (-20, 28),
        'wind_range': (2, 15),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'URML': {
        'temp_range': (0, 32),
        'wind_range': (2, 18),
        'visibility_range': (2000, 10000),
        'pressure_range': (990, 1025),
        'description': 'Тёплый'
    },

    # === РОССИЯ: Север, Сибирь и Дальний Восток ===
    'ULAA': {
        'temp_range': (-25, 20),
        'wind_range': (2, 15),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1020),
        'description': 'Холодный'
    },
    'ULMM': {
        'temp_range': (-30, 15),
        'wind_range': (2, 18),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1020),
        'description': 'Арктический'
    },
    'ULPB': {
        'temp_range': (-20, 22),
        'wind_range': (2, 14),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1020),
        'description': 'Холодный'
    },
    'ULKK': {
        'temp_range': (-22, 23),
        'wind_range': (2, 14),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1020),
        'description': 'Холодный'
    },
    'UIII': {
        'temp_range': (-25, 25),
        'wind_range': (1, 12),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'UHHH': {
        'temp_range': (-25, 27),
        'wind_range': (2, 15),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Муссонный'
    },
    'UHWW': {
        'temp_range': (-15, 25),
        'wind_range': (2, 18),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Муссонный'
    },
    'UHPP': {
        'temp_range': (-20, 20),
        'wind_range': (2, 18),
        'visibility_range': (500, 8000),
        'pressure_range': (970, 1020),
        'description': 'Морской'
    },
    'UHMA': {
        'temp_range': (-30, 15),
        'wind_range': (2, 20),
        'visibility_range': (500, 8000),
        'pressure_range': (970, 1020),
        'description': 'Арктический'
    },
    'UHSS': {
        'temp_range': (-15, 22),
        'wind_range': (2, 15),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1020),
        'description': 'Муссонный'
    },
    'UEEE': {
        'temp_range': (-40, 25),
        'wind_range': (1, 12),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1025),
        'description': 'Резко континентальный'
    },
    'UERR': {
        'temp_range': (-45, 22),
        'wind_range': (1, 12),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1025),
        'description': 'Резко континентальный'
    },
    'USNN': {
        'temp_range': (-30, 23),
        'wind_range': (2, 15),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'USHS': {
        'temp_range': (-35, 20),
        'wind_range': (2, 15),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1020),
        'description': 'Арктический'
    },
    'USMM': {
        'temp_range': (-25, 24),
        'wind_range': (2, 15),
        'visibility_range': (500, 8000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },
    'UHBB': {
        'temp_range': (-30, 27),
        'wind_range': (1, 13),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Континентальный'
    },

    # === СНГ ===
    'UAAA': {
        'temp_range': (-20, 30),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'UACC': {
        'temp_range': (-30, 28),
        'wind_range': (2, 15),
        'visibility_range': (500, 10000),
        'pressure_range': (975, 1025),
        'description': 'Резко континентальный'
    },
    'UTAA': {
        'temp_range': (-10, 35),
        'wind_range': (1, 12),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Тёплый'
    },
    'UZFF': {
        'temp_range': (-5, 35),
        'wind_range': (1, 12),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Тёплый'
    },
    'UTFN': {
        'temp_range': (-5, 35),
        'wind_range': (1, 12),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Тёплый'
    },
    'UZST': {
        'temp_range': (0, 38),
        'wind_range': (1, 12),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Жаркий'
    },
    'UTDD': {
        'temp_range': (-5, 35),
        'wind_range': (1, 12),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Тёплый'
    },
    'UBBB': {
        'temp_range': (0, 35),
        'wind_range': (2, 18),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Тёплый'
    },
    'UMMS': {
        'temp_range': (-15, 25),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1025),
        'description': 'Умеренный'
    },
    'UUDL': {
        'temp_range': (-15, 25),
        'wind_range': (1, 12),
        'visibility_range': (1000, 10000),
        'pressure_range': (980, 1025),
        'description': 'Умеренный'
    },

    # === МЕЖДУНАРОДНЫЕ ===
    'LTFM': {
        'temp_range': (0, 35),
        'wind_range': (2, 15),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Средиземноморский'
    },
    'LTAI': {
        'temp_range': (5, 40),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Средиземноморский'
    },
    'OTHH': {
        'temp_range': (15, 45),
        'wind_range': (2, 15),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Пустынный'
    },
    'OMDB': {
        'temp_range': (15, 45),
        'wind_range': (2, 15),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Пустынный'
    },
    'OMAA': {
        'temp_range': (15, 45),
        'wind_range': (2, 15),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Пустынный'
    },
    'ZBAA': {
        'temp_range': (-15, 30),
        'wind_range': (1, 13),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'ZSPD': {
        'temp_range': (0, 35),
        'wind_range': (2, 15),
        'visibility_range': (1000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Субтропический'
    },
    'ZGGG': {
        'temp_range': (10, 38),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Субтропический'
    },
    'ZGSZ': {
        'temp_range': (10, 38),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Субтропический'
    },
    'ZYTX': {
        'temp_range': (-15, 30),
        'wind_range': (1, 13),
        'visibility_range': (800, 10000),
        'pressure_range': (980, 1025),
        'description': 'Континентальный'
    },
    'ZJSY': {
        'temp_range': (18, 38),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'VHHH': {
        'temp_range': (15, 35),
        'wind_range': (2, 15),
        'visibility_range': (3000, 10000),
        'pressure_range': (985, 1020),
        'description': 'Субтропический'
    },
    'VTBS': {
        'temp_range': (20, 38),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'VTSP': {
        'temp_range': (22, 38),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'VVTS': {
        'temp_range': (22, 38),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'VIDP': {
        'temp_range': (5, 40),
        'wind_range': (1, 12),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1020),
        'description': 'Субтропический'
    },
    'VOGO': {
        'temp_range': (20, 38),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'VCBI': {
        'temp_range': (22, 35),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'VRMM': {
        'temp_range': (25, 35),
        'wind_range': (1, 12),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'OIIE': {
        'temp_range': (-5, 35),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1025),
        'description': 'Континентальный'
    },
    'HECA': {
        'temp_range': (10, 38),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Пустынный'
    },
    'HESH': {
        'temp_range': (15, 42),
        'wind_range': (1, 13),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Пустынный'
    },
    'HEGN': {
        'temp_range': (15, 42),
        'wind_range': (1, 13),
        'visibility_range': (3000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Пустынный'
    },
    'HAAB': {
        'temp_range': (10, 30),
        'wind_range': (1, 12),
        'visibility_range': (2000, 10000),
        'pressure_range': (985, 1020),
        'description': 'Горный'
    },
    'GMMN': {
        'temp_range': (8, 30),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (990, 1025),
        'description': 'Средиземноморский'
    },
    'DAAG': {
        'temp_range': (5, 35),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (990, 1025),
        'description': 'Средиземноморский'
    },
    'DTTA': {
        'temp_range': (8, 35),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (990, 1025),
        'description': 'Средиземноморский'
    },
    'MUHA': {
        'temp_range': (18, 35),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'MUVR': {
        'temp_range': (18, 35),
        'wind_range': (1, 13),
        'visibility_range': (2000, 10000),
        'pressure_range': (990, 1020),
        'description': 'Тропический'
    },
    'UMKK': {
        'temp_range': (-5, 25),
        'wind_range': (2, 14),
        'visibility_range': (1500, 10000),
        'pressure_range': (985, 1025),
        'description': 'Мягкий'
    }
}

DEFAULT_CLIMATE = {
    'temp_range': (-10, 25),
    'wind_range': (1, 12),
    'visibility_range': (1000, 10000),
    'pressure_range': (980, 1030),
    'description': 'Умеренный'
}


def get_climate(icao_code):
    """Возвращает климатические данные для аэродрома"""
    return CLIMATE_ZONES.get(icao_code, DEFAULT_CLIMATE)