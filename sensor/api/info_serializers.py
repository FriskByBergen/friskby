from rest_framework import serializers
from sensor.models import *
from sensor.api.serializers import *

# The various 'info' serializers in this module typically internalize
# the representation of foreign keys, instead of just using the id of
# the related object.

class DeviceTypeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'name')



class DeviceInfoSerializer(serializers.ModelSerializer):
    location = LocationSerializer( read_only = True )
    device_type = DeviceTypeInfoSerializer( read_only = True )

    class Meta:
        model = Device
        fields = ('id', 'location' , 'device_type','description')


class SensorTypeInfoSerializer(serializers.ModelSerializer):
    measurement_type = MeasurementTypeSerializer( read_only = True )
    class Meta:
        model = SensorType
        fields = ('id', 'product_name','short_description','measurement_type','description','unit','min_value','max_value')



class SensorInfoSerializer(serializers.ModelSerializer):
    parent_device = DeviceInfoSerializer( read_only = True )
    sensor_type = SensorTypeInfoSerializer( read_only = True )

    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_type', 'parent_device','data_type','description','on_line' , 'last_value','last_timestamp')



    
