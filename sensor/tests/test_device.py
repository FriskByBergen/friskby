import json

from django.urls import reverse
from django.test import TestCase, Client
from rest_framework import status

from sensor.models import *
from .context import TestContext


class DeviceTest(TestCase):
    def setUp(self):
        self.context = TestContext( )


    def test_get_config(self):
        client = Client( )
        response = client.get( reverse("api.device.info" , args = ["XXX"]))
        self.assertEqual( response.status_code , status.HTTP_404_NOT_FOUND )

        url = reverse( "api.device.info" , args = [ self.context.dev.id ])
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )

        data = json.loads(response.content)
        self.assertTrue( "client_config" in data )

        client_config = data["client_config"]
        self.assertFalse( "post_key" in client_config )

        self.assertEqual( len(self.context.dev.sensorList( )) , 2 )
        sensor_list = client_config["sensor_list"]
        self.assertEqual( len(sensor_list) , 2 )

        self.assertTrue( "TEMP:XX" in sensor_list )
        self.assertTrue( "HUM:XX" in sensor_list )

        self.context.dev.save(  )
        response = client.get("/sensor/api/device/%s/" % self.context.dev.id)
        data = json.loads(response.content)
        client_config = data["client_config"]

        self.assertEqual(client_config["channel"], self.context.channel)
        self.assertTrue( "post_path" in client_config )
        self.assertTrue( "config_path" in client_config )
        self.assertEqual( client_config["device_id"] , self.context.dev.id )



    def test_get_open_config(self):
        device = Device.objects.get( pk = self.context.dev.id )
        device.locked = False
        device.save( )

        client = Client( )
        url = reverse( "api.device.info" , args = [ self.context.dev.id ])
        response = client.get( url )
        data = json.loads(response.content)
        client_config = data["client_config"]
        self.assertTrue( self.context.dev.valid_post_key( client_config["post_key"] ))
        device.locked = True
        device.save( )


    def test_get_closed_config(self):
        device = Device.objects.get( pk = self.context.dev.id )

        # Invalid key supplied - closed device
        client = Client( )
        url = reverse( "api.device.info" , args = [ self.context.dev.id ])
        response = client.get( url , {"key" : "Invalid"})
        obj = json.loads( response.content )
        client_config = obj["client_config"]
        self.assertEqual( response.status_code , status.HTTP_200_OK )
        obj = json.loads( response.content )
        self.assertEqual( False, self.context.dev.valid_post_key( obj["post_key"] ))
        
        response = client.get( url , {"key" : device.post_key.external_key})
        data = json.loads(response.content)
        client_config = data["client_config"]
        self.assertEqual( True, self.context.dev.valid_post_key( data["post_key"] ))
        self.assertEqual( True, self.context.dev.valid_post_key( client_config["post_key"] ))






    def test_post_log(self):
        client = Client( )
        device_id = self.context.dev.id

        # Invalid key -> 403
        data = {"device_id" : device_id , "key" : "Invalid key" , "msg" : "Msg"}
        url = reverse("sensor.api.client_log")
        response = client.post(url,
                               data = json.dumps( data ) ,
                               content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_403_FORBIDDEN )


        # Invalid device_id -> 400
        data = {"device_id" : "invalid_device" ,
                "key" : str(self.context.dev.post_key.external_key) ,
                "msg" : "Msg"}

        response = client.post(url,
                               data = json.dumps( data ) ,
                               content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )

        data = {"device_id" : "invalid_device" ,
                "key" : str(self.context.dev.post_key.external_key) ,
                "msg" : "Msg"}

        response = client.post(url,
                               data = json.dumps( data ) ,
                               content_type = "application/json")
        self.assertEqual( response.status_code , status.HTTP_400_BAD_REQUEST )


        # All good : 201
        data = {"device_id" : device_id,
                "key" : str(self.context.dev.post_key.external_key) ,
                "msg" : "Msg"}

        response = client.post(url,
                               data = json.dumps( data ) ,
                               content_type = "application/json")
        self.assertEqual( response.status_code , 201 )


        # All good with long_msg: 201
        data = {"device_id" : device_id,
                "key" : str(self.context.dev.post_key.external_key) ,
                "msg" : "Msg",
                "long_msg" : "LONG"}

        response = client.post(url,
                               data = json.dumps( data ) ,
                               content_type = "application/json")
        self.assertEqual( response.status_code , 201 )


        # Get : 200
        response = client.get(url)
        self.assertEqual( len(response.data) , 2 )
        last = response.data[1]
        self.assertEqual( last["long_msg"] , "LONG")
