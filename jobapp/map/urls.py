from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name="map.show"),
]