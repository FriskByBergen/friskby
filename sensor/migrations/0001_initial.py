# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'Device manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'Name of the device')),
                ('company', models.ForeignKey(to='sensor.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'Location')),
                ('latitude', models.FloatField(verbose_name=b'Latitude')),
                ('longitude', models.FloatField(verbose_name=b'Longitude')),
                ('altitude', models.FloatField(null=True, verbose_name=b'Altitude')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'Type of measurement')),
            ],
        ),
        migrations.CreateModel(
            name='SensorID',
            fields=[
                ('id', models.CharField(max_length=60, serialize=False, verbose_name=b'Sensor ID', primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[-_:a-zA-Z0-9]+$')])),
                ('description', models.CharField(max_length=256, verbose_name=b'Description')),
                ('unit', models.CharField(max_length=60, verbose_name=b'Unit')),
                ('min_value', models.FloatField(verbose_name=b'Minimum value')),
                ('max_value', models.FloatField(verbose_name=b'Maximum value')),
                ('location', models.ForeignKey(to='sensor.Location', null=True)),
                ('measurement_type', models.ForeignKey(to='sensor.MeasurementType')),
                ('parent_device', models.ForeignKey(to='sensor.DeviceType')),
            ],
        ),
    ]
