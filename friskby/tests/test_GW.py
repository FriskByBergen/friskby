import requests
import os
import sys
from unittest import TestCase
from django.conf import settings

try:
    from friskby_gw import FriskByGW
except ImportError:
    path = os.path.join( settings.BASE_DIR , "GW")
    sys.path.insert( 0 , path )
    from friskby_gw import FriskByGW , FriskBySensor
    sys.path.pop(0)


try:
    response = requests.get("https://github.com")
    network = True
except Exception:
    network = False


class GWTest(TestCase):
    def setUp(self):
        pass


    def test_get_sensors(self):
        if network == False:
            sys.stderr.write("Sorry - no network connection - skipping GW tests\n")
            return

        gw = FriskByGW( )
        sensors = gw.sensorList()
        for sensor in sensors:
            self.assertTrue( isinstance( sensor , FriskBySensor ))
            
        if len(sensors) > 0:
            sensor = sensors[0]

        try:
            last_value = sensor.getLastValue( )
        except Exception:
            pass
        

        
    def test_get_sensor(self):
        if network == False:
            sys.stderr.write("Sorry - no network connection - skipping GW tests\n")
            return

        gw = FriskByGW( )
        sensor = gw.getSensor( "NO/does/not/exist")
        self.assertIsNone( sensor )
        
