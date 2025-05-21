
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.utils import timezone
from .serializers import ProfileSerializer, RegisterSerializer, ChangePasswordSerializer
from account.permessions import IsAssistant, IsInstructor, IsStudent

class RegisterAPIView(CreateAPIView):
    model = User
    serializer_class = RegisterSerializer
    

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent | IsInstructor | IsAssistant]

    def get_object(self):
        return self.request.user.profile
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Explicitly update the profile fields
        for attr, value in serializer.validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return Response(serializer.data)
class ChangePasswordView(APIView):
    """
    API endpoint for changing the user's password.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent | IsInstructor | IsAssistant]
    serializer_class = ChangePasswordSerializer

    def post(self, request) :
        """
        Change the user's password.
        """
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.profile.password_changed_at = timezone.now()
        user.profile.save()
        user.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
