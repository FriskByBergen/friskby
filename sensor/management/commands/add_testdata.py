import sys

from django.core.management.base import BaseCommand, CommandError
from sensor.models import *
from ._sample import sample
from ._sensor_list import sensor_list

class Command(BaseCommand):
    help = """Will add entries to the RawData table. By default it will 100
    measurements to each sensor, but by passing one of the --device=
    or --sensor= options you can limit which sensors get data. Using
    the --num= you can control how many measurements are added."""
    
    def add_arguments(self, parser):
        parser.add_argument('--num' , default = 100, type=int)
        parser.add_argument('--device' )
        parser.add_argument('--sensor' )

    
    def handle(self, *args, **options):
        for sensor in sensor_list( options ):
            sample( sensor , int(options["num"]) )
        
