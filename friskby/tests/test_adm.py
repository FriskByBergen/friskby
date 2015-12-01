from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

class AdmTest(TestCase):
    def setUp(self):
        pass
        

    def test_get_root(self):
        client = Client( )
        response = client.get("/friskby/adm/")
        # Should get a redirect here - because it should be redirected to 
        # the login page.
        self.assertEqual( response.status_code , status.HTTP_302_FOUND )
