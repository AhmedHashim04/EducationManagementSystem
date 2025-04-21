from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=Profile.ROLES,
        write_only=True
    )  # Role will be handled by signal
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = super().create(validated_data)
        # Set temporary attribute for the signal to use
        user._role = role
        return user

