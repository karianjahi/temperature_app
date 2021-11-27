"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url
from temperature.views import WeatherList, WeatherDetail

urlpatterns = [
    url(r'^my_apps/temperature$',
        WeatherList.as_view(),
        name="weather_list"),
    url(r'^my_apps/temperature/(?P<weather_id>[0-9]+)$',
        WeatherDetail.as_view(),
        name="weather_detail"),
]
