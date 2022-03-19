import uuid

from mock import patch

from apps.oraculum.clients import OWMClient, OWMClientError
from apps.oraculum.models import DAILY, HOURLY, MINUTELY, CURRENT
from apps.oraculum.tests.bodys_request import body_daily_weather_ok, body_hourly_weather_ok, body_unauthorized, \
    body_nothing_to_geocode
from common.utils.test import ResponseHttp, WFAPITestCase


class TpagaClientTestCase(WFAPITestCase):
    def test_get_weather_forecast_data_daily(self):
        client = OWMClient()
        values = {'lat': -34.918339, 'lon': -57.961068, 'forecast_type': DAILY}

        data = body_daily_weather_ok

        with patch('apps.oraculum.clients.requests.get', return_value=ResponseHttp(200, data)):
            response = client.get_weather_forecast_data(values.get("lat"), values.get("lon"),
                                                        values.get("forecast_type"))
            self.assertEqual(response, data)
            self.assertEqual(response.get("daily"), data.get("daily"))

    def test_get_weather_forecast_data_hourly(self):
        client = OWMClient()
        values = {'lat': -34.918339, 'lon': -57.961068, 'forecast_type': HOURLY}

        data = body_hourly_weather_ok

        with patch('apps.oraculum.clients.requests.get', return_value=ResponseHttp(200, data)):
            response = client.get_weather_forecast_data(values.get("lat"), values.get("lon"),
                                                        values.get("forecast_type"))
            self.assertEqual(response, data)
            self.assertEqual(response.get("hourly"), data.get("hourly"))

    def test_get_weather_forecast_data_minutely(self):
        client = OWMClient()
        values = {'lat': -34.918339, 'lon': -57.961068, 'forecast_type': MINUTELY}

        data = body_hourly_weather_ok

        with patch('apps.oraculum.clients.requests.get', return_value=ResponseHttp(200, data)):
            response = client.get_weather_forecast_data(values.get("lat"), values.get("lon"),
                                                        values.get("forecast_type"))
            self.assertEqual(response, data)
            self.assertEqual(response.get("minutely"), data.get("minutely"))

    def test_get_weather_forecast_data_current(self):
        client = OWMClient()
        values = {'lat': -34.918339, 'lon': -57.961068, 'forecast_type': CURRENT}

        data = body_hourly_weather_ok

        with patch('apps.oraculum.clients.requests.get', return_value=ResponseHttp(200, data)):
            response = client.get_weather_forecast_data(values.get("lat"), values.get("lon"),
                                                        values.get("forecast_type"))
            self.assertEqual(response, data)
            self.assertEqual(response.get("current"), data.get("current"))

    def test_no_api_key(self):
        client = OWMClient()
        values = {'lat': -34.918339, 'lon': -57.961068, 'forecast_type': CURRENT}

        data = body_unauthorized

        with patch('apps.oraculum.clients.requests.get', return_value=ResponseHttp(401, data)):
            with self.assertRaises(OWMClientError):
                response = client.get_weather_forecast_data(values.get("lat"), values.get("lon"),
                                                            values.get("forecast_type"))
                self.assertEqual(response.get("cod"), 401)

    def test_no_latlng(self):
        client = OWMClient()
        values = {'forecast_type': CURRENT}

        data = body_nothing_to_geocode

        with patch('apps.oraculum.clients.requests.get', return_value=ResponseHttp(400, data)):
            with self.assertRaises(OWMClientError):
                response = client.get_weather_forecast_data(values.get("lat"), values.get("lon"),
                                                            values.get("forecast_type"))
                self.assertEqual(response.get("cod"), 400)
