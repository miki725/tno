# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OTSecret',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(db_index=True, unique=True, max_length=32, editable=False, blank=True)),
                ('salt', models.BinaryField(max_length=32)),
                ('iv', models.BinaryField(max_length=32)),
                ('associated_data', models.BinaryField(max_length=16)),
                ('tag', models.BinaryField(max_length=16)),
                ('ciphertext', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expires', models.DateTimeField()),
                ('user', models.ForeignKey(related_name=b'one_time_secrets', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'One Time Secret',
            },
            bases=(models.Model,),
        ),
    ]
