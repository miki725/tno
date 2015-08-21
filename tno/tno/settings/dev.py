# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from .base import *  # noqa


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tno.sqlite',
    }
}

INSTALLED_APPS += [
    'django_extensions',
]

ALLOWED_HOSTS = [
    '*',
]

SECRET_KEY = '+0_&9oud0)bh&^un!dolfms5zh1+u^ktdn(gmw67xq8#rg19bx'
