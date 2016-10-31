# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from .base import Base


class Dev(Base):
    DEBUG = True

    ALLOWED_HOSTS = [
        '*',
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'tno',
            'USER': 'tno',
            'PASSWORD': 'tno',
            'HOST': 'localhost',
            'PORT': 5432,
            'CONN_MAX_AGE': None,
        }
    }

    REDIS = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }

    INSTALLED_APPS = Base.INSTALLED_APPS + [
        'django_extensions',
        'debug_toolbar',
    ]

    MIDDLEWARE_CLASSES = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + Base.MIDDLEWARE_CLASSES

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    SECRET_KEY = '+0_&9oud0)bh&^un!dolfms5zh1+u^ktdn(gmw67xq8#rg19bx'

    INTERNAL_IPS = [
        '127.0.0.1',
    ]
