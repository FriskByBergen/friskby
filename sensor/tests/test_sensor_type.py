from django.test import TestCase
from sensor.models import *


class SensorTypeTest(TestCase):
    def setUp(self):
        company = Company(name = "Texas Instrument")
        company.save()

        device_type = DeviceType(name = "Integrated temp/hum sensor:H1562")
        device_type.company = company
        device_type.save()

        mtype = MeasurementType( name = "Temperature" )
        mtype.save()

        self.sensor_type = SensorType.objects.create( measurement_type = mtype , 
                                                      short_description = "Temp",
                                                      description = "Temparture", 
                                                      unit = "Celcius", 
                                                      min_value = -10 , 
                                                      max_value = 100 , 
                                                      parent_device = device_type)
        

    def test_validate(self):
        self.assertFalse( self.sensor_type.valid_input(  -100  ))
        self.assertFalse( self.sensor_type.valid_input(   200 ))
        self.assertFalse( self.sensor_type.valid_input(   "XYZ"  ))
        
        self.assertTrue( self.sensor_type.valid_input(  "50"  ))
        self.assertTrue( self.sensor_type.valid_input(  50  ))
        
        
