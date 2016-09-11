# -*- coding: utf-8 -*-
"""
Checklist for production-ready settings:
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
"""
from __future__ import print_function, unicode_literals

from core.utils import env

from .base import Base


class Prod(Base):
    DEBUG = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT', default='5432'),
            'CONN_MAX_AGE': None,
        }
    }

    ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')
    SECRET_KEY = env('SECRET_KEY')

    INSTALLED_APPS = Base.INSTALLED_APPS

    MIDDLEWARE_CLASSES = [
        'breach_buster.middleware.gzip.GZipMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ] + Base.MIDDLEWARE_CLASSES

    TEMPLATES = Base.TEMPLATES
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

    STATIC_ROOT = '/data/static/'
    MEDIA_ROOT = '/data/media/'

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = False  # needed for django-csrf.js
    SESSION_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = None  # added nginx. results in duplicate header
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # added nginx. results in duplicate header
    SECURE_SSL_REDIRECT = True  # nginx
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 10,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    if env('OPBEAT_ENABLED', default=False):
        OPBEAT = {
            'ORGANIZATION_ID': env('OPBEAT_ORGANIZATION_ID'),
            'APP_ID': env('OPBEAT_APP_ID'),
            'SECRET_TOKEN': env('OPBEAT_SECRET_TOKEN'),
        }
        MIDDLEWARE_CLASSES.insert(0, 'opbeat.contrib.django.middleware.OpbeatAPMMiddleware')
        INSTALLED_APPS.insert(0, 'opbeat.contrib.django')
