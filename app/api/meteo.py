import random
import time
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, current_app
from ..core.auth import require_auth
from ..core.rate_limiter import rate_limiter
from ..models import Aerodrome, Radar, WeatherHistory
from ..generators.metar_gen import generate_metar
from ..generators.taf_gen import generate_taf
from ..generators.sigmet_gen import generate_sigmet
from ..generators.airmet_gen import generate_airmet
from ..generators.gamet_gen import generate_gamet
from ..generators.rwindtmp_gen import generate_wind_temp
from ..generators.adwrng_gen import generate_adwrng
from ..generators.wswrng_gen import generate_wswrng
from ..generators.dmrl_gen import generate_dmrl_polygon
from ..generators.airep_gen import generate_airep
from ..generators.zond_gen import generate_zond
from ..generators.vaac_gen import generate_vaac
from ..generators.tcac_gen import generate_tcac
from ..generators.swx_gen import generate_swx
from ..generators.fpl_parser import parse_fpl
from ..generators.brief_gen import create_brief_pdf
from ..utils.time_utils import get_unix_timestamp

meteo_bp = Blueprint('meteo', __name__)


@meteo_bp.route('/', methods=['GET', 'POST'])
@require_auth
def get_meteo():
    # Получаем токен из заголовка
    auth_header = request.headers.get('AUTHORIZATION', '')
    token = auth_header[7:] if auth_header.startswith('Bearer ') else ''

    # Проверяем rate limit
    allowed, error_msg = rate_limiter.check(token)
    if not allowed:
        return jsonify({
            'status': 'error',
            'message': error_msg
        }), 429

    mode = current_app.config.get('MODE', 'realtime')

    if request.method == 'POST':
        # Для POST только brief
        kind = request.args.get('kind')
        if kind == 'brief':
            return handle_brief(request)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Method not allowed'
            }), 405

    device = request.args.get('device')
    kind = request.args.get('kind')
    code = request.args.get('code')

    if not device:
        return jsonify({
            'status': 'error',
            'message': 'Invalid device'
        }), 400

    if not kind:
        return jsonify({
            'status': 'error',
            'message': 'Invalid kind'
        }), 400

    # Если режим history — отдаём данные из таблицы weather_history
    if mode == 'history':
        return handle_history(kind, code, request.args.get('time'))
    elif mode != 'realtime':
        return jsonify({
            'status': 'error',
            'message': 'Invalid mode'
        }), 400

    # Имитация задержки
    time.sleep(random.uniform(0.01, 0.1))

    # Обработка разных видов запросов
    if kind == 'metar':
        return handle_metar(code)
    elif kind == 'taf':
        return handle_taf(code)
    elif kind == 'sigmet':
        return handle_sigmet(code)
    elif kind == 'airmet':
        return handle_airmet(code)
    elif kind == 'gamet':
        return handle_gamet(code)
    elif kind == 'vfr':
        return handle_vfr(code)
    elif kind == 'rwindtmp':
        return handle_rwindtmp(request)
    elif kind == 'adwrng':
        return handle_adwrng(code)
    elif kind == 'wswrng':
        return handle_wswrng(code)
    elif kind == 'airep':
        return handle_airep(code)
    elif kind == 'zond':
        return handle_zond(code)
    elif kind == 'vaac':
        return handle_vaac(code)
    elif kind == 'tcac':
        return handle_tcac(code)
    elif kind == 'swx':
        return handle_swx()
    elif kind in ['wdmrl', 'pdmrl', 'tdmrl']:
        return handle_dmrl(code, kind, request.args.get('time'))
    elif kind == 'brief':
        return handle_brief(request)
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid kind'
        }), 400


def handle_history(kind, code, time_param):
    """Отдаёт данные из таблицы weather_history"""
    if not code:
        return jsonify({"status": "error", "message": "Aerodrome not found"}), 404

    if kind == 'metar':
        kind_str = 'METAR'
    elif kind == 'taf':
        kind_str = 'TAF'
    else:
        return jsonify({"status": "error", "message": "Kind not supported in history mode"}), 400

    # Определяем время
    if time_param:
        try:
            dt = datetime.fromtimestamp(int(time_param), tz=timezone.utc)
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid time"}), 400
    else:
        dt = datetime.now(timezone.utc)

    records = WeatherHistory.query.filter(
        WeatherHistory.aerodrome == code.upper(),
        WeatherHistory.date_time >= dt
    ).order_by(WeatherHistory.date_time).all()

    for record in records:
        props = record.weather_data.get('properties', {})
        if props.get('kind') == kind_str:
            return jsonify(record.weather_data)

    return jsonify({"status": "error", "message": "No data"}), 404


def handle_metar(code):
    if not code:
        return jsonify({"status": "error", "message": "Aerodrome not found"}), 404

    aerodrome = Aerodrome.query.filter_by(icao_code=code.upper()).first()
    if not aerodrome:
        return jsonify({"status": "error", "message": "Aerodrome not found"}), 404

    properties = generate_metar(aerodrome)

    response = {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": "Point",
            "coordinates": [aerodrome.longitude, aerodrome.latitude]
        }
    }

    return jsonify(response)


def handle_taf(code):
    if not code:
        return jsonify({"status": "error", "message": "Aerodrome not found"}), 404

    aerodrome = Aerodrome.query.filter_by(icao_code=code.upper()).first()
    if not aerodrome:
        return jsonify({"status": "error", "message": "Aerodrome not found"}), 404

    properties = generate_taf(aerodrome)

    response = {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": "Point",
            "coordinates": [aerodrome.longitude, aerodrome.latitude]
        }
    }

    return jsonify(response)


def handle_sigmet(code):
    fir_codes = code.split('.') if code else ['ULLL']
    features = []

    for fir_code in fir_codes:
        sigmet_data = generate_sigmet(fir_code)
        features.append({
            "type": "Feature",
            "geometry": sigmet_data["geometry"],
            "properties": sigmet_data["properties"]
        })

    return jsonify({
        "type": "FeatureCollection",
        "features": features,
        "totalFeatures": len(features),
        "date": get_unix_timestamp()
    })


def handle_airmet(code):
    fir_codes = code.split('.') if code else ['ULLL']
    features = []

    for fir_code in fir_codes:
        airmet_data = generate_airmet(fir_code)
        features.append({
            "type": "Feature",
            "geometry": airmet_data["geometry"],
            "properties": airmet_data["properties"]
        })

    return jsonify({
        "type": "FeatureCollection",
        "features": features,
        "totalFeatures": len(features),
        "date": get_unix_timestamp()
    })


def handle_gamet(code):
    area_name = request.args.get('area_name', 'MOSCOW')
    area_number = request.args.get('area_number', '1')
    fir_code = 'ULLL'

    properties = generate_gamet(fir_code, area_name, area_number)

    return jsonify({
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": properties,
            "geometry": None
        }],
        "totalFeatures": 1,
        "date": get_unix_timestamp()
    })


def handle_vfr(code):
    """Обработка запроса VFR"""
    if not code:
        return jsonify({
            'status': 'error',
            'message': 'Aerodromes not found'
        }), 404

    codes = code.split('.')

    features = []
    for aerodrome_code in codes:
        aerodrome = Aerodrome.query.filter_by(icao_code=aerodrome_code.upper()).first()

        if aerodrome:
            visibility = random.choice([1000, 2000, 5000, 8000, 10000])
            cloud_base = random.choice([300, 600, 1000, 1500, 3000])

            # Рассчитываем категории
            if visibility >= 5000 and cloud_base >= 1500:
                icao = "VMC"
            else:
                icao = "IMC"

            if visibility < 1600 or cloud_base < 500:
                noaa = "LIFR"
            elif visibility < 5000 or cloud_base < 1000:
                noaa = "IFR"
            elif visibility < 8000 or cloud_base < 3000:
                noaa = "MVFR"
            else:
                noaa = "VFR"

            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [aerodrome.longitude, aerodrome.latitude]
                },
                'properties': {
                    'code': aerodrome.icao_code,
                    'icao': icao,
                    'noaa': noaa,
                    'time': get_unix_timestamp()
                }
            })

    if not features:
        return jsonify({
            'status': 'error',
            'message': 'Aerodromes not found'
        }), 404

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features)
    })


def handle_rwindtmp(request):
    """Обработка запроса ветра и температуры по маршруту"""
    points = []

    # Собираем все точки из параметров p[0], p[1], ...
    for i in range(250):  # Максимум 250 точек
        point_str = request.args.get(f'p[{i}]')
        if not point_str:
            break

        # Парсим строку вида: x37.5y55.6z150t1685450553
        # или: x37.5y55.6t1685450553 (без эшелона)
        try:
            lon = None
            lat = None
            fl = None
            point_time = get_unix_timestamp()

            # Разбиваем строку на части
            # Пример: "x37.5y55.6z150t1685450553"
            # → ["", "37.5", "55.6", "150", "1685450553"]
            parts = point_str.replace('x', '|').replace('y', '|').replace('z', '|').replace('t', '|').split('|')
            # parts = ['', '37.5', '55.6', '150', '1685450553']

            # Убираем пустые строки
            parts = [p for p in parts if p]
            # parts = ['37.5', '55.6', '150', '1685450553']

            if len(parts) >= 2:
                lon = float(parts[0])
                lat = float(parts[1])

            # Если есть z, то parts[2] = эшелон, parts[3] = время
            # Если нет z, то parts[2] = время (если есть t)
            if 'z' in point_str:
                if len(parts) >= 3:
                    fl = int(parts[2])
                if len(parts) >= 4:
                    point_time = int(parts[3])
            else:
                # Нет эшелона
                fl = None
                if len(parts) >= 3:
                    point_time = int(parts[2])

            if lon is not None and lat is not None:
                points.append({
                    'lon': lon,
                    'lat': lat,
                    'fl': fl,
                    'time': point_time
                })
        except (IndexError, ValueError):
            continue

    if not points:
        return jsonify({
            'status': 'error',
            'message': 'Points not defined'
        }), 400

    features = []
    for point in points:
        # Если эшелон не указан, возвращаем все уровни
        if point['fl'] is None:
            for fl in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
                wind_temp = generate_wind_temp(point['lat'], point['lon'], fl, point['time'])
                features.append({
                    'type': 'Feature',
                    'properties': wind_temp,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [point['lon'], point['lat']]
                    }
                })
        else:
            wind_temp = generate_wind_temp(point['lat'], point['lon'], point['fl'], point['time'])
            features.append({
                'type': 'Feature',
                'properties': wind_temp,
                'geometry': {
                    'type': 'Point',
                    'coordinates': [point['lon'], point['lat']]
                }
            })

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features),
        'date': get_unix_timestamp()
    })


def handle_adwrng(code):
    """Обработка запроса предупреждений по аэродрому"""
    if code:
        codes = code.split('.')
    else:
        codes = []

    features = []
    for aerodrome_code in codes:
        aerodrome = Aerodrome.query.filter_by(icao_code=aerodrome_code.upper()).first()
        if aerodrome:
            warning = generate_adwrng(aerodrome)
            features.append({
                'type': 'Feature',
                'properties': warning,
                'geometry': {
                    'type': 'Point',
                    'coordinates': [aerodrome.longitude, aerodrome.latitude]
                }
            })

    if not features:
        return jsonify({
            'status': 'error',
            'message': 'No data'
        }), 404

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features),
        'date': get_unix_timestamp()
    })


def handle_wswrng(code):
    """Обработка запроса предупреждений о сдвиге ветра"""
    if code:
        codes = code.split('.')
    else:
        codes = []

    features = []
    for aerodrome_code in codes:
        aerodrome = Aerodrome.query.filter_by(icao_code=aerodrome_code.upper()).first()
        if aerodrome:
            warning = generate_wswrng(aerodrome)
            features.append({
                'type': 'Feature',
                'properties': warning,
                'geometry': {
                    'type': 'Point',
                    'coordinates': [aerodrome.longitude, aerodrome.latitude]
                }
            })

    if not features:
        return jsonify({
            'status': 'error',
            'message': 'No data'
        }), 404

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features),
        'date': get_unix_timestamp()
    })


def handle_airep(code):
    """Обработка запроса AIREP"""
    fir_code = code if code else 'ULLL'

    airep = generate_airep(fir_code)

    features = [{
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [airep['longitude'], airep['latitude']]
        },
        'properties': {
            'code': fir_code,
            'raw': airep['raw']
        }
    }]

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features)
    })


def handle_zond(code):
    """Обработка запроса радиозондов"""
    fir_code = code if code else 'ULLL'

    zond = generate_zond(fir_code)

    features = [{
        'type': 'Feature',
        'geometry': None,
        'properties': zond
    }]

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features)
    })


def handle_vaac(code):
    """Обработка запроса VAAC"""
    vaac_code = code if code else 'RJTD'

    vaac = generate_vaac(vaac_code)

    features = [{
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [vaac['polygon']]
        },
        'properties': {
            'code': vaac_code,
            'raw': vaac['raw']
        }
    }]

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features)
    })


def handle_tcac(code):
    """Обработка запроса TCAC"""
    tcac_code = code if code else 'KNHC'

    tcac = generate_tcac(tcac_code)

    features = [{
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [tcac['polygon']]
        },
        'properties': {
            'code': tcac_code,
            'raw': tcac['raw']
        }
    }]

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features)
    })


def handle_swx():
    """Обработка запроса SWX"""
    swx = generate_swx()

    features = [{
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [swx['polygon']]
        },
        'properties': {
            'code': swx['code'],
            'raw': swx['raw']
        }
    }]

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features)
    })


def handle_brief(request):
    """Обработка запроса полетной документации"""
    # Получаем текст плана полета
    fpl_text = request.get_data(as_text=True)

    if not fpl_text or not fpl_text.strip():
        return jsonify({
            'status': 'error',
            'message': 'No flight plan'
        }), 400

    # Парсим план полета
    try:
        flight_plan = parse_fpl(fpl_text)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid flight plan format: {str(e)}'
        }), 400

    # Проверяем, что план содержит обязательные поля
    if not flight_plan.callsign and not flight_plan.departure:
        return jsonify({
            'status': 'error',
            'message': 'Invalid flight plan format'
        }), 400

    if not flight_plan.departure or not flight_plan.destination:
        return jsonify({
            'status': 'error',
            'message': 'Invalid flight plan format'
        }), 400

    # Находим аэродромы
    aerodromes = {}

    if flight_plan.departure:
        dep = Aerodrome.query.filter_by(icao_code=flight_plan.departure).first()
        if dep:
            aerodromes['departure'] = dep

    if flight_plan.destination:
        dest = Aerodrome.query.filter_by(icao_code=flight_plan.destination).first()
        if dest:
            aerodromes['destination'] = dest

    if flight_plan.alternate:
        alt = Aerodrome.query.filter_by(icao_code=flight_plan.alternate).first()
        if alt:
            aerodromes['alternate'] = alt

    # Если ни один аэродром не найден
    if not aerodromes:
        return jsonify({
            'status': 'error',
            'message': 'No briefing'
        }), 404

    # Создаем PDF
    try:
        pdf_bytes = create_brief_pdf(flight_plan, aerodromes)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'PDF generation error: {str(e)}'
        }), 500

    # Возвращаем PDF
    return pdf_bytes, 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename=briefing.pdf'
    }


def handle_dmrl(code, kind, time_param):
    """Обработка запроса данных ДМРЛ"""
    if not code:
        return jsonify({
            'status': 'error',
            'message': 'Radar not found'
        }), 404

    radar = Radar.query.filter_by(code=code.lower()).first()
    if not radar:
        return jsonify({
            'status': 'error',
            'message': 'Radar not found'
        }), 404

    # Если радар не работает, возвращаем пустые данные
    if radar.status == 0:
        return jsonify({
            'type': 'FeatureCollection',
            'features': [],
            'totalFeatures': 0,
            'timeStamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'radar': radar.code,
            'date': get_unix_timestamp()
        })

    # Генерируем полигоны
    polygons = generate_dmrl_polygon(radar, kind)

    return jsonify({
        'type': 'FeatureCollection',
        'features': polygons,
        'totalFeatures': len(polygons),
        'timeStamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'radar': radar.code,
        'date': get_unix_timestamp()
    })