from .database import db
from sqlalchemy.dialects.postgresql import JSONB


class Aerodrome(db.Model):
    __tablename__ = 'aerodromes'

    id = db.Column(db.Integer, primary_key=True)
    icao_code = db.Column(db.String(4), unique=True, nullable=False)  # например URSS
    iata_code = db.Column(db.String(3), unique=True, nullable=False)  # например AER
    name = db.Column(db.String(100), nullable=False)  # Сочи (Адлер)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)  # в метрах

    def to_dict(self):
        return {
            'icao': self.icao_code,
            'iata': self.iata_code,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'elevation': self.elevation
        }


class Radar(db.Model):
    __tablename__ = 'radars'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    range_km = db.Column(db.Integer, nullable=False, default=250)
    status = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'range': self.range_km,
            'status': self.status
        }


class WeatherHistory(db.Model):
    __tablename__ = 'weather_history'

    id = db.Column(db.Integer, primary_key=True)
    aerodrome = db.Column(db.String(4), nullable=False, index=True)
    date_time = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    weather_data = db.Column(JSONB, nullable=False)
