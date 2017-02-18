from api_key.models import *
from sensor.models import *
from sensor.tests.context import TestContext as SensorContext


class TestContext(object):
    def __init__(self):
        
        self.sensor_context = SensorContext( )
        self.pm10_mtype = MeasurementType.objects.create( name = "PM10" )
        self.pm25_mtype = MeasurementType.objects.create( name = "PM25" )
        
        self.sensor_type_pm25 = SensorType.objects.create( product_name = "Test PM25",
                                                           short_description = "Short",
                                                           measurement_type = self.pm25_mtype ,
                                                           description = "Long description",
                                                           unit = "c",
                                                           min_value = 0,
                                                           max_value = 1000)

        self.sensor_type_pm10 = SensorType.objects.create( product_name = "Test PM10",
                                                           short_description = "Short",
                                                           measurement_type = self.pm10_mtype ,
                                                           description = "Long description",
                                                           unit = "c",
                                                           min_value = 0,
                                                           max_value = 1000)
                                                           

        self.sensor_pm10 = Sensor.objects.create( sensor_id = "Test:PM10",
                                                  parent_device = self.sensor_context.dev,
                                                  description = "??",
                                                  sensor_type = self.sensor_type_pm10 )

        self.sensor_pm25 = Sensor.objects.create( sensor_id = "Test:PM25",
                                                  parent_device = self.sensor_context.dev,
                                                  description = "??",
                                                  sensor_type = self.sensor_type_pm25 )

        self.key = ApiKey.objects.create( description = "Newkey")
        self.external_key = str(self.key.external_key)
        
        RawData.create( {"key" : self.external_key , "sensorid" : "Test:PM10" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100 } )
        RawData.create( {"key" : self.external_key , "sensorid" : "Test:PM10" , "timestamp" : "2015-10-11T12:12:00+01" , "value" :  50 } )
        RawData.create( {"key" : self.external_key , "sensorid" : "Test:PM10" , "timestamp" : "2015-10-12T12:12:00+01" , "value" :  10 } )
        RawData.create( {"key" : self.external_key , "sensorid" : "Test:PM25" , "timestamp" : "2015-10-10T12:12:00+01" , "value" : 100 } )
        RawData.create( {"key" : self.external_key , "sensorid" : "Test:PM25" , "timestamp" : "2015-10-11T12:12:00+01" , "value" : 200 } )
        RawData.create( {"key" : self.external_key , "sensorid" : "Test:PM25" , "timestamp" : "2015-10-12T12:12:00+01" , "value" : 300 } )
