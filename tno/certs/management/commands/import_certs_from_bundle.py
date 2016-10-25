# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from ...constants import CERT_PATTERN
from ...exceptions import NoIssuerCertificateFound
from ...models import Certificate


class Command(BaseCommand):
    args = 'path_to_bundle'
    help = 'Import Certs from a CA bundle (PEM certs in a single file)'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+', type=str)
        parser.add_argument('--skip-errors', default=False, action='store_true')

    def handle(self, paths, *args, **options):
        for path in paths:
            path = Path(path)

            if not path.exists():
                raise CommandError('Path {} does not exist'.format(path))

            with path.open('rb') as fid:
                data = b''.join([i for i in fid.readlines() if not i.startswith(b'#')]).strip()

            for cert in CERT_PATTERN.findall(data):
                try:
                    cert = Certificate.from_x509(cert)

                except NoIssuerCertificateFound as e:
                    msg = 'No issuer cert found for subject={} issuer={}'.format(e.subject, e.issuer)

                    if options['skip_errors']:
                        print(self.style.ERROR(
                            'Error: {}'.format(msg)
                        ))

                    else:
                        raise CommandError(
                            '{}. You can use --skip-errors to ignore this error.'
                            ''.format(msg, e.subject)
                        )

                else:
                    cert, created = Certificate.objects.get_or_create_by_fingerprint(cert)
                    if created:
                        print(self.style.SUCCESS(
                            'Inserted: subject={}'
                            ''.format(cert.subject)
                        ))
                    else:
                        print(self.style.WARNING(
                            'Skipping: subject={}'
                            ''.format(cert.subject)
                        ))
