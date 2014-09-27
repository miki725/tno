# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import getpass

from cryptography.exceptions import InvalidTag
from django.core.management.base import BaseCommand, CommandError

from onetime.models import OTSecret


class Command(BaseCommand):
    args = '<uuid uuid ...>'
    help = 'Decrypt One Time Secret stored in database'

    def handle(self, *args, **options):
        for secret_id in args:
            if secret_id.isdigit():
                field = 'id'
            else:
                field = 'uuid'

            try:
                secret = OTSecret.objects.get(**{field: secret_id})
            except OTSecret.DoesNotExist:
                msg = 'OTSecret does not exist with {}="{}"'
                raise CommandError(msg.format(field, secret_id))

            try:
                plaintext = secret.decrypt(self.get_password(None, secret_id))
                print(plaintext)
            except InvalidTag:
                raise CommandError('invalid password')

    def get_password(self, password=None, secret_id=None):
        if password:
            return password.decode('utf-8')

        if secret_id is None:
            msg = 'Password: '
        else:
            msg = 'Password for {}: '.format(secret_id)

        return self.get_password(getpass.getpass(msg), secret_id)
