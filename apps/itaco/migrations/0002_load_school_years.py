# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

def add_school_years(apps, schema_editor):
	call_command('loaddata', 'initial_schoolyears.json')


def remove_school_years(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('itaco', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_school_years,
            ),
    ]
