from django.conf.urls import  url

from views import *

urlpatterns = [
    url(r'^$' , MainView.as_view())
]


