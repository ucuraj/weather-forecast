import logging
from datetime import datetime
from django.utils.timezone import now as tz_now

from django.db import models
from django.contrib.postgres.fields import JSONField

from common.utils.cache import get_object_by_key, set_object_by_key
from common.utils.date import timestamp_to_date

CURRENT = 'CUR'
MINUTELY = 'MIN'
HOURLY = 'HOU'
DAILY = 'DAI'
FORECAST_CHOICES = [
    (CURRENT, 'Currently Forecast'),
    (MINUTELY, 'Minute Forecast'),
    (HOURLY, 'Hourly Forecast'),
    (DAILY, 'Daily Forecast'),
]

FORECAST_CHOICES_REVERSE = {
    CURRENT: 'Currently Forecast',
    MINUTELY: 'Minute Forecast',
    HOURLY: 'Hourly Forecast',
    DAILY: 'Daily Forecast',
}


class WeatherForecast(models.Model):
    """Represent WeatherForecast Model.

    It is not considered to use inheritance and polymorphism
    because the data of each type of forecast is not used to
    perform different actions. Only the coordinates and the
    type need to be parsed to return the corresponding forecast.

    The raw_data field of type JSONField is used to store the
    data of each type."""

    time_zone = models.CharField(max_length=100)
    time_zone_offset = models.IntegerField()
    lat = models.DecimalField(decimal_places=4, max_digits=16, default=0)
    lon = models.DecimalField(decimal_places=4, max_digits=16, default=0)
    dt = models.DateTimeField(default=tz_now)
    raw_data = JSONField()

    CURRENT = CURRENT
    MINUTELY = MINUTELY
    HOURLY = HOURLY
    DAILY = DAILY

    forecast_type = models.CharField(
        max_length=3,
        choices=FORECAST_CHOICES,
        default=CURRENT,
    )

    class Meta:
        unique_together = ('lat', 'lon', 'forecast_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        datestring = timestamp_to_date(kwargs.get('dt'))
        self.dt = datestring if datestring else tz_now()

    @property
    def caching_key(self):
        """
        returns the key for get/set the instance from/to cache
        """
        return self.get_caching_key(self.lat, self.lon, self.forecast_type)

    def persist_instance_cache(self):
        """
        Caches de instance with the caching_key
        """
        return set_object_by_key(self.caching_key, self)

    @classmethod
    def get_or_create_persist(cls, time_zone, time_zone_offset, lat, lon, dt, raw_data, forecast_type,
                              persist_to_cache=True):
        """
        Update or create an instance of WeatherForecast. If persist_to_cache is True,
        caches the instance
        """
        obj, _created = WeatherForecast.objects.update_or_create(lat=lat, lon=lon, forecast_type=forecast_type,
                                                                 defaults={
                                                                     "time_zone": time_zone,
                                                                     "time_zone_offset": time_zone_offset,
                                                                     "dt": dt, "raw_data": raw_data, "lat": lat,
                                                                     "lon": lon,
                                                                     "forecast_type": forecast_type
                                                                 })
        if persist_to_cache:
            obj.persist_instance_cache()
        return obj, _created

    @staticmethod
    def get_caching_key(lat, lon, forecast_type):
        """returns the key for get/set the instance from/to cache"""
        lat = str(lat).replace(",", "").replace(".", "")
        lon = str(lon).replace(",", "").replace(".", "")
        return f'wf_x_{lat}_y_{lon}_{forecast_type}'

    @classmethod
    def retrieve_instance_cache(cls, lat, lon, forecast_type):
        """Calculate the object key, and retrieve from the cache."""
        return get_object_by_key(cls.get_caching_key(lat, lon, forecast_type))

    @classmethod
    def get_forecast_by_type(cls, lat, lon, forecast_type):
        """
        Try to get a WeatherForecast from cache filtering by lat,
        lon and forecast_type. With these fields, calculate de cache key
        for the object and try to get it. If not found, try to get
        the object from the local database.
        """
        if forecast_type not in FORECAST_CHOICES_REVERSE.keys():
            return None

        try:
            cache_instance = cls.retrieve_instance_cache(lat, lon, forecast_type)
            if cache_instance:
                return cache_instance
        except Exception:
            logging.exception("WeatherForecast.get_forecast_by_type")

        return WeatherForecast.objects.get(lat=lat, lon=lon, forecast_type=forecast_type)

    @classmethod
    def create_from_data(cls, data, forecast_type, create_persist=True):
        """
        Create or update a WeatherForecast instance from data received.
        If create_persist if True, the object is create/updated and cached.
        """

        lat = data.get("lat")
        lon = data.get("lon")
        time_zone = data.get("timezone")
        time_zone_offset = data.get("timezone_offset")
        dtime = timestamp_to_date(data.get("current", {}).get("dt"))
        dt = dtime if dtime else tz_now()
        return cls.get_or_create_persist(time_zone, time_zone_offset, lat, lon, dt, data, forecast_type, create_persist)
