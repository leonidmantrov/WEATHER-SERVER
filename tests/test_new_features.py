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


# Тесты для rwindtmp (ветер/температура по маршруту)
def test_get_rwindtmp(client, auth_headers):
    """Тест получения ветра и температуры по маршруту"""
    response = client.get(
        '/meteo/?device=test-device&kind=rwindtmp'
        '&p[0]=x37.5y55.6z150t1685450553'
        '&p[1]=x38.5y56.6z200t1685454153',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) == 2
    assert 'tmp' in data['features'][0]['properties']
    assert 'wind' in data['features'][0]['properties']
    assert 'wdir' in data['features'][0]['properties']


def test_get_rwindtmp_no_points(client, auth_headers):
    """Тест получения rwindtmp без точек"""
    response = client.get(
        '/meteo/?device=test-device&kind=rwindtmp',
        headers=auth_headers
    )
    assert response.status_code == 400


def test_get_rwindtmp_multiple_levels(client, auth_headers):
    """Тест получения rwindtmp без указания эшелона"""
    response = client.get(
        '/meteo/?device=test-device&kind=rwindtmp'
        '&p[0]=x37.5y55.6t1685450553',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    # Должны вернуться все эшелоны
    assert len(data['features']) == 10
    assert data['features'][0]['properties']['pointFl'] == 50


def test_rwindtmp_geometry(client, auth_headers):
    """Тест что rwindtmp содержит геометрию"""
    response = client.get(
        '/meteo/?device=test-device&kind=rwindtmp'
        '&p[0]=x37.5y55.6z150t1685450553',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'geometry' in feature
    assert feature['geometry']['type'] == 'Point'
    assert len(feature['geometry']['coordinates']) == 2


# Тесты для adwrng (предупреждения по аэродрому)
def test_get_adwrng(client, auth_headers):
    """Тест получения предупреждений по аэродрому"""
    response = client.get(
        '/meteo/?device=test-device&kind=adwrng&code=URSS',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'AD WRNG' in data['features'][0]['properties']['raw']


def test_get_adwrng_multiple_aerodromes(client, auth_headers):
    """Тест получения предупреждений для нескольких аэродромов"""
    response = client.get(
        '/meteo/?device=test-device&kind=adwrng&code=URSS.UUDD',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['totalFeatures'] == 2


def test_get_adwrng_invalid_aerodrome(client, auth_headers):
    """Тест получения предупреждений для несуществующего аэродрома"""
    response = client.get(
        '/meteo/?device=test-device&kind=adwrng&code=XXXX',
        headers=auth_headers
    )
    assert response.status_code == 404


def test_adwrng_valid_period(client, auth_headers):
    """Тест что предупреждение содержит период действия"""
    response = client.get(
        '/meteo/?device=test-device&kind=adwrng&code=URSS',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'validPeriod' in feature['properties']
    assert 'begin' in feature['properties']['validPeriod']
    assert 'end' in feature['properties']['validPeriod']


# Тесты для wswrng (предупреждения о сдвиге ветра)
def test_get_wswrng(client, auth_headers):
    """Тест получения предупреждений о сдвиге ветра"""
    response = client.get(
        '/meteo/?device=test-device&kind=wswrng&code=URSS',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert len(data['features']) > 0
    assert 'raw' in data['features'][0]['properties']
    assert 'WS WRNG' in data['features'][0]['properties']['raw']


def test_get_wswrng_multiple_aerodromes(client, auth_headers):
    """Тест получения предупреждений для нескольких аэродромов"""
    response = client.get(
        '/meteo/?device=test-device&kind=wswrng&code=URSS.UUDD',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['totalFeatures'] == 2


def test_wswrng_geometry(client, auth_headers):
    """Тест что предупреждение содержит геометрию"""
    response = client.get(
        '/meteo/?device=test-device&kind=wswrng&code=URSS',
        headers=auth_headers
    )
    data = response.get_json()
    feature = data['features'][0]
    assert 'geometry' in feature
    assert feature['geometry']['type'] == 'Point'


# Тесты для ДМРЛ данных
def test_get_wdmrl(client, auth_headers):
    """Тест получения метеоявлений с радара"""
    response = client.get(
        '/meteo/?device=test-device&kind=wdmrl&code=rudn',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert 'radar' in data
    assert data['radar'] == 'rudn'


def test_get_pdmrl(client, auth_headers):
    """Тест получения интенсивности осадков с радара"""
    response = client.get(
        '/meteo/?device=test-device&kind=pdmrl&code=rudn',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    if data['totalFeatures'] > 0:
        assert 'intensity' in data['features'][0]['properties']


def test_get_tdmrl(client, auth_headers):
    """Тест получения верхней границы облачности с радара"""
    response = client.get(
        '/meteo/?device=test-device&kind=tdmrl&code=rudn',
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    if data['totalFeatures'] > 0:
        assert 'height' in data['features'][0]['properties']


def test_dmrl_invalid_radar(client, auth_headers):
    """Тест получения данных с несуществующего радара"""
    response = client.get(
        '/meteo/?device=test-device&kind=wdmrl&code=xxxx',
        headers=auth_headers
    )
    assert response.status_code == 404


def test_dmrl_geometry(client, auth_headers):
    """Тест что данные ДМРЛ содержат геометрию"""
    response = client.get(
        '/meteo/?device=test-device&kind=wdmrl&code=rudn',
        headers=auth_headers
    )
    data = response.get_json()
    if data['totalFeatures'] > 0:
        feature = data['features'][0]
        assert 'geometry' in feature
        assert feature['geometry']['type'] == 'Polygon'


# Тесты на авторизацию
def test_new_features_require_auth(client):
    """Тест что новые функции требуют авторизацию"""
    response = client.get(
        '/meteo/?device=test-device&kind=rwindtmp&p[0]=x37.5y55.6z150t1685450553'
    )
    assert response.status_code == 401

    response = client.get(
        '/meteo/?device=test-device&kind=adwrng&code=URSS'
    )
    assert response.status_code == 401

    response = client.get(
        '/meteo/?device=test-device&kind=wdmrl&code=rudn'
    )
    assert response.status_code == 401