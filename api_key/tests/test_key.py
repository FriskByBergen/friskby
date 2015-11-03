from django.test import TestCase
from api_key.models import *


class ApiKeyTest(TestCase):

    def test_access(self):
        key = ApiKey.objects.create( description = "New key" )
        self.assertFalse( key.access("No/not/this"))

        ext_key = str(key.external_key)
        self.assertTrue( key.access( ext_key ))
        
        key.reset()
        self.assertFalse( key.access( ext_key ))


    def test_valid(self):
        key = ApiKey.objects.create( description = "New key" )
        ext_key = str(key.external_key)

        self.assertTrue( ApiKey.valid( ext_key ) )
        self.assertFalse( ApiKey.valid( "invalidKey") )
        
        ext_key2 = ext_key.replace("1" , "2")
        self.assertFalse( ApiKey.valid( "invalidKey") )

