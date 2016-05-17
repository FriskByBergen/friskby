from django.test import TestCase
from plot.models import *

class PlotTest(TestCase):
    def setUp(self):
        pass


    def test_create(self):
        with self.assertRaises(ValueError):
            plot = Plot( name = "XYZ",
                         description = "ABC"
                         call = "no/this/does/not/exist")
                         
