#!/usr/bin/env python
import os
import requests
import django

restdb_url = "https://friskbybergen-1d96.restdb.io/rest/posts"
restdb_key = os.getenv("RESTDB_KEY")
post_key = "407f1ef4-2eb2-4299-b977-464e26a094e7"

#from django.utils import dateparse , timezone
#from django.conf import settings
#from filter.filter import *

def update_env(*args):
    for arg in args:
        var,value = arg.split("=")
        os.environ[var] = value
    
    if not os.environ.has_key("DJANGO_SETTINGS_MODULE"):
        os.environ["DJANGO_SETTINGS_MODULE"] = "friskby.settings"


    new_path = os.path.realpath( os.path.join( os.path.dirname(__file__) , "../../") )
    if os.environ.has_key("PYTHONPATH"):
        os.environ["PYTHONPATH"] = "%s:%s" % (new_path , os.environ["PYTHONPATH"])
    else:
        os.environ["PYTHONPATH"] = new_path
    



def assert_env():
    assert os.environ.has_key("DATABASE_URL")
    assert os.environ.has_key("DJANGO_SETTINGS_MODULE")

#################################################################
update_env()
assert_env()
django.setup()

from sensor.models import *


response = requests.get( restdb_url , 
                         params = {"max" : 10000000}, 
                         headers = {"x-apikey" : restdb_key , "Content-Type" : "application/json"})


data = {}
if response.status_code == 200:
    for line in response.json( ):
        device_id = line["deviceid"]
        if device_id == "FriskPI03":
            continue

        ts = line["timestamp"]
        pm10 = line["data"]["PM10"]
        pm25 = line["data"]["PM25"]

        sensor_id_pm10 = "%s_PM10" % device_id
        sensor_id_pm25 = "%s_PM25" % device_id
        if not sensor_id_pm10 in data:
            data[sensor_id_pm10] = []

        if not sensor_id_pm25 in data:
            data[sensor_id_pm25] = []
            
        data[sensor_id_pm10].append( (ts , pm10 ))
        data[sensor_id_pm25].append( (ts , pm25 ))


for sensor_id in data.keys():
    print "Deleting old %s entries" % sensor_id
    RawData.objects.filter( sensor_id = sensor_id ).delete()
    print "Inserting new %s entries" % sensor_id
    cnt = 0
    for (ts,pm) in data[sensor_id]:
        post = {"key" : post_key,
                "sensorid" : sensor_id,
                "value" : pm,
                "timestamp" : ts }
        
        rd = RawData.create( post )
        if rd.status != RawData.RAWDATA:
            raise ValueError("Invalid RawData:%s " % rd)
            
        cnt += 1 
        if cnt % 100 == 0:
            print "%s : %d/%d" % (sensor_id , cnt, len(data[sensor_id]))
