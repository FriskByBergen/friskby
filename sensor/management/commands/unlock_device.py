import sys
import random

from django.core.management.base import BaseCommand, CommandError
from sensor.models import *


class Command(BaseCommand):
    help = """Will unlock a device"""


    def add_arguments(self, parser):
        parser.add_argument('device' , nargs = '+')


    def handle(self, *args, **options):
        for dev_id in options["device"]:
            try:
                dev = Device.objects.get( pk = dev_id )
                dev.locked = False
                dev.save( )
            except Device.DoesNotExist:
                sys.stderr.write("No such device: %s" % dev_id)

