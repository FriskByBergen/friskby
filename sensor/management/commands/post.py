import sys
import requests
import json
import httplib

from django.core.management.base import BaseCommand, CommandError
from sensor.models import *
from ._sample import sample
from ._sensor_list import sensor_list
    
class Command(BaseCommand):
    help = ""
    

    def add_arguments( self, parser):
        parser.add_argument('sensor')
        parser.add_argument('value')
        parser.add_argument('--url')
        parser.add_argument('--key')


    def handle(self , *args , **options):
        sensor_id = options["sensor"]
        value = float( options["value"] )
        
        url = options["url"]
        if url is None:
            url = "http://127.0.0.1:8000"

        key = options["key"]
        if key is None:
            sensor = Sensor.objects.get( sensor_id = sensor_id )
            key = str(sensor.parent_device.post_key.external_key)

        data = {"sensorid" : sensor_id , 
                "value" : value, 
                "timestamp" : TimeStamp.create( ),
                "key" : key}

        full_url = "%s/sensor/api/reading/" % url
        print("Posting to: %s" % full_url)
        try:
            respons = requests.post( full_url, 
                                     headers = {'Content-Type': 'application/json'},
                                     data = json.dumps(data))
        except:
            sys.exit("Exception raised when posting")

        status_code = respons.status_code
        print("%d : %s" % (status_code, httplib.responses[ status_code ]))
        

