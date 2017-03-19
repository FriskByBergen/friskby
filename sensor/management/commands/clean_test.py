import sys
import datetime
from django.core.management.base import BaseCommand, CommandError
from sensor.models import *

class Command(BaseCommand):
    help = """Will remove all test entries from RawData table."""


    def handle(self, *args, **options):
        try:
            test_dev = Device.objects.get( pk = "FriskPITest" )
        except Device.DoesNotExist:
            return
            
        time_limit = TimeStamp.now() - datetime.timedelta( days = 1 )
        sensor_list = test_dev.sensorList()
        rd = RawData.objects.filter( s_id__in = test_dev.sensorList( ) , timestamp_data__lt = time_limit)
        rd.delete( )
        
