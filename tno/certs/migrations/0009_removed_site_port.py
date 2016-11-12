# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0008_added_site_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='port',
        ),
    ]
