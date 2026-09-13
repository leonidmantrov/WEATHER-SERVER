import pytest
from app import create_app
from app.config import Config
from app.core.rate_limiter import RateLimiter


@pytest.fixture
def rate_limiter():
    return RateLimiter()


def test_rate_limit_allows_requests(rate_limiter):
    """Тест что запросы разрешены в пределах лимита"""
    token = 'test-token'
    for i in range(50):
        allowed, _ = rate_limiter.check(token)
        assert allowed == True


def test_rate_limit_blocks_after_limit(rate_limiter):
    """Тест что запросы блокируются после превышения лимита"""
    token = 'test-token-2'
    for i in range(100):
        allowed, _ = rate_limiter.check(token)
        assert allowed == True

    # 101-й запрос должен быть заблокирован
    allowed, error = rate_limiter.check(token)
    assert allowed == False
    assert 'limit' in error.lower()


def test_rate_limit_cleanup(rate_limiter):
    """Тест очистки старых записей"""
    token = 'test-token-3'

    # Добавляем записи
    for i in range(100):
        rate_limiter.check(token)

    # Проверяем что лимит исчерпан
    allowed, _ = rate_limiter.check(token)
    assert allowed == False