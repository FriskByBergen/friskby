# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0020_sensor_on_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicetype',
            name='company',
        ),
        migrations.RemoveField(
            model_name='sensortype',
            name='company',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
