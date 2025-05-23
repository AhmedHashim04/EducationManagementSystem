from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from django_ratelimit.decorators import ratelimit

class ChatListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows chats to be viewed or created.
    
    get:
    Return a list of all chats for the authenticated user.
    
    post:
    Create a new chat and add participants.
    """
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return chats where the user is a participant"""
        return Chat.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Create a new chat and add participants"""
        chat = serializer.save()
        participant_id = self.request.data.get('participant_id')
        if participant_id:
            chat.participants.add(self.request.user.id, participant_id)

class ChatDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows a specific chat to be viewed.
    
    get:
    Return the details of a specific chat.
    """
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        """Return chats where the user is a participant"""
        return Chat.objects.filter(participants=self.request.user)

class MessageListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows messages to be viewed or created within a chat.
    
    get:
    Return a list of all messages in a specific chat.
    Messages from other users will be marked as read.
    
    post:
    Create a new message in the specified chat.
    Requires the user to be a participant in the chat.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return messages for a specific chat and mark them as read"""
        chat_id = self.kwargs['chat_id']
        messages = Message.objects.filter(
            chat_id=chat_id,
            chat__participants=self.request.user
        )
        messages.exclude(sender=self.request.user).update(is_read=True)
        return messages
    
    @ratelimit(key='ip', rate='5/m', block=True)
    def perform_create(self, serializer):
        """Create a new message in the chat"""
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
