import math
import datetime
import numpy
from django.db.models import *


class NumpyArrayField(BinaryField):
    dtype = numpy.float32

    @classmethod
    def load_numpy_array(cls , blob):
        return numpy.fromstring(blob , NumpyArrayField.dtype)

    def __init__(self , *args , **kwargs):
        kwargs['default'] = None
        super(NumpyArrayField , self).__init__(*args , **kwargs)


    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.load_numpy_array( value )


    def to_python(self, value):
        if isinstance(value, numpy.ndarray):
            return value

        if value is None:
            return value

        return self.load_numpy_array( value )


def createArray(size = 0):
    return numpy.ndarray( shape = [size] , dtype = NumpyArrayField.dtype)


class RegularTimeSeries(Model):
    start = DateTimeField( )
    step = IntegerField( )
    data = NumpyArrayField( )


    def __unicode__(self):
        return "TimeSeries: %s" % self.id

    @classmethod
    def createArray(cls , size = 0):
        return numpy.ndarray( shape = [size] , dtype = NumpyArrayField.dtype)

    @classmethod
    def new(cls , start , step):
        if step <= 0:
            raise ValueError("The step variable must be positive")

        ts = cls( start = start , 
                  step = step ,
                  data = RegularTimeSeries.createArray( ) )
        return ts


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
            shape = self.data.shape
            return shape[0]
    

    def addValue(self , value):
        new_size = self.data.shape[0] + 1
        self.data.resize( [ new_size ] )
        self.data[new_size -1] = value
        

    def addList(self , data):
        if len(data) > 0:
            old_size = self.data.shape[0]
            new_size = old_size + len(data)
            self.data.resize( [ new_size ] )

            index = old_size
            for v in data:
                self.data[index] = v
                index += 1

    def addTimeSeries(self , ts):
        if self.step != ts.step:
            raise ValueError("The two timeseries must have the same step length")

        last = self.lastTime()
        if ts.start <= last:
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
        
