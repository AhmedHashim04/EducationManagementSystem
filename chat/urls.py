from django.urls import path
from .views import ChatListCreateView, ChatDetailView, MessageListCreateView

app_name = 'chat'

urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat-list-create'),
    path('<str:id>/', ChatDetailView.as_view(), name='chat-detail'),
    path('<str:chat_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
]