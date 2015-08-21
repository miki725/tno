# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os


def abspath(*components):
    return os.path.abspath(os.path.join(*components))


def env(key, **kwargs):
    try:
        return os.environ[key]
    except KeyError:
        if 'default' in kwargs:
            return kwargs['default']
        raise
