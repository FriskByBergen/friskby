from pythoncall.models import *

def create_string( ):
    return "Plot"

def error_call():
    return None

    
class TestContext(object):
    def __init__(self):
        self.simple_call = PythonCall.objects.create( description = "math.sin",
                                                      python_callable = "plot.tests.context.create_string" )
        
        self.error_call = PythonCall.objects.create( description = "math.sin",
                                                     python_callable = "plot.tests.context.error_call" )
        
        self.plotly_call = PythonCall.objects.create( description = "PlotLy",
                                                     python_callable = "plot.lib.test")
        
        
