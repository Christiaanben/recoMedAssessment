import pytest

from enums.error_enums import INVALID_PARAMS
from .app import app

BUSINESS_SECOND_URI = '/api/business-seconds?start_time={}&end_time={}'
ISO_8AM = '2021-02-19T08:00:00'
ISO_9AM = '2021-02-19T09:00:00'
ISO_INVALID = '2021-02-19T09:00:60'


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_server_online(client):
    response = client.get('/')
    assert response.status_code == 200


def test_business_seconds_8_to_9(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_8AM, ISO_9AM))
    assert response.status_code == 200
    assert response.get_json() == 60*60


def test_business_seconds_invalid_iso_date(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_8AM, ISO_INVALID))
    assert response.status_code == 400
    assert response.get_json()['error'] == INVALID_PARAMS
