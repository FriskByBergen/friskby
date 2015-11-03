from django.conf import settings

from django.utils import timezone,dateparse
from django.test import TestCase
from sensor.models import *

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
        self.assertTrue( rd.extra_data is None )

        # Valid 
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100 , "extra_key" : "extra_value"}
        rd = RawData.create( data )
        extra_data = json.loads( rd.extra_data )
        self.assertEqual( extra_data , {"extra_key" : "extra_value"} )
        
        # Force recognized key:
        data = {"key" : "123" , "sensorid" : "ggg" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100 , "extra_key" : "extra_value"}

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
