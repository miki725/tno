# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from rest_framework.routers import DefaultRouter

from .viewsets import EntropyViewSet, OneTimeSecretViewSet


router = DefaultRouter(trailing_slash=True)
router.include_root_view = False

router.register('entropy', EntropyViewSet, 'entropy')
router.register('one-time-secrets', OneTimeSecretViewSet, 'one-time-secret')

urlpatterns = router.urls
