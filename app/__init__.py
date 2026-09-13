import json
import os
from flask import Flask
from .config import Config
from .database import db
from .models import Aerodrome, Radar


def load_aerodromes():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'aerodromes.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_codes = {item['icao'] for item in data['aerodromes']}

    Aerodrome.query.filter(Aerodrome.icao_code.notin_(json_codes)).delete(synchronize_session=False)
    db.session.commit()

    for item in data['aerodromes']:
        existing = Aerodrome.query.filter_by(icao_code=item['icao']).first()
        if existing:
            existing.iata_code = item['iata']
            existing.name = item['name']
            existing.latitude = item['latitude']
            existing.longitude = item['longitude']
            existing.elevation = item['elevation']
        else:
            aerodrome = Aerodrome(
                icao_code=item['icao'],
                iata_code=item['iata'],
                name=item['name'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                elevation=item['elevation']
            )
            db.session.add(aerodrome)

    db.session.commit()
    print(f"Загружено аэродромов: {Aerodrome.query.count()}")


def load_radars():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'radars.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_codes = {item['code'] for item in data['radars']}

    # Удаляем радары, которых нет в JSON
    Radar.query.filter(Radar.code.notin_(json_codes)).delete(synchronize_session=False)
    db.session.commit()

    for item in data['radars']:
        existing = Radar.query.filter_by(code=item['code']).first()
        if existing:
            existing.name = item['name']
            existing.latitude = item['latitude']
            existing.longitude = item['longitude']
            existing.range_km = item['range']
            existing.status = item.get('status', 1)
        else:
            radar = Radar(
                code=item['code'],
                name=item['name'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                range_km=item['range'],
                status=item.get('status', 1)
            )
            db.session.add(radar)

    db.session.commit()
    print(f"Загружено радаров: {Radar.query.count()}")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"Подключение к БД: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)

    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/')

    with app.app_context():
        db.create_all()
        load_aerodromes()
        load_radars()
        total_aerodromes = Aerodrome.query.count()
        total_radars = Radar.query.count()
        print(f"Всего аэродромов в БД: {total_aerodromes}")
        print(f"Всего радаров в БД: {total_radars}")

    return app