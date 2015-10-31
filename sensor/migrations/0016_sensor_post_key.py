# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_key', '0001_initial'),
        ('sensor', '0015_sensor_parent_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='post_key',
            field=models.ForeignKey(default=1, to='api_key.ApiKey'),
            preserve_default=False,
        ),
    ]
