# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import ugettext_lazy as _


class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'full_name',
            'preferred_name',
            'email',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
            'last_login',
            'date_joined',
        )}),
    )

    list_display = (
        'username',
        'email',
        'full_name',
        'preferred_name',
        'is_staff',
    )
    search_fields = (
        'username',
        'full_name',
        'preferred_name',
        'email',
    )
