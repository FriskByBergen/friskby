# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sensor.models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0003_auto_20151025_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorid',
            name='data_type',
            field=models.ForeignKey(default="TEST", to='sensor.DataType'),
        ),
    ]
