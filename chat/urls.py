from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list_view, name='chat-list'),
    path('<int:room_id>/', views.chat_room_view, name='chat-room'),
    path('boshlash/<int:listing_id>/', views.chat_start_view, name='chat-start'),
]