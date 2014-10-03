# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from rest_framework.routers import DefaultRouter

from .viewsets import EntropyViewSet, OneTimeSecretViewSet


router = DefaultRouter(trailing_slash=True)

router.register('entropy', EntropyViewSet, 'api-entropy')
router.register('one-time-secrets', OneTimeSecretViewSet, 'api-one-time-secret')

urlpatterns = router.urls
