from django.utils import timezone
from time_series.models import *

class TestContext(object):
    def __init__(self):
        self.ts = RegularTimeSeries( start = timezone.now() , step = 100 )
        self.ts.addList( range(10) )
        self.ts.save()
    
