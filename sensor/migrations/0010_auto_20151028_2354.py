# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0009_sensortype'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensortype',
            name='company',
            field=models.ForeignKey(default=1, to='sensor.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensortype',
            name='product_name',
            field=models.CharField(default='DefaultProductName', max_length=256, verbose_name=b'Product name'),
            preserve_default=False,
        ),
    ]
