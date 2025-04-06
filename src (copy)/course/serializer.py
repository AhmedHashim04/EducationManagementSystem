from rest_framework import serializers
from .models import Course , CourseRegistration

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code','name']

class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description','credit','created_at','manager','updated_at','is_active','instructor']
