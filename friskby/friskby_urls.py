from   django.conf.urls import url, include
        
from views import Home
from views import Adm

urlpatterns = [
    url(r'^$'    , Home.as_view()),
    url(r'adm/$' , Adm.as_view())
]
