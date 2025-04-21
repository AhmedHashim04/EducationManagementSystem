
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from .models import Profile


class Register(CreateAPIView):
    model = User
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return user
