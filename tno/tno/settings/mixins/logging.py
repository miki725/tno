# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


class LoggingMixin(object):
    @property
    def LOGGING(self):
        logging = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(asctime)s '
                              '%(levelname)s '
                              '%(name)s '
                              '%(message)s',
                },
                'simple': {
                    'format': '%(levelname)s '
                              '%(name)s '
                              '%(message)s',
                },
            },
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse',
                },
            },
            'handlers': {
                'null': {
                    'level': 'INFO',
                    'class': 'logging.NullHandler',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                'django.request': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate': True,
                },
                'tno': {
                    'level': 'INFO',
                    'handlers': ['console'],
                },
            }
        }

        logging['loggers'].update({
            k: {
                'level': 'INFO',
                'handlers': ['console'],
            }
            for k in self.PROJECT_APPS
        })

        return logging
