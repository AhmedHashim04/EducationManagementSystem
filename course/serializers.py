from rest_framework import serializers
from .models import Course, CourseRegistration
from assignment.models import Assignment

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name']


class CourseDetailsSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()
    instructor_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'name', 'code', 'description', 'credit', 'created_at', 'manager_name',
            'updated_at', 'is_active', 'instructor_name','assginments'
        ]

    def get_assignments(self, obj):
        assignments =Assignment.objects.filter(course=obj).values_list('title', flat=True)
        if assignments:
            return assignments
        return "No Assignments"

    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.first_name} {obj.instructor.last_name}"
        return "Unknown"
