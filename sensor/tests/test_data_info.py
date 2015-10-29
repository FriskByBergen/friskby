from django.utils import timezone,dateparse
from django.test import TestCase
from sensor.models import *

from .context import TestContext

class DataInfoTest(TestCase):
    
    def setUp(self):
        self.context = TestContext( )
        company = Company(name = "Texas Instrument")
        company.save()

        device_type = DeviceType(name = "Integrated temp/hum sensor:H1562")
        device_type.company = company
        device_type.save()

        device = Device.objects.create( id = "ID",
                                        device_type = device_type ,
                                        description = "Besk")

        mtype = MeasurementType( name = "Temperature" )
        mtype.save()

        self.sensor = Sensor.objects.create( id = "TEMP", 
                                             sensor_type = self.context.sensor_type_temp,
                                             description = "Temparture", 
                                             parent_device = device)

        self.location = Location.objects.create( name = "Location" , 
                                                 latitude = 1000,
                                                 longitude = 50,
                                                 altitude = 10 )
                                                 
        self.timestamp = TimeStamp.objects.create( timestamp = TimeStamp.parse_datetime("2015-10-10T10:10:00+01"))
        

    def test_create(self):
        date_info = DataInfo.objects.create( sensor = self.sensor , 
                                             location = self.location,
                                             timestamp = self.timestamp )
        
