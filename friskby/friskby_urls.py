from   django.conf.urls import url, include
        
from views import Home
from views import Adm
from views import JSHome
from views import Quick

urlpatterns = [
    url(r'^friskby/adm/$' , Adm.as_view(), name = "friskby.view.adm"),
    url(r'quick/$'        , Quick.as_view(), name = "friskby.view.quick"),
    url(r'friskby/$'      , Home.as_view()),
    url(r'^$'             , JSHome.as_view())
]
