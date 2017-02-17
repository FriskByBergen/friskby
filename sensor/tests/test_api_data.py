import random
import json

from django.urls import reverse
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
        url = reverse( "sensor.api.post" )
        
        pre_length = len(RawData.objects.all( ))
        # Missing key 
        data = {"sensorid" : "TEMP:XX" , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01"}
        string_data = json.dumps( data )
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        post_length = len(RawData.objects.all( ))

        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)
        self.assertEqual( pre_length , post_length )


        # Invalid key 
        data = {"sensorid" : "TEMP:XX" , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01" , "key" : "Invalid"}
        string_data = json.dumps( data )
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)
        post_length = len(RawData.objects.all( ))
        self.assertEqual( pre_length , post_length )
        

    def test_post_offline(self):
        client = Client( )
        self.context.temp_sensor.on_line = False
        self.context.temp_sensor.save( ) 
        sensor_id = self.context.temp_sensor.sensor_id
        data = {"sensorid" : sensor_id , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        url = reverse( "sensor.api.post" )
        get_url = reverse( "sensor.api.get" , args = [sensor_id])
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        get_url = reverse( "sensor.api.get" , args = [sensor_id])
        response = client.get( get_url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( len(result) , 0 )
        self.assertEqual( 1 , len(self.context.temp_sensor.get_rawdata( status = RawData.SENSOR_OFFLINE )))
        

    
    def test_post(self):
        client = Client( )

        # Missing data
        url = reverse( "sensor.api.post" )
        response = client.post( url )
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)
        
        # Payload is not valid json
        response = client.post( url , data = "Not valid json" , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # Payload structure is invalid - missing timestamp
        data = {"sensorid" : "TEMP:XX" , "value" : 50, "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # SensorID is invalid
        data = {"sensorid" : "TempXX" , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value out of range
        data = {"sensorid" : "TEMP:XX" , "value" : 400, "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value not float
        data = {"sensorid" : "TEMP:XX" , "value" : "50X" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post(url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value is string-float - OK
        data = {"sensorid" : "TEMP:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)

        #No location - fails
        data = {"sensorid" : "NO_LOC:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post( url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        
    def test_get(self):
        sensor_id = "TEMP:XX:%04d" % random.randint(0,9999)
        Sensor.objects.create( id = sensor_id,
                               parent_device = self.context.dev,
                               sensor_type = self.context.sensor_type_temp , 
                               description = "Measurement of ..")

        
        
        client = Client( )
        post_url = reverse( "sensor.api.post" )
        response = client.get( post_url )
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        get_url = reverse("sensor.api.get" , args = [sensor_id])
        response = client.get( get_url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : self.context.external_key}]

        for data in data_list:
            string_data = json.dumps( data )
            response = client.post( post_url , data = json.dumps( data ) , content_type = "application/json")
            self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)
        

        info_url = reverse( "sensor.api.info" , args = [ sensor_id ] )
        response = client.get( info_url )
        result = response.data
        self.assertEqual( result["last_value"] , 20 )
        self.assertEqual( TimeStamp.parse_datetime( result["last_timestamp"] ) , TimeStamp.parse_datetime("2015-10-10T12:14:00+01"))

        
        response = client.get( get_url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        self.assertEqual( 3 , len(result) )
        for res,d in zip(result , data_list):
            ts = TimeStamp.parse_datetime( d["timestamp"] )
            self.assertEqual( ts , res[0] )
            self.assertEqual( float(d["value"]) , res[1] )

        response = client.get( get_url , {"num" : 10})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        self.assertEqual( 3 , len(result) )
        for res,d in zip(result , data_list):
            ts = TimeStamp.parse_datetime( d["timestamp"] )
            self.assertEqual( ts , res[0] )
            self.assertEqual( float(d["value"]) , res[1] )


        response = client.get( get_url , {"num" : 1})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        self.assertEqual( 1 , len(result) )
        res = result[0]
        d = data_list[2]
        ts = TimeStamp.parse_datetime( d["timestamp"] )
        self.assertEqual( ts , res[0] )
        self.assertEqual( float(d["value"]) , res[1] )


        response = client.get( get_url , {"start" : "2015-10-10T12:11:00+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 3 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:11:59+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 3 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:12:30+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 2 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:13:30+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 1 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:14:30+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 0 , len(result) )


    def test_post_multiple(self):
        client = Client( )
        post_url = reverse( "sensor.api.post" )
        # Payload structure is invalid invalid - missing timestamp
        data = {"sensorid" : "TEMP:XX" , 
                "value_list" : [("2015-10-10T12:12:00+01" , 50), ("2015-10-10T12:13:00+01" , 60)],
                "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post( post_url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)


        # Value out of range
        data = {"sensorid" : "TEMP:XX" , "value" : 400, "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post(post_url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value not float
        data = {"sensorid" : "TEMP:XX" , "value" : "50X" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post(post_url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value is string-float - OK
        data = {"sensorid" : "TEMP:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post(post_url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)

        #No location - fails
        data = {"sensorid" : "NO_LOC:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key}
        string_data = json.dumps( data )
        response = client.post(post_url , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        
    def test_get(self):
        sensor_id = "TEMP:XX:%04d" % random.randint(0,9999)
        Sensor.objects.create( sensor_id = sensor_id,
                               parent_device = self.context.dev,
                               sensor_type = self.context.sensor_type_temp , 
                               description = "Measurement of ..")

        
        
        client = Client( )
        post_url = reverse( "sensor.api.post" )
        get_url = reverse( "sensor.api.get" , args = [sensor_id ])
        response = client.get( post_url )
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        response = client.get( get_url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : self.context.external_key}]

        for data in data_list:
            string_data = json.dumps( data )
            response = client.post(post_url , data = json.dumps( data ) , content_type = "application/json")
            self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)
        

        info_url = reverse("sensor.api.info" , args = [sensor_id])
        response = client.get( info_url )
        result = response.data
        self.assertEqual( result["last_value"] , 20 )
        self.assertEqual( TimeStamp.parse_datetime( result["last_timestamp"] ) , TimeStamp.parse_datetime("2015-10-10T12:14:00+01"))

        
        response = client.get( get_url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        self.assertEqual( 3 , len(result) )
        for res,d in zip(result , data_list):
            ts = TimeStamp.parse_datetime( d["timestamp"] )
            self.assertEqual( ts , res[0] )
            self.assertEqual( float(d["value"]) , res[1] )

        response = client.get( get_url , {"num" : 10})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        self.assertEqual( 3 , len(result) )
        for res,d in zip(result , data_list):
            ts = TimeStamp.parse_datetime( d["timestamp"] )
            self.assertEqual( ts , res[0] )
            self.assertEqual( float(d["value"]) , res[1] )


        response = client.get( get_url , {"num" : 1})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data

        self.assertEqual( 1 , len(result) )
        res = result[0]
        d = data_list[2]
        ts = TimeStamp.parse_datetime( d["timestamp"] )
        self.assertEqual( ts , res[0] )
        self.assertEqual( float(d["value"]) , res[1] )


        response = client.get( get_url , {"start" : "2015-10-10T12:11:00+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 3 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:11:59+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 3 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:12:30+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 2 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:13:30+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 1 , len(result) )

        response = client.get( get_url , {"start" : "2015-10-10T12:14:30+01"})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        self.assertEqual( 0 , len(result) )


