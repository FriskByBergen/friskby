from   django.conf.urls import url, include


urlpatterns = [
    url(r'^api/'  , include('time_series.api.urls'))
]

