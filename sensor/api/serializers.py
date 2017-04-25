from django.contrib.auth.models import User

from rest_framework import serializers
from sensor.models import *
import sensor.sample as sample

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



# Would have preferred to implement this as a proper serializer,
# now it is just a simple class inspired by the rest framework serializers

class DeviceSerializer(object):

    def __init__(self, data = None, context = None):
        if data is None:
            self._data = {}
            return

        key = None
        if context:
            if "key" in context:
                key = context["key"]
        
            
        device = data
        data = {"id" : device.id,
                "owner" : { "name" : device.owner.get_full_name( ),
                            "email" : device.owner.email }}

        if device.location:
            loc = device.location
            data["location"] = {"name" : loc.name,
                                "latitude" : loc.latitude,
                                "longitude" : loc.longitude }


        data["client_config"] = device.clientConfig( )
        
        data["post_key"] = "----------"
        if device.locked:
            if device.valid_post_key( key ):
                data["post_key"] = str(device.post_key.external_key)
                data["client_config"]["post_key"] = str(device.post_key.external_key)
        else:
            data["post_key"] = str(device.post_key.external_key)
            data["client_config"]["post_key"] = str(device.post_key.external_key)

        sensor_list = device.sensorList( )
        sensor_types = [sensor.sensor_type.id for sensor in sensor_list]
        data["sensor_types"] = sensor_types


        # Time range is hardcoded for the last week.
        period = 7*3600*24 
        end_time = TimeStamp.now( )
        start_time = end_time - datetime.timedelta( seconds = period )

        
        data_all = RawData.objects.filter(timestamp_data__range=(start_time,end_time), sensor__in=sensor_list).values('sensor',
                                                                                                                      'value',
                                                                                                                      'timestamp_data').order_by('timestamp_data')
        sample_data = {}
        for sensor in sensor_list:
            sample_data[ str(sensor.sensor_type.measurement_type)  ] = sample.make_datalist([ x for x in data_all if x['sensor'] == sensor.s_id ] , block_size = 30, value_cutoff = 100)
        data["data"] = sample_data

        self._data = data

    def get_data(self):
        return self._data

    

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






