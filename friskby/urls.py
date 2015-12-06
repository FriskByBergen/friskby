"""friskby URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

import filter.urls
import sensor.urls
import time_series.urls
import friskby_urls

urlpatterns = [
    url(r'^accounts/login/$'  , auth_views.login,{'template_name': 'admin/login.html'}),
    url(r'^admin/'            , include(admin.site.urls)),
    url(r'^sensor/'           , include(sensor.urls)),
    url(r'^time_series/'      , include(time_series.urls)),
    url(r'^filter/'           , include(filter.urls)),
    url(r'^friskby/'          , include(friskby_urls))
]
