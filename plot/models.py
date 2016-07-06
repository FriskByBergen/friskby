from __future__ import unicode_literals

import pytz
import datetime
from django.db.models import *
from pythoncall.models import * 


class Plot(Model):
    name = CharField( max_length = 32 )
    description = CharField( max_length = 256 )
    tag = CharField( max_length = 128 )
    python_callable = ForeignKey( PythonCall )
    html_code = TextField( blank = True )
    last_update = DateTimeField( blank = True)

    def __unicode__(self):
        return self.description

        
    def updatePlot(self):
        try:
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
        
            
        

    def save(self, *args, **kwargs):
        if not self.html_code:
            self.updatePlot( )
        else:
            super(Plot , self).save( *args , **kwargs )

