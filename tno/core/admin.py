# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from user.admin import UserAdmin
from user.models import User


class TNOAdminSite(AdminSite):
    site_title = 'TNO.io Admin'
    site_header = 'TNO.io Admin'
    index_title = 'TNO.io Admin'


site = TNOAdminSite()


site.register(User, UserAdmin)
site.register(Group, GroupAdmin)
