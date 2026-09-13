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


# Тесты AIREP
def test_get_airep(client, auth_headers):
    """Тест получения AIREP"""
    response = client.get(
        '/meteo/?device=test-device&kind=airep&code=ULLL',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    # Проверяем, что есть любое явление (TURB, ICE, CAT, WS)
    raw = data['features'][0]['properties']['raw']
    assert any(word in raw for word in ['TURB', 'ICE', 'CAT', 'WS'])


def test_airep_geometry(client, auth_headers):
    """Тест что AIREP содержит геометрию"""
    response = client.get(
        '/meteo/?device=test-device&kind=airep&code=ULLL',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'geometry' in feature
    assert feature['geometry']['type'] == 'Point'


# Тесты ZOND
def test_get_zond(client, auth_headers):
    """Тест получения радиозондов"""
    response = client.get(
        '/meteo/?device=test-device&kind=zond&code=ULLL',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'path' in data['features'][0]['properties']
    assert len(data['features'][0]['properties']['path']) > 0


def test_zond_path(client, auth_headers):
    """Тест что траектория зонда содержит координаты"""
    response = client.get(
        '/meteo/?device=test-device&kind=zond&code=ULLL',
        headers=auth_headers
    )
    data = response.get_json()
    path = data['features'][0]['properties']['path']
    assert 'lat' in path[0]
    assert 'lon' in path[0]
    assert 'height' in path[0]


# Тесты VAAC
def test_get_vaac(client, auth_headers):
    """Тест получения VAAC"""
    response = client.get(
        '/meteo/?device=test-device&kind=vaac&code=RJTD',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'VA ADVISORY' in data['features'][0]['properties']['raw']


def test_vaac_geometry(client, auth_headers):
    """Тест что VAAC содержит полигон"""
    response = client.get(
        '/meteo/?device=test-device&kind=vaac&code=RJTD',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert feature['geometry']['type'] == 'Polygon'


# Тесты TCAC
def test_get_tcac(client, auth_headers):
    """Тест получения TCAC"""
    response = client.get(
        '/meteo/?device=test-device&kind=tcac&code=KNHC',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'TC ADVISORY' in data['features'][0]['properties']['raw']


def test_tcac_geometry(client, auth_headers):
    """Тест что TCAC содержит полигон"""
    response = client.get(
        '/meteo/?device=test-device&kind=tcac&code=KNHC',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert feature['geometry']['type'] == 'Polygon'


# Тесты SWX
def test_get_swx(client, auth_headers):
    """Тест получения SWX"""
    response = client.get(
        '/meteo/?device=test-device&kind=swx',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'SWX ADVISORY' in data['features'][0]['properties']['raw']


def test_swx_geometry(client, auth_headers):
    """Тест что SWX содержит полигон"""
    response = client.get(
        '/meteo/?device=test-device&kind=swx',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert feature['geometry']['type'] == 'Polygon'


# Тесты авторизации
def test_special_data_require_auth(client):
    """Тест что специальные данные требуют авторизацию"""
    response = client.get('/meteo/?device=test-device&kind=airep&code=ULLL')
    assert response.status_code == 401

    response = client.get('/meteo/?device=test-device&kind=zond&code=ULLL')
    assert response.status_code == 401

    response = client.get('/meteo/?device=test-device&kind=vaac&code=RJTD')
    assert response.status_code == 401