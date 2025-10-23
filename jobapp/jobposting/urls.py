from django.urls import path
from . import views

urlpatterns = [
    path('', views.browsing, name='jobposting.browsing'), #default is job post browsing
    path('addpost/', views.addpost, name='jobposting.addpost'), #goes to addpost page
    path('<int:id>/', views.viewpost, name='jobposting.viewpost'), #goes to specific post
    path('<int:id>/apply/', views.apply, name='jobposting.apply'),
    path('edit/<int:id>/', views.edit_post, name='jobposting.edit_post'), #goes to edit specific post
    path('<int:jobpost_id>/applications/', views.list_applications, name='jobposting.list_applications'), # list applications for a job post
    path('application/<int:application_id>/<int:jobpost_id>/update_stage/', views.update_application_stage, name='jobposting.update_application_stage'),
    path('my-applications/', views.seeker_applications, name='jobposting.seeker_applications'),
]