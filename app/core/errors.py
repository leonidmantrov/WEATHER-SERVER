from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Регистрирует обработчики ошибок"""

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            'status': 'error',
            'message': 'Bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({
            'status': 'error',
            'message': 'Forbidden'
        }), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'status': 'error',
            'message': 'Not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            'status': 'error',
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(429)
    def too_many_requests(e):
        return jsonify({
            'status': 'error',
            'message': 'Too many requests'
        }), 429

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500