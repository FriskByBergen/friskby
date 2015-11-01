import random
import json

from django.utils import timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *
from .context import TestContext


class Readingtest(TestCase):
    def setUp(self):
        self.context = TestContext()
    
    def test_post_key(self):
        client = Client( )

        # Missing key 
        data = {"sensorid" : "TEMP:XX" , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01"}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Invalid key 
        data = {"sensorid" : "TEMP:XX" , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01" , "key" : "Invalid"}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_403_FORBIDDEN , response.data)

    

    
    def test_post(self):
        client = Client( )

        # Missing data
        response = client.post("/sensor/api/reading/")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)
        
        # Payload is not valid json
        response = client.post("/sensor/api/reading/" , data = "Not valid json" , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # Payload structure is invalid - missing timestamp
        data = {"sensorid" : "TEMP:XX" , "value" : 50, "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # SensorID is invalid
        data = {"sensorid" : "TempXX" , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND , response.data)

        # Value out of range
        data = {"sensorid" : "TEMP:XX" , "value" : 400, "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value not float
        data = {"sensorid" : "TEMP:XX" , "value" : "50X" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value is string-float - OK
        data = {"sensorid" : "TEMP:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)

        #No location - fails
        data = {"sensorid" : "HUM:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        response = client.get("/sensor/api/datainfo/")
        self.assertEqual( len(response.data) , 3 )
        last_info = response.data[2]
        self.assertEqual( last_info["sensor"] , "TEMP:XX")

        response = client.get("/sensor/api/datavalue/")
        self.assertEqual( len(response.data) , 1 )
        last_value = response.data[0]
        self.assertEqual( last_value["value"] , 50)


        
    def test_get(self):
        # The funny construction with a random sensorID is to work
        # around a bug/limitation/misunderstanding in the restdb.io
        # api which seems to cap the return at 100 elements?
        sensor_id = "TEMP:XX:%04d" % random.randint(0,9999)
        Sensor.objects.create( id = sensor_id,
                               post_key = self.context.key , 
                               location = self.context.loc,
                               parent_device = self.context.dev,
                               sensor_type = self.context.sensor_type_temp , 
                               description = "Measurement of ..")

        
        
        client = Client( )
        response = client.get("/sensor/api/reading/")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        response = client.get("/sensor/api/reading/%s/" % sensor_id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        len1 = len(result)

        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}]

        for data in data_list:
            string_data = json.dumps( data )
            response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
            self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)

        
        response = client.get("/sensor/api/reading/%s/" % sensor_id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        len2 = len(result)        

        self.assertEqual( 3 , len2 - len1 )
        
        response = client.get("/sensor/api/reading/%s/" % sensor_id , )
