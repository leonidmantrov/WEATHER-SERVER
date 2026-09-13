from functools import wraps
from flask import request, jsonify
from ..config import Config


def check_auth(token):
    return token == Config.USER_TOKEN


def check_admin_key(key):
    return key == Config.ADMIN_KEY


def require_auth(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized'
            }), 401

        token = auth_header[7:]  # Убираем 'Bearer '
        if not check_auth(token):
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized'
            }), 401

        return f(*args, **kwargs)

    return decorated_function


def require_admin(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized'
            }), 401

        key = auth_header[7:]
        if not check_admin_key(key):
            return jsonify({
                'status': 'error',
                'message': 'Forbidden'
            }), 403

        return f(*args, **kwargs)

    return decorated_function