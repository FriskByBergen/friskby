# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0021_auto_20151122_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Rawdata'), (1, b'Processed data'), (2, b'Invalid key')]),
        ),
    ]
