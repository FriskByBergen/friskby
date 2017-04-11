import random
import json

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *
from .context import TestContext


class DeviceInfoTest(TestCase):

    def setUp(self):
        self.context = TestContext()

    def test_get_list(self):
        url = reverse("api.device.info")
        client = Client( )
        response = client.get(url)
        self.assertEqual( response.status_code , status.HTTP_200_OK)
        device_list = response.data
        self.assertEqual( len(device_list) , 2 )
        dev_map = dict( device_list )
        self.assertTrue( "DevXYZ" in dev_map )
        self.assertTrue( "DevNoLoc" in dev_map )


    def test_get_device(self):
        client = Client( )
        response = client.get( reverse("api.device.info" , kwargs = {"pk" : "NO_SUCH_DEVICE"}) )
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND)

        
        response = client.get( reverse("api.device.info" , kwargs = {"pk" : self.context.dev.id}) )
        self.assertEqual( response.status_code , status.HTTP_200_OK)
        expected = {"id" : self.context.dev.id,
                    "location" :  {"name"     : self.context.loc.name,
                                   "latitude" : float(self.context.loc.latitude),
                                   "longitude" : float(self.context.loc.longitude)},
                    "owner" : {"name" : self.context.user.get_full_name( ),
                               "email" : self.context.user.email },
                    "sensor_types" : [ self.context.sensor_type_temp.id, self.context.sensor_type_hum.id ]}

        for key in expected.keys():
            self.assertEqual( response.data[key] , expected[key] )


