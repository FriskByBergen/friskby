from django.test import TestCase
from sensor.models import *


class DeviceTypeTest(TestCase):

    def setUp(self):
        pass
        

    def test_valid_input(self):
        sensor_company = Company(name = "Texas")
        sensor_company.save()

        device_type = DeviceType(name = "SensorName" , 
                                 company = sensor_company)
        device_type.save()
        
        mtype_temp = MeasurementType( name = "Temperature" )
        mtype_temp.save()

        mtype_hum = MeasurementType( name = "Humidity" )
        mtype_hum.save()

        
        temp = Sensor( id = "temp", 
                       measurement_type = mtype_temp , 
                       description = "Temp / Hum", 
                       unit = "Celcius", 
                       min_value = -10 , 
                       max_value = 100 , 
                       parent_device = device_type)

        hum  = Sensor( id = "hum" , 
                       measurement_type = mtype_hum , 
                       description = "Temp / Hum", 
                       unit = "Celcius", 
                       min_value = -10 , 
                       max_value = 100 , 
                       parent_device = device_type)
        
        temp.save()
        hum.save()

        
        
