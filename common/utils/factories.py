# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory

from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "api@weather.com"
    email = factory.LazyAttribute(lambda x: x.username)
    password = '123456'

    is_staff = False
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        # ensure the raw password gets set after the initial save
        obj.set_password(password)
        obj.save()
        obj.confirm_email(obj.confirmation_key)
        return obj
