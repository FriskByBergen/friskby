from   django.conf.urls import  url, include
from   rest_framework.urlpatterns import format_suffix_patterns
from filter.models import *
from sensor.models import *

from .api_views import *

urlpatterns = [
    url(r'^filter_data/$', FilterDataView.as_view(), name="api.filter.overview"),
    url(r'^filter_data/(?P<sensor_id>%s)/$' % Sensor.IDPattern , FilterDataView.as_view(), name="api.filter.sensor"),
    url(r'^filter_data/(?P<sensor_id>%s)/(?P<filter_id>%s)/$' % (Sensor.IDPattern , Filter.IDPattern) , FilterDataView.as_view(), name="api.filter.data"),
    #
    url(r'^sampled_data/$' , SampledDataView.as_view(), name="api.sampled.overview"),
    url(r'^sampled_data/(?P<sensor_id>%s)/$' % Sensor.IDPattern  , SampledDataView.as_view(), name="api.sampled.sensor"),
    url(r'^sampled_data/(?P<sensor_id>%s)/(?P<transform_id>%s)/$' % (Sensor.IDPattern , Filter.IDPattern) , SampledDataView.as_view(), name="api.sampled.data")
]


urlpatterns = format_suffix_patterns(urlpatterns)
