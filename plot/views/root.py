from django.shortcuts import render
from django.views.generic import View

from plot.models import *

class Root(View):
    
    def get(self , request):
        gen_plot = []
        dev_plot = []
        for plot in Plot.objects.all():
            try:
                dev_plot.append( plot.deviceplot )
            except DevicePlot.DoesNotExist:
                gen_plot.append( plot )
                
        context = {"gen_plot" : gen_plot,
                   "dev_plot" : dev_plot ,
                   "url_root" : "%s://%s" % (request.scheme , request.get_host()) }
        
        return render( request , "plot/root.html" , context)
