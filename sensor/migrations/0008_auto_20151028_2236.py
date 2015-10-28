# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0007_datavalue'),
    ]

    operations = [
        migrations.RenameModel("SensorID" , "Sensor")
    ]
