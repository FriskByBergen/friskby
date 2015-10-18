from   django.conf.urls import  patterns, url, include
from   rest_framework.urlpatterns import format_suffix_patterns
import sensor.models as models

from api_views import *

urlpatterns = [
    url(r'^measurement_type/$' , MeasurementTypeList.as_view()),
    url(r'^measurement_type/(?P<pk>[0-9]+)/$' , MeasurementType.as_view()),
    #
    url(r'^company/$' , CompanyList.as_view()),
    url(r'^company/(?P<pk>[0-9]+)/$' , Company.as_view()),
    #
    url(r'^device/$' , DeviceList.as_view()),
    url(r'^device/(?P<pk>[0-9]+)/$' , Device.as_view()),
    #
    url(r'^location/$' , LocationList.as_view()),
    url(r'^location/(?P<pk>[0-9]+)/$' , Location.as_view()),
    #
    url(r'^sensorID/$' , SensorIDList.as_view()),
    url(r'^sensorID/(?P<pk>%s)/$' % models.SensorID.IDPattern , SensorID.as_view()),
    #
    url(r'^sensorinfo/$' , SensorInfo.as_view()),
    url(r'^sensorinfo/(?P<sensor_id>%s)/$' % models.SensorID.IDPattern , SensorInfo.as_view()),
    #
    url(r'^reading/$'            , Reading.as_view()),
    url(r'^reading/(?P<sensor_id>%s)/$' % models.SensorID.IDPattern , Reading.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
