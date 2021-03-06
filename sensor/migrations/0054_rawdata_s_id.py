# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-05 18:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    import sys
    if not schema_editor.connection.alias == 'default':
        return
    sensor = apps.get_model('sensor', 'Sensor')
    rawdata = apps.get_model('sensor', 'RawData')

    sensors = {}
    for row in sensor.objects.all():
        sensor_name = row.sensor_id
        sensor_id = row.s_id
        sensors[sensor_name] = row

    for row in rawdata.objects.all():
        sensor_name = row.sensor_id
        if sensor_name not in sensors:
            sys.stderr.write('\nNo sensor for key "%s".\n' % sensor_name)
            row.s_id = None
        else:
            row.s_id = sensors[sensor_name]
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0053_auto_20170305_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='s_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sensor.Sensor'),
        ),
        migrations.RunPython(forwards)
    ]
