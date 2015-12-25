# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0024_auto_20151225_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='value',
            field=models.FloatField(default=-1),
        ),
    ]
