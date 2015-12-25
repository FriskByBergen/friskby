# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0022_rawdata_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rawdata',
            old_name='value',
            new_name='string_value',
        ),
    ]
