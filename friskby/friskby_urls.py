from   django.conf.urls import url, include
        
from home import Home

urlpatterns = [
    url(r''   , Home.as_view())
]
