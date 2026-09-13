from datetime import datetime, timezone, timedelta
import time


def get_unix_timestamp(dt=None):
    if dt is None:
        dt = datetime.now(timezone.utc)
    return int(dt.timestamp())


def get_current_utc():
    return datetime.now(timezone.utc)


def format_metar_time(dt=None):
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.strftime('%d%H%M') + 'Z'


def format_taf_time(dt=None):
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.strftime('%d%H') + '/' + (dt + timedelta(hours=24)).strftime('%d%H')


def add_minutes(dt, minutes):
    return dt + timedelta(minutes=minutes)


def add_hours(dt, hours):
    return dt + timedelta(hours=hours)


def is_valid_unix_timestamp(ts):
    try:
        ts = int(ts)
        return ts > 0
    except (ValueError, TypeError):
        return False


def ensure_valid_period(start: datetime, end: datetime) -> tuple[datetime, datetime]:
    if end <= start:
        end = start + timedelta(hours=1)
    return start, end


def generate_valid_period(
    base_time: datetime,
    min_start_hours: int = 1,
    max_start_hours: int = 6,
    min_duration_hours: int = 2,
    max_duration_hours: int = 4,
) -> tuple[datetime, datetime]:
    import random

    start_offset = random.randint(min_start_hours, max_start_hours)
    duration = random.randint(min_duration_hours, max_duration_hours)

    start = base_time + timedelta(hours=start_offset)
    end = start + timedelta(hours=duration)

    return ensure_valid_period(start, end)