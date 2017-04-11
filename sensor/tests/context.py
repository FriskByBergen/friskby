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
        self.channel = "stable"
        self.user_passwd = get_random_string( length = 10 ),
        self.user = User.objects.create_user( get_random_string( length = 10 ),
                                              password = self.user_passwd ,
                                              first_name = "First",
                                              last_name = "Last",
                                              email = "joe@example.org" )

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

        self.mtype_temp = MeasurementType.objects.create( name = "Temperature" )
        self.mtype_hum = MeasurementType.objects.create( name = "Hum" )
        self.mtype_pressure = MeasurementType.objects.create( name = "Press" )
        self.raw_data = DataType.objects.get( pk = "RAWDATA" )
        self.test_data = DataType.objects.get( pk = "TEST" )

        self.sensor_type_temp = SensorType.objects.create( product_name = "XX12762 Turbo",
                                                           measurement_type = self.mtype_temp,
                                                           short_description = "Temp",
                                                           description = "Measurement of temperature",
                                                           unit = "Degree celcius",
                                                           min_value = 0,
                                                           max_value = 100)

        self.sensor_type_hum = SensorType.objects.create( product_name = "XX12762 Turbo",
                                                          measurement_type = self.mtype_hum,
                                                          short_description = "Temp",
                                                          description = "Measurement of temperature",
                                                          unit = "Degree celcius",
                                                          min_value = 0,
                                                          max_value = 100)


        self.sensor_type_pressure = SensorType.objects.create( product_name = "XX12762 Turbo",
                                                               measurement_type = self.mtype_pressure,
                                                               short_description = "Temp",
                                                               description = "Measurement of temperature",
                                                               unit = "Degree celcius",
                                                               min_value = 0,
                                                               max_value = 100)


        self.temp_sensor = Sensor.objects.create( sensor_id = "TEMP:XX",
                                                  s_id = abs(hash("TEMP:XX")),
                                                  parent_device = self.dev,
                                                  description = "tempm",
                                                  sensor_type = self.sensor_type_temp)

        self.hum_sensor = Sensor.objects.create( sensor_id = "HUM:XX",
                                                 s_id = abs(hash("HUM:XX")),
                                                 description = "Measurement humidity",
                                                 data_type = self.raw_data ,
                                                 parent_device = self.dev,
                                                 sensor_type = self.sensor_type_hum)

        self.loc0_sensor = Sensor.objects.create( sensor_id = "NO_LOC:XX",
                                                  s_id = abs(hash("NO_LOC:XX")),
                                                  description = "Measurement pressure",
                                                  data_type = self.raw_data ,
                                                  parent_device = self.dev_loc0,
                                                  sensor_type = self.sensor_type_pressure)

        self.test_user_passwd = get_random_string( length = 10 ),
        self.test_user = User.objects.create_user( get_random_string( length = 10 ),
                                                   password = self.test_user_passwd ,
                                                   email = "joe@invalid.email.com" )

