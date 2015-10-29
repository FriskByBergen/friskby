# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0013_remove_sensortype_parent_device'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='parent_device',
        ),
    ]
