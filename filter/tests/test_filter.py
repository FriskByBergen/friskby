import datetime
import math
from unittest import TestCase

from filter.filter import *

class FilterTest(TestCase):
    
    def test_count(self):
        start = datetime.datetime(2015 , 12 , 1 , 12 , 0 , 0 )
        
        #    [     4     |     0    |     2    >
        #  12:00       13:00      14:00      15:00 
        
        data = []
        data.append( (start + datetime.timedelta( seconds = 100 ) , 1) )
        data.append( (start + datetime.timedelta( seconds = 200 ) , 1) )
        data.append( (start + datetime.timedelta( seconds = 300 ) , 1) )
        data.append( (start + datetime.timedelta( seconds = 400 ) , 1) )

        data.append( (start + datetime.timedelta( seconds = 7300 ) , 1) )
        data.append( (start + datetime.timedelta( seconds = 7400 ) , 1) )
        
        cnt = count( start , 3600 , data )
        self.assertEqual( cnt[0] , 4 )
        self.assertEqual( cnt[1] , 0 )
        self.assertEqual( cnt[2] , 2 )


    def test_mean(self):
        start = datetime.datetime(2015 , 12 , 1 , 12 , 0 , 0 )
        
        #    [     4     |     0    |     2    >
        #  12:00       13:00      14:00      15:00 
        
        data = []
        data.append( (start + datetime.timedelta( seconds = 100 ) , 2) )
        data.append( (start + datetime.timedelta( seconds = 200 ) , 2) )
        data.append( (start + datetime.timedelta( seconds = 300 ) , 4) )
        data.append( (start + datetime.timedelta( seconds = 400 ) , 4) )

        data.append( (start + datetime.timedelta( seconds = 7300 ) , 50) )
        data.append( (start + datetime.timedelta( seconds = 7400 ) , 10) )
        
        mean = blockedMean( start , 3600 , data )
        self.assertEqual( mean[0] , 3 )
        self.assertTrue( math.isnan( mean[1] ))
        self.assertEqual( mean[2] , 30 )
        
        
