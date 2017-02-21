from django.test import TestCase

from sensor.management.commands.post import Command as Post
from sensor.management.commands.drop_testdata import Command as DropTestData
from sensor.management.commands.add_testdata import Command as AddTestData
from sensor.management.commands.drop_testdevice import Command as DropTestDevice
from sensor.management.commands.add_testdevice import Command as AddTestDevice

from sensor.models import *

class CommandTest(TestCase):
    
    def test_post(self):
        cmd = Post( )
        

    def test_data(self):
        add_dev = AddTestDevice( )
        add_dev.handle( num = 100, device = ["Dev1","Dev2"])
        dev1 = Device.objects.get( pk = "Dev1")
        s1 = Sensor.objects.get( sensor_id = "Dev1_PM10" )
        s2 = Sensor.objects.get( sensor_id = "Dev2_PM25" )
        
        add_data = AddTestData(  )
        add_data.handle( device = "Dev1", num = 100 , sensor = None)
        v1 = s1.get_ts( )
        v2 = s2.get_ts( )
        
        self.assertEqual( len(v1) , 200 )
        self.assertEqual( len(v2) , 100 )
        
        drop_data = DropTestData( )
        drop_data.handle( device = "Dev2" , sensor = None)
        v2 = s2.get_ts( )
        self.assertEqual( len(v2) , 0 )

        drop_dev = DropTestDevice( )
        drop_dev.handle( device = ["Dev2"] , all = None)
        with self.assertRaises( Device.DoesNotExist ):
            Device.objects.get( pk = "Dev2" )

        with self.assertRaises( Sensor.DoesNotExist ):
            Sensor.objects.get( sensor_id = "Dev2_PM10" )
