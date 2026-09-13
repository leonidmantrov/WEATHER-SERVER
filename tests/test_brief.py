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


def test_brief_no_plan(client, auth_headers):
    """Тест запроса brief без плана полета"""
    response = client.post(
        '/meteo/?device=test-device&kind=brief',
        headers=auth_headers
    )
    assert response.status_code == 400


def test_brief_with_plan(client, auth_headers):
    """Тест запроса brief с планом полета"""
    fpl = """(FPL-PPP1441-IS
-A319/M-SDFGHIRWY/B1L
-ULMM1735
-K0768F320 ASGO1K ASGOR T693 PILAN/K0779F330 M856 KUKUM/K0788F340
M856 GIKUR/K0801F350 T458 BEPOL BEPO1A
-ULLI0142 UUEE
-PBN/B1D1A1S2O1 DOF/230220 REG/PP00000 EET/ULLL0005 SEL/SSSS
CODE/000000 OPR/PPP RALT/ULMM ULLI RMK/ACASII EQUIPPED)"""

    response = client.post(
        '/meteo/?device=test-device&kind=brief',
        data=fpl,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'


def test_brief_invalid_plan(client, auth_headers):
    """Тест запроса brief с неверным планом"""
    response = client.post(
        '/meteo/?device=test-device&kind=brief',
        data='invalid plan',
        headers=auth_headers
    )
    assert response.status_code == 400


def test_brief_requires_auth(client):
    """Тест что brief требует авторизацию"""
    response = client.post(
        '/meteo/?device=test-device&kind=brief',
        data='test'
    )
    assert response.status_code == 401