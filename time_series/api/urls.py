from   django.conf.urls import  patterns, url, include
from   rest_framework.urlpatterns import format_suffix_patterns
import time_series.models as models

from .api_views import *

urlpatterns = [
    url(r'^regular/(?P<ts_id>[0-9]+)/$' , RegularTimeSeriesView.as_view()),
    #
    url(r'^sampled/(?P<ts_id>[0-9]+)/$' , SampledTimeSeriesView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
