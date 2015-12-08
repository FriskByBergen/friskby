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
