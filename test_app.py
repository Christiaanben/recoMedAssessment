import pytest

from .enums.error_enums import INVALID_PARAMS
from .app import app

BUSINESS_SECOND_URI = '/api/business-seconds?start_time={}&end_time={}'

ISO_NEW_YEARS_1AM = '2021-01-01T01:00:00'

ISO_WEDNESDAY_9AM = '2021-02-17T09:00:00'
ISO_THURSDAY_9AM = '2021-02-18T09:00:00'
ISO_THURSDAY_5PM = '2021-02-18T17:00:00'
ISO_FRIDAY_1AM = '2021-02-19T01:00:00'
ISO_FRIDAY_7AM = '2021-02-19T07:00:00'
ISO_FRIDAY_8AM = '2021-02-19T08:00:00'
ISO_FRIDAY_9AM = '2021-02-19T09:00:00'
ISO_FRIDAY_11PM = '2021-02-19T23:00:00'
ISO_MONDAY_9AM = '2021-02-22T09:00:00'

ISO_FRIDAY_BEFORE_WEEKEND_HOLIDAY_10AM = '2021-03-19T10:00:00'
ISO_MONDAY_AFTER_WEEKEND_HOLIDAY_10AM = '2021-03-22T10:00:00'
ISO_TUESDAY_AFTER_WEEKEND_HOLIDAY_10AM = '2021-03-23T10:00:00'

ISO_DAY_BEFORE_HOLIDAY_1PM = '2021-06-15T13:00:00'
ISO_HOLIDAY_9AM = '2021-06-16T09:00:00'
ISO_HOLIDAY_4PM = '2021-06-16T16:00:00'
ISO_DAY_AFTER_HOLIDAY_1PM = '2021-06-17T13:00:00'

ISO_NEW_YEARS_EVE_11PM = '2021-12-31T23:00:00'

ISO_INVALID = '2021-02-19T09:00:60'



@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_server_online(client):
    response = client.get('/')
    assert response.status_code == 200


def test_business_seconds_8_to_9(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_FRIDAY_8AM, ISO_FRIDAY_9AM))
    assert response.status_code == 200
    assert response.get_json() == 60*60


def test_business_seconds_7_to_9(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_FRIDAY_7AM, ISO_FRIDAY_9AM))
    assert response.status_code == 200
    assert response.get_json() == 60*60


def test_business_seconds_1_to_23(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_FRIDAY_1AM, ISO_FRIDAY_11PM))
    assert response.status_code == 200
    assert response.get_json() == 9*60*60


def test_business_seconds_yesterday_17_to_8(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_THURSDAY_5PM, ISO_FRIDAY_8AM))
    assert response.status_code == 200
    assert response.get_json() == 0


def test_business_seconds_thursday_to_friday(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_THURSDAY_9AM, ISO_FRIDAY_9AM))
    assert response.status_code == 200
    assert response.get_json() == 9*60*60


def test_business_seconds_wednesday_to_friday(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_WEDNESDAY_9AM, ISO_FRIDAY_9AM))
    assert response.status_code == 200
    assert response.get_json() == 2*9*60*60


def test_business_seconds_friday_to_monday(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_FRIDAY_9AM, ISO_MONDAY_9AM))
    assert response.status_code == 200
    assert response.get_json() == 9*60*60


def test_business_seconds_holiday_morning_to_afternoon(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_HOLIDAY_9AM, ISO_HOLIDAY_4PM))
    assert response.status_code == 200
    assert response.get_json() == 0


def test_business_seconds_before_to_after_holiday(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_DAY_BEFORE_HOLIDAY_1PM, ISO_DAY_AFTER_HOLIDAY_1PM))
    assert response.status_code == 200
    assert response.get_json() == 9*60*60


def test_business_seconds_before_weekend_holiday_to_monday(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_FRIDAY_BEFORE_WEEKEND_HOLIDAY_10AM, ISO_MONDAY_AFTER_WEEKEND_HOLIDAY_10AM))
    assert response.status_code == 200
    assert response.get_json() == 9*60*60


def test_business_seconds_before_weekend_holiday_to_tuesday(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_FRIDAY_BEFORE_WEEKEND_HOLIDAY_10AM, ISO_TUESDAY_AFTER_WEEKEND_HOLIDAY_10AM))
    assert response.status_code == 200
    assert response.get_json() == 9*60*60


def test_business_seconds_start_to_end_of_year(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_NEW_YEARS_1AM, ISO_NEW_YEARS_EVE_11PM))
    assert response.status_code == 200
    assert response.get_json() == 251*9*60*60


def test_business_seconds_invalid_iso_date(client):
    response = client.get(BUSINESS_SECOND_URI.format(ISO_FRIDAY_8AM, ISO_INVALID))
    assert response.status_code == 400
    assert response.get_json()['error'] == INVALID_PARAMS
