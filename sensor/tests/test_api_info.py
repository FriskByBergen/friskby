import random
import json

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *
from .context import TestContext


class SensorInfoTest(TestCase):
    def setUp(self):
        self.context = TestContext()

    def test_get_list(self):
        client = Client( )


        # Missing data
        url = reverse("sensor.api.list_info")
        response = client.get(url)
        self.assertEqual( response.status_code , status.HTTP_200_OK , response.data)
        sensor_list = response.data
        sensor0 = sensor_list[0]
        self.assertEqual( sensor0["data_type"] , "TEST" )
        loc = sensor0["parent_device"]["location"]
        self.assertEqual( loc , {"id" : 1 , "name" : "Ulriken" , "latitude" : 200 , "longitude" : 120 , "altitude" : 600})

        dev = sensor0["parent_device"]
        self.assertEqual( dev["id"] , self.context.dev.id )
        self.assertEqual( dev["description"] , self.context.dev.description )

        dev_type = dev["device_type"]
        self.assertEqual( dev_type["name"] , self.context.dev_type.name )
        

        sensor_type = sensor0["sensor_type"]
        self.assertEqual( sensor_type["product_name"] , "XX12762 Turbo" ) 
        
        self.assertEqual( sensor_type["min_value"] , 0 )
        self.assertEqual( sensor_type["max_value"] , 100 )
        self.assertTrue( sensor0["on_line"] )



    def test_get(self):
        client = Client( )

        url = reverse("sensor.api.info" , args = ["XYZ"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        url = reverse("sensor.api.info" , args = ["TEMP:XX"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        sensor0 = response.data
        loc = sensor0["parent_device"]["location"]
        self.assertEqual( loc , {"id" : 1 , "name" : "Ulriken" , "latitude" : 200 , "longitude" : 120 , "altitude" : 600})

        dev = sensor0["parent_device"]

        sensor_type = sensor0["sensor_type"]
        self.assertEqual( sensor_type["measurement_type"] , {"id" : 1 , "name" : "Temperature"} ) 
        self.assertEqual( sensor_type["min_value"] , 0 )
        self.assertEqual( sensor_type["max_value"] , 100 )

        url = reverse("sensor.api.info" , args = ["HUM:XX"])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        sensor0 = response.data
        self.assertEqual( sensor0["data_type"] , "RAWDATA" )
