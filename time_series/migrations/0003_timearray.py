# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import time_series.numpy_field


class Migration(migrations.Migration):

    dependencies = [
        ('time_series', '0002_auto_20151207_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeArray',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', time_series.numpy_field.NumpyArrayField(default=None)),
            ],
        ),
    ]
