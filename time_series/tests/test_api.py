import random
import json

from django.utils import timezone
from django.test import TestCase, Client
from rest_framework import status

from time_series.models import *
from .context import TestContext
        


class RegularTimeSeriesTest(TestCase):
    def setUp(self):
        self.context = TestContext()


    def test_get(self):
        client = Client( )

        #Invalid ID
        response = client.get("/time_series/api/regular/X123/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        #Valid ID form - but not existing element
        response = client.get("/time_series/api/regular/100/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )
        
        response = client.get("/time_series/api/regular/1/")
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        data = json.loads(response.content)
        for i in range(len(self.context.ts.data)):
            a = data[i][1]
            b = self.context.ts.data[i]
            self.assertEqual(a,b)
        
