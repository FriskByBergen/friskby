import json
from django.urls import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *

class ViewTest(TestCase):
    def setUp(self):
        pass


    def test_get_root(self):
        client = Client( )
        response = client.get("/sensor/view/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
