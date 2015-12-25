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

qs_size = 10000
offset = 0

while offset < 2000000:
    
    qs = make_qs( offset , qs_size)
    for rd in qs:
        if rd.value == -1:
            if rd.status in [RawData.RAWDATA , RawData.PROCESSED]:
                try:
                    rd.value = float(rd.string_value)
                    rd.string_value = None
                    rd.status = RawData.RAWDATA
                except ValueError:
                    rd.status = RawData.FORMAT_ERROR
                    print "\nFormat error: %d" % rd.id
        
                rd.save()

    offset += qs_size            
