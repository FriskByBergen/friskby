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
    url(r'^device_type/$' , DeviceTypeList.as_view()),
    url(r'^device_type/(?P<pk>[0-9]+)/$' , DeviceType.as_view()),
    #
    url(r'^device/$' , DeviceList.as_view()),
    url(r'^device/(?P<pk>%s)/$' % models.Device.IDPattern, Device.as_view()),
    #
    url(r'^location/$' , LocationList.as_view()),
    url(r'^location/(?P<pk>[0-9]+)/$' , Location.as_view()),
    #
    url(r'^data_type/$' , DataTypeList.as_view()),
    url(r'^data_type/(?P<pk>[0-9]+)/$' , DataType.as_view()),
    #
    url(r'^timestamp/$' , TimeStampList.as_view()),
    url(r'^timestamp/(?P<pk>[0-9]+)/$' , TimeStamp.as_view()),
    #
    url(r'^datainfo/$' , DataInfoList.as_view()),
    url(r'^datainfo/(?P<pk>[0-9]+)/$' , DataInfo.as_view()),
    #
    url(r'^datavalue/$' , DataValueList.as_view()),
    url(r'^datavalue/(?P<pk>[0-9]+)/$' , DataValue.as_view()),
    #
    url(r'^sensortype/$' , SensorTypeList.as_view()),
    url(r'^sensortype/(?P<pk>[0-9]+)/$' , SensorType.as_view()),
    #
    url(r'^sensor/$' , SensorList.as_view()),
    url(r'^sensor/(?P<pk>%s)/$' % models.Sensor.IDPattern , Sensor.as_view()),
    #
    url(r'^sensorinfo/$' , SensorInfo.as_view()),
    url(r'^sensorinfo/(?P<sensor_id>%s)/$' % models.Sensor.IDPattern , SensorInfo.as_view()),
    #
    url(r'^reading/$'            , Reading.as_view()),
    url(r'^reading/(?P<sensor_id>%s)/$' % models.Sensor.IDPattern , Reading.as_view()),
    #
    url(r'^current/$'   , CurrentValue.as_view()),
    url(r'^current/(?P<sensor_id>%s)/$' % models.Sensor.IDPattern , CurrentValue.as_view())
]


urlpatterns = format_suffix_patterns(urlpatterns)
