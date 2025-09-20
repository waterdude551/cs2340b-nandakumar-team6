from django.urls import path
from . import views
urlpatterns = [
    path('browsing/', views.signup, name='jobposting.browsing'),
    path('addpost/', views.login, name='jobposting.addpost'),
    path('addpost/', views.addpost, name='addpost'),
    #path('/', views.logout, name='jobposting.url3'),

]