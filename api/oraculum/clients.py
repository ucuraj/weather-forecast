import logging
import requests

from django.conf import settings


class OWMClientError(Exception):
    pass


class OWMClientDataError(OWMClientError):
    pass


class OWMClient:
    """Client for request data to OpenWeatherMap API."""

    def __init__(self):
        self.BASE_URL = settings.OWM_API_URL
        self.TOKEN = settings.OWM_API_TOKEN

    def check_errors(self, caller, response):
        """
        Do nothing if it is ok
        In case of controled error (409) return the msg and log the full info
        """

        if response.status_code == 200:
            return
        elif response.status_code == 409:
            msg = response.json()['message']
            logging.exception('OpenWeatherMap API response: {}'.format(response.content))
            raise OWMClientDataError(msg)
        else:
            msg = 'OpenWeatherMap Client {} error: {}'.format(caller, response.content)
            logging.exception(msg)
            raise OWMClientError(msg)

    def _get_exclude_field(self, field_to_exclude):
        """returns a comma separted string with fields to exclude. Used for OWP OneCall"""
        exclude = ['current', 'minutely', 'hourly', 'alerts', 'daily']
        return ','.join(list(filter(lambda x: x != field_to_exclude.lower(), exclude)))

    def get_weather_forecast_data(self, lat, lon, forecast_type, process_response=True):
        """
        Get Daily Weather Forecast Data from OpenWeatherMap API
        """
        exclude = self._get_exclude_field(forecast_type)
        url = f'{self.BASE_URL}onecall?lat={lat}&lon={lon}&appid={self.TOKEN}&exclude={exclude}'

        response = requests.get(url)
        self.check_errors('get_weather_forecast_data', response)
        if process_response:
            return response.json()
        return response
