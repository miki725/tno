# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from core.admin import site

from .models import OTSecret


site.register(OTSecret)
