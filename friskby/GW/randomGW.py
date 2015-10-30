#!/usr/bin/env python
import sys
import requests
import random
import time
from friskby_gw import FriskByGW


gw = FriskByGW(  )
sensor_id = "RANDOM"
sensor = gw.getSensor( sensor_id )
if sensor is None:
    msg = "Sorry - the friskby server at:%s does not have a %s sensor - add that manually first." % (gw.getRootURL() , sensor_id)
    sys.exit( msg )

num = 1
min_value = sensor.getMinValue( )
max_value = sensor.getMaxValue( )
sleep_time = 1
corr = 0.90

if len(sys.argv) > 1:
    num = int(sys.argv[1])

try:
    last_value = sensor.getLastValue( )[1]
except Exception:
    last_value = 0.50 * (min_value + max_value)


for i in range(num):
    random_value = (max_value - min_value) * (0.5 + 1.25 * (random.random() - 0.5))
    new_value = last_value * corr + (1 - corr) * random_value 

    if new_value > max_value:
        new_value = max_value
    
    if new_value < min_value:
        new_value = min_value

    sensor.postValue( new_value )
    last_value = new_value
