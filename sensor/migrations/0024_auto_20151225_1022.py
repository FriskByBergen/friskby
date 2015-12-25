# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0023_auto_20151225_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='string_value',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
