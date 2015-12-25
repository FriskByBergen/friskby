import random
import json

from django.utils import timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *
from .context import TestContext


#class CurrentTest(TestCase):
#    def setUp(self):
#        self.context = TestContext()
#    
#    def test_get(self):
#        client = Client( )
#        
#        # Missing sensor => 404
#        response = client.get( "/sensor/api/current/MISSING-SENSOR/" ) 
#        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
#
#        t = TimeStamp.now( )
#        t = t.replace( microsecond = 0)
#        data = {"sensorid" : "TEMP:XX" , 
#                "value" : 50 , 
#                "timestamp" : TimeStamp.create( t ),
#                "key" : self.context.external_key}
#        response = client.post("/sensor/api/reading/" , 
#                               data = json.dumps( data ) , 
#                               content_type = "application/json")
#        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)
#
#        # Normal happy path
#        response = client.get( "/sensor/api/current/TEMP:XX/" ) 
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        loc = response.data["location"]
#        self.assertEqual( response.data["sensorid"] , data["sensorid"] )
#        self.assertEqual( response.data["value"] , data["value"] )
#        self.assertEqual( loc["latitude"] , self.context.loc.latitude )
#        self.assertEqual( loc["longitude"] , self.context.loc.longitude )
#
#        response = client.get( "/sensor/api/sensorinfo/TEMP:XX/" )
#        self.assertEqual( response.data["current_value"] , 50 )
#        self.assertEqual( response.data["current_timestamp"] , t )
#
#        # Get with an invalid measurement type -> 404
#        response = client.get( "/sensor/api/current/TEMP:XX/" , data = {"mtype" : 888}) 
#        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
#
#        # Get with a valid - but not matching sensor - measurement type -> 404
#        mtype2 = MeasurementType.objects.create( name = "Temperature2" )
#        response = client.get( "/sensor/api/current/TEMP:XX/" , data = {"mtype" : mtype2.id}) 
#        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )
#
#
#    def test_no_data(self):
#        client = Client( )
#        sensor = Sensor.objects.create( id = "sensor2",
#                                        location = self.context.loc,
#                                        parent_device = self.context.dev,
#                                        description = "Desc",
#                                        post_key = self.context.key,
#                                        sensor_type = self.context.sensor_type_temp)
#
#        # Sensor has absolutely no data
#        response = client.get( "/sensor/api/current/sensor2/" ) 
#        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
#
#        response = client.get( "/sensor/api/sensorinfo/sensor2/" )
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        self.assertEqual( response.data["current_value"] , None )
#        self.assertEqual( response.data["current_timestamp"] , None )
#
#
#
#    def test_expired(self):
#        client = Client( )
#        
#        t = timezone.now( ) - datetime.timedelta( seconds = 4000 )
#        t = t.replace( microsecond = 0)
#        data = {"sensorid" : "TEMP:XX" , 
#                "value" : 50 , 
#                "timestamp" : TimeStamp.create( t ),
#                "key" : self.context.external_key}
#        response = client.post("/sensor/api/reading/" , 
#                               data = json.dumps( data ) , 
#                               content_type = "application/json")
#        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)
#
#        
#        # Get "old" data (more than default 3600 seconds) -> value is set to None
#        response = client.get( "/sensor/api/current/TEMP:XX/" ) 
#        print response.data
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        self.assertTrue( response.data["value"] is None )
#        self.assertEqual( response.data["timestamp"]  , t )
#
#        response = client.get( "/sensor/api/sensorinfo/TEMP:XX/" )
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        self.assertEqual( response.data["current_value"] , None )
#        self.assertEqual( response.data["current_timestamp"]  , t )
#
#
#        response = client.get( "/sensor/api/current/TEMP:XX/" , {"timeout" : 5000}) 
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        self.assertEqual( response.data["value"] , 50 )
#        self.assertEqual( response.data["timestamp"]  , t )
#
#        # Timeout == 0 => effectively no timeout limit.
#        response = client.get( "/sensor/api/current/TEMP:XX/" , {"timeout" : 0}) 
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        self.assertEqual( response.data["value"] , 50 )
#        self.assertEqual( response.data["timestamp"]  , t )
#
#        
#    def test_get_list(self):
#        client = Client( )
#        # Get with an invalid measurement type -> 404
#        response = client.get( "/sensor/api/current/" , data = {"mtype" : 888}) 
#        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
#        
#        mtype2 = MeasurementType.objects.create( name = "Temperature2" )
#
#        response = client.get( "/sensor/api/current/" , data = {"mtype" : mtype2.id}) 
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        self.assertEqual( response.data , [] )
#
#        response = client.get( "/sensor/api/current/" ) 
#        self.assertEqual( response.status_code , status.HTTP_200_OK )
#        self.assertEqual( len(response.data) , 2 )
