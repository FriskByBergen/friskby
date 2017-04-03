import sys

from django.core.management.base import BaseCommand, CommandError
from api_key.models import *
from sensor.models import *
from ._sample import sample


class Command(BaseCommand):
    help = """Will remove testdevices and all related data.
    The devices you wish to remove should be given as commandline
    arguments.
    """


    def add_arguments(self, parser):
        parser.add_argument('--all' , action="store_true", default=False, dest="all")
        parser.add_argument('device' , nargs = '*')


    def drop_device(self , dev):
        sys.stdout.write("Dropping device:%s and all related data\n" % dev.id)
        for sensor in dev.sensorList():
            RawData.objects.filter( sensor = sensor ).delete()

        dev.delete()

    
    def handle(self, *args, **options):
        if options["all"]:
            device_list = Device.objects.all( )
        else:
            device_list = []
            for dev_id in options["device"]:
                try:
                    device = Device.objects.get( pk = dev_id )
                    device_list.append( device )
                except Device.DoesNotExist:
                    sys.stderr.write("No such device: %s\n" % dev_id)

        for dev in device_list:
            self.drop_device( dev )
        
        
