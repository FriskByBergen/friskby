import time
import datetime
from django.db import IntegrityError
from django.utils import dateparse , timezone
from django.test import TestCase
from time_series.models import *
from .context import TestContext

class SampledTimeSeriesTest(TestCase):

    def test_create(self):
        stamp = TimeArray( )
        stamp.save( ) 
        ts = SampledTimeSeries( timestamp = stamp )
        self.assertEqual( len(ts) , 0 )

        now0 = TimeArray.now( )
        ts.addPair( now0 , 100 )
        self.assertEqual( len(ts) , 1 )
        
        stamp.addValue( TimeArray.now( ) )
        with self.assertRaises(IntegrityError):
            ts.addPair( TimeArray.now( ) , 100 )
            
        time.sleep( 1 )
        ts.addValue( 100 )
        now3 = TimeArray.now( )
        now3 = now3.replace( microsecond = 0 )
        ts.addPair( now3 , 119 )
        self.assertEqual( len(ts) , 3 )
        self.assertEqual( ts[2] , (now3 , 119 ))

        # Must be increasing 
        with self.assertRaises(ValueError):
            ts.addPair( TimeArray.parse_datetime('2013-10-22T03:30Z') , 119 )
        self.assertEqual( len(ts) , 3 )

        ts.addPairList( [now3 , now3] , [119,120] )
        self.assertEqual( len(ts) , 5 )
        
        self.assertEqual( ts.length( ) , 5 )
        self.assertEqual( ts.max( ) , 120 )
        self.assertEqual( ts.min( ) , 100 )
        self.assertTrue( abs(ts.avg( )  -  (100 + 100 + 119 + 119 + 120)/5.0) < 1e-5)
        
        with self.assertRaises(ValueError):
            ts.addPairList( [now0 , now0] , [119,120] )
        self.assertEqual( len(ts) , 5 )

        with self.assertRaises(ValueError):
            ts.addPair( TimeArray.parse_datetime('2013-10-22T03:30Z') , 119 )
        self.assertEqual( len(ts) , 5 )

        x = range(10)
        ts.addPairList( [ now3 ] * len(x) , x )
        ts.save()
        id = ts.id

        ts2 = SampledTimeSeries.objects.get( pk = id )
        
