import datetime
import time
from django.utils import dateparse , timezone
from django.test import TestCase
from time_series.models import *
from .context import TestContext


class TimeArrayTest(TestCase):

    def test_create(self):
        ta = TimeArray( )
        self.assertEqual(len(ta) , 0)
        
        now = TimeArray.now( )
        now = now.replace( microsecond = 0 )
        ta.addValue( now )
        self.assertEqual(len(ta) , 1)
        self.assertEqual( ta[0], now )

        self.assertEqual( ta.length() , 1 )
        self.assertEqual( ta.end() , now )
        self.assertEqual( ta.start() , now )

        now2 = TimeArray.now( )
        now2 = now2.replace( microsecond = 0 )
        ta[0] = now2
        self.assertEqual(ta[0], now2)


    def test_increasing(self):
        ta1 = TimeArray(  )
        ta1.save( )
        ta2= TimeArray(  )
        ta2.increasing = False
        
        now0 = TimeArray.now( )
        ta1.addValue( now0 )
        ta2.addValue( now0 )
       
        with self.assertRaises(ValueError):
            ta1.addValue( TimeArray.parse_datetime('2013-10-22T03:30Z') )
        self.assertEqual( len(ta1) , 1 )
        ta2.addValue( TimeArray.parse_datetime('2013-10-22T03:30Z') )
        
        with self.assertRaises(ValueError):
            ta1.addList( [ TimeArray.parse_datetime('2013-10-22T03:30Z') , TimeArray.parse_datetime('2013-11-22T03:30Z')]) 

        ta1 = TimeArray( )
        ta1.addValue( TimeArray.parse_datetime('2013-09-22T03:30Z') )
        self.assertEqual( len(ta1) , 1 )
        with self.assertRaises(ValueError):
            ta1.addList( [ TimeArray.parse_datetime('2013-11-22T03:30Z') , TimeArray.parse_datetime('2013-10-22T03:30Z')]) 
        self.assertEqual( len(ta1) , 1 )



