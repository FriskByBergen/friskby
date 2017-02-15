from django.conf.urls import url, include

from views import Home
from views import Adm
from views import JSHome
from views import Quick

urlpatterns = [
    url(r'^friskby/adm/$' , Adm.as_view(), name = "friskby.view.adm"),
    url(r'friskby/$'      , Home.as_view()),
    url(r'legacy/$'       , JSHome.as_view()),
    url(r'^$'             , Quick.as_view(), name = "friskby.view.quick")
]
