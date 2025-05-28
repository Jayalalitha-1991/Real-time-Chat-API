from django.urls import path
from .views import ChatListCreateView, MessageListCreateView

urlpatterns = [
    path('chat/', ChatListCreateView.as_view()),
    path('messages/<int:chat_id>/', MessageListCreateView.as_view()),
]