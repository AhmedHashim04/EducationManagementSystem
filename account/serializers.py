from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=Profile.ROLES,
        write_only=True
    )  
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = super().create(validated_data)

        user._role = role
        return user

