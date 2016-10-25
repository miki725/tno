# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0006_changed_valility_to_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='root_certificate',
        ),
        migrations.AlterField(
            model_name='certificate',
            name='trust_certificate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaf_certificates', to='certs.Certificate'),
        ),
    ]
