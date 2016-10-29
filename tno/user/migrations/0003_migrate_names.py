# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import F, Value
from django.db.models.functions import Concat


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    User = apps.get_model('user', 'User')
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).all().update(
        full_name=Concat('first_name', Value(' '), 'last_name'),
        preferred_name=F('first_name')
    )


def reverse_func(apps, schema_editor):
    """
    It is hard to parse back the first and last names from
    full and preferred names so we simply do nothing.
    """


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_added_name_fields'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
