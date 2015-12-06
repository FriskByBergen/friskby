from   django.conf.urls import  patterns, url, include
from   rest_framework.urlpatterns import format_suffix_patterns
import time_series.models as models

from .api_views import *

urlpatterns = [
    url(r'^$'                   , TimeSeriesView.as_view()),
    url(r'^(?P<ts_id>[0-9]+)/$' , TimeSeriesView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
