from __future__ import unicode_literals

from django.db.models import *

class Plot(Model):
    name = CharField( max_length = 32 )
    description = CharField( max_length = 256 )
    python_callable = CharField( max_length = 256 )
    html_code = TextField( )

    
    

