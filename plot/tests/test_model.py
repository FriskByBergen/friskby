from django.test import TestCase
from django.core.exceptions import ValidationError
from plot.models import *
from pythoncall.models import *

from .context import TestContext


class PlotTest(TestCase):
    def setUp(self):
        self.context = TestContext()
        
        
    def test_create(self):
        plot1 = Plot.objects.create( name = "XYZ1",
                                     description = "ABC",
                                     tag = "tag",
                                     python_callable = self.context.simple_call )

        plot2 = Plot( name = "XYZ2",
                      description = "ABC",
                      tag = "tag2",
                      python_callable = self.context.error_call )

        with self.assertRaises(ValidationError):
            plot2.save( )

        plot2.python_callable = self.context.simple_call
        plot2.save( )

        
        plot3 = Plot.objects.create( name = "XYZ3",
                                     description = "ABC",
                                     tag = "XYZ",
                                     python_callable = self.context.plotly_call )
        
        plot3.python_callable = self.context.error_call
        plot3.save( )
        with self.assertRaises(ValidationError):
            plot3.updatePlot( )
            
        qs = Plot.select( r"tag.*" )
        self.assertEqual( len(qs) , 2 )
            
        
