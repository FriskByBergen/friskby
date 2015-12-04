import random
import json

from django.utils import timezone
from django.test import TestCase, Client
from rest_framework import status

from time_series.models import *
from .context import TestContext
        


class TimeSeriesTest(TestCase):
    pass
    def setUp(self):
        self.context = TestContext()


    def test_get(self):
        client = Client( )

        #Invalid ID
        response = client.get("/time_series/api/X123/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        #Valid ID form - but not existing element
        response = client.get("/time_series/api/100/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
        
        response = client.get("/time_series/api/1/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        for (a,b) in zip(data["data"] , self.context.ts.data):
            self.assertEqual(a,b)
        
