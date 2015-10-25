from django.test import TestCase
from sensor.models import *


class SensorIDTest(TestCase):
    def setUp(self):
        company = Company(name = "Texas Instrument")
        company.save()

        device_type = DeviceType(name = "Integrated temp/hum sensor:H1562")
        device_type.company = company
        device_type.save()

        mtype = MeasurementType( name = "Temperature" )
        mtype.save()

        SensorID.objects.create( id = "TEMP", 
                                 measurement_type = mtype , 
                                 description = "Temparture", 
                                 unit = "Celcius", 
                                 min_value = -10 , 
                                 max_value = 100 , 
                                 parent_device = device_type)
        

    def test_create(self):
        test_state = DataType.objects.get( pk = "TEST" )
        obj = SensorID.objects.get( pk = "TEMP")
        self.assertEqual( obj.id , "TEMP")
        self.assertEqual( obj.data_type , test_state )
        

    def test_validate(self):
        obj = SensorID.objects.get( pk = "TEMP" )
        self.assertFalse( obj.valid_input(  -100  ))
        self.assertFalse( obj.valid_input(   200 ))
        self.assertFalse( obj.valid_input(   "XYZ"  ))

        self.assertTrue( obj.valid_input(  "50"  ))
        self.assertTrue( obj.valid_input(  50  ))
        
        
