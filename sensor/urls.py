from   django.conf.urls import url, include

urlpatterns = [
    url(r'^api/' , include('sensor.api.urls'))
]

