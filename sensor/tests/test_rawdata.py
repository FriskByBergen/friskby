import random
from django.conf import settings
from django.utils import timezone,dateparse
from django.test import TestCase, Client
from rest_framework import status

from sensor.models import *
from filter.models import SampledData 

from .context import TestContext

class RawDataTest(TestCase):
    
    def setUp(self):
        self.context = TestContext( )
        

    def test_valid(self):
        self.assertFalse( RawData.is_valid( None ))
        self.assertEqual( RawData.error( None ) , "Error: empty payload")

        # Missing value
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01"}
        self.assertFalse( RawData.is_valid( data ))
        self.assertEqual( RawData.error( data ) , "Error: missing fields in payload: ['value']")

        # Missing key and sensorid
        data = {"timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}
        self.assertFalse( RawData.is_valid( data ))
        self.assertEqual( RawData.error( data ) , "Error: missing fields in payload: ['key', 'sensorid']")

        # Missing key, sensorid and value
        data = {"timestamp" : "2015-10-10T12:12:00+01"}
        self.assertFalse( RawData.is_valid( data ))
        self.assertEqual( RawData.error( data ) , "Error: missing fields in payload: ['key', 'sensorid', 'value']")
        
        # Invalid timestamp
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12" , "value" : 100}
        self.assertFalse( RawData.is_valid( data ))
        self.assertEqual( RawData.error( data ) , "Error: invalid timestamp - expected: YYYY-MM-DDTHH:MM:SS+zz")
        with self.assertRaises( ValueError ):
            RawData.create( data )
            
        # Valid 
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}
        self.assertTrue( RawData.is_valid( data ))
        self.assertTrue( RawData.error( data ) is None )
        rd = RawData.create( data )
        self.assertEqual( False , rd.parsed )

        #Force recognized sensor
        tmp = settings.FORCE_VALID_SENSOR
        settings.FORCE_VALID_SENSOR = True
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}
        self.assertFalse( RawData.is_valid( data ))

        settings.FORCE_VALID_SENSOR = False
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}
        self.assertTrue( RawData.is_valid( data ))
        rd = RawData.create( data )
        self.assertEqual( rd.status , RawData.INVALID_SENSOR )
        self.assertEqual( rd.value , -1 )
        self.assertEqual( rd.string_value , "100")

        # Valid 
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100 }
        rd = RawData.create( data )
        
        # Force recognized key:
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}

        try:
            tmp = settings.FORCE_VALID_KEY
            settings.FORCE_VALID_KEY = True
            with self.assertRaises( ValueError ):
                RawData.create( data )
            self.assertEqual( RawData.error( data ) , "Error: invalid key")
        finally:
            settings.FORCE_VALID_KEY = False

        try:
            data["key"] = self.context.external_key
            tmp = settings.FORCE_VALID_KEY
            settings.FORCE_VALID_KEY = True
            rd = RawData.create( data )
        finally:
            settings.FORCE_VALID_KEY = False


    def test_get_api(self):
        sensor_id = "TEMP:XX:%04d" % random.randint(0,9999)
        sensor = Sensor.objects.create( id = sensor_id,
                                        post_key = self.context.key , 
                                        location = self.context.loc,
                                        parent_device = self.context.dev,
                                        sensor_type = self.context.sensor_type_temp , 
                                        description = "Measurement of ..")

        client = Client( )

        # Sensor missing -> 404
        response = client.get("/sensor/api/rawdata/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        # Invalid sensor -> 404
        response = client.get("/sensor/api/rawdata/missing/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        # Invalid type -> 400
        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : 199})
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        # Invalid type -> 400
        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : "ABC"})
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : 0 })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 0 )
        
        

        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : self.context.external_key}]

        for data in data_list:
            response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
            self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)

        
        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : 0 })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        # Just use default status - status == 0
        response = client.get("/sensor/api/rawdata/%s/" % sensor_id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : 1 })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 0 )
        
        data = {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : "InvalidKey"}
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        
        response = client.get("/sensor/api/rawdata/%s/" % sensor_id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : RawData.INVALID_KEY})
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 1 )

        sd = SampledData.updateRawData( sensor )
        self.assertEqual(len(sd) , 3)
        
        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : RawData.RAWDATA })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 0 )

        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : RawData.PROCESSED })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        sd = SampledData.updateRawData( sensor )
        self.assertEqual(len(sd) , 3)
        
        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : RawData.RAWDATA })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 0 )

        response = client.get("/sensor/api/rawdata/%s/" % sensor_id , {"status" : RawData.PROCESSED })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )


    def test_create(self):
        sensor_id = self.context.temp_sensor.id
        data = {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}                
        data["value"] = "XXX"
        rd = RawData.create( data )
        self.assertEqual( rd.value , -1 )
        self.assertEqual( rd.string_value , "XXX" )
        self.assertEqual( rd.status , RawData.FORMAT_ERROR )

        data = {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}
        rd = RawData.create( data )
        self.assertEqual( rd.value , 10 )
        self.assertEqual( rd.string_value , None )
        self.assertEqual( rd.status , RawData.RAWDATA )

        data = {"sensorid" : "Missing" , "value" : 150, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}
        rd = RawData.create( data )
        self.assertEqual( rd.value , -1 )
        self.assertEqual( rd.string_value , "150" )
        self.assertEqual( rd.status , RawData.INVALID_SENSOR )

        data = {"sensorid" : sensor_id , "value" : 150, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}
        rd = RawData.create( data )
        self.assertEqual( rd.value , -1 )
        self.assertEqual( rd.string_value , "150" )
        self.assertEqual( rd.status , RawData.RANGE_ERROR )

        data = {"sensorid" : sensor_id , "value" : 15, "timestamp" : "2015-10-10T12:13:00+01", "key" : "InvalidKey" }
        rd = RawData.create( data )
        self.assertEqual( rd.value , 15 )
        self.assertEqual( rd.string_value , None )
        self.assertEqual( rd.status , RawData.INVALID_KEY )

        
