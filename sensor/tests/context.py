import requests
import sys 

from django.conf import settings
from django.contrib.auth.models import User 
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from git_version.models import * 
from api_key.models import *
from sensor.models import *

class TestContext(object):
    def __init__(self):
        self.git_version = GitVersion.objects.create( ref = "master" , repo = "uri://git.no" , description = "description" , follow_head = True)
        self.key = ApiKey.objects.create( description = "Newkey")
        self.external_key = str(self.key.external_key)
        self.loc = Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)
        self.dev_type = DeviceType.objects.create( name = "HP-X123" )
        self.user = User.objects.create_user( "test-user" )
        self.dev = Device.objects.create( id = "DevXYZ" , 
                                          location = self.loc , 
                                          device_type = self.dev_type , 
                                          description = "Besrkivels",
                                          post_key = self.key,
                                          owner = self.user )

        self.dev_loc0 = Device.objects.create( id = "DevNoLoc" , 
                                               device_type = self.dev_type , 
                                               description = "Besrkivels",
                                               owner = self.user,
                                               post_key = self.key )

        self.mtype = MeasurementType.objects.create( name = "Temperature" )
        self.raw_data = DataType.objects.get( pk = "RAWDATA" )
        self.test_data = DataType.objects.get( pk = "TEST" )

        self.sensor_type_temp = SensorType.objects.create( product_name = "XX12762 Turbo",
                                                           measurement_type = self.mtype,
                                                           short_description = "Temp",
                                                           description = "Measurement of temperature",
                                                           unit = "Degree celcius",
                                                           min_value = 0,
                                                           max_value = 100)
        
        self.temp_sensor = Sensor.objects.create( id = "TEMP:XX",
                                                  parent_device = self.dev,
                                                  description = "tempm",
                                                  sensor_type = self.sensor_type_temp)
        
        self.hum_sensor = Sensor.objects.create( id = "HUM:XX",
                                                 description = "Measurement humidity",
                                                 data_type = self.raw_data ,
                                                 parent_device = self.dev,
                                                 sensor_type = self.sensor_type_temp)

        self.loc0_sensor = Sensor.objects.create( id = "NO_LOC:XX",
                                                 description = "Measurement humidity",
                                                 data_type = self.raw_data ,
                                                 parent_device = self.dev_loc0,
                                                 sensor_type = self.sensor_type_temp)


        self.test_user_passwd = get_random_string( length = 10 ),
        self.test_user = User.objects.create_user( get_random_string( length = 10 ),
                                                   password = self.test_user_passwd , 
                                                   email = "joe@invalid.email.com" )

        try:
            response = requests.get("https://github.com/")
            self.network = True
        except Exception:
            self.network = False
            settings.RESTDB_IO_URL = None
            sys.stderr.write("** WARNING: No network connection - skipping post to restdb.io\n")
        
