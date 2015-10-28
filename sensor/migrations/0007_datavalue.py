# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0006_datainfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('data_info', models.ForeignKey(to='sensor.DataInfo')),
                ('data_type', models.ForeignKey(to='sensor.DataType')),
            ],
        ),
    ]
