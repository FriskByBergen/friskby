# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0018_auto_20151103_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='timestamp_recieved',
            field=models.DateTimeField(),
        ),
    ]
