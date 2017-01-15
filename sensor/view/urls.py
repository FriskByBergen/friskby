from django.conf.urls import  url

from views import *
from keys  import *

urlpatterns = [
    url(r'^$'      , MainView.as_view(), name = "sensor.view.main"),
    url(r'^keys/$' , KeyView.as_view(), name = "key.view.main")
]
    


