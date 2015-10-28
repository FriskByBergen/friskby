from django.test import TestCase
from sensor.models import *
from .context import TestContext


class DataValueTest(TestCase):


    def test_create(self):
        context = TestContext( )
        data_value = DataValue( data_type = context.raw_data ,
                                data_info = context.data_info1 , 
                                value = 1000 )

        #with self.assertRaises(ValueError):
        #    data_value.save()
        #
        #data_value.value = 50
        #data_value.save( ) 
        
