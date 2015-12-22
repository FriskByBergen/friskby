import datetime
import time
import calendar
import math
import pytz
import numpy
from django.conf import settings
from django.utils import timezone, dateparse
from django.db.models import *
from django.db import IntegrityError
from .numpy_field import *

class OperatorMixin(object):

    def __getitem__(self , index):
        if self.data is None:
            raise IndexError
        else:
            return self.data[index]
        
    def __setitem__(self , index , value):
        if self.data is None:
            raise IndexError
        else:
            self.data[index] = value
        
    def __len__(self):
        if self.data is None:
            return 0
        else:
            return len(self.data)

    def last(self):
        return self[-1]


    def resize(self , new_size):
        self.data.resize( [ new_size ] )


    def addValue(self , value):
        if self.data is None:
            new_size = 1
            self.data = self.createArray( size = new_size )
        else:
            new_size = self.data.shape[0] + 1
            self.resize( new_size )

        self.data[new_size -1] = value


    
    def addList(self , data):
        if len(data) > 0:
            if self.data is None:
                new_size = len(data)
                self.data = RegularTimeSeries.createArray( size = new_size )
                old_size = 0
            else:
                old_size = self.data.shape[0]
                new_size = old_size + len(data)
                self.resize( new_size )

            index = old_size
            for v in data:
                self.data[index] = v
                index += 1




class TimeArray(Model, OperatorMixin):
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    # When parsing a string the format should be as: "2015-10-10T10:10:00+01";
    # i.e. yyyy-mm-ddTHH:MM:SS+z1
    # Where the +zz is a timezone shift relative to UTC; i.e. +01 for Central European Time.
    increasing = True
    data = NumpyArrayField( dtype = NumpyArrayField.date_type )
    time_zone = pytz.timezone( settings.TIME_ZONE )



    @classmethod
    def createArray(cls, size = 0):
        return numpy.ndarray( shape = [size] , dtype = NumpyArrayField.date_type )
        

    @classmethod
    def new(cls , increasing = True):
        ts = cls( data = TimeArray.createArray( ) )
        ts.increasing = increasing
        return ts


    def save(self, *args, **kwargs):
        super(TimeArray , self).save( *args , **kwargs )

    
    # This takes a time_string which is supposed to be in the time
    # zone given by the settings.TIME_ZONE variable. The resulting
    # dt variable is a time zone aware datetime instance.
    @classmethod
    def parse_datetime(cls , time_string ):
        dt = dateparse.parse_datetime( time_string )
        return dt

    @classmethod
    def create(cls , time = None):
        if time is None:
            time = timezone.now()
        return time.strftime(cls.DATETIME_FORMAT)


    @classmethod
    def now(cls):
        return timezone.now( )


    @classmethod
    def datetime2EpochSeconds(cls , dt):
        return int(calendar.timegm( dt.timetuple() ))


    @classmethod
    def epochSeconds2Datetime(cls , dt):
        return datetime.datetime.fromtimestamp( epoch_seconds , self.time_zone )


    def __getitem__(self , index):
        if self.data is None:
            raise IndexError
        else:
            epoch_seconds = self.data[index]
            dt = datetime.datetime.fromtimestamp( epoch_seconds , self.time_zone )
            return dt


    def __setitem__(self , index , dt):
        if self.data is None:
            raise IndexError
        else:
            self.data[index] = self.datetime2EpochSeconds( dt )


    def export(self):
        l = [0] * len(self)
        index = 0
        for t in self:
            l[index] = t
            index += 1
        return l


    def addValue(self , value):
        value = self.datetime2EpochSeconds(value)
        if self.data is None:
            new_size = 1
            self.data = self.createArray( size = new_size )
        else:
            new_size = self.data.shape[0] + 1
            if new_size >= 2:
                prev_value = self.data[ new_size - 2 ]
                if self.increasing and value < prev_value:
                    raise ValueError("Elements must be weakly increasing")
                
            self.resize( new_size )

        self.data[new_size -1] = value


    
    def addList(self , data):
        if len(data) > 0:
            if self.data is None:
                new_size = len(data)
                self.data = RegularTimeSeries.createArray( size = new_size )
                old_size = 0
            else:
                old_size = self.data.shape[0]
                new_size = old_size + len(data)
                self.resize( new_size )

            index = old_size
            for v in data:
                s = self.datetime2EpochSeconds(v)
                if index > 0 and self.increasing:
                    if s < self.data[index - 1]:
                        msg = "Elements must be weakly increasing %s < %s" % (s , self.data[index - 1])
                        self.resize( old_size )
                        raise ValueError( msg )

                self.data[index] = s
                index += 1
                

    


class RegularTimeSeries(Model, OperatorMixin):
    start = DateTimeField( )
    step = IntegerField( )
    data = NumpyArrayField( dtype = NumpyArrayField.value_type )


    def __unicode__(self):
        return "TimeSeries: %s" % self.id

    @classmethod
    def createArray(cls , size = 0 ):
        return numpy.ndarray( shape = [size] , dtype = NumpyArrayField.value_type )

    @classmethod
    def new(cls , start , step):
        if step <= 0:
            raise ValueError("The step variable must be positive")

        ts = cls( start = start , 
                  step = step ,
                  data = RegularTimeSeries.createArray(  ))
        return ts



    def addTimeSeries(self , ts):
        if self.step != ts.step:
            raise ValueError("The two timeseries must have the same step length")

        last = self.lastTime()
        if ts.start < last:
            raise ValueError("The next timeseries must come _after_ self in time")

        diff = ts.start - last
        int_value = int(0.5 + diff.seconds / self.step)
        float_value = 1.0 * diff.seconds / self.step
        delta = abs(float_value - int_value)
        
        if delta > 1e-3:
            raise ValueError("The timeseries must be commensurable")

        if int_value > 1:
            nan_list = [ float("nan") ] * (int_value - 1)
            self.addList( nan_list )
        
        self.addList( ts )


                
    def export(self):
        return {"start" : self.start , 
                "step"  : self.step ,
                "data"  : self.data.tolist() }


    def lastTime(self):
        last = self.start
        return self.start + datetime.timedelta( seconds = len(self.data) * self.step )



class SampledTimeSeries(Model, OperatorMixin):        
    timestamp = ForeignKey( TimeArray )
    data = NumpyArrayField( dtype = NumpyArrayField.value_type )

    @classmethod
    def new(cls , timestamp , size = 0):
        ts = cls( timestamp = timestamp , 
                  data = numpy.ndarray( shape = [size] , dtype = NumpyArrayField.value_type ))
        return ts


    def save(self, *args, **kwargs):
        self.timestamp.save()
        super(SampledTimeSeries , self).save( *args , **kwargs )


    def assertSize(self):
        if len(self.timestamp) != len(self):
            raise IntegrityError("Timestamp and data not equally long");
        

    def addPair(self , ts , value):
        self.assertSize( )
        size0 = len(self)
        try:
            self.timestamp.addValue( ts )
            self.addValue( value )
        except ValueError:
            self.resize( size0 )
            self.timestamp.resize( size0 )
            raise ValueError
        


    def addPairList(self , ts , values):
        self.assertSize( )
        if len(ts) != len(values):
            raise ValueError( )

        size0 = len(self)
        try:
            self.timestamp.addList( ts )
            self.addList( values )
        except ValueError as e:
            self.resize( size0 )
            self.timestamp.resize( size0 )
            raise ValueError( str(e) )

    
    def __getitem__(self, index):
        self.assertSize( )
        if self.data is None:
            return None
        else:
            if index < len(self):
                return (self.timestamp[index] , self.data[index])
            else:
                raise IndexError
    
    def export(self):
        self.assertSize()
        return {"timestamp" : self.timestamp.export(),
                "data" : self.data.tolist() }
        

    def lastTime(self):
        return self.timestamp.last() 
