import numpy
from django.db.models import *


class NumpyArrayField(BinaryField):
    value_type = numpy.float32

    def load_numpy_array(self , blob):
        return numpy.fromstring(blob , self.dtype)

    def __init__(self , *args , **kwargs):
        kwargs['default'] = None
        if "dtype" in kwargs:
            self.dtype = kwargs["dtype"]
            del kwargs["dtype"]
        else:
            self.dtype = self.value_type
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
