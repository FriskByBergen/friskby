import requests
from django.test import Client

from pythoncall.models import *
from filter.models import *

class TestContext(object):
    def __init__(self):
        
        code_mean = PythonCall.objects.create( description = "XY" , 
                                               python_callable = "filter.filter.blockedMean")


        code_max = PythonCall.objects.create( description = "XY" , 
                                              python_callable = "filter.filter.blockedMax")

        code_min = PythonCall.objects.create( description = "XY" , 
                                              python_callable = "filter.filter.blockedMin")

        
        
        self.f_mean = Filter.objects.create( id = "MEAN_1HOUR",
                                             width = 3600,
                                             description = "Average from 1Hour" , 
                                             python_code = code_mean )

        self.f_max = Filter.objects.create( id = "MAX_1HOUR",
                                            width = 3600,
                                            description = "Average from 1Hour" , 
                                            python_code = code_max )


        self.f_min = Filter.objects.create( id = "MIN_1HOUR",
                                            width = 3600,
                                            description = "Average from 1Hour" , 
                                            python_code = code_min )
        
        
        code_sin = PythonCall.objects.create( description = "XY" , 
                                              python_callable = "math.sin")


        self.t_sin = Transform.objects.create( id = "SIN",
                                               description = "Sinus ...",
                                               python_code = code_sin )
