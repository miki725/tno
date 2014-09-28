# -*- coding: utf-8 -*-
"""
Checklist for production-ready settings:
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

This is a base for production settings without including
any sensitive information. Include all sensitive information
in ``prod.py`` settings file which should not be committed
to version-control.
"""
from __future__ import print_function, unicode_literals

from .base import *


DEBUG = False

ADMINS = (
    ('Miroslav Shubernetskiy', 'miroslav@miki725.com'),
)

ALLOWED_HOSTS = [
    'tno.io',
    'localhost',
    '127.0.0.1',
]

if os.environ.get('HOST_IP', None):
    ALLOWED_HOSTS += [
        os.environ['HOST_IP'],
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'postgres.tno.docker',
        'PORT': '5432',
    }
}

MIDDLEWARE_CLASSES = (
    (
        'breach_buster.middleware.gzip.GZipMiddleware',
    )
    + MIDDLEWARE_CLASSES
)

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True

EMAIL_SUBJECT_PREFIX = '[Django tno] '
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
