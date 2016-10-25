# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0005_trusted_certs_data_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='valid_not_after',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='valid_not_before',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='site',
            name='port',
            field=models.PositiveSmallIntegerField(default=443),
        ),
    ]
