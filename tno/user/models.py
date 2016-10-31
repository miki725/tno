# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    PermissionsMixin,
    UserManager,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = AbstractUser._meta.get_field('username')
    full_name = models.CharField(
        _('full name'),
        max_length=64,
        blank=True,
    )
    preferred_name = models.CharField(
        _('preferred name'),
        max_length=64,
        blank=True,
    )
    email = AbstractUser._meta.get_field('email')
    is_staff = AbstractUser._meta.get_field('is_staff')
    is_active = AbstractUser._meta.get_field('is_active')
    date_joined = AbstractUser._meta.get_field('date_joined')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.preferred_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
