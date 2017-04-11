import requests
import json

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import View
from rest_framework import status

from sensor.models import Device

class MainView(View):

    def get(self , request):
        return render( request , "sensor/main.html" )



class DeviceView(View):
    
    def get(self, request, pk):
        device = get_object_or_404( Device, pk = pk)

        # Using the api call:
        url = reverse("api.device.info" , kwargs = {"pk" : device.id} )
        api_get = requests.get( request.build_absolute_uri( url ))

        return render( request , "sensor/device.html" , api_get.json( ))
        
