# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0012_device'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensortype',
            name='parent_device',
        ),
    ]
