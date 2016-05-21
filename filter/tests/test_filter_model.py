import datetime
from django.utils import dateparse , timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from filter.models import *
from pythoncall.models import PythonCall

var = "Not callable"

def func(x,y):
    return x + y


class FilterDataTest(TestCase):

    def test_create(self):
        with self.assertRaises(ValidationError):
            code = PythonCall.objects.create( description = "XY" , 
                                              python_callable = "does.not.exist")

        with self.assertRaises(ValidationError):
            code = PythonCall.objects.create( description = "XY" , 
                                              python_callable = "math.unknwon_function")

        with self.assertRaises(ValidationError):
            fm = PythonCall.objects.create( description = "XY" , 
                                            python_callable = "filter.tests.test_filter_model.var")

        code = PythonCall.objects.create( description = "XY" , 
                                          python_callable = "filter.tests.test_filter_model.func")

        fm = Filter.objects.create( description = "XY",
                                    width = 1000,
                                    python_code = code )
                                    
        
        func = fm.getCallable( )
        self.assertEqual( func(10,20) , 30 )

        # Invalid ID
        fm = Filter.objects.create( id = "filter1  []",
                                    description = "XY" , 
                                    width = 100,
                                    python_code = code)
        with self.assertRaises(ValidationError):
            fm.full_clean( )
            
        code_exp = PythonCall.objects.create( description = "XY" , 
                                              python_callable = "math.exp")

        fm = Filter.objects.create( id = "exp",
                                    description = "XY1" , 
                                    width = 100,
                                    python_code = code_exp)

        func = fm.getCallable( )
        self.assertEqual( func(0) , 1 )
        

        code_mean = PythonCall.objects.create( description = "XY" , 
                                               python_callable = "filter.filter.blockedMean")
        

        fm = Filter.objects.create( id = "MEAN_1HOUR",
                                    description = "XY2" , 
                                    width = 100,
                                    python_code = code_mean)
        

    def test_create_transform(self):
        code_sin = PythonCall.objects.create( description = "XY" , 
                                               python_callable = "math.sin")

        tr = Transform.objects.create( id = "sinx",
                                       description = "XYZ",
                                       python_code = code_sin )
