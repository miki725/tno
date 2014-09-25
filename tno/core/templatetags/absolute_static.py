# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.contrib.staticfiles import finders
from django.template import Library


register = Library()


@register.filter
def absolute_static(path):
    return finders.find(path)
