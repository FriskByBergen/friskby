# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import time_series.numpy_field


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegularTimeSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('step', models.IntegerField()),
                ('data', time_series.numpy_field.NumpyArrayField(default=None)),
            ],
        ),
    ]
