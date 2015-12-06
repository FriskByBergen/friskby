from   django.conf.urls import  patterns, url, include
from   rest_framework.urlpatterns import format_suffix_patterns
from filter.models import *
from sensor.models import *

from .api_views import *

urlpatterns = [
    url(r'^data/$' , FilterDataView.as_view()),
    url(r'^data/(?P<sensor_id>%s)/$' % Sensor.IDPattern , FilterDataView.as_view()),
    url(r'^data/(?P<sensor_id>%s)/(?P<filter_id>%s)/$' % (Sensor.IDPattern , Filter.IDPattern) , FilterDataView.as_view())
]


urlpatterns = format_suffix_patterns(urlpatterns)
