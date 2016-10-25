# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import getpass

from django.core.management.base import BaseCommand

from onetime.models import OTSecret


class Command(BaseCommand):
    help = 'Creates One Time Secret'

    def handle(self, *args, **options):
        password = self.get_password()
        secret = self.get_message()

        secret = OTSecret.objects.encrypt(password, secret)

        msg = 'created secret with uuid="{}"'
        print(msg.format(secret.uuid))

    def get_password(self, password=None):
        if password:
            return password.decode('utf-8')

        return self.get_password(getpass.getpass())

    def get_message(self, message=None):
        if message:
            return message.decode('utf-8')

        msg = 'Secret: '
        return self.get_message(input(msg))
