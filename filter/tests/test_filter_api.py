import random
import json

from django.utils import timezone
from django.test import TestCase, Client
from rest_framework import status

from filter.models import *
from .context import TestContext
from sensor.tests.context import TestContext as SensorContext        
    

class FilterApiTest(TestCase):
    def setUp(self):
        self.context = TestContext()
        self.sensor_context = SensorContext( )

    def test_get(self):
        client = Client( )
        
        sensor_id = "TEMP:XX"
        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.sensor_context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.sensor_context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : self.sensor_context.external_key}]
        
        client = Client( )
        for data in data_list:
            string_data = json.dumps( data )
            response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")

        SampledData.updateRawData( self.sensor_context.temp_sensor )
        self.fd_mean  = FilterData.update( self.sensor_context.temp_sensor , self.context.f_mean )
        self.fd_max   = FilterData.update( self.sensor_context.temp_sensor , self.context.f_max )

        # The root endpoint should return a dict {'sensor_id' :
        # ["filter1","filter2"]} of the available sensor/filter
        # combinations.
        response = client.get("/filter/api/filter_data/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        d = response.data
        self.assertEqual( len(d) , 1 )
        self.assertTrue( "TEMP:XX" in d )

        l = d["TEMP:XX"]
        self.assertTrue( "MEAN_1HOUR" in l)
        self.assertTrue( "MAX_1HOUR" in l)
        self.assertEqual( len(l) , 2 )

        
        response = client.get("/filter/api/filter_data/missing_sensor/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        # Missing filter:
        response = client.get("/filter/api/filter_data/TEMP:XX/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        # Missing filter:
        response = client.get("/filter/api/filter_data/TEMP:XX/missing_filter/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        response = client.get("/filter/api/filter_data/TEMP:XX/MEAN_1HOUR/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        response = client.get("/filter/api/filter_data/TEMP:XX/MIN_1HOUR/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
        
