import requests
import json

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import View
from rest_framework import status

from sensor.models import Device
from sensor.api.serializers import DeviceSerializer

class MainView(View):

    def get(self , request):
        return render( request , "sensor/main.html" )



class DeviceView(View):
    
    def get(self, request, pk):
        device = get_object_or_404( Device, pk = pk)
        device_data = DeviceSerializer( data = device )
        
        return render( request , "sensor/device.html" , device_data.get_data( ))
        
