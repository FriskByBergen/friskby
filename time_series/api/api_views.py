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

from time_series.models import *


class RegularTimeSeriesView(APIView):


    def get(self, request , ts_id):
        try:
            ts = RegularTimeSeries.objects.get( pk = int(ts_id) )
        except RegularTimeSeries.DoesNotExist:
            return Response("No such timeseries:%s" % ts_id , status = status.HTTP_404_NOT_FOUND )

        return Response( ts.export( ) )
            


class SampledTimeSeriesView(APIView):


    def get(self, request , ts_id):
        try:
            ts = SampledTimeSeries.objects.get( pk = int(ts_id) )
        except SampledTimeSeries.DoesNotExist:
            return Response("No such timeseries:%s" % ts_id , status = status.HTTP_404_NOT_FOUND )

        return Response( ts.export( ) )
            
