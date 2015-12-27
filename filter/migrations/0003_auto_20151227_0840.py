# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0002_auto_20151211_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterdata',
            name='ts',
            field=models.OneToOneField(to='time_series.RegularTimeSeries'),
        ),
        migrations.AlterField(
            model_name='sampleddata',
            name='data',
            field=models.OneToOneField(to='time_series.SampledTimeSeries'),
        ),
    ]
