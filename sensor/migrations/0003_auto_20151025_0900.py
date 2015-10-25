# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def install(apps,key):
    DataType = apps.get_model("sensor", "DataType")
    DataType.objects.create( id = key )
    
def install_TEST(apps,schema_editor):
    install(apps,"TEST")

def install_RAWDATA(apps,schema_editor):
    install(apps,"RAWDATA")

class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0002_datatype'),
    ]

    operations = [
        migrations.RunPython( install_TEST ),
        migrations.RunPython( install_RAWDATA ),
    ]
