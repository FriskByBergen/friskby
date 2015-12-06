import requests
from django.test import Client

from filter.models import *

class TestContext(object):
    def __init__(self):
        
        code_mean = PythonCode.objects.create( description = "XY" , 
                                               python_callable = "filter.filter.blockedMean")


        code_max = PythonCode.objects.create( description = "XY" , 
                                              python_callable = "filter.filter.blockedMax")


        
        self.f_mean = Filter.objects.create( id = "MEAN_1HOUR",
                                             width = 3600,
                                             description = "Average from 1Hour" , 
                                             code = code_mean )

        self.f_max = Filter.objects.create( id = "MAX_1HOUR",
                                            width = 3600,
                                            description = "Average from 1Hour" , 
                                            code = code_max )
        



