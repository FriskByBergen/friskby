# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('time_series', '0001_initial'),
        ('sensor', '0022_rawdata_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.CharField(max_length=60, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[-_:a-zA-Z0-9]+$')])),
                ('description', models.CharField(max_length=256)),
                ('width', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FilterData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter_code', models.ForeignKey(to='filter.Filter')),
                ('sensor', models.ForeignKey(to='sensor.Sensor')),
                ('ts', models.ForeignKey(to='time_series.RegularTimeSeries')),
            ],
        ),
        migrations.CreateModel(
            name='PythonCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=256)),
                ('python_callable', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='filter',
            name='code',
            field=models.ForeignKey(to='filter.PythonCode'),
        ),
        migrations.AlterUniqueTogether(
            name='filterdata',
            unique_together=set([('sensor', 'filter_code')]),
        ),
    ]
