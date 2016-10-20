from   django.conf.urls import url, include
        
from views import Home
from views import Adm
from views import JSHome

urlpatterns = [
    url(r'^friskby/adm/$' , Adm.as_view()),
    url(r'friskby/$'      , Home.as_view()),
    url(r'^$'             , JSHome.as_view())
]
