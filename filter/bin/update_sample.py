#!/usr/bin/env python
import datetime
import sys
import django
from django.utils import dateparse , timezone
from django.conf import settings

django.setup()

from time_series.models import *
from sensor.models import *
from filter.models import *




def update(sensor , transform = None):
    SampledData.updateSampledData( sensor , transform )
    for f in Filter.objects.all():
        FilterData.update( sensor , f , transform = transform)
            


    

if len(sys.argv) == 1:
    sensor_list = Sensor.objects.all( )
else:
    sys.exit("Only mode GLOBAL is supported")

for sensor in sensor_list:
    print "Updating: %s" % sensor.id
    try:
        update( sensor )
    except Exception as e:
        print e

