# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0005_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.ForeignKey(to='sensor.Location')),
                ('sensor', models.ForeignKey(to='sensor.SensorID')),
                ('timestamp', models.ForeignKey(to='sensor.TimeStamp')),
            ],
        ),
    ]
