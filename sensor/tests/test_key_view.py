from django.urls import reverse
from django.test import TestCase, Client
from django.test import TestCase
from rest_framework import status
from api_key.models import *
from sensor.models import *
from .context import TestContext


class ApiKeyViewTest(TestCase):


    def setUp(self):
        self.context = TestContext() 
        
        
    def test_get_not_logged_in_fails(self):
        client = Client( )
        url = reverse( "key.view.main" )

        # Not logged in
        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_302_FOUND )
        
        client.login( username = self.context.test_user.username , 
                      password = self.context.test_user_passwd )

        response = client.get( url )
        self.assertEqual( response.status_code , status.HTTP_200_OK )
