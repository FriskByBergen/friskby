# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0011_auto_20151029_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.CharField(max_length=60, serialize=False, verbose_name=b'Device ID', primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[-_:a-zA-Z0-9]+$')])),
                ('description', models.CharField(max_length=256, verbose_name=b'Description')),
                ('device_type', models.ForeignKey(to='sensor.DeviceType')),
                ('location', models.ForeignKey(to='sensor.Location', null=True)),
            ],
        ),
    ]
