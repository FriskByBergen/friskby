import datetime
from django.utils import dateparse , timezone
from django.test import TestCase
from time_series.models import *
from .context import TestContext

class RegularTimeSeriesTest(TestCase):

    def test_create(self):

        with self.assertRaises(ValueError):
            RegularTimeSeries.new( timezone.now( ) , 0)

        with self.assertRaises(ValueError):
            RegularTimeSeries.new( timezone.now( ) , -1)

        ts = RegularTimeSeries.new( timezone.now( ) , 100)

        self.assertEqual( len(ts) , 0 )
        with self.assertRaises(IndexError):
            ts[0]        

        ts.addValue( 1 )
        ts.addValue( 2 )
        ts.addValue( 3 )
        ts.addValue( 4 )
        ts.addValue( 5 )
        
        self.assertEqual( len(ts) , 5 )
        with self.assertRaises(IndexError):
            ts[6]

        self.assertEqual( ts[4] , 5 )

        ts.addList( [6,7,8,9,10] )
        self.assertEqual( ts[9] , 10 )
        self.assertEqual( len(ts) , 10 )

        ts.addList( (16,17,18,19,110) )
        self.assertEqual( ts[14] , 110 )
        self.assertEqual( len(ts) , 15 )

        data = RegularTimeSeries.createArray( size = 3 )
        self.assertEqual( data.shape[0] , 3 )
        data[0] = 99
        data[1] = 99
        data[2] = 109
        ts.addList( data )
        self.assertEqual( ts[17] , 109 )
        self.assertEqual( len(ts) , 18 )
        
        ts.save()

        ts2 = RegularTimeSeries.objects.get( pk = 1 )
        self.assertEqual( ts2[17] , 109 )
        self.assertEqual( len(ts2) , 18 )
        ts[0] = 100
        ts2[0] = 200


        
    def test_extend(self):
        context = TestContext( )
        start = context.ts.start
        last_time = context.ts.lastTime( )
        
        dt = last_time - start
        self.assertEqual( dt.seconds + dt.days * 3600 * 24 , context.ts.step * len( context.ts ))
    
        ts1 = RegularTimeSeries.new( timezone.now( ) , 100)
        ts1.addList( [0 , 1 , 2 , 3 , 4 ] )

        delta_600 = datetime.timedelta( seconds = 600 )
        ts2 = RegularTimeSeries.new( ts1.start + delta_600 , 99 )
        ts2.addList( [0 , 1 , 2 , 3 , 4 ] )

        # ts1 and ts2 are not commensurable - different step
        with self.assertRaises(ValueError):
            ts1.addTimeSeries( ts2 )

        delta_m600 = datetime.timedelta( seconds = -600 )
        ts2 = RegularTimeSeries.new( ts1.start + delta_m600 , 100 )
        ts2.addList( [0 , 1 , 2 , 3 , 4 ] )

        # ts2 must come after ts1
        with self.assertRaises(ValueError):
            ts1.addTimeSeries( ts2 )

        
        
        delta_550 = datetime.timedelta( seconds = 550 )
        ts2 = RegularTimeSeries.new( ts1.start + delta_550 , 100 )
        ts2.addList( [0 , 1 , 2 , 3 , 4 ] )

        # ts1 and ts2 are not commensurable
        with self.assertRaises(ValueError):
            ts1.addTimeSeries( ts2 )

        delta_800 = datetime.timedelta( seconds = 800 )            
        ts2 = RegularTimeSeries.new( ts1.start + delta_800 , 100 )
        ts2.addList( [100 , 10 , 20 , 30 , 40 ] )
        ts1.addTimeSeries( ts2 )
        self.assertEqual( len( ts1 ) , 12 )
        
        self.assertTrue( math.isnan( ts1[5] ))
        self.assertTrue( math.isnan( ts1[6] ))
        self.assertEqual( ts1[7] , 100 )
        self.assertEqual( ts1[11] ,  40 )
