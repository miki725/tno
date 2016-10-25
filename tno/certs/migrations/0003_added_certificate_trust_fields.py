# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0002_gin_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='is_root',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='certificate',
            name='is_trusted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='certificate',
            name='trust_certificate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trust_leaf_certificates', to='certs.Certificate'),
        ),
    ]
