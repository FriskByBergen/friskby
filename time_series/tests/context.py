from django.utils import timezone
from time_series.models import *

class TestContext(object):
    def __init__(self):
        self.ts = TimeSeries.new( timezone.now(), 100 )
        self.ts.addList( range(10) )
        self.ts.save()
    
