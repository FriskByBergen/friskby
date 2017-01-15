import random
import json

from django.urls import reverse
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
        sensor_id = "TEMP:XX"
        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.sensor_context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.sensor_context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : self.sensor_context.external_key}]
        
        client = Client( )
        for data in data_list:
            string_data = json.dumps( data )
            post_url = reverse( "sensor.api.post" )
            response = client.post( post_url , data = json.dumps( data ) , content_type = "application/json")

        SampledData.updateRawData( self.sensor_context.temp_sensor )
        self.fd_mean  = FilterData.update( self.sensor_context.temp_sensor , self.context.f_mean )
        self.fd_max   = FilterData.update( self.sensor_context.temp_sensor , self.context.f_max )

        # The root endpoint should return a dict {'sensor_id' :
        # ["filter1","filter2"]} of the available sensor/filter
        # combinations.

        url = reverse("api.filter.overview")
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        d = response.data
        self.assertEqual( len(d) , 1 )
        self.assertTrue( "TEMP:XX" in d )

        l = d["TEMP:XX"]
        self.assertTrue( "MEAN_1HOUR" in l)
        self.assertTrue( "MAX_1HOUR" in l)
        self.assertEqual( len(l) , 2 )

        url = reverse("api.filter.sensor", args = ["INVALID_SENSOR"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        # No data
        url = reverse("api.filter.sensor", args = ["TEMP:XX"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        # Missing filter:
        url = reverse("api.filter.data", args = ["TEMP:XX", "missing_filter"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        url = reverse("api.filter.data", args = ["TEMP:XX", "MEAN_1HOUR"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        url = reverse("api.filter.data", args = ["TEMP:XX", "MIN_1HOUR"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
        
