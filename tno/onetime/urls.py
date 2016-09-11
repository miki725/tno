# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.conf.urls import url

from .views import OneTimeSecretView


urlpatterns = [
    url(r'^',
        OneTimeSecretView.as_view(),
        name='index'),
]
