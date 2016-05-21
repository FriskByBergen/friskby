#!/usr/bin/env python
import datetime
import sys
import django
from django.utils import dateparse , timezone
from django.conf import settings

django.setup()

from plot.models import *

for id in sys.argv[1:]:
    
    try:
        plot = Plot.objects.get( pk = id )
        plot.updatePlot( )
    except Plot.DoesNotExist:
        print "No such plot:%s" % id
