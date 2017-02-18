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

    def listView(self):
        data = {}
        qs =  FilterData.objects.all()

        for fd in qs:
            sensor_id = fd.sensor.sensor_id
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
        
        try:
            filter = Filter.objects.get( pk = filter_id )
        except Filter.DoesNotExist:
            return Response( "Filter:%s not found" % filter_id , status = status.HTTP_404_NOT_FOUND )

        try:
            fd = FilterData.objects.get( filter_code = filter , sensor = sensor )
            return Response( fd.ts.export() )
        except FilterData.DoesNotExist:
            return Response( "FilterData %s/%s not found" % (sensor_id , filter_id) , status = status.HTTP_404_NOT_FOUND )


##################################################################


class SampledDataView(APIView):

    def listView(self):
        data = {}
        qs =  SampledData.objects.all()

        for sd in qs:
            sensor_id = sd.sensor.sensor_id
            if not sensor_id in data:
                data[sensor_id] = []

            transform = sd.transform
            if not transform is None:
                data[sensor_id].append( transform.id )

        return Response( data )




    def get(self, request , sensor_id = None , transform_id = None):
        if sensor_id is None:
            return self.listView( )
            
        try:
            sensor = Sensor.objects.get( pk = sensor_id )
        except Sensor.DoesNotExist:
            return Response( "Sensor:%s not found" % sensor_id , status = status.HTTP_404_NOT_FOUND )

        transform = None
        if not transform_id is None:
            try:
                transform = Transform.objects.get( pk = transform_id )
            except Transform.DoesNotExist:
                return Response( "Transform:%s not found" % transform_id , status = status.HTTP_404_NOT_FOUND )

        num = None
        if "num" in request.GET:
            try:
                num = int(request.GET["num"])
            except ValueError:
                pass

        start = None
        if "start" in request.GET:
            if not num is None:
                return Response( "Can not specify both start= and num=", status = status.HTTP_400_BAD_REQUEST  )
                
            try:
                start = TimeArray.parse_datetime( request.GET["start"] )
            except ValueError:
                pass



        try:
            sd = SampledData.objects.get( transform = transform , sensor = sensor )
            return Response( sd.data.export( num = num , start = start) )
        except SampledData.DoesNotExist:
            return Response( "SampledData %s/%s not found" % (sensor_id , transform_id) , status = status.HTTP_404_NOT_FOUND )
