# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0017_rawdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='extra_data',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='timestamp_recieved',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
