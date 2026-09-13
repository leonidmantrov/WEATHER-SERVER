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

@pytest.fixture
def auth_headers():
    return {'AUTHORIZATION': f'Bearer {Config.USER_TOKEN}'}

def test_get_metar(client, auth_headers):
    """Тест получения METAR"""
    response = client.get(
        '/meteo/?device=test-device&kind=metar&code=URSS',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'Feature'
    assert data['properties']['kind'] == 'METAR'
    assert 'raw' in data['properties']

def test_get_metar_invalid_aerodrome(client, auth_headers):
    """Тест получения METAR для несуществующего аэродрома"""
    response = client.get(
        '/meteo/?device=test-device&kind=metar&code=XXXX',
        headers=auth_headers
    )
    assert response.status_code == 404

def test_get_taf(client, auth_headers):
    """Тест получения TAF"""
    response = client.get(
        '/meteo/?device=test-device&kind=taf&code=URSS',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['properties']['kind'] == 'TAF'

def test_get_vfr(client, auth_headers):
    """Тест получения VFR"""
    response = client.get(
        '/meteo/?device=test-device&kind=vfr&code=URSS',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0

def test_invalid_kind(client, auth_headers):
    """Тест с неверным kind"""
    response = client.get(
        '/meteo/?device=test-device&kind=invalid&code=URSS',
        headers=auth_headers
    )
    assert response.status_code == 400

def test_missing_device(client, auth_headers):
    """Тест без device"""
    response = client.get(
        '/meteo/?kind=metar&code=URSS',
        headers=auth_headers
    )
    assert response.status_code == 400