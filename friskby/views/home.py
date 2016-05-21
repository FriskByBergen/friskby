from django.shortcuts import render
from django.views.generic import View

from plot.models import *

class Home(View):
    
    def get(self , request):
        try:
            p2 = Plot.objects.get( pk = 2 )
            plot_div = p2.html_code
        except Plot.DoesNotExist:
            plot_div = "No such plot:2"

        context = {"plot_div" : plot_div }
        return render( request , "friskby/main.html" , context )
