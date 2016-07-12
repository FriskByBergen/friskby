from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from plot.models import *
from pythoncall.models import *

from .context import TestContext


class PlotUrlTest(TestCase):
    def setUp(self):
        self.context = TestContext()
        
    def test_get(self):
        plot1 = Plot.objects.create( name = "XYZ1",
                                     description = "ABC",
                                     tag = "tag",
                                     python_callable = self.context.simple_call )
        
        client = Client( )
        response = client.get( reverse("plot_root") )
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        response = client.get( reverse("plot_one" , args = [1000]))
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        response = client.get( reverse("plot_one" , args = [plot1.id]))
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        response = client.get( reverse("plot_get" , args = [plot1.id]))
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        
