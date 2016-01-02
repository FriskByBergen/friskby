import sys
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

        response = client.get("/filter/api/sample_data/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
                              
        # The root endpoint should return a dict {'sensor_id' :
        # ["transform1","transform2"]} of the available sensor/transformation
        # combinations
        response = client.get("/filter/api/sampled_data/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        d = response.data
        self.assertEqual( len(d) , 1 )
        self.assertTrue( "TEMP:XX" in d )
        
        l = d["TEMP:XX"]
        self.assertEqual( len(l) , 0 )

        response = client.get("/filter/api/sampled_data/TEMP:XX/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = response.data
        self.assertEqual( len(data) , 3 )

        self.assertEqual( data[0][0] , TimeArray.parse_datetime( "2015-10-10T12:12:00+01" ))
        self.assertEqual( data[1][0] , TimeArray.parse_datetime( "2015-10-10T12:13:00+01" ))
        self.assertEqual( data[2][0] , TimeArray.parse_datetime( "2015-10-10T12:14:00+01" ))
        
        self.assertEqual( data[0][1] , 60 )
        self.assertEqual( data[1][1] , 10 )
        self.assertEqual( data[2][1] , 20 )

        response = client.get("/filter/api/sampled_data/TEMP:XX/" , {"num" : 1})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = response.data
        self.assertEqual( len(data) , 1 )

        self.assertEqual( data[0][0] , TimeArray.parse_datetime( "2015-10-10T12:14:00+01" ))
        self.assertEqual( data[0][1] , 20 )

        response = client.get("/filter/api/sampled_data/TEMP:XX/" , {"start" : "2015-10-10T12:13:00+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = response.data
        self.assertEqual( len(data) , 1 )

        self.assertEqual( data[0][0] , TimeArray.parse_datetime( "2015-10-10T12:14:00+01" ))
        self.assertEqual( data[0][1] , 20 )

        response = client.get("/filter/api/sampled_data/TEMP:XX/" , {"start" : "2015-10-10T12:13:00+01" , "num" : 1})
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )
