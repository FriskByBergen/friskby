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

def run_filter(sensor_id , filter_id):
    try: 
        sensor = Sensor.objects.get( pk = sensor_id )
    except Sensor.DoesNotExist:
        sys.stderr.write("Sensor:%s not found\n" % sensor_id);
        return 

    try:
        filter_ = Filter.objects.get( pk = filter_id )
    except Filter.DoesNotExist:
        sys.stderr.write("Filter:%s not found\n" % filter_id);
        return
        
    FilterData.update( sensor , filter_ )

if len(sys.argv) > 1:
    for i in range((len(sys.argv) - 1) / 2):
        sensor_id = sys.argv[1 + 2*i]
        filter_id = sys.argv[2 + 2*i]

        run_filter( sensor_id , filter_id )
else:
    run_filter( "RANDOM" , "MEAN_1HOUR" )

