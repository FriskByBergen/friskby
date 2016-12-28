import requests
from unittest import skipUnless
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from git_version.models import *

try:
    response = requests.get("https://github.com/")
    have_network = True
except:
    have_network = False

@skipUnless(have_network , "This test class requires network access")
class GitVersionTest(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        with self.assertRaises(ValidationError):
            v = GitVersion.objects.create( ref = "master_does_not_exist",
                                           description = "Hei")

        v = GitVersion.objects.create( ref = "master" , repo = "Does/not/exist" , description = "d")
        self.assertEqual( v.follow_head , False )

        v = GitVersion.objects.create( ref = "master" , repo = "Does/not/exist" , description = "d",
                                       follow_head = True )
        self.assertEqual( v.follow_head , True )
            
        
