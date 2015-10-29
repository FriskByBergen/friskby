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
        response = client.get("/sensor/api/device_type/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 2 )
        
        dev0 = data[0]
        self.assertEqual( dev0["company"] , self.hp.id )


class DeviceTest(TestCase):
    def setUp(self):
        ti = Company.objects.create( name = "Texas Instrument" )
        dev_type = DeviceType.objects.create( name = "TI123" , company = ti )
        self.loc = Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)
        self.dev = Device( device_type = dev_type , 
                           location = self.loc , 
                           description = "desc")


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
        sensor.id = "Invalid id"
        with self.assertRaises(ValidationError):
            sensor.full_clean()

        sensor.id = "?=+/"
        with self.assertRaises(ValidationError):
            sensor.full_clean()
            
        sensor.id = "TEMP:XX_aa-23864"
        sensor.save( )
        sensor.full_clean()

        
        

    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/sensor/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 2 )

        response = client.get("/sensor/api/sensor/TEMP:XX/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads( response.content )

        sensor0 = data
        self.assertEqual( sensor0["description"] , "tempm")



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
        self.assertEqual( sensor0["data_type"] , "TEST" )
        loc = sensor0["location"]
        self.assertEqual( loc , {"id" : 1 , "name" : "Ulriken" , "latitude" : 200 , "longitude" : 120 , "altitude" : 600})

        dev = sensor0["parent_device"]
        #self.assertEqual( dev , {"id" : 1 , "name" : "HP-X123" , "company" : {"id" : 1 , "name" : "Hewlett Packard"} } )

        sensor_type = sensor0["sensor_type"]
        self.assertEqual( sensor_type["product_name"] , "XX12762 Turbo" ) 
        
        self.assertEqual( sensor_type["min_value"] , 0 )
        self.assertEqual( sensor_type["max_value"] , 100 )


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
        #self.assertEqual( dev , {"id" : 1 , "name" : "HP-X123" , "company" : {"id" : 1 , "name" : "Hewlett Packard"} } )

        sensor_type = sensor0["sensor_type"]
        self.assertEqual( sensor_type["measurement_type"] , {"id" : 1 , "name" : "Temperature"} ) 
        self.assertEqual( sensor_type["min_value"] , 0 )
        self.assertEqual( sensor_type["max_value"] , 100 )

        
        response = client.get("/sensor/api/sensorinfo/HUM:XX/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        sensor0 = response.data
        self.assertEqual( sensor0["data_type"] , "RAWDATA" )



class DataInfoTest(TestCase):
    def setUp(self):
        self.context = TestContext()
        

    def test_get(self):
        client = Client( )
        response = client.get("/sensor/api/datainfo/")
        self.assertEqual( response.status_code , status.HTTP_200_OK , response.data)
        info_list = response.data
        self.assertEqual( len(info_list) , 2 )


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
        data = {"sensorid" : "TEMP:XX" , "value" : 50}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)


        # SensorID is invalid
        data = {"sensorid" : "TempXX" , "value" : 50 , "timestamp" : "2015-10-10T12:12:00+01"}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND , response.data)

        # Value out of range
        data = {"sensorid" : "TEMP:XX" , "value" : 400, "timestamp" : "2015-10-10T12:12:00+01"}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value not float
        data = {"sensorid" : "TEMP:XX" , "value" : "50X" , "timestamp" : "2015-10-10T12:12:00+01"}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST , response.data)

        # Value is string-float - OK
        data = {"sensorid" : "TEMP:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01"}
        string_data = json.dumps( data )
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)

        #No location - fails
        data = {"sensorid" : "HUM:XX" , "value" : "50" , "timestamp" : "2015-10-10T12:12:00+01"}
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

        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01"},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:12:00+01"},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:12:00+01"}]

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
