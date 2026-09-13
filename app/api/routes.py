from flask import Blueprint
from .meteo import meteo_bp
from .catalog import catalog_bp
from .registration import reg_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(meteo_bp, url_prefix='/meteo')
api_bp.register_blueprint(catalog_bp, url_prefix='/cat')
api_bp.register_blueprint(reg_bp, url_prefix='/reg')