from django.shortcuts import render
from django.views.generic import View

from plot.models import *

import sensor.models as models

class Quick(View):
    
    def get(self , request):
        sensor_list = models.Sensor.objects.all()
        
        for s in sensor_list:
            print vars(s)

        context = {"sensor_list" : sensor_list }
        return render( request , "friskby/quick.html" , context )
