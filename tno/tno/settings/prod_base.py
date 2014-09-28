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
    'www.tno.io',
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
        'NAME': 'tnodb',
        'USER': 'tnouser',
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

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'data', 'static')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'data', 'media')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = None  # added by nginx
SECURE_HSTS_INCLUDE_SUBDOMAINS = None  # added by nginx
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True

SECURE_CHECKS = [
    "djangosecure.check.csrf.check_csrf_middleware",
    "djangosecure.check.sessions.check_session_cookie_secure",
    "djangosecure.check.sessions.check_session_cookie_httponly",
    "djangosecure.check.djangosecure.check_security_middleware",
    # "djangosecure.check.djangosecure.check_sts",
    "djangosecure.check.djangosecure.check_frame_deny",
    "djangosecure.check.djangosecure.check_content_type_nosniff",
    "djangosecure.check.djangosecure.check_xss_filter",
    "djangosecure.check.djangosecure.check_ssl_redirect",
]

EMAIL_SUBJECT_PREFIX = '[Django tno] '
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
