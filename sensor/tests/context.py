import requests

from django.conf import settings
from django.contrib.auth.models import User 
from django.utils.crypto import get_random_string

from api_key.models import *
from sensor.models import *

class TestContext(object):
    def __init__(self):
        self.key = ApiKey.objects.create( description = "Newkey")
        self.external_key = str(self.key.external_key)
        self.loc = Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)
        self.dev_type = DeviceType.objects.create( name = "HP-X123" )
        self.dev = Device.objects.create( id = "DevXXX" , location = self.loc , device_type = self.dev_type , description = "Besrkivels")
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
                                                  location = self.loc,
                                                  parent_device = self.dev,
                                                  description = "tempm",
                                                  post_key = self.key,
                                                  sensor_type = self.sensor_type_temp)

        self.hum_sensor = Sensor.objects.create( id = "HUM:XX",
                                                 description = "Measurement humidity",
                                                 data_type = self.raw_data ,
                                                 parent_device = self.dev,
                                                 post_key = self.key,
                                                 sensor_type = self.sensor_type_temp)

        self.ts = TimeStamp.objects.create( timestamp = TimeStamp.parse_datetime("2015-10-10T10:10:00+01") )
        self.data_info1 = DataInfo.objects.create( timestamp = self.ts, 
                                                   location = self.loc,
                                                   sensor = self.hum_sensor )

        self.data_info2 = DataInfo.objects.create( timestamp = self.ts, 
                                                   sensor = self.temp_sensor )

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
        
