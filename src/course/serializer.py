from rest_framework import serializers
from .models import Course, CourseRegistration

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name']


class CourseDetailsSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()
    instructor_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Course
        fields = [
            'name', 'code', 'description', 'credit', 'created_at', 'manager_name',
            'updated_at', 'is_active', 'instructor_name'
        ]

    def get_manager_name(self, obj):
        if obj.manager and obj.manager.user:
            return f"{obj.manager.user.first_name} {obj.manager.user.last_name}"
        return "Unknown"

    def get_instructor_name(self, obj):
        if obj.instructor and obj.instructor.user:
            return f"{obj.instructor.user.first_name} {obj.instructor.user.last_name}"
        return "Unknown"
