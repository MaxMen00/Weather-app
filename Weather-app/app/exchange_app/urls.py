from django.urls import path
from .views import exchange, weather_list, city_autocomplete

app_name = 'weather'

urlpatterns = [
    path('', exchange, name='exchange'),
    path('list/<slug:city>/', weather_list, name="weather_list"),
    path('cities/', city_autocomplete, name='city_autocomplete'),
]
