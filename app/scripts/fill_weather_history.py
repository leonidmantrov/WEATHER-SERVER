from datetime import datetime, timezone, timedelta
from app import create_app
from app.database import db
from app.models import Aerodrome, WeatherHistory
from app.generators.metar_gen import generate_metar
from app.generators.taf_gen import generate_taf

app = create_app()

with app.app_context():
    # Очистить старые записи
    db.session.query(WeatherHistory).delete()
    db.session.commit()

    aerodromes = Aerodrome.query.all()
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)

    total_records = 0

    for aerodrome in aerodromes:
        for i in range(12):  # 12 * 5 минут = 60 минут
            dt = now + timedelta(minutes=i * 5)

            metar_props = generate_metar(aerodrome)
            taf_props = generate_taf(aerodrome)

            metar_json = {
                "type": "Feature",
                "properties": metar_props,
                "geometry": {
                    "type": "Point",
                    "coordinates": [aerodrome.longitude, aerodrome.latitude]
                }
            }

            taf_json = {
                "type": "Feature",
                "properties": taf_props,
                "geometry": {
                    "type": "Point",
                    "coordinates": [aerodrome.longitude, aerodrome.latitude]
                }
            }

            db.session.add(WeatherHistory(
                aerodrome=aerodrome.icao_code,
                date_time=dt,
                weather_data=metar_json
            ))
            db.session.add(WeatherHistory(
                aerodrome=aerodrome.icao_code,
                date_time=dt,
                weather_data=taf_json
            ))

            total_records += 2

        print(f"Заполнено для {aerodrome.icao_code}")

    db.session.commit()
    print(f"Готово! Всего записей: {total_records}")