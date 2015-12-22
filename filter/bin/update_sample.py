#!/usr/bin/env python
import datetime
import sys
import django
from django.utils import dateparse , timezone
from django.conf import settings
from time_series.models import *
from sensor.models import *
from filter.models import *

django.setup()

sensor_list = []
if len(sys.argv) > 1:
    for sensor_id in sys.argv[1:]:
        try:
            sensor = Sensor.objects.get( pk = sensor_id )
            sensor_list.append( sensor )
        except Sensor.DoesNotExist:
            sys.stderr.write("** Sensor:%s not found\n" % sensor_id)
else:
    for sensor in Sensor.objects.all():    
        sensor_list.append( sensor )


for sensor in sensor_list:
    print "Updating: %s" % sensor.id
    SampledData.updateRawData( sensor )

