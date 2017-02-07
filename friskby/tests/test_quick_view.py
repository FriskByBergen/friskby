from django.urls import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from .context import TestContext
from sensor.models import *

class QuickTest(TestCase):
    def setUp(self):
        self.context = TestContext( )
        
        
    def test_get(self):
        url = reverse("friskby.view.quick")
        client = Client( )
        response = client.get(url)
        self.assertEqual( response.status_code , status.HTTP_200_OK )


    def test_time_param(self):
        url = reverse("friskby.view.quick")
        client = Client( )
        response = client.get(url , {"time" : "2016-10-10T12:12:00+01" } )
        self.assertEqual( response.status_code , status.HTTP_200_OK )

    def test_invalid_mtypes(self):
        mtype10 = MeasurementType.objects.get( name = "PM10" )
        mtype10.name = "PM10_modified"
        mtype10.save( )

        url = reverse("friskby.view.quick")
        client = Client( )
        response = client.get(url)

        self.assertEqual( response.status_code , status.HTTP_500_INTERNAL_SERVER_ERROR )
