from pythoncall.models import *
from git_version.models import * 
from api_key.models import *
from sensor.models import *
from django.contrib.auth.models import User

def create_string( ):
    return "Plot"

def error_call():
    return None

    
class TestContext(object):
    def __init__(self):
        self.simple_call = PythonCall.objects.create( description = "math.sin",
                                                      python_callable = "plot.tests.context.create_string" )
        
        self.error_call = PythonCall.objects.create( description = "math.sin",
                                                     python_callable = "plot.tests.context.error_call" )
        
        self.plotly_call = PythonCall.objects.create( description = "PlotLy",
                                                     python_callable = "plot.lib.test")
        

        self.git_version = GitVersion.objects.create( ref = "master" , repo = "uri://git.no" , description = "description")
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
        
        self.temp_sensor = Sensor.objects.create( sensor_id = "TEMP:XX",
                                                  parent_device = self.dev,
                                                  description = "tempm",
                                                  sensor_type = self.sensor_type_temp)

        RawData.create( {"sensorid" : self.temp_sensor.sensor_id , 
                         "value" : "10",
                         "key" : str(self.key.external_key),
                         "timestamp" : "2015-10-10T10:10:00+01" })

        RawData.create( {"sensorid" : self.temp_sensor.sensor_id , 
                         "value" : "12",
                         "key" : str(self.key.external_key),
                         "timestamp" : "2015-11-10T10:10:00+01" })
    
        
 
