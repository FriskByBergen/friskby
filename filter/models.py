import importlib

from django.db.models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from time_series.models import *
from sensor.models import *




class PythonCode(Model):
    description = CharField( max_length= 256 )
    python_callable = CharField( max_length = 128 )
    

    def __unicode__(self):
        return self.python_callable


    def getCallable(self):
        name_list = self.python_callable.split(".")
        module_name = ".".join( name_list[:-1] )
        func_name = name_list[-1]
        try:
            module = importlib.import_module( module_name )
        except ImportError:
            raise ValidationError("Could not import symbol:%s" % self.python_callable)
        
        try:
            func = getattr(module , func_name)
            if not callable(func):
                raise ValidationError("Symbol is not callable")
        except Exception:
            raise ValidationError("Could not import symbol:%s" % self.python_callable)
            
        return func

    def save(self , *args , **kwargs):
        func = self.getCallable( )
        super(PythonCode, self).save( *args, **kwargs)


    

    
class Filter(Model):
    IDPattern = "[-_:a-zA-Z0-9]+"
    
    id = CharField(max_length = 60 , primary_key = True , validators = [RegexValidator(regex = "^%s$" % IDPattern)])
    description = CharField( max_length= 256 )
    width = IntegerField( )
    code = ForeignKey( PythonCode )


    def __unicode__(self):
        return self.description


    def getCallable(self):
        return self.code.getCallable( )



class FilterData(Model):
    sensor = ForeignKey( Sensor )
    filter_code = ForeignKey( Filter )
    ts = ForeignKey( RegularTimeSeries )

    def __unicode__(self):
        return "%s : %s" % (self.sensor , self.filter_code)

    class Meta:
        unique_together = ('sensor' , 'filter_code')
        

    @classmethod
    def update(cls , sensor , filter_):
        try:
            fd = FilterData.objects.get( sensor = sensor , filter_code = filter_ )
            start = fd.ts.lastTime( )
        except FilterData.DoesNotExist:
            fd = None
            start = None
        
        ts = sensor.get_ts( start = start )
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
            filtered_ts = RegularTimeSeries.new( data_start , filter_.width)
            filtered_ts.addList( func( data_start , filter_.width , ts ) )

            if new_fd:
                filtered_ts.save( )
                fd.ts = filtered_ts
            else:
                fd.ts.addTimeSeries( filtered_ts )

            fd.save( )

        return fd

