from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name="map.show"),
    path('applicants/', views.applicant_map, name="map.applicants"),
]