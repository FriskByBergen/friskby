from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from plot.models import *
from pythoncall.models import *

from .context import TestContext


class DevicePlotTest(TestCase):
    def setUp(self):
        self.context = TestContext()

        
    def test_create(self):
        with self.assertRaises(ValueError):
            DevicePlot.objects.create( name = "XYZ",
                                       device = self.context.dev,
                                       duration = timedelta( days = -1))

            
        plot = DevicePlot.objects.create( name = "XYZ",
                                          device = self.context.dev)

        self.assertEqual( plot.tag , "DEV:DevXYZ" )
        
        
