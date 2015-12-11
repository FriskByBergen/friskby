import datetime
from django.utils import dateparse , timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status
from filter.models import *

from sensor.tests.context import TestContext as SensorContext
from .context import TestContext

class SampledDataTest(TestCase):
    

    def setUp(self):
        self.sensor_context = SensorContext( )
        self.filter_context = TestContext( )



    def test_create(self):
        client = Client( )
        sensor_id = "TEMP:XX"
        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.sensor_context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.sensor_context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : self.sensor_context.external_key}]

        for data in data_list:
            string_data = json.dumps( data )
            response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
            self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)


        sd = SampledData.updateRawData( self.sensor_context.temp_sensor )
        self.assertEqual( len(sd) , 3 )
        
        sd = SampledData.updateRawData( self.sensor_context.temp_sensor )
        self.assertEqual( len(sd) , 3 )
