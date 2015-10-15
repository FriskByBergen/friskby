#!/usr/bin/env python
import requests
import json

headers = {"Content-Type" : "application/json"}
url = "http://friskby.herokuapp.com/sensor/api/reading/"

data = [{"sensorid" : "TEMP:XX" , "value" : 50, "timestamp" : "10-10-2015 12:12:00"},
        {"sensorid" : "HUM:XX"  , "value" : 20, "timestamp" : "10-10-2015 12:12:00"}]

response = requests.post( url , data = json.dumps( data ) , headers = headers )

if response.status_code == 201:
    print "Posted %s measurements" % response.text
else:
    print "ERROR - posting failed"
    print "Status: %s" % response.status_code
    print "Msg: %s" % response.text
