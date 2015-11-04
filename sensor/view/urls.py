from django.conf.urls import  url

from views import *
from keys  import *

urlpatterns = [
    url(r'^$'      , MainView.as_view()),
    url(r'^keys/$' , KeyView.as_view())
]
    


