# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.routers import DefaultRouter

from .api import WeatherForecastViewSet

router = DefaultRouter()

# Public Section
router.register(r'weather-forecast', WeatherForecastViewSet, basename='weather-forecast-view-v1')

urlpatterns = []

urlpatterns += router.urls
