from django.contrib import admin

from models import *

admin.site.register( SampledTimeSeries )
admin.site.register( RegularTimeSeries )
admin.site.register( TimeArray )
