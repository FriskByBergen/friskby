from   django.conf.urls import url, include


urlpatterns = [
    url(r'^view/' , include('sensor.view.urls')),
    url(r'^api/'  , include('sensor.api.urls'))
]

