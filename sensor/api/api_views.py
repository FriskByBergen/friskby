import json

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

            try:
                sensor = models.SensorID.objects.get( pk = sensorid )
                if not sensor.valid_input( value ):
                    return (status.HTTP_400_BAD_REQUEST , "The value:%s for sensor:%s is invalid" % (value , sensorid))
            except models.SensorID.DoesNotExist:
                return (status.HTTP_404_NOT_FOUND , "The sensorID:%s is not found" % sensorid)
            
        return (status.HTTP_200_OK , "")




    def post(self , request , format = None):
        if request.data:
            payload_status , msg = self.checkPayload( request.data )
            if payload_status == status.HTTP_200_OK:
                return Response(len(request.data) , status = status.HTTP_200_OK)
            else:
                return Response( msg , status = payload_status )
        else:
            return Response("Missing data" , status = status.HTTP_400_BAD_REQUEST )
