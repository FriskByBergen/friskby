import sys

from django.core.management.base import BaseCommand, CommandError
from sensor.models import *

class Command(BaseCommand):
    help = """Will add entries to the RawData table. By default it will 100
    measurements to each sensor, but by passing one of the --device=
    or --sensor= options you can limit which sensors get data. Using
    the --num= you can control how many measurements are added."""
    
    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        for rd in RawData.objects.all():
            rd.location = rd.sensor.get_location( )
            rd.save( )
