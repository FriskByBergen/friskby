import sys

from django.core.management.base import BaseCommand, CommandError
from sensor.models import *

class Command(BaseCommand):
    help = """Will add entries to the RawData table. By default it will 100
    measurements to each sensor, but by passing one of the --device=
    or --sensor= options you can limit which sensors get data. Using
    the --num= you can control how many measurements are added."""
    
    def add_arguments(self, parser):
        parser.add_argument('--offset' , default = 0 , type=int)
        parser.add_argument('--num'    , default = 10000, type=int)

        
    def handle(self, *args, **options):
        offset = 0
        num = 10000

        if "offset" in options:
            offset = int(options["offset"])

        if "num" in options:
            num = int(options["num"])

        total_size = RawData.objects.all().count()
        qs = RawData.objects.all()[offset:offset+num]
        index = offset
        size = len(qs)
        for rd in qs:
            rd.location = rd.sensor.get_location( )
            rd.save( )

            index += 1
            if (index % 100) == 0:
                print "%d / %d / %d" % (index, offset + size , total_size)
                
            if index == total_size:
                print "Complete"
            
