import uuid
from flask import Blueprint, request, jsonify
from ..core.auth import require_admin, require_auth

reg_bp = Blueprint('registration', __name__)


@reg_bp.route('/give', methods=['POST'])
@require_admin
def give_tokens():
    """Выдача лицензионных ключей"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request'
        }), 400

    request_id = data.get('id')
    number = data.get('number', 1)

    if not request_id:
        return jsonify({
            'status': 'error',
            'message': 'Invalid id'
        }), 400

    # Генерируем ключи
    tokens = [str(uuid.uuid4()) for _ in range(number)]

    return jsonify({
        'id': request_id,
        'tokens': tokens
    })


@reg_bp.route('/revoke', methods=['POST'])
@require_admin
def revoke_tokens():
    """Отзыв лицензионных ключей"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid request'
        }), 400

    tokens = data.get('tokens', [])

    return jsonify({
        'revoked': tokens
    })


@reg_bp.route('/devices/', methods=['GET'])
@require_auth
def get_devices():
    """Получение списка устройств пользователя"""
    # Заглушка
    return jsonify([])