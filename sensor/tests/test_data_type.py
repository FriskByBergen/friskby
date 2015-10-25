from django.test import TestCase
from sensor.models import *


class DataTypeTest(TestCase):

    def setUp(self):
        pass
        

    def test_initial_data_migration(self):
        test_type = DataType.objects.get( pk = "TEST" )
        
