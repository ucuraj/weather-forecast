# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.routers import DefaultRouter

from .api import OraculumViewSet

router = DefaultRouter()

# Public Section
router.register(r'oraculum', OraculumViewSet, basename='oraculum-view-v1')

urlpatterns = []

urlpatterns += router.urls
