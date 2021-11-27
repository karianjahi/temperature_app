from django.urls import include, path,path
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'weather', views.WeatherViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
]