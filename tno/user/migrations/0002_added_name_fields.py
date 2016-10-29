# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=64, verbose_name='full name'),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_name',
            field=models.CharField(blank=True, max_length=64, verbose_name='preferred name'),
        ),
    ]
