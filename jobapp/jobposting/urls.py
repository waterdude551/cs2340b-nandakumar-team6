from django.urls import path
from . import views

urlpatterns = [
    path('', views.browsing, name='jobposting.browsing'), #default is job post browsing
    path('addpost/', views.addpost, name='jobposting.addpost'), #goes to addpost page
    path('<int:id>/', views.viewpost, name='jobposting.viewpost'), #goes to specific post
    path('addpost/create', views.createpost, name='jobposting.createpost'),
]