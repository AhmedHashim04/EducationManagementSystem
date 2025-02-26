from rest_framework import serializers
from .models import Course , CourseRegistration

class CourseSerializer(serializers.Serializer):
    class Meta:
        model  = Course
        fields = ['code','name','description','credit']