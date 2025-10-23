# game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_room, name='create_room'),
    path('join/', views.join_room, name='join_room'),
    path('room/<str:room_code>/', views.room_view, name='room'),
    path('room/<str:code>/messages/', views.messages_api, name='messages_api'),
]
