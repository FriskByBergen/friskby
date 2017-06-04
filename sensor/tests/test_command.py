from django.test import TestCase

from sensor.management.commands.lock_device import Command as Lock
from sensor.management.commands.unlock_device import Command as UnLock
from sensor.management.commands.post import Command as Post
from sensor.management.commands.drop_testdata import Command as DropTestData
from sensor.management.commands.add_testdata import Command as AddTestData
from sensor.management.commands.drop_testdevice import Command as DropTestDevice
from sensor.management.commands.add_testdevice import Command as AddTestDevice

from sensor.management.commands.clean_test import Command as CleanTest
from sensor.models import *

from .context import TestContext

class CommandTest(TestCase):

    def setUp(self):
        self.context = TestContext( )
    
    def test_post(self):
        cmd = Post( )
        

    def test_locking(self):
        add_dev = AddTestDevice( )
        add_dev.handle( num = 100, device = ["Dev1"])
        dev1 = Device.objects.get( pk = "Dev1")
        self.assertEqual( True , dev1.locked )
        
        unlock = UnLock( )
        unlock.handle( device = ["Dev1"] )
        dev1.refresh_from_db( )
        self.assertEqual( False , dev1.locked )     

        lock = Lock( )
        lock.handle( )
        dev1.refresh_from_db( )
        self.assertEqual( True , dev1.locked )     

        unlock.handle( device = ["Dev1"] )
        dev1.refresh_from_db( )
        self.assertEqual( False , dev1.locked )     
        lock.handle( device = ["Dev2"])
        dev1.refresh_from_db( )
        self.assertEqual( False , dev1.locked )     

        lock.handle( device = ["Dev1"])
        dev1.refresh_from_db( )
        self.assertEqual( True , dev1.locked )     





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


    def test_clean(self):
        add_dev = AddTestDevice( )
        add_dev.handle( num = 10, device = ["FriskPITest", "Other"])
        rd = RawData.objects.all( )
        self.assertEqual( len(rd) , 40 )        

        rd = RawData.objects.all( )
        for d in rd:
            d.timestamp_data = TimeStamp.parse_datetime("2015-01-01T00:00:00+01")
            d.save()
            
        clean_test = CleanTest( )
        clean_test.handle( )
        rd = RawData.objects.all( )
        self.assertEqual( len(rd) , 20 )

        add_data = AddTestData(  )
        add_data.handle( device = "FriskPITest", num = 100 , sensor = None)
        rd = RawData.objects.all( )
        for d in rd:
            d.timestamp_data = TimeStamp.now( )
            d.save()

        rd = RawData.objects.all( )
        len1 = len(rd)
        clean_test.handle( )
        rd = RawData.objects.all( )
        self.assertEqual(len(rd), len1)


