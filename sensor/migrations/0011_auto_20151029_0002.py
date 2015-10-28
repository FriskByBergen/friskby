# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0010_auto_20151028_2354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='max_value',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='measurement_type',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='min_value',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='unit',
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(default=1, to='sensor.SensorType'),
            preserve_default=False,
        ),
    ]
