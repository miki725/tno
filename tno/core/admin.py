# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.contrib.admin import AdminSite


class TNOAdminSite(AdminSite):
    site_title = 'TNO.io Admin'
    site_header = 'TNO.io Admin'
    index_title = 'TNO.io Admin'


site = TNOAdminSite()
