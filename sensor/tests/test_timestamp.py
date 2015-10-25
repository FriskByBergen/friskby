from django.utils import timezone,dateparse

from django.test import TestCase
from sensor.models import *


class TimeStampTest(TestCase):

    def setUp(self):
        pass
        

    def test_create(self):
        ts1 = TimeStamp.objects.create( timestamp = timezone.now() )
        ts2 = TimeStamp.objects.create( timestamp = dateparse.parse_datetime("2015-10-10T10:10:00+01"))
        
