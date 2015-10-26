#!/usr/bin/env python
import sys
import requests
import random
import time
from friskby_gw import FriskByGW


gw = FriskByGW(  )
sensor_id = sys.argv[1]
sensor = gw.getSensor( sensor_id )
if sensor is None:
    msg = "Sorry - the friskby server at:%s does not have a %s sensor - add that manually first." % (gw.getRootURL() , sensor_id)
    sys.exit( msg )

values = sensor.getData( )
for (ts , value) in values:
    print ts 
