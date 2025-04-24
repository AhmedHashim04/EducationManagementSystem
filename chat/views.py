from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        chat = serializer.save()
        # Add the creator and the selected participant to the chat
        participant_id = self.request.data.get('participant_id')
        if participant_id:
            chat.participants.add(self.request.user.id, participant_id)

class ChatDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        # Mark messages as read when retrieved
        messages = Message.objects.filter(
            chat_id=chat_id,
            chat__participants=self.request.user
        )
        messages.exclude(sender=self.request.user).update(is_read=True)
        return messages

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = Chat.objects.filter(
            id=chat_id,
            participants=self.request.user
        ).first()
        
        if not chat:
            raise PermissionError("You don't have access to this chat")
            
        serializer.save(
            chat_id=chat_id,
            sender=self.request.user
        )
