# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x509', models.TextField()),
                ('subject', django.contrib.postgres.fields.jsonb.JSONField()),
                ('serial_number', models.CharField(max_length=256)),
                ('valid_not_before', models.DateField()),
                ('valid_not_after', models.DateField()),
                ('key_type', models.CharField(choices=[('RSA', 'RSA'), ('DSA', 'DSA'), ('EC', 'Elliptic Curve')], max_length=3)),
                ('key_size', models.PositiveIntegerField(blank=True, null=True)),
                ('fingerprint_sha2', models.CharField(db_index=True, max_length=64, unique=True)),
                ('issuer_certificate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_certificates', to='certs.Certificate')),
                ('root_certificate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaf_certificates', to='certs.Certificate')),
            ],
        ),
    ]
