# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0026_auto_20151225_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='last_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='last_value',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
