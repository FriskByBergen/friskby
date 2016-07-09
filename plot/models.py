from __future__ import unicode_literals

import pytz
import datetime
from django.db.models import *
from pythoncall.models import * 
from sensor.models import *

from . import lib

class Plot(Model):
    name = CharField( max_length = 32 )
    description = CharField( max_length = 256 )
    tag = CharField( max_length = 128 , blank = True )

    # Derived class can implement plotting inline in the updatePlot( )
    # method, therefor this can be null and void.
    python_callable = ForeignKey( PythonCall , blank = True , null = True) 
    html_code = TextField( blank = True )
    last_update = DateTimeField( blank = True)

    def __unicode__(self):
        return self.description

        
    def updatePlot(self):
        try:
            if self.python_callable is None:
                raise ValidationError("No callable")

            func = self.python_callable.getCallable( )
        except:
            raise ValidationError("Import python callable:%s failed" % self.python_callable)

        new_html = func( )

        if new_html:
            self.html_code = new_html
            self.last_update = datetime.datetime.now( pytz.utc )
            super(Plot , self).save( )
        else:
            raise ValidationError("Python callable produced an empty string")
        
            
    @classmethod
    def select(cls , regexp):
        return Plot.objects.filter( tag__iregex=regexp)
            
        

    def save(self, *args, **kwargs):
        if not self.html_code:
            self.updatePlot( )
        else:
            super(Plot , self).save( *args , **kwargs )


    def nextId(self):
        try:
            ret = Plot.objects.filter(id__gt=self.id).order_by("id")[0:1].get().id
        except Plot.DoesNotExist:
            ret = Plot.objects.aggregate(Min("id"))['id__min']
        return ret


    def prevId(self):
        try:
            ret = Plot.objects.filter(id__lt=self.id).order_by("id")[0:1].get().id
        except Plot.DoesNotExist:
            ret = Plot.objects.aggregate(Max("id"))['id__max']
        return ret

            


class DevicePlot(Plot):
    device = ForeignKey( Device )
    duration = DurationField( blank = True , null = True )

    @classmethod
    def makeDurationTag(cls , duration):
        days = duration.days
        seconds = duration.seconds
                
        hours = 1.0 * seconds / 3600
        minutes = 1.0 * seconds / 60

        if days > 0:
            return "%dD" % days

        if hours > 0:
            return "%dH" % hours

        if minutes > 0:
            return "%dM" % minutes

        if seconds > 0:
            return "%dS" % seconds


        

    def save(self, *args, **kwargs):
        if self.description is None:
            self.description = "Timeseries plot of sensors on:%s" % self.device.id

        if self.tag == "":
            if self.duration is None:
                self.tag = "DEV:%s" % self.device.id
            else:
                if self.duration.total_seconds( ) <= 0:
                    raise ValueError("Duration must be positive")
                
                self.tag = "DEV:%s:%s" % (self.device.id , self.makeDurationTag( self.duration ))

        super(DevicePlot , self).save( *args , **kwargs )



    def updatePlot(self):
        try:
            func = lib.device_plot
        except:
            raise ValidationError("Import python callable:%s failed" % self.python_callable)

        new_html = func( self.device , self.duration )
        if new_html:
            self.html_code = new_html
            self.last_update = datetime.datetime.now( pytz.utc )
            super(Plot , self).save( )
        else:
            raise ValidationError("Python callable produced an empty string")

