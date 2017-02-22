import sys
import random

from django.core.management.base import BaseCommand, CommandError
from api_key.models import *
from sensor.models import *
from ._sample import sample


def random_location(name):
    locations = Location.objects.all()
    altitude = 0
    SW = (60.37 , 5.36) 
    NE = (60.45 , 5.40)
    latitude  = SW[0] + random.random() * (NE[0] - SW[0])
    longitude = SW[1] + random.random() * (NE[1] - SW[1])
    
    loc = Location.objects.create( name = name , latitude = latitude , longitude = longitude , altitude = altitude)
    return loc


class Command(BaseCommand):
    help = """Will create devices and sensors. The devices you wish to add should
    be given as commandline arguments. By default the script will
    generate 100 random points for each sensor, but by passing the
    option --num you can ask for a different number.  """


    def add_arguments(self, parser):
        parser.add_argument('--num' , default = 100, type=int)
        parser.add_argument('device' , nargs = '+')


    def add_device( self, device_id , owner , num):
        try:
            Device.objects.get( pk = device_id )
            sys.stdout.write("Device %s already exists \n" % device_id)
            return
        except Device.DoesNotExist:
            pass

        sys.stdout.write("Adding device %s ... \n" % device_id)
        key = ApiKey.objects.create( description = "Newkey")
        loc = random_location(device_id)
        dev_type = DeviceType.objects.create( name = "HP-X123" )
        dev = Device.objects.create( id = device_id , 
                                     location = loc , 
                                     device_type = dev_type , 
                                     description = "Description",
                                     post_key = key,
                                     owner = owner )
        
        try:
            mtype_PM10 = MeasurementType.objects.get( name = "PM10" )
        except MeasurementType.DoesNotExist:
            mtype_PM10 = MeasurementType.objects.create( name = "PM10" )


        sensor_type_PM10 = SensorType.objects.create( product_name = "XX12762 Turbo",
                                                      measurement_type = mtype_PM10,
                                                      short_description = "Temp",
                                                      description = "Measurement of temperature",
                                                      unit = "Degree celcius",
                                                      min_value = -1000,
                                                      max_value = 1000)

        try:
            mtype_PM25 = MeasurementType.objects.get( name = "PM25" )
        except MeasurementType.DoesNotExist:
            mtype_PM25 = MeasurementType.objects.create( name = "PM25" )

        sensor_type_PM25 = SensorType.objects.create( product_name = "XX12762 Turbo",
                                                      measurement_type = mtype_PM25,
                                                      short_description = "Temp",
                                                      description = "Measurement of temperature",
                                                      unit = "Degree celcius",
                                                      min_value = -1000,
                                                      max_value = 1000)
        
        raw_data = DataType.objects.get( pk = "RAWDATA" )
        sensor_PM10 = Sensor.objects.create( sensor_id = "%s_PM10" % device_id , 
                                             description = "PM10",
                                             data_type = raw_data , 
                                             parent_device = dev,
                                             sensor_type = sensor_type_PM10 )

        sensor_PM25 = Sensor.objects.create( sensor_id = "%s_PM25" % device_id , 
                                             description = "PM25",
                                             data_type = raw_data , 
                                             parent_device = dev,
                                             sensor_type = sensor_type_PM25 )
        
        if num > 0:
            sys.stdout.write("Sampling %d random measurements for:%s\n" % (num , device_id))
            for sensor in dev.sensorList():
                sample( sensor , num )


    
    def handle(self, *args, **options):
        try:
            owner = User.objects.get( username = "friskby")
        except User.DoesNotExist:
            owner = User.objects.create_superuser( "friskby" , "friskby@invalid.com" , "friskby" )
        
        num = int(options["num"])
        for dev_id in options["device"]:
            self.add_device(dev_id , owner, num)
        
        
