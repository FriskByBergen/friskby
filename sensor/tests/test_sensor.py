import datetime
import pytz

from django.test import TestCase
from sensor.models import *
from .context import TestContext

class SensorTest(TestCase):
    def setUp(self):
        self.context = TestContext( )


    def test_validate(self):
        obj = Sensor.objects.get( pk = "TEMP:XX" )
        self.assertFalse( obj.valid_input(  -100  ))
        self.assertFalse( obj.valid_input(   200 ))
        self.assertFalse( obj.valid_input(   "XYZ"  ))

        self.assertTrue( obj.valid_input(  "50"  ))
        self.assertTrue( obj.valid_input(  50  ))
        
    

    def test_get_ts( self ):
        sensor = self.context.temp_sensor
        ts_input = []
        for i in range(10):
            ts = datetime.datetime.now( pytz.utc )
            ts_object = TimeStamp.objects.create( timestamp = ts )
            value = i
            ts_input.append( (ts , value) )

            data_info = DataInfo.objects.create( timestamp = ts_object , 
                                                 sensor = sensor )

            data_value = DataValue.objects.create( data_info = data_info ,
                                                   data_type = sensor.data_type ,  
                                                   value = value )

        ts = sensor.get_ts( )
        self.assertEqual(len(ts) , 10)
        self.assertEqual( ts , ts_input)

