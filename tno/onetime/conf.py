# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.conf import settings


EXPIRES_IN_DAYS = getattr(settings, 'ONETIME_EXPIRED_IN_DAYS', 7)
PBKDF2_ITERATIONS = getattr(settings, 'ONETIME_PBKDF2_ITERATIONS', 30000)
