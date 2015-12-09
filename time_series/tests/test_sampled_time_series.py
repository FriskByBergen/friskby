import time
import datetime
from django.db import IntegrityError
from django.utils import dateparse , timezone
from django.test import TestCase
from time_series.models import *
from .context import TestContext

class SampledTimeSeriesTest(TestCase):

    def test_create(self):
        stamp = TimeArray.new( )
        ts = SampledTimeSeries.new( stamp )
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
        ts.addPair( now3 , 119 )
        self.assertEqual( len(ts) , 3 )
        self.assertEqual( ts[2] , (now3 , 119 ))

        # Must be increasing 
        with self.assertRaises(ValueError):
            ts.addPair( numpy.datetime64('2013-10-22T03:30Z') , 119 )
        self.assertEqual( len(ts) , 3 )

        ts.addPairList( [now3 , now3] , [119,120] )
        self.assertEqual( len(ts) , 5 )
        
        with self.assertRaises(ValueError):
            ts.addPairList( [now0 , now0] , [119,120] )
        self.assertEqual( len(ts) , 5 )

        with self.assertRaises(ValueError):
            ts.addPair( numpy.datetime64('2013-10-22T03:30Z') , 119 )
        self.assertEqual( len(ts) , 5 )
