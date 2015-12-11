# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('time_series', '0002_auto_20151211_0836'),
        ('sensor', '0022_rawdata_status'),
        ('filter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampledData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.ForeignKey(to='time_series.SampledTimeSeries')),
                ('parent_data', models.ForeignKey(to='filter.SampledData', null=True)),
                ('sensor', models.ForeignKey(to='sensor.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Transform',
            fields=[
                ('id', models.CharField(max_length=60, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[-_:a-zA-Z0-9]+$')])),
                ('description', models.CharField(max_length=256)),
                ('code', models.ForeignKey(to='filter.PythonCode')),
            ],
        ),
        migrations.AddField(
            model_name='sampleddata',
            name='transform',
            field=models.ForeignKey(to='filter.Transform', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='sampleddata',
            unique_together=set([('sensor', 'transform')]),
        ),
    ]
