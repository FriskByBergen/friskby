from api_key.models import *
from sensor.models import *

class TestContext(object):
    def __init__(self):
        self.key = ApiKey.objects.create( description = "Newkey")
        self.external_key = str(self.key.external_key)
        self.loc = Location.objects.create( name = "Ulriken" , latitude = 200 , longitude = 120 , altitude = 600)
        self.hp = Company.objects.create( name = "Hewlett Packard" )
        self.dev_type = DeviceType.objects.create( name = "HP-X123" , company = self.hp)
        self.dev = Device.objects.create( id = "DevXXX" , location = self.loc , device_type = self.dev_type , description = "Besrkivels")
        self.mtype = MeasurementType.objects.create( name = "Temperature" )
        self.raw_data = DataType.objects.get( pk = "RAWDATA" )
        self.test_data = DataType.objects.get( pk = "TEST" )

        self.sensor_type_temp = SensorType.objects.create( company = self.hp,
                                                           product_name = "XX12762 Turbo",
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
