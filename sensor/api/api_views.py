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

class DeviceList(generics.ListCreateAPIView):
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceSerializer
    

class Device(generics.RetrieveAPIView):    
    queryset = models.DeviceType.objects.all()
    serializer_class = DeviceSerializer

#################################################################

class LocationList(generics.ListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    

class Location(generics.RetrieveAPIView):    
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer

#################################################################

class SensorIDList(generics.ListCreateAPIView):
    queryset = models.SensorID.objects.all()
    serializer_class = SensorIDSerializer
    

class SensorID(generics.RetrieveAPIView):    
    queryset = models.SensorID.objects.all()
    serializer_class = SensorIDSerializer


#################################################################

class SensorInfo(APIView):
    def get(self , request , sensor_id = None):
        if sensor_id is None:
            sensor_list = models.SensorID.objects.all()
        else:
            try:
                sensor_list = [ models.SensorID.objects.get( pk = sensor_id ) ]
            except models.SensorID.DoesNotExist:
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

    def checkPayload(self , data):
        for reading in data:
            if "sensorid" in reading:
                sensorid = reading["sensorid"]
            else:
                return (status.HTTP_400_BAD_REQUEST , "Missing 'sensorid' field in payload")

                    
            if "value" in reading:
                value = reading["value"]
            else:
                return (status.HTTP_400_BAD_REQUEST , "Missing 'value' field in payload")

            if not "timestamp" in reading:
                return (status.HTTP_400_BAD_REQUEST , "Missing 'timestamp' field in payload")

            try:
                sensor = models.SensorID.objects.get( pk = sensorid )
                if not sensor.valid_input( value ):
                    return (status.HTTP_400_BAD_REQUEST , "The value:%s for sensor:%s is invalid" % (value , sensorid))

                if sensor.location is None:
                    if not "location" in reading:
                        return (status.HTTP_400_BAD_REQUEST , "Sensor:%s does not have location - must supply in post" % sensorid)
                        
            except models.SensorID.DoesNotExist:
                return (status.HTTP_404_NOT_FOUND , "The sensorID:%s is not found" % sensorid)
            
        return (True , "")


    def restdb_io_post( self , data ):
        headers = {"Content-Type" : "application/json",
                   "x-apikey" :  settings.RESTDB_IO_POST_KEY}

        for reading in data:
            post_data = json.dumps( reading )
            response = requests.post( settings.RESTDB_IO_URL , data = post_data , headers = headers )
            if response.status_code != status.HTTP_201_CREATED:
                return (response.status_code , response.text)

        return (status.HTTP_201_CREATED , len(data))

        

    def post(self , request , format = None):
        if request.data:
            payload_status , msg = self.checkPayload( request.data )
            if payload_status is True:
                restdb_io_status , msg = self.restdb_io_post( request.data )
                if restdb_io_status == status.HTTP_201_CREATED:
                    return Response(msg , status = restdb_io_status)
                else:
                    return Response("Posting to restdb.io failed: %s" % msg , status = status.HTTP_500_INTERNAL_SERVER_ERROR )
            else:
                return Response( msg , status = payload_status )
        else:
            return Response("Missing data" , status = status.HTTP_400_BAD_REQUEST )


    def restdb_io_get(self , sensor_id , request_params):
        headers = {"Content-Type" : "application/json",
                   "x-apikey" :  settings.RESTDB_IO_GET_KEY}
        query_string = json.dumps( {"sensorid" : sensor_id} )

        params = {"q" : query_string}
        params.update( request_params )
        if not "max" in params:
            params["max"] = 99999999

        response = requests.get( settings.RESTDB_IO_URL , headers = headers , params = params)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            time_series = []
            for reading in data:
                time_series.append( (reading["timestamp"] , reading["value"]) )
            return Response( json.dumps( time_series ) , status = response.status_code ) 
        else:
            return Response( response.data , status = response.status_code ) 

        

    def get(self , request , sensor_id = None):
        if sensor_id is None:
            return Response("Must supply sensorid when querying" , status = status.HTTP_400_BAD_REQUEST )
            
        try:
            sensor = models.SensorID.objects.get( pk = sensor_id )
            return self.restdb_io_get( sensor_id , request.GET )
        except models.SensorID.DoesNotExist:
            return Response("No such sensor:%s" % sensor_id , status = status.HTTP_200_OK )
            
        
