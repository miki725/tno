# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.conf.urls import patterns, url

from .views import OneTimeSecretView


urlpatterns = patterns(
    '',

    url(r'^',
        OneTimeSecretView.as_view(),
        name='index'),
)
