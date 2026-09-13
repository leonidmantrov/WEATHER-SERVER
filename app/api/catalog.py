import random
from flask import Blueprint, request, jsonify
from ..core.auth import require_auth
from ..models import Radar
from ..utils.time_utils import get_unix_timestamp

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/', methods=['GET'])
@require_auth
def get_catalog():
    code = request.args.get('code')

    if not code:
        return jsonify({
            'status': 'error',
            'message': 'Catalog code not specified'
        }), 400

    if code == 'dmrl-list':
        return get_dmrl_list()
    elif code == 'dmrl-phenomena':
        return get_dmrl_phenomena()
    elif code == 'dmrl-intensities':
        return get_dmrl_intensities()
    elif code == 'dmrl-heights':
        return get_dmrl_heights()
    else:
        return jsonify({
            'status': 'error',
            'message': 'Catalog not found'
        }), 404


def get_dmrl_list():
    """Справочник ДМРЛ из БД"""
    radars = Radar.query.all()

    features = []
    for radar in radars:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [radar.longitude, radar.latitude]
            },
            'properties': radar.to_dict()
        })

    return jsonify({
        'type': 'FeatureCollection',
        'features': features,
        'totalFeatures': len(features)
    })


def get_dmrl_phenomena():
    """Справочник метеоявлений"""
    phenomena = [
        {'code': 1, 'nameRu': 'Облака в среднем ярусе', 'nameEn': 'Clouds mid level', 'color': '#dcf8fb'},
        {'code': 2, 'nameRu': 'Слоистообразная облачность', 'nameEn': 'Stratus', 'color': '#a3c7f9'},
        {'code': 3, 'nameRu': 'Конвективная облачность', 'nameEn': 'Convective clouds', 'color': '#f9a3a3'},
        {'code': 4, 'nameRu': 'Осадки', 'nameEn': 'Precipitation', 'color': '#a3f9a3'},
        {'code': 5, 'nameRu': 'Гроза', 'nameEn': 'Thunderstorm', 'color': '#f9f9a3'}
    ]

    return jsonify({
        'type': 'dmrl-phenomena',
        'phenomena': phenomena,
        'timeStamp': '2023-01-01T00:00:00Z'
    })


def get_dmrl_intensities():
    """Справочник интенсивности осадков"""
    intensities = [
        {'min': 0, 'max': 0.5, 'color': '#ffffff', 'nameRu': 'Нет осадков', 'nameEn': 'No precipitation'},
        {'min': 0.5, 'max': 2, 'color': '#a3f9a3', 'nameRu': 'Слабые', 'nameEn': 'Light'},
        {'min': 2, 'max': 5, 'color': '#f9f9a3', 'nameRu': 'Умеренные', 'nameEn': 'Moderate'},
        {'min': 5, 'max': 10, 'color': '#f9a3a3', 'nameRu': 'Сильные', 'nameEn': 'Heavy'}
    ]

    return jsonify({
        'type': 'dmrl-intensities',
        'intensities': intensities,
        'timeStamp': '2023-01-01T00:00:00Z'
    })


def get_dmrl_heights():
    """Справочник высоты облачности"""
    heights = [
        {'min': 0, 'max': 500, 'color': '#f9a3a3', 'nameRu': 'Низкая', 'nameEn': 'Low'},
        {'min': 500, 'max': 1500, 'color': '#f9f9a3', 'nameRu': 'Средняя', 'nameEn': 'Medium'},
        {'min': 1500, 'max': 3000, 'color': '#a3f9a3', 'nameRu': 'Высокая', 'nameEn': 'High'}
    ]

    return jsonify({
        'type': 'dmrl-heights',
        'heights': heights,
        'timeStamp': '2023-01-01T00:00:00Z'
    })