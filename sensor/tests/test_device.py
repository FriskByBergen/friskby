from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from sensor.models import *
from .context import TestContext


class DeviceTest(TestCase):
    def setUp(self):
        self.context = TestContext( )
        

    def test_get_config(self):
        client = Client( )
        response = client.get("/sensor/api/device/XXX/")
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        response = client.get("/sensor/api/device/%s/" % self.context.dev.id)
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        
        data = json.loads(response.content)
        self.assertTrue( "client_config" in data )

        client_config = data["client_config"]
        self.assertTrue( self.context.dev.valid_post_key( client_config["post_key"] ))

        self.assertEqual( len(self.context.dev.sensorList( )) , 2 )
        sensor_list = client_config["sensor_list"]
        self.assertEqual( len(sensor_list) , 2 )

        self.assertTrue( "TEMP:XX" in sensor_list )
        self.assertTrue( "HUM:XX" in sensor_list )
        
        self.assertFalse( "git_repo" in client_config )
        self.assertFalse( "git_ref" in client_config )
        
        self.context.dev.git_version = self.context.git_version
        self.context.dev.save(  )
        response = client.get("/sensor/api/device/%s/" % self.context.dev.id)
        data = json.loads(response.content)
        client_config = data["client_config"]

        self.assertTrue( client_config["git_repo"] , self.context.git_version.repo )
        self.assertTrue( client_config["git_ref"] , self.context.git_version.ref )
        
