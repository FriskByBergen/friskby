#!/usr/bin/env python
import datetime
import sys
import django
from django.utils import dateparse , timezone
from django.conf import settings
from time_series.models import *
from sensor.models import *
from filter.filter import *

django.setup()

sensor_id = "RANDOM"
sensor = Sensor.objects.get( pk = sensor_id )
ts = sensor.get_ts( )

start = TimeStamp.parse_datetime("2015-10-1T12:00:00Z")
mean = blockedMean_1HOUR( start , ts )

ts = TimeSeries.create( start = start , step = 3600 )
ts.addList( mean )
ts.save( )
