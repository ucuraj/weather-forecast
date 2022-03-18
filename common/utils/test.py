# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.test import APITestCase, APIClient

from common.utils.factories import (
    UserFactory,
)


class WFAPIClient(APIClient):
    pass


class WFAPITestCase(APITestCase):
    client_class = WFAPIClient
    user_factory = UserFactory
