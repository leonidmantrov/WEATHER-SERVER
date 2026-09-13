import time
from collections import defaultdict
from flask import jsonify


class RateLimiter:
    def __init__(self):
        # Словарь: token -> {'minute': [(timestamp, count)], 'day': [...]}
        self.requests = defaultdict(lambda: {
            'minute': [],
            'day': []
        })
        self.minute_limit = 100
        self.day_limit = 10000

    def check(self, token):
        """Проверяет, не превышен ли лимит запросов"""
        now = time.time()

        # Очищаем старые записи
        self._cleanup(token, now)

        # Проверяем лимиты
        minute_count = len(self.requests[token]['minute'])
        day_count = len(self.requests[token]['day'])

        if minute_count >= self.minute_limit:
            return False, 'Too many requests (minute limit)'

        if day_count >= self.day_limit:
            return False, 'Too many requests (day limit)'

        # Добавляем запись
        self.requests[token]['minute'].append(now)
        self.requests[token]['day'].append(now)

        return True, None

    def _cleanup(self, token, now):
        """Удаляет записи старше 1 минуты и 24 часов"""

        self.requests[token]['minute'] = [
            t for t in self.requests[token]['minute']
            if now - t < 60
        ]

        self.requests[token]['day'] = [
            t for t in self.requests[token]['day']
            if now - t < 86400
        ]


rate_limiter = RateLimiter()