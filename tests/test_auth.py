import pytest
from app import create_app
from app.config import Config

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_unauthorized_access(client):
    """Тест доступа без авторизации"""
    response = client.get('/meteo/?device=test&kind=metar&code=URSS')
    assert response.status_code == 401

def test_authorized_access(client):
    """Тест доступа с авторизацией"""
    headers = {
        'AUTHORIZATION': f'Bearer {Config.USER_TOKEN}'
    }
    response = client.get(
        '/meteo/?device=test-device&kind=metar&code=URSS',
        headers=headers
    )
    assert response.status_code == 200

def test_invalid_token(client):
    """Тест с неверным токеном"""
    headers = {
        'AUTHORIZATION': 'Bearer invalid-token'
    }
    response = client.get(
        '/meteo/?device=test&kind=metar&code=URSS',
        headers=headers
    )
    assert response.status_code == 401