from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('profile/<int:id>/', views.profile, name='accounts.profile'),
    path('search/', views.search_users, name='accounts.search'),
    path('edit-profile/<int:id>/', views.edit_profile, name='accounts.edit_profile'),
    path('email-seeker/<int:id>/', views.email_seeker, name='accounts.email_seeker'),
    path('send_email/', views.send_email, name='accounts.send_email')
]