import random
import json

from django.utils import timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *
from .context import TestContext
        


class MeasurementTypeTest(TestCase):

    def setUp(self):
        MeasurementType.objects.create( name = "Temperature" )
        MeasurementType.objects.create( name = "Particles" )
        MeasurementType.objects.create( name = "Humidity" )

        
    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/measurement_type/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        response = client.get("/sensor/api/measurement_type/1/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertTrue( isinstance( data , dict ))
        self.assertEqual( data["id"] , 1 )
        self.assertEqual( data["name"] , "Temperature" )

        response = client.get("/sensor/api/measurement_type/9/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )



        

class DeviceTypeTest(TestCase):
    def setUp(self):
        DeviceType.objects.create( name = "HP-X12")
        DeviceType.objects.create( name = "TI123" )


    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/device_type/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 2 )
        
        dev0 = data[0]


class DeviceTest(TestCase):
    def setUp(self):
        test_context = TestContext( )
        dev_type = DeviceType.objects.create( name = "TI123" )
        self.loc = Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)
        self.post_key =  ApiKey.objects.create( description = "DeviceKey")
        self.dev = Device( device_type = dev_type , 
                           location = self.loc , 
                           description = "desc",
                           post_key = self.post_key ,
                           owner = test_context.user )


    def test_id_pattern(self):
        self.dev.id = "Invalid ID"
        with self.assertRaises(ValidationError):
             self.dev.full_clean()


    def test_get(self):
        self.dev.id = "Valid-ID"
        self.dev.save()
        client = Client( )
        response = client.get("/sensor/api/device/Valid-ID/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( data["description"] , "desc" )
        


class DataTypeTest(TestCase):
    def setUp(self):
        DataType.objects.create( id = "FILTEREDX" )
        
    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/data_type/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 3 )
        
        type_list = [ x["id"] for x in data ]
        self.assertTrue("TEST" in type_list)
        self.assertTrue("RAWDATA" in type_list)
        self.assertTrue("FILTEREDX" in type_list)




class LocationTest(TestCase):
    def setUp(self):
        Location.objects.create( name = "DanmarksPlass" , latitude = 100.0 , longitude = 60)
        Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)


    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/location/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 2 )
        
        loc0 = data[0]
        self.assertEqual( loc0["name"] , "DanmarksPlass" )
        self.assertEqual( loc0["latitude"] , 100.0 )
        self.assertTrue( loc0["altitude"] is None )
        

class SensorTypeTest(TestCase):
    def setUp(self):
        self.context = TestContext( )
    
    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/sensortype/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 1 )

        response = client.get("/sensor/api/sensortype/%d/" % self.context.sensor_type_temp.id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( data["max_value"] , self.context.sensor_type_temp.max_value )



class SensorTest(TestCase):
    def setUp(self):
        self.context = TestContext( )


    def test_valid_key(self):
        sensor = self.context.temp_sensor
        sensor.sensor_id = "Invalid id"
        with self.assertRaises(ValidationError):
            sensor.full_clean()

        sensor.sensor_id = "?=+/"
        with self.assertRaises(ValidationError):
            sensor.full_clean()
            
        sensor.sensor_id = "TEMP:XX_aa-23864"
        sensor.save( )
        sensor.full_clean()

        
        

    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/sensor/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 3 )

        response = client.get("/sensor/api/sensor/TEMP:XX/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )

        sensor0 = data
        self.assertEqual( sensor0["description"] , "tempm")








