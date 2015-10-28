# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0008_auto_20151028_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_description', models.CharField(max_length=40, verbose_name=b'Short description')),
                ('description', models.CharField(max_length=256, verbose_name=b'Description')),
                ('unit', models.CharField(max_length=60, verbose_name=b'Unit')),
                ('min_value', models.FloatField(verbose_name=b'Minimum value')),
                ('max_value', models.FloatField(verbose_name=b'Maximum value')),
                ('measurement_type', models.ForeignKey(to='sensor.MeasurementType')),
                ('parent_device', models.ForeignKey(to='sensor.DeviceType')),
            ],
        ),
    ]
