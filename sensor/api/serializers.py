from rest_framework import serializers
from sensor.models import *


# This module only contains 'pure' serializers; in particular that
# implies that foreign keys are just represented with their ID. In the
# module info_serializers are several serializers which collect
# information from related classes to present a more convenient view
# for consumers.

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name' , 'latitude', 'longitude', 'altitude')


class MeasurementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementType
        fields = ('id', 'name')


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'name')


class DeviceSerializer(serializers.ModelSerializer):
    location = LocationSerializer( read_only = True )
    device_type = DeviceTypeSerializer( read_only = True )
    client_config = serializers.ReadOnlyField( source = "clientConfig" )

    class Meta:
        model = Device
        fields = ('id', 'location' , 'device_type','description' , 'client_config')



class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = ('id',)


class TimeStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = ('timestamp',)




class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = ('id', 'product_name','short_description','measurement_type','description','unit','min_value','max_value')





class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_type','parent_device','description')






