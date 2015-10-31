from django.test import TestCase
from api_key.models import *


class ApiKeyTest(TestCase):

    def test_access(self):
        key = ApiKey.objects.create( description = "New key" )
        self.assertFalse( key.access("No/not/this"))

        ext_key = key.external_key
        self.assertTrue( key.access( ext_key ))
        
        key.reset()
        self.assertFalse( key.access( ext_key ))
