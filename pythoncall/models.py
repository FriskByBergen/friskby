from __future__ import unicode_literals
import importlib

from django.core.exceptions import ValidationError
from django.db.models import *


class PythonCall(Model):
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
        super(PythonCall, self).save( *args, **kwargs)

