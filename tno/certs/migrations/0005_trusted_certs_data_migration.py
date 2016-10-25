# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

import certifi
from django.db import migrations

from ..models import Certificate as _Certificate


SHA2_FINGERPRINT_PAIRS_PATTERN = re.compile(r'([a-z0-9]{2})')


with open(certifi.where(), 'rb') as fid:
    certs = fid.read().decode('utf-8')


def sha_to_pairs(fingerprint: str) -> str:
    return SHA2_FINGERPRINT_PAIRS_PATTERN.sub(r'\g<1>:', fingerprint, count=len(fingerprint) // 2 - 1)


def is_trusted(cert: _Certificate) -> bool:
    return sha_to_pairs(cert.fingerprint_sha2) in certs


def forwards_func(apps, schema_editor):
    Certificate = apps.get_model('certs', 'Certificate')
    db_alias = schema_editor.connection.alias
    base_q = Certificate.objects.using(db_alias)

    for cert in base_q.filter(root_certificate_id__isnull=True):
        cert.is_trusted = is_trusted(cert)
        cert.is_root = True
        cert.save()

    for cert in base_q.filter(root_certificate__is_trusted=True):
        cert.trust_certificate = cert.root_certificate
        cert.save()


def reverse_func(apps, schema_editor):
    Certificate = apps.get_model('certs', 'Certificate')
    db_alias = schema_editor.connection.alias
    Certificate.objects.using(db_alias).update(
        is_root=False,
        is_trusted=False,
        trust_certificate_id=None,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0004_added_site_model'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
