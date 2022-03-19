import logging

import requests

from apps.oraculum.clients import OWMClientDataError, OWMClient, OWMClientError, FORECAST_TYPES
from apps.oraculum.models import WeatherForecast, FORECAST_CHOICES_REVERSE
from common.utils.cache import get_object_by_key
from common.utils.exceptions import ConflictError


class WeatherForecastServiceError(ConflictError):
    pass


class WeatherForecastService:
    def __init__(self):
        self.client = OWMClient()

    def get_weather_forecast(self, data, caching=True):
        """
        Tries to get object from cache. If not found in cache,
        retrieves data from Weather API and caches it for
        settings.CACHE_TIMEOUT seconds.
        Always return WeatherForecast instance
        """

        try:
            lat = str(data["lat"])
            lon = str(data["lon"])
            forecast_type = data["forecast_type"]

            cache_key = WeatherForecast.get_caching_key(lat, lon, forecast_type)

            obj = get_object_by_key(cache_key)
            if obj:
                return obj
            print("Retrieving data from API")
            response_data = self.client.get_weather_forecast_data(lat, lon, FORECAST_TYPES[forecast_type], caching)
            obj, _created = WeatherForecast.create_from_data(response_data, forecast_type)
            return obj
        except KeyError as e:
            logging.exception("Missing parameters on WeatherForecastService")
            raise WeatherForecastServiceError(f"Check data. Error: {e}")
        except (OWMClientDataError, requests.RequestException) as e:
            logging.exception("Error trying to read client response")
            raise WeatherForecastServiceError(f"Client data error. Error: {e}")
        except OWMClientError as e:
            logging.exception("Error on WeatherForecastService client")
            raise WeatherForecastServiceError(f"Client error. Error: {e}")
        except Exception as e:
            logging.exception("Unhandled error")
            raise WeatherForecastServiceError(f"Unknown error. Error: {e}")
