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


# Тесты для SIGMET
def test_get_sigmet(client, auth_headers):
    """Тест получения SIGMET"""
    response = client.get(
        '/meteo/?device=test-device&kind=sigmet&code=ULLL',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'ULLL SIGMET' in data['features'][0]['properties']['raw']


def test_get_sigmet_multiple_fir(client, auth_headers):
    """Тест получения SIGMET для нескольких РПИ"""
    response = client.get(
        '/meteo/?device=test-device&kind=sigmet&code=ULLL.UUDD',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert data['totalFeatures'] == 2


def test_get_sigmet_no_code(client, auth_headers):
    """Тест получения SIGMET без кода РПИ"""
    response = client.get(
        '/meteo/?device=test-device&kind=sigmet',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0


def test_sigmet_geometry(client, auth_headers):
    """Тест что SIGMET содержит геометрию"""
    response = client.get(
        '/meteo/?device=test-device&kind=sigmet&code=ULLL',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'geometry' in feature
    assert feature['geometry']['type'] == 'Polygon'
    assert 'coordinates' in feature['geometry']


def test_sigmet_valid_period(client, auth_headers):
    """Тест что SIGMET содержит период действия"""
    response = client.get(
        '/meteo/?device=test-device&kind=sigmet&code=ULLL',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'validPeriod' in feature['properties']
    assert 'begin' in feature['properties']['validPeriod']
    assert 'end' in feature['properties']['validPeriod']


# Тесты для AIRMET
def test_get_airmet(client, auth_headers):
    """Тест получения AIRMET"""
    response = client.get(
        '/meteo/?device=test-device&kind=airmet&code=ULLL',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'AIRMET' in data['features'][0]['properties']['raw']


def test_get_airmet_multiple_fir(client, auth_headers):
    """Тест получения AIRMET для нескольких РПИ"""
    response = client.get(
        '/meteo/?device=test-device&kind=airmet&code=ULLL.UUDD',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['totalFeatures'] == 2


def test_airmet_geometry(client, auth_headers):
    """Тест что AIRMET содержит геометрию"""
    response = client.get(
        '/meteo/?device=test-device&kind=airmet&code=ULLL',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'geometry' in feature
    assert feature['geometry']['type'] == 'Polygon'


def test_airmet_phenomen(client, auth_headers):
    """Тест что AIRMET содержит код явления"""
    response = client.get(
        '/meteo/?device=test-device&kind=airmet&code=ULLL',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'phenomen' in feature['properties']
    assert feature['properties']['phenomen'] != ''


# Тесты для GAMET
def test_get_gamet(client, auth_headers):
    """Тест получения GAMET"""
    response = client.get(
        '/meteo/?device=test-device&kind=gamet&area_name=TVER&area_number=5',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'GAMET' in data['features'][0]['properties']['raw']


def test_gamet_default_area(client, auth_headers):
    """Тест получения GAMET без указания района"""
    response = client.get(
        '/meteo/?device=test-device&kind=gamet',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0


def test_gamet_valid_period(client, auth_headers):
    """Тест что GAMET содержит период действия"""
    response = client.get(
        '/meteo/?device=test-device&kind=gamet&area_name=TVER&area_number=5',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'validPeriod' in feature['properties']
    assert 'begin' in feature['properties']['validPeriod']
    assert 'end' in feature['properties']['validPeriod']


def test_gamet_area_info(client, auth_headers):
    """Тест что GAMET содержит информацию о районе"""
    response = client.get(
        '/meteo/?device=test-device&kind=gamet&area_name=TVER&area_number=5',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'areaName' in feature['properties']
    assert feature['properties']['areaName'] == 'TVER'
    assert 'areaNumbers' in feature['properties']
    assert '5' in feature['properties']['areaNumbers']


# Тесты на ошибки
def test_sigmet_invalid_kind(client, auth_headers):
    """Тест что неверный kind для SIGMET не работает"""
    response = client.get(
        '/meteo/?device=test-device&kind=sigmet_invalid&code=ULLL',
        headers=auth_headers
    )
    assert response.status_code == 400


def test_airmet_requires_auth(client):
    """Тест что AIRMET требует авторизацию"""
    response = client.get(
        '/meteo/?device=test-device&kind=airmet&code=ULLL'
    )
    assert response.status_code == 401


def test_gamet_requires_auth(client):
    """Тест что GAMET требует авторизацию"""
    response = client.get(
        '/meteo/?device=test-device&kind=gamet&area_name=TVER&area_number=5'
    )
    assert response.status_code == 401