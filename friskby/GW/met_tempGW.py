#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sys
import requests
import random
import datetime
from friskby_gw import FriskByGW


sensor_map = {"MET:TEMP:FLORIDA" : "http://www.yr.no/place/Norway/Hordaland/Bergen/Bergen_(Florida)_observation_site/varsel.xml", 
              "MET:TEMP:BLINDERN" : "http://www.yr.no/place/Norway/Oslo/Oslo/Blindern/varsel.xml"}


gw = FriskByGW( )
for sensor_id , url in sensor_map.items():
    sensor = gw.getSensor(sensor_id)
    if sensor is None:
        msg = "Sorry - the friskby server at:%s does not have a %s sensor - add that manually first." % (gw.getRootURL() , sensor_id)


    response = requests.get( url )
    if response.status_code == 200:
        source = response.text
        tree = ET.fromstring( source.encode( "utf-8") )
        temp_node  = tree.find("observations").find("weatherstation").find("temperature")

        temp = float(temp_node.get("value"))
        ts = temp_node.get("time")
        ts = ts.replace("T"," ")
        t = datetime.datetime.strptime( ts[:-1] , "%Y-%m-%d %H:%M:%S")
        ts = sensor.timeStamp( time = t )
        sensor.postValue( temp , timestamp = ts )

