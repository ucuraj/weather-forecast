# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

from rest_framework.test import APITestCase, APIClient

from common.utils.factories import (
    UserFactory,
)


class WFAPIClient(APIClient):
    pass


class WFAPITestCase(APITestCase):
    client_class = WFAPIClient
    user_factory = UserFactory


# MOCK RESPONSE


class ResponseHttp:
    status_code = 200
    data = None
    content = None

    def __init__(self, status_code=200, data=None):
        self.status_code = status_code
        self.data = data
        self.content = data

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.status_code < 200 or self.status_code >= 300:
            raise requests.exceptions.HTTPError('HTTP Error', response=self)
