# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0003_added_certificate_trust_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('host', models.CharField(db_index=True, max_length=256, unique=True)),
                ('port', models.PositiveSmallIntegerField()),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='certs.Certificate')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
