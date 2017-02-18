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
        sensor_id = self.context.temp_sensor.sensor_id

        # Missing value
        data = {"key" : self.context.external_key , "sensorid" : sensor_id , "timestamp" : "2015-10-10T12:12:00+01"}
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
        data = {"key" : self.context.external_key , "sensorid" : sensor_id , "timestamp" : "2015-10-10T12" , "value" : 100}
        self.assertFalse( RawData.is_valid( data ))
        self.assertEqual( RawData.error( data ) , "Error: invalid timestamp - expected: YYYY-MM-DDTHH:MM:SS+zz")
        with self.assertRaises( ValueError ):
            RawData.create( data )
            
        # Valid 
        data = {"key" : self.context.external_key , "sensorid" : sensor_id , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}
        self.assertTrue( RawData.is_valid( data ))
        self.assertTrue( RawData.error( data ) is None )
        rd = RawData.create( data )

        # Invalid sensor id
        settings.FORCE_VALID_SENSOR = True
        data = {"key" : self.context.external_key , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}
        self.assertFalse( RawData.is_valid( data ))
        with self.assertRaises(ValueError):
            rd = RawData.create( data )

        # Invalid key
        data = {"key" : "Invalid" , "sensorid" : sensor_id , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100}
        with self.assertRaises(ValueError):
            rd = RawData.create( data )

    def test_get_api(self):
        sensor_id = "TEMP:XX:%04d" % random.randint(0,9999)
        sensor = Sensor.objects.create( sensor_id = sensor_id,
                                        parent_device = self.context.dev,
                                        sensor_type = self.context.sensor_type_temp , 
                                        description = "Measurement of ..")

        client = Client( )
        
        # Invalid sensor -> 404
        response = client.get( reverse("sensor.api.rawdata" , args = ["missing"]))
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        # Invalid type -> 400
        
        url = reverse( "sensor.api.rawdata" , args = [sensor_id])
        response = client.get( url, {"status" : 199})
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        # Invalid type -> 400
        response = client.get(url , {"status" : "ABC"})
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        response = client.get(url , {"status" : 0 })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 0 )
        
        

        data_list = [{"sensorid" : sensor_id , "value" : "60", "timestamp" : "2015-10-10T12:12:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key},
                     {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : self.context.external_key}]

        for data in data_list:
            post_url = reverse("sensor.api.post")
            response = client.post( post_url , data = json.dumps( data ) , content_type = "application/json")
            self.assertEqual( response.status_code , status.HTTP_201_CREATED , response.data)

        
        response = client.get( url , {"status" : 0 })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        # Just use default status - status == 0
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        response = client.get(url , {"status" : 1 })
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )
        
        data = {"sensorid" : sensor_id , "value" : 20, "timestamp" : "2015-10-10T12:14:00+01", "key" : "InvalidKey"}
        response = client.post("/sensor/api/reading/" , data = json.dumps( data ) , content_type = "application/json")
        
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        sd = SampledData.updateRawData( sensor )
        self.assertEqual(len(sd) , 3)
        
        response = client.get( url , {"status" : RawData.VALID })
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        self.assertEqual( len(data) , 3 )

        sd = SampledData.updateRawData( sensor )
        self.assertEqual(len(sd) , 3)
        self.assertEqual( len(RawData.objects.filter( processed = True )) , 3)


    def test_ts(self):
        ts = RawData.get_ts( self.context.temp_sensor )
        self.assertEqual( len(ts) , 0 )

        sensor_id = self.context.temp_sensor.sensor_id
        for i in range(10):
            data = {"sensorid" : sensor_id , "value" : i, "timestamp" : "2015-10-10T12:13:%02d+01" % (30 - i), "key" : self.context.external_key}
            RawData.create( data )
            
        qs = RawData.objects.all()

        ts = RawData.get_ts( self.context.temp_sensor )
        self.assertEqual( len(ts) , 10 )
        for index,pair in enumerate(ts):
            self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:%02d+01" % (21 + index)))
            self.assertEqual( pair[1] , 9 - index )

            

        
        ts = RawData.get_ts( self.context.temp_sensor , num = 100)
        self.assertEqual( len(ts) , 10 )
        for index,pair in enumerate(ts):
            self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:%02d+01" % (21 + index)))
            self.assertEqual( pair[1] , 9 - index )

        ts = RawData.get_ts( self.context.temp_sensor , num = 2)
        self.assertEqual( len(ts) , 2 )
        pair = ts[0]
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:29+01" ))
        self.assertEqual( pair[1] , 1 )

        pair = ts[1]
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:30+01" ))
        self.assertEqual( pair[1] , 0 )

        # Illegal with both num and start
        with self.assertRaises(ValueError):
            ts = RawData.get_ts( self.context.temp_sensor , num = 2, start = TimeStamp.parse_datetime( "2015-10-10T12:13:09+01" ))
        # Illegal with both num and end
        with self.assertRaises(ValueError):
            ts = RawData.get_ts( self.context.temp_sensor , num = 2, end = TimeStamp.parse_datetime( "2015-10-10T12:13:09+01" ))

        ts = RawData.get_ts( self.context.temp_sensor , start = TimeStamp.parse_datetime( "2015-10-10T12:13:29+01" ))
        self.assertEqual( len(ts) , 2 )
        pair = ts[0]
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:29+01" ))
        self.assertEqual( pair[1] , 1 )

        pair = ts[1]
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:30+01" ))
        self.assertEqual( pair[1] , 0 )

        ts = RawData.get_ts( self.context.temp_sensor , start = TimeStamp.parse_datetime( "2015-11-10T12:13:08+01" ))
        self.assertEqual( len(ts) , 0 )

        ts = RawData.get_ts( self.context.temp_sensor , end = TimeStamp.parse_datetime( "2015-10-10T12:13:22+01" ))
        self.assertEqual( len(ts) , 2 )

        pair = ts[0]
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:21+01" ))
        self.assertEqual( pair[1] , 9 )

        pair = ts[1]
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:22+01" ))
        self.assertEqual( pair[1] , 8 )


        ts = RawData.get_ts( self.context.temp_sensor , 
                             start = TimeStamp.parse_datetime( "2015-10-10T12:13:24+01" ),
                             end = TimeStamp.parse_datetime( "2015-10-10T12:13:26+01" ))
        self.assertEqual( len(ts) , 3 )
        p0 = ts[0]
        p1 = ts[1]
        p2 = ts[2]
        self.assertEqual( p0[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:24+01" ))
        self.assertEqual( p1[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:25+01" ))
        self.assertEqual( p2[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:26+01" ))



    def test_create(self):
        sensor_id = self.context.temp_sensor.sensor_id
        data = {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}                
        data["value"] = "XXX"
        rd = RawData.create( data )
        self.assertEqual( rd[0].value , -1 )
        self.assertEqual( rd[0].string_value , "XXX" )
        self.assertEqual( rd[0].status , RawData.FORMAT_ERROR )

        data = {"sensorid" : sensor_id , "value" : 10, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}
        rd = RawData.create( data )
        self.assertEqual( rd[0].value , 10 )
        self.assertEqual( rd[0].string_value , None )
        self.assertEqual( rd[0].status , RawData.VALID )

        data = {"sensorid" : "Missing" , "value" : 150, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}
        with self.assertRaises(ValueError):
            rd = RawData.create( data )

        data = {"sensorid" : sensor_id , "value" : 150, "timestamp" : "2015-10-10T12:13:00+01", "key" : self.context.external_key}
        rd = RawData.create( data )
        self.assertEqual( rd[0].value , -1 )
        self.assertEqual( rd[0].string_value , "150" )
        self.assertEqual( rd[0].status , RawData.RANGE_ERROR )

        data = {"sensorid" : sensor_id , "value" : 15, "timestamp" : "2015-10-10T12:13:00+01", "key" : "InvalidKey" }
        with self.assertRaises(ValueError):
            rd = RawData.create( data )

        data = {"sensorid" : sensor_id , 
                "value_list" : [("2015-10-10T12:13:00+01", 10), ("2015-10-10T12:14:00+01", 20)],
                "key" : self.context.external_key }

        rd = RawData.create( data )
        self.assertEqual( len(rd) , 2)
        self.assertEqual( rd[0].value , 10 )
        self.assertEqual( rd[0].string_value , None )
        self.assertEqual( rd[0].status , RawData.VALID )

        self.assertEqual( rd[1].value , 20 )
        self.assertEqual( rd[1].string_value , None )
        self.assertEqual( rd[1].status , RawData.VALID )





    def test_vectors(self):
        (ts,values) = RawData.get_vectors( self.context.temp_sensor )
        self.assertEqual( len(ts) , 0 )
        self.assertEqual( len(values) , 0 )

        sensor_id = self.context.temp_sensor.sensor_id
        for i in range(10):
            data = {"sensorid" : sensor_id , "value" : i, "timestamp" : "2015-10-10T12:13:%02d+01" % i, "key" : self.context.external_key}
            RawData.create( data )
            
        qs = RawData.objects.all()

        ts,values = RawData.get_vectors( self.context.temp_sensor )
        self.assertEqual( len(ts) , 10 )
        self.assertEqual( len(values) , 10 )
        for index in range(len(ts)):
            pair = (ts[index] , values[index])
            self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:%02d+01" % index))
            self.assertEqual( pair[1] , index )
        
        ts,values = RawData.get_vectors( self.context.temp_sensor , num = 100)
        self.assertEqual( len(ts) , 10 )
        for index in range(len(ts)):
            pair = (ts[index] , values[index])
            self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:%02d+01" % index))
            self.assertEqual( pair[1] , index )

        ts,values = RawData.get_vectors( self.context.temp_sensor , num = 2)
        self.assertEqual( len(ts) , 2 )
        pair = (ts[0] , values[0])
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:08+01" ))
        self.assertEqual( pair[1] , 8 )

        pair = (ts[1] , values[1])
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:09+01" ))
        self.assertEqual( pair[1] , 9 )

        # Illegal with both num and start
        with self.assertRaises(ValueError):
            ts,values = RawData.get_vectors( self.context.temp_sensor , num = 2, start = TimeStamp.parse_datetime( "2015-10-10T12:13:09+01" ))

        ts,values = RawData.get_vectors( self.context.temp_sensor , start = TimeStamp.parse_datetime( "2015-10-10T12:13:08+01" ))
        self.assertEqual( len(ts) , 2 )
        pair = (ts[0] , values[0])
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:08+01" ))
        self.assertEqual( pair[1] , 8 )

        pair = (ts[1] , values[1])
        self.assertEqual( pair[0] , TimeStamp.parse_datetime( "2015-10-10T12:13:09+01" ))
        self.assertEqual( pair[1] , 9 )

        ts,values = RawData.get_vectors( self.context.temp_sensor , start = TimeStamp.parse_datetime( "2015-11-10T12:13:08+01" ))
        self.assertEqual( len(ts) , 0 )
