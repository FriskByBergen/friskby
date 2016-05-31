from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from rest_framework import status

from git_version.models import *


class GitVersionTest(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        with self.assertRaises(ValidationError):
            v = GitVersion.objects.create( ref = "master_does_not_exist",
                                           description = "Hei")

        v = GitVersion.objects.create( ref = "master" , repo = "Does/not/exist" , description = "d")
        
            
        
