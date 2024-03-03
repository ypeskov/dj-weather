from django.urls import path

from .views import CurrentWeatherView

urlpatterns = [
    path('current/', CurrentWeatherView.as_view(), name='weather_current'),
]