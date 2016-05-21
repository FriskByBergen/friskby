from   django.conf.urls import url, include
        
from views import Root

urlpatterns = [
    url(r'^$'    , Root.as_view())
]
