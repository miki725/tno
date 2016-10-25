# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='CREATE INDEX "certs_certificate_subject_gin" '
                'ON certs_certificate '
                'USING GIN ("subject");',
            reverse_sql='DROP INDEX "certs_certificate_subject_gin"',
            elidable=False,
        )
    ]
