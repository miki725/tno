# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.core.management.base import BaseCommand

from onetime.models import OTSecret


class Command(BaseCommand):
    help = 'Deletes all expired secret messages'

    def handle(self, *args, **options):
        expired = OTSecret.objects.expired()
        count = expired.count()

        if count:
            expired.delete()

        msg = 'Deleted {} secret messages'
        print(msg.format(count))
