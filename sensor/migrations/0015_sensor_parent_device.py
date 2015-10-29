# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0014_remove_sensor_parent_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='parent_device',
            field=models.ForeignKey(default='RANDOM_DEVICE', to='sensor.Device'),
            preserve_default=False,
        ),
    ]
