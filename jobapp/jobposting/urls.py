from django.urls import path
from . import views

urlpatterns = [
    path('', views.browsing, name='jobposting.browsing'), #default is job post browsing
    path('addpost/', views.addpost, name='jobposting.addpost'), #goes to addpost page
    path('<int:id>/', views.browsepost, name='jobposting.browsepost'), #goes to specific post

]