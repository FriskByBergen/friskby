from rest_framework import serializers

from sensor.models import *


class MeasurementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementType
        fields = ('id', 'name')



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'name' , 'company')



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name' , 'latitude', 'longitude', 'altitude')



class SensorIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorID
        fields = ('id', 'location','parent_device','measurement_type','description','unit','min_value','max_value')
