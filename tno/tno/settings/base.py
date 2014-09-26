"""
Django settings for tno project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import print_function, unicode_literals
import os

from .conf.pipeline import *  # noqa


PROJECT_PATH = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
PROJECT_NAME = os.path.basename(PROJECT_PATH)

INSTALLED_APPS = (
    'braces',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_auxilium',
    'django_extensions',
    'djangosecure',
    'pipeline',
    'rest_framework',
    'vanilla',

    'core',
    'onetime',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auxilium.middleware.html.MinifyHTMLMiddleware',
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media files
MEDIA_ROOT = os.path.join(PROJECT_PATH, PROJECT_NAME, 'media')
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.join(PROJECT_PATH, PROJECT_NAME, 'all_static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, PROJECT_NAME, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Templates
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, PROJECT_NAME, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
)

ALLOWED_INCLUDE_ROOTS = STATICFILES_DIRS

# URLs
ROOT_URLCONF = 'tno.urls'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'
WSGI_APPLICATION = 'tno.wsgi.application'
