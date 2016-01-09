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

def make_qs(offset , size):
    last_id = offset + size
    print "Range [%d , %d)" % (offset , last_id)
    return RawData.objects.filter(id__gte = offset, id__lt = last_id) 

qs_size = 2000
offset = 0

sensor_map = {}
for sensor in Sensor.objects.all():
    sensor_map[sensor.id] = sensor

while offset < 3000000:
    qs = make_qs( offset , qs_size)
    for rd in qs:
        if rd.status in [RawData.RAWDATA , RawData.PROCESSED]:
            if rd.sensor_id in sensor_map:
                sensor = sensor_map[rd.sensor_id]
                try:
                    if not rd.string_value is None:
                        rd.value = float(rd.string_value)

                    if sensor.sensor_type.valid_range( rd.value ):
                        rd.status = RawData.RAWDATA
                        rd.string_value = None
                    else:
                        rd.string_value = "%s" % rd.value
                        rd.value = -1
                        rd.status = RawData.RANGE_ERROR
                        print "\nRange error: %d" % rd.id
                except ValueError:
                    rd.status = RawData.FORMAT_ERROR
                    print "\nFormat error: %d" % rd.id
        
                if rd.status == RawData.RAWDATA:
                    assert( sensor.sensor_type.valid_range( rd.value ) )
            else:
                rd.status = RawData.INVALID_SENSOR
                if rd.value != -1:
                    rd.string_value = "%s" % rd.value
                    rd.value = -1
                    
            rd.save()

    offset += qs_size            
