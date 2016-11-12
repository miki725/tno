# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certs', '0008_removed_site_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('description', models.TextField(blank=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_collections', to=settings.AUTH_USER_MODEL)),
                ('sites', models.ManyToManyField(blank=True, related_name='site_collections', to='certs.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
