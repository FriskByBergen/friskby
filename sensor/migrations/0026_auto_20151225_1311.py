# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0025_rawdata_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawdata',
            name='extra_data',
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Rawdata'), (1, b'Processed data'), (2, b'Invalid key'), (3, b'Format error in value'), (4, b'Value out of range'), (5, b'Invalid sensor ID')]),
        ),
    ]
