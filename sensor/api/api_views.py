import json
import requests
import time

from django.conf import settings

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import sensor.models as models
from sensor.api.serializers import *
from sensor.api.info_serializers import *

class MeasurementTypeList(generics.ListCreateAPIView):
    queryset = models.MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer
    


class MeasurementType(generics.RetrieveAPIView):    
    queryset = models.MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer
    

#################################################################


class CompanyList(generics.ListCreateAPIView):
    queryset = models.Company.objects.all()
    serializer_class = CompanySerializer
    


class Company(generics.RetrieveAPIView):    
    queryset = models.Company.objects.all()
    serializer_class = CompanySerializer

#################################################################

class DeviceTypeList(generics.ListCreateAPIView):
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    

class DeviceType(generics.RetrieveAPIView):    
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

#################################################################

class DeviceList(generics.ListCreateAPIView):
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer
    

class Device(generics.RetrieveAPIView):    
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer

#################################################################

class LocationList(generics.ListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    

class Location(generics.RetrieveAPIView):    
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer

#################################################################


class DataTypeList(generics.ListCreateAPIView):
    queryset = models.DataType.objects.all()
    serializer_class = DataTypeSerializer
    

class DataType(generics.RetrieveAPIView):    
    queryset = models.DataType.objects.all()
    serializer_class = DataTypeSerializer


#################################################################

class DataInfoList(generics.ListCreateAPIView):
    queryset = models.DataInfo.objects.all()
    serializer_class = DataInfoSerializer
    

class DataInfo(generics.RetrieveAPIView):    
    queryset = models.DataInfo.objects.all()
    serializer_class = DataInfoSerializer

#################################################################

class DataValueList(generics.ListCreateAPIView):
    queryset = models.DataValue.objects.all()
    serializer_class = DataValueSerializer
    

class DataValue(generics.RetrieveAPIView):    
    queryset = models.DataValue.objects.all()
    serializer_class = DataValueSerializer

#################################################################


class TimeStampList(generics.ListCreateAPIView):
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer
    

class TimeStamp(generics.RetrieveAPIView):    
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer


#################################################################


class SensorList(generics.ListCreateAPIView):
    queryset = models.Sensor.objects.all()
    serializer_class = SensorSerializer
    

class Sensor(generics.RetrieveAPIView):    
    queryset = models.Sensor.objects.all()
    serializer_class = SensorSerializer


#################################################################

class SensorTypeList(generics.ListCreateAPIView):
    queryset = models.SensorType.objects.all()
    serializer_class = SensorTypeSerializer
    

class SensorType(generics.RetrieveAPIView):    
    queryset = models.SensorType.objects.all()
    serializer_class = SensorTypeSerializer


#################################################################


class SensorInfo(APIView):
    def get(self , request , sensor_id = None):
        if sensor_id is None:
            sensor_list = models.Sensor.objects.all()
        else:
            try:
                sensor_list = [ models.Sensor.objects.get( pk = sensor_id ) ]
            except models.Sensor.DoesNotExist:
                return Response("The sensorID:%s is not found" % sensor_id , status.HTTP_404_NOT_FOUND)
            
        result = []
        for sensor in sensor_list:
            serialized = SensorInfoSerializer( sensor )
            result.append( serialized.data )
            
        if sensor_id is None:
            return Response( result , status = status.HTTP_200_OK ) 
        else:
            return Response( result[0] , status = status.HTTP_200_OK ) 


class Reading(APIView):

    def cleanPayload(self , data):
        if "sensorid" in data:
            sensorid = data["sensorid"]
        else:
            return (status.HTTP_400_BAD_REQUEST , "Missing 'sensorid' field in payload")

                    
        if "value" in data:
            value = data["value"]
        else:
            return (status.HTTP_400_BAD_REQUEST , "Missing 'value' field in payload")

        if not "timestamp" in data:
            return (status.HTTP_400_BAD_REQUEST , "Missing 'timestamp' field in payload")

        try:
            sensor = models.Sensor.objects.get( pk = sensorid )
            if not sensor.valid_input( value ):
                return (status.HTTP_400_BAD_REQUEST , "The value:%s for sensor:%s is invalid" % (value , sensorid))

            if sensor.location is None:
                if not "location" in data:
                    return (status.HTTP_400_BAD_REQUEST , "Sensor:%s does not have location - must supply in post" % sensorid)
                        
        except models.Sensor.DoesNotExist:
            return (status.HTTP_404_NOT_FOUND , "The sensorID:%s is not found" % sensorid)
            
        return (True , "")


    def restdb_io_post( self , data ):
        headers = {"Content-Type" : "application/json",
                   "x-apikey" :  settings.RESTDB_IO_POST_KEY}

        post_data = json.dumps( data )
        response = requests.post( settings.RESTDB_IO_URL , data = post_data , headers = headers )
        if response.status_code != status.HTTP_201_CREATED:
            return (response.status_code , response.text)

        return (status.HTTP_201_CREATED , 1)


    def post(self , request , format = None):
        if request.data is None:
            return Response("Missing data" , status = status.HTTP_400_BAD_REQUEST )
            
        data = request.data
        for key in ["key" , "sensorid" , "value" , "timestamp"]:
            if not key in data:
                return Response("Missing '%s' field in payload" % key , status.HTTP_400_BAD_REQUEST)

        key = data["key"]
        sensorid = data["sensorid"]
        value = data["value"]
        timestring = data["timestamp"]
        timestamp = models.TimeStamp.parse_datetime( timestring )
        location = None
        if timestamp is None:
            return Response("Timestamp '%s' is invalid" % timestring , status.HTTP_400_BAD_REQUEST)

        try:
            sensor = models.Sensor.objects.get( pk = sensorid )
        except models.Sensor.DoesNotExist:
            return Response("The sensorID:%s is not found" % sensorid , status.HTTP_404_NOT_FOUND)

        if not sensor.valid_post_key( key ):
            return Response("Invalid key:'%s' when posting to:'%s'" % (key , sensorid) , status.HTTP_403_FORBIDDEN)

        if not sensor.valid_input( value ):
            return Response("The value:%s for sensor:%s is invalid" % (value , sensorid) , status.HTTP_400_BAD_REQUEST)

        if sensor.location is None:
            if not "location" in data:
                return Response("Sensor:%s does not have location - must supply in post" % sensorid , status.HTTP_400_BAD_REQUEST)
            location = data["location"]
                    



        ts = models.TimeStamp.objects.create( timestamp = timestamp )
        data_info = models.DataInfo( timestamp = ts , 
                                     sensor = sensor )
        if not location is None:
            data_info.location = location
        data_info.save()

        data_value = models.DataValue( data_info = data_info ,
                                       data_type = sensor.data_type ,  
                                       value = value )
        data_value.save( )
        

        restdb_io_status , msg = self.restdb_io_post( request.data )
        if restdb_io_status == status.HTTP_201_CREATED:
            return Response(msg , status = restdb_io_status)
        else:
            return Response("Posting to restdb.io failed: %s" % msg , status = status.HTTP_500_INTERNAL_SERVER_ERROR )
            



    def restdb_io_get(self , sensor_id , request_params):
        headers = {"Content-Type" : "application/json",
                   "x-apikey" :  settings.RESTDB_IO_GET_KEY}
        query_string = json.dumps( {"sensorid" : sensor_id} )

        params = {"q" : query_string,
                  "sort" : "timestamp",
                  "dir" : 1 }
        params.update( request_params )
        if not "max" in params:
            params["max"] = 99999999

        response = requests.get( settings.RESTDB_IO_URL , headers = headers , params = params)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            time_series = []
            for reading in data:
                time_series.append( (reading["timestamp"] , reading["value"]) )
            return Response( time_series , status = response.status_code ) 
        else:
            return Response( response.data , status = response.status_code ) 

        

    def get(self , request , sensor_id = None):
        if sensor_id is None:
            return Response("Must supply sensorid when querying" , status = status.HTTP_400_BAD_REQUEST )
            
        try:
            sensor = models.Sensor.objects.get( pk = sensor_id )
            ts = sensor.get_ts( )
            return Response(ts , status = status.HTTP_200_OK )
            #return self.restdb_io_get( sensor_id , request.GET )
        except models.Sensor.DoesNotExist:
            return Response("No such sensor:%s" % sensor_id , status = status.HTTP_200_OK )
            
        
