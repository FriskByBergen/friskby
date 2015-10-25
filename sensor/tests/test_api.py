import random
import json

from django.utils import timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *

class TestContext(object):
    def __init__(self):
        self.loc = Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)
        self.hp = Company.objects.create( name = "Hewlett Packard" )
        self.dev = DeviceType.objects.create( name = "HP-X123" , company = self.hp)
        self.mtype = MeasurementType.objects.create( name = "Temperature" )
        self.raw_data = DataType.objects.get( pk = "RAWDATA" )

        self.temp_sensor = SensorID.objects.create( id = "TEMP:XX",
                                                    location = self.loc,
                                                    parent_device = self.dev,
                                                    measurement_type = self.mtype,
                                                    description = "Measurement of temperature",
                                                    unit = "Degree celcius",
                                                    min_value = 0,
                                                    max_value = 100)

        self.hum_sensor = SensorID.objects.create( id = "HUM:XX",
                                                   parent_device = self.dev,
                                                   measurement_type = self.mtype,
                                                   description = "Measurement humidity",
                                                   unit = "Percent humidity",
                                                   min_value = 0,
                                                   max_value = 100,
                                                   data_type = self.raw_data )
        



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



class CompanyTest(TestCase):
    def setUp(self):
        Company.objects.create( name = "Texas Instruments" )
        Company.objects.create( name = "Hewlett Packard" )


    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/company/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 2 )

        response = client.get("/sensor/api/company/9/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
        
        response = client.get("/sensor/api/company/2/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertTrue( isinstance( data , dict ))
        self.assertEqual( data["id"] , 2 )
        self.assertEqual( data["name"] , "Hewlett Packard" )
        

class DeviceTypeTest(TestCase):
    def setUp(self):
        self.ti = Company.objects.create( name = "Texas Instrument" )
        self.hp = Company.objects.create( name = "Hewlett Packard" )

        DeviceType.objects.create( name = "HP-X12" , company = self.hp )
        DeviceType.objects.create( name = "TI123" , company = self.ti )


    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/device/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 2 )
        
        dev0 = data[0]
        self.assertEqual( dev0["company"] , self.hp.id )


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


class TimeStampTest(TestCase):

    def setUp(self):
        TimeStamp.objects.create( timestamp = timezone.now() )
        TimeStamp.objects.create( timestamp = timezone.now() )
        TimeStamp.objects.create( timestamp = timezone.now() )

        
    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/timestamp/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 3 )



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
        



class SensorIDTest(TestCase):
    def setUp(self):
        loc = Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)
        hp = Company.objects.create( name = "Hewlett Packard" )
        dev = DeviceType.objects.create( name = "HP-X123" , company = hp)
        mtype = MeasurementType.objects.create( name = "Temperature" )
        
        self.sensor = SensorID.objects.create( id = "TEMP:XX",
                                               location = loc,
                                               parent_device = dev,
                                               measurement_type = mtype,
                                               description = "Measurement of ..",
                                               unit = "Degree celcius",
                                               min_value = 0,
                                               max_value = 100)
        

    def test_valid_key(self):
        self.sensor.id = "Invalid id"
        with self.assertRaises(ValidationError):
            self.sensor.full_clean()

        self.sensor.id = "?=+/"
        with self.assertRaises(ValidationError):
            self.sensor.full_clean()
            
        self.sensor.id = "TEMP:XX_aa-23864"
        self.sensor.full_clean()

        
        

    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/sensorID/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 1 )

        response = client.get("/sensor/api/sensorID/TEMP:XX/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )

        sensor0 = data
        self.assertEqual( sensor0["min_value"] , 0 )
        self.assertEqual( sensor0["max_value"] , 100 )



class SensorInfoTest(TestCase):
    def setUp(self):
        self.context = TestContext()

    def test_get_list(self):
        client = Client( )

        # Missing data
        response = client.get("/sensor/api/sensorinfo/")
        self.assertEqual( response.status_code , status.HTTP_200_OK , response.data)
        sensor_list = response.data
        sensor0 = sensor_list[0]
        loc = sensor0["location"]
        self.assertEqual( loc , {"id" : 1 , "name" : "Ulriken" , "latitude" : 200 , "longitude" : 120 , "altitude" : 600})

        dev = sensor0["parent_device"]
        self.assertEqual( dev , {"id" : 1 , "name" : "HP-X123" , "company" : {"id" : 1 , "name" : "Hewlett Packard"} } )

        mtype = sensor0["measurement_type"]
        self.assertEqual( mtype , {"id" : 1 , "name" : "Temperature"} ) 
        
        self.assertEqual( sensor0["min_value"] , 0 )
        self.assertEqual( sensor0["max_value"] , 100 )
        self.assertEqual( sensor0["data_type"] , "TEST" )


    def test_get(self):
        client = Client( )

        response = client.get("/sensor/api/sensorinfo/XYZ/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        response = client.get("/sensor/api/sensorinfo/TEMP:XX/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        sensor0 = response.data
        loc = sensor0["location"]
        self.assertEqual( loc , {"id" : 1 , "name" : "Ulriken" , "latitude" : 200 , "longitude" : 120 , "altitude" : 600})

        dev = sensor0["parent_device"]
        self.assertEqual( dev , {"id" : 1 , "name" : "HP-X123" , "company" : {"id" : 1 , "name" : "Hewlett Packard"} } )

        mtype = sensor0["measurement_type"]
        self.assertEqual( mtype , {"id" : 1 , "name" : "Temperature"} ) 
        
        self.assertEqual( sensor0["min_value"] , 0 )
        self.assertEqual( sensor0["max_value"] , 100 )


        response = client.get("/sensor/api/sensorinfo/HUM:XX/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        sensor0 = response.data
        self.assertEqual( sensor0["data_type"] , "RAWDATA" )



class Readingtest(TestCase):
    def setUp(self):
        self.context = TestContext()
    
    
    def test_post(self):
        client = Client( )

        # Missing data
        response = client.post("/sensor/api/reading/")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)
        
        # Payload is not valid json
        response = client.post("/sensor/api/reading/" , data = "Not valid json" , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # Payload structure is invalid - missing timestamp
        data = [{"sensorid" : "TEMP:XX" , "value" : 50}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # SensorID is invalid
        data = [{"sensorid" : "TempXX" , "value" : 50 , "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND , response.data)

        # Value out of range
        data = [{"sensorid" : "TEMP:XX" , "value" : 400, "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value not float
        data = [{"sensorid" : "TEMP:XX" , "value" : "50X" , "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # A list of several readings - error in one.
        data = [{"sensorid" : "TEMP:XX" , "value" : 50 , "timestamp" : "10-10-2015 12:12:00"},
                {"sensorid" : "TEMP:XX" , "value" : 60 , "timestamp" : "10-10-2015 12:12:00"},
                {"sensorid" : "TEMP:XX" , "value" : 160 , "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # Value is string-float - OK
        data = [{"sensorid" : "TEMP:XX" , "value" : "50" , "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)
        self.assertEqual( response.data , 1)


        #List of reading - return value == len(list)
        data = [{"sensorid" : "TEMP:XX" , "value" : "60", "timestamp" : "10-10-2015 12:12:00"},
                {"sensorid" : "TEMP:XX" , "value" : 10, "timestamp" : "10-10-2015 12:12:00"},
                {"sensorid" : "TEMP:XX" , "value" : 20, "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)
        self.assertEqual( response.data , 3)

        #No location - fails
        data = [{"sensorid" : "HUM:XX" , "value" : "50" , "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        
    def test_get(self):
        # The funny construction with a random sensorID is to work
        # around a bug/limitation/misunderstanding in the restdb.io
        # api which seems to cap the return at 100 elements?
        sensor_id = "TEMP:XX:%04d" % random.randint(0,9999)
        SensorID.objects.create( id = sensor_id,
                                 location = self.context.loc,
                                 parent_device = self.context.dev,
                                 measurement_type = self.context.mtype,
                                 description = "Measurement of ..",
                                 unit = "Degree celcius",
                                 min_value = 0,
                                 max_value = 100)
        
        
        client = Client( )
        response = client.get("/sensor/api/reading/")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        response = client.get("/sensor/api/reading/%s/" % sensor_id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        len1 = len(result)

        data = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "10-10-2015 12:12:00"},
                {"sensorid" : sensor_id , "value" : 10, "timestamp" : "10-10-2015 12:12:00"},
                {"sensorid" : sensor_id , "value" : 20, "timestamp" : "10-10-2015 12:12:00"}]
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)
        self.assertEqual( response.data , 3)

        
        response = client.get("/sensor/api/reading/%s/" % sensor_id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        result = response.data
        len2 = len(result)        

        self.assertEqual( 3 , len2 - len1 )
        
        response = client.get("/sensor/api/reading/%s/" % sensor_id , )
