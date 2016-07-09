from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from rest_framework import status
from plot.models import *

class PlotView(View):
    
    def get(self , request , plot_id):
        try:
            plot = Plot.objects.get( pk = int(plot_id))
        except Plot.DoesNotExist:
            return HttpResponse("Plot id:%s does not exist" % plot_id , status = status.HTTP_404_NOT_FOUND )

        return render( request , "plot/plot_view.html" , {"plot_div" : plot.html_code} )


