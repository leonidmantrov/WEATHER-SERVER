"""
Парсер плана полета (FPL) в формате ICAO.
"""


class FlightPlan:
    """Класс для хранения распарсенного плана полета"""
    def __init__(self):
        self.callsign = None
        self.flight_rules = None
        self.aircraft_type = None
        self.wake_category = None
        self.equipment = None
        self.departure = None
        self.departure_time = None
        self.cruising_speed = None
        self.cruising_level = None
        self.route = None
        self.destination = None
        self.total_eet = None
        self.alternate = None
        self.other_info = None

    def get_route_points(self):
        """Извлекает точки маршрута"""
        if not self.route:
            return []

        points = []
        parts = self.route.split()

        for part in parts:
            # Пропускаем служебные обозначения
            if part in ['DCT', 'T', 'V', 'A', 'B', 'G', 'R']:
                continue
            # Пропускаем координаты
            if part.startswith(('N', 'E')) and any(c.isdigit() for c in part):
                continue
            # Если есть /, берем часть до /
            if '/' in part:
                point = part.split('/')[0]
                if point and len(point) >= 5:
                    points.append(point)
            else:
                # Обычная точка маршрута (5 букв)
                if len(part) == 5 and part.isalpha():
                    points.append(part)
                elif len(part) == 5 and part.isalnum():
                    points.append(part)

        return points

    def to_dict(self):
        """Возвращает словарь с данными плана"""
        return {
            'callsign': self.callsign,
            'aircraft_type': self.aircraft_type,
            'departure': self.departure,
            'destination': self.destination,
            'alternate': self.alternate,
            'cruising_level': self.cruising_level,
            'route_points': self.get_route_points()
        }


def parse_fpl(fpl_text):
    """
    Парсит план полета в формате ICAO.

    Пример плана:
    (FPL-SDM6346-IS
    -A319/M-SDFGHIRWY/B1L
    -ULMM1735
    -K0768F320 ASGO1K ASGOR T693 PILAN/K0779F330 M856 KUKUM/K0788F340
    M856 GIKUR/K0801F350 T458 BEPOL BEPO1A
    -ULLI0142 UUEE
    -PBN/B1D1A1S2O1 DOF/230220 REG/RA73216 EET/ULLL0005 SEL/ELPS
    CODE/151E00 OPR/SDM RALT/ULMM ULLI RMK/ACASII EQUIPPED)
    """
    plan = FlightPlan()

    # Очищаем текст
    fpl_text = fpl_text.strip()
    if fpl_text.startswith('('):
        fpl_text = fpl_text[1:]
    if fpl_text.endswith(')'):
        fpl_text = fpl_text[:-1]

    # Проверяем, что текст похож на план полета
    if not fpl_text or len(fpl_text) < 20:
        raise ValueError("Invalid flight plan: too short")

    # Разбиваем на строки
    lines = fpl_text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    # Убираем ведущие дефисы
    lines = [line[1:] if line.startswith('-') else line for line in lines]

    # Если менее 3 строк - план неполный
    if len(lines) < 3:
        raise ValueError("Invalid flight plan: incomplete")

    # Секция 0: FPL-SDM6346-IS
    if lines:
        line0 = lines[0]
        if line0.startswith('FPL'):
            line0 = line0[3:]
            if line0.startswith('-'):
                line0 = line0[1:]

        parts = line0.split('-')
        if len(parts) >= 1:
            plan.callsign = parts[0]
        if len(parts) >= 2:
            plan.flight_rules = parts[1]

    # Секция 1: A319/M-SDFGHIRWY/B1L (тип ВС и оборудование)
    if len(lines) > 1:
        line1 = lines[1]
        parts = line1.split('-')
        aircraft_part = parts[0] if parts else ''
        equipment_part = parts[1] if len(parts) > 1 else ''

        # Разбираем тип ВС и категорию
        if '/' in aircraft_part:
            aircraft_info = aircraft_part.split('/')
            plan.aircraft_type = aircraft_info[0]
            if len(aircraft_info) > 1:
                plan.wake_category = aircraft_info[1]
        else:
            plan.aircraft_type = aircraft_part

        # Оборудование
        if '/' in equipment_part:
            plan.equipment = equipment_part.split('/')[0]
        else:
            plan.equipment = equipment_part

    # Секция 2: ULMM1735 (аэродром вылета и время)
    if len(lines) > 2:
        line2 = lines[2]
        if len(line2) >= 4:
            plan.departure = line2[:4]
            plan.departure_time = line2[4:8] if len(line2) >= 8 else None

    # Секция 3: Маршрут (может занимать несколько строк)
    route_lines = []
    found_destination = False

    for i in range(3, len(lines)):
        line = lines[i]
        parts = line.split()

        # Проверяем, является ли строка аэродромом посадки
        # Формат: ULLI0142 UUEE (4 буквы + 4 цифры + запасной)
        if len(parts) >= 1:
            first = parts[0]
            if (len(first) >= 8 and
                first[:4].isalpha() and
                first[4:8].isdigit()):
                # Это аэродром посадки
                plan.destination = first[:4]
                plan.total_eet = first[4:8]
                if len(parts) >= 2:
                    plan.alternate = parts[1]
                found_destination = True
                break

        # Иначе это часть маршрута
        route_lines.append(line)

    # Обрабатываем маршрут
    if route_lines:
        route_text = ' '.join(route_lines)
        parts = route_text.split()

        if parts:
            # Первая часть - скорость и эшелон
            speed_level = parts[0]
            if 'F' in speed_level:
                f_index = speed_level.index('F')
                level = speed_level[f_index+1:f_index+4]
                plan.cruising_level = f"F{level}"
                speed_part = speed_level[:f_index]
                if speed_part and len(speed_part) > 1:
                    plan.cruising_speed = speed_part[1:]

            # Остальное - маршрут
            plan.route = ' '.join(parts[1:])

    # Секция 5: Дополнительная информация
    if found_destination:
        # Ищем строку с доп. информацией после аэродрома посадки
        for i in range(3, len(lines)):
            line = lines[i]
            if line.startswith(('PBN/', 'DOF/', 'REG/', 'EET/', 'SEL/', 'CODE/', 'OPR/', 'RALT/', 'RMK/')):
                plan.other_info = line
                break

    # Проверяем, что план содержит обязательные поля
    if not plan.departure:
        raise ValueError("Invalid flight plan: no departure aerodrome")

    if not plan.destination:
        raise ValueError("Invalid flight plan: no destination aerodrome")

    return plan