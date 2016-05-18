import importlib
import datetime
import pytz

from django.db.models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from time_series.models import *
from time_series.numpy_field import * 
from sensor.models import *
from pythoncall.models import * 



    
class Filter(Model):
    IDPattern = "[-_:a-zA-Z0-9]+"
    
    id = CharField(max_length = 60 , primary_key = True , validators = [RegexValidator(regex = "^%s$" % IDPattern)])
    description = CharField( max_length= 256 )
    width = IntegerField( )
    python_code = ForeignKey( PythonCall )

    def __unicode__(self):
        return self.description


    def getCallable(self):
        return self.python_code.getCallable( )


class Transform(Model):
    IDPattern = "[-_:a-zA-Z0-9]+"
    
    id = CharField(max_length = 60 , primary_key = True , validators = [RegexValidator(regex = "^%s$" % IDPattern)])
    description = CharField( max_length= 256 )
    python_code = ForeignKey( PythonCall )


    def __unicode__(self):
        return self.description


    def getCallable(self):
        return self.python_code.getCallable( )




class FilterData(Model):
    sensor = ForeignKey( Sensor )
    filter_code = ForeignKey( Filter )
    ts = OneToOneField( RegularTimeSeries , on_delete = CASCADE)

    def __unicode__(self):
        return "%s : %s" % (self.sensor , self.filter_code)

    class Meta:
        unique_together = ('sensor' , 'filter_code')
        

    @classmethod
    def update(cls , sensor , filter_ , transform = None ):
        try:
            fd = FilterData.objects.get( sensor = sensor , filter_code = filter_ )
            start = fd.ts.lastTime( )
        except FilterData.DoesNotExist:
            fd = None
            start = None
            
        try:
            sd = SampledData.objects.get( sensor = sensor , 
                                          transform = transform )
        except SampledData.DoesNotExist:
            sd = None
            
        if sd is None:
            return None

        ts = sd.data.export( start = start )
        if len(ts):
            new_fd = False
            if fd is None:
                new_fd = True
                data_start = ts[0][0]
                seconds = data_start.second + 60 * data_start.minute
                if filter_.width > 3600:
                    seconds += data_start.hour * 3600

                data_start -= datetime.timedelta( seconds = seconds )
                    
                fd = FilterData( sensor = sensor , 
                                 filter_code = filter_ )
            else:
                data_start = fd.ts.lastTime( )
                                 

                
            func = fd.filter_code.getCallable( )
            filtered_ts = RegularTimeSeries( start = data_start , 
                                             step = filter_.width)
            filtered_ts.addList( func( data_start , filter_.width , ts ) )

            if new_fd:
                filtered_ts.save( )
                fd.ts = filtered_ts
            else:
                fd.ts.addTimeSeries( filtered_ts )

            fd.save( )

        return fd



class SampledData(Model):
    sensor = ForeignKey( Sensor )
    data = OneToOneField( SampledTimeSeries , on_delete = CASCADE )
    parent_data = ForeignKey( "SampledData" , null = True )
    transform = ForeignKey( Transform , null = True )
    
    def __unicode__(self):
        if self.transform is None:
            return "<%s : Rawdata>" % self.sensor 
        else:
            return "<%s : %s>" % (self.sensor , self.transform)

    class Meta:
        unique_together = ('sensor' , 'transform')

    def __len__(self):
        return len(self.data)

    def save(self , *args , **kwargs):
        self.data.save( )
        super(SampledData , self).save( *args , **kwargs)


    @classmethod
    def updateSampledData( cls , sensor , transform):    
        if transform is None:
            cls.updateRawData( sensor )
        else:
            raise NotImplementedError("not implemented...")


    @classmethod
    def updateRawData( cls , sensor ):
        try:
            sd = SampledData.objects.get( sensor = sensor , transform = None)
            start = sd.data.lastTime( )
            start = start.replace( tzinfo = pytz.UTC )
        except SampledData.DoesNotExist:
            sd = None
            start = None
            
        qs = sensor.get_rawdata( )
        if len(qs):
            if sd is None:
                timestamp = TimeArray.objects.create( )
                data = SampledTimeSeries( timestamp = timestamp )
                data.save( )

                sd = SampledData( sensor = sensor , 
                                  data = data , 
                                  parent_data = None,
                                  transform = None )

            ts_list = [ 0 ] * len(qs)
            values = [ 0 ] * len(qs)

            for i in range(len(qs)):
                ts_list[i] = qs[i][1]
                values[i] = qs[i][2]
            
            data = sd.data
            data.addPairList( ts_list , values )
            sd.save()
            qs.update( status = RawData.PROCESSED )

        return sd


