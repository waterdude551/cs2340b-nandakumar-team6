from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_convos, name='chat.list_convos'),
    path('<int:conversation_id>/', views.show_convo, name='chat.show_convo'),
    path('start/', views.start_convo, name='chat.start_convo'),
]