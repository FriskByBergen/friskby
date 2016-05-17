from django.test import TestCase
from pythoncall.models import *

class PythonCallTest(TestCase):
    def setUp(self):
        pass

        
    def test_create(self):
        with self.assertRaises(ValidationError):
            pc = PythonCall.objects.create(description = "Hei",
                                           python_callable = "no.this.does.not.exist")

        with self.assertRaises(ValidationError):
            pc = PythonCall.objects.create(description = "Hei",
                                           python_callable = "math.pi")
        
        pc = PythonCall.objects.create(description = "Hei",
                                       python_callable = "math.exp")

        func = pc.getCallable()
        self.assertEqual( func(0) , 1 )
