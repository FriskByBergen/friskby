# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0002_auto_20151205_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transform',
            fields=[
                ('id', models.CharField(max_length=60, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[-_:a-zA-Z0-9]+$')])),
                ('description', models.CharField(max_length=256)),
                ('code', models.ForeignKey(to='filter.PythonCode')),
            ],
        ),
    ]
