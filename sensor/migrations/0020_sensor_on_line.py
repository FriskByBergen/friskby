# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0019_auto_20151103_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='on_line',
            field=models.BooleanField(default=True),
        ),
    ]
