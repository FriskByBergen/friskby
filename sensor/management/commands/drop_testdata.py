import sys

from django.core.management.base import BaseCommand, CommandError
from sensor.models import *
from ._sensor_list import sensor_list

class Command(BaseCommand):
    help = """Will drop entries from the RawData table. By default it will drop
    all entries, but by using one of --sensor= or --device= options
    you can drop only data from that sensor/device.  """

    def add_arguments(self, parser):
        parser.add_argument('--device' )
        parser.add_argument('--sensor' )

    
    def handle(self, *args, **options):
        for sensor in sensor_list( options ):
            RawData.objects.filter( sensor_string_id = sensor.sensor_id ).delete()
        
