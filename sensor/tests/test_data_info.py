from django.utils import timezone,dateparse
from django.test import TestCase
from sensor.models import *


class DataInfoTest(TestCase):

    def setUp(self):
        company = Company(name = "Texas Instrument")
        company.save()

        device_type = DeviceType(name = "Integrated temp/hum sensor:H1562")
        device_type.company = company
        device_type.save()

        mtype = MeasurementType( name = "Temperature" )
        mtype.save()

        self.sensor = SensorID.objects.create( id = "TEMP", 
                                               measurement_type = mtype , 
                                               description = "Temparture", 
                                               unit = "Celcius", 
                                               min_value = -10 , 
                                               max_value = 100 , 
                                               parent_device = device_type)

        self.location = Location.objects.create( name = "Location" , 
                                                 latitude = 1000,
                                                 longitude = 50,
                                                 altitude = 10 )
                                                 
        self.timestamp = TimeStamp.objects.create( timestamp = TimeStamp.parse_datetime("2015-10-10T10:10:00+01"))
        

    def test_create(self):
        date_info = DataInfo.objects.create( sensor = self.sensor , 
                                             location = self.location,
                                             timestamp = self.timestamp )
        
