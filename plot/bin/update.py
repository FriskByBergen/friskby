#!/usr/bin/env python
import datetime
import sys
import django
from django.utils import dateparse , timezone
from django.conf import settings

from plot.models import *

django.setup()

for id in sys:
    
    try:
        plot = Plot.objects.get( pk = id )
        plot.update( )
    except Plot.DoesNotExist:
        print "No such plot:%s" % id
