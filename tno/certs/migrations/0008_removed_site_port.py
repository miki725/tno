# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certs', '0007_removed_root_certiticate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='port',
        ),
    ]
