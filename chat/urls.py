from django.urls import path
from .views import ChatListCreateView, ChatDetailView, MessageListCreateView

app_name = 'chat'

urlpatterns = [
    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:id>/', ChatDetailView.as_view(), name='chat-detail'),
    path('chats/<int:chat_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
]