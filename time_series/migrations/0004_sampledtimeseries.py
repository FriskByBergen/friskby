# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import time_series.numpy_field
import time_series.models


class Migration(migrations.Migration):

    dependencies = [
        ('time_series', '0003_timearray'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampledTimeSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', time_series.numpy_field.NumpyArrayField(default=None)),
                ('timestamp', models.ForeignKey(to='time_series.TimeArray')),
            ],
            bases=(models.Model, time_series.models.OperatorMixin),
        ),
    ]
