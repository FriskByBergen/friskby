# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-05 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0064_remove_rawdata_processed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='git_version',
        ),
    ]
