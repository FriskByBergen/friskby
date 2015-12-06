import json
import requests
import time
import datetime 

from django.conf import settings

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from filter.models import *
from sensor.models import *


class FilterDataView(APIView):

    def listView(self , sensor = None):
        data = {}
        if sensor is None:
            qs =  FilterData.objects.all()
        else:
            qs =  FilterData.objects.filter( sensor = sensor )

        for fd in qs:
            sensor_id = fd.sensor.id
            filter_id = fd.filter_code.id
            
            if not sensor_id in data:
                data[sensor_id] = []
            
            data[sensor_id].append( filter_id )

        return Response( data )




    def get(self, request , sensor_id = None , filter_id = None):
        if sensor_id is None:
            return self.listView( )
            
        try:
            sensor = Sensor.objects.get( pk = sensor_id )
        except Sensor.DoesNotExist:
            return Response( "Sensor:%s not found" % sensor_id , status = status.HTTP_404_NOT_FOUND )
        
        if filter_id is None:
            return self.listView( sensor = sensor )
        
        try:
            filter = Filter.objects.get( pk = filter_id )
        except Filter.DoesNotExist:
            return Response( "Filter:%s not found" % filter_id , status = status.HTTP_404_NOT_FOUND )

        try:
            fd = FilterData.objects.get( filter_code = filter , sensor = sensor )
            return Response( fd.ts.export() )
        except FilterData.DoesNotExist:
            return Response( "FilterData %s/%s not found" % (sensor_id , filter_id) , status = status.HTTP_404_NOT_FOUND )
