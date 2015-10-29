from rest_framework import serializers

from sensor.models import *

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name' , 'latitude', 'longitude', 'altitude')



class MeasurementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementType
        fields = ('id', 'name')



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')



class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'name' , 'company')


class DeviceSerializer(serializers.ModelSerializer):
    location = LocationSerializer( read_only = True )
    device_type = DeviceTypeSerializer( read_only = True )

    class Meta:
        model = Device
        fields = ('id', 'location' , 'device_type','description')



class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = ('id',)


class TimeStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = ('timestamp',)


class DeviceTypeInfoSerializer(serializers.ModelSerializer):
    company = CompanySerializer( read_only = True )
    class Meta:
        model = DeviceType
        fields = ('id', 'name' , 'company')


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = ('id', 'product_name','company','short_description','measurement_type','description','unit','min_value','max_value')


class SensorTypeInfoSerializer(serializers.ModelSerializer):
    measurement_type = MeasurementTypeSerializer( read_only = True )
    class Meta:
        model = SensorType
        fields = ('id', 'product_name','company','short_description','measurement_type','description','unit','min_value','max_value')



class SensorInfoSerializer(serializers.ModelSerializer):
    location = LocationSerializer( read_only = True )
    parent_device = DeviceTypeInfoSerializer( read_only = True )
    sensor_type = SensorTypeInfoSerializer( read_only = True )

    class Meta:
        model = Sensor
        fields = ('id', 'sensor_type', 'location','parent_device','data_type','description')



class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('id', 'sensor_type','location','parent_device','description')




class DataInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataInfo
        fields = ('location','timestamp','sensor')


class DataValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataValue
        fields = ('data_type','data_info','value')
