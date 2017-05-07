from django.conf.urls import  url

import sensor.models as models
from views import *
from keys  import *

urlpatterns = [
    url(r'^$' , MainView.as_view(), name = "sensor.view.main"),
    url(r'^device/(?P<pk>%s)/$' % models.Device.IDPattern, DeviceView.as_view() , name = "view.device.info"),
    url(r'^keys/$' , KeyView.as_view(), name = "key.view.main")
]
